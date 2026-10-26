# roundtrip_backtest.py — Strategie so, wie sie gedacht ist: Einstieg beim Kaufsignal, Ausstieg beim Gegensignal (kein fester Horizont)
#
#   python roundtrip_backtest.py --period 10y --out roundtrip_results
#   python roundtrip_backtest.py --period 5y --limit 120            (Schnelltest)
#
# Ablauf je Ticker: Kaufsignal (Schluss) -> Einstieg Open Folgetag -> gehalten, bis das Ausstiegs-Signal kommt -> Ausstieg Open Folgetag.
# Während eine Position läuft, werden neue Einstiegssignale ignoriert (keine Aufstockung). Nach dem Ausstieg kann sofort neu eingestiegen werden.
# Spiegelbildlich: Short-Einstieg beim Verkaufssignal, Eindeckung beim Kaufsignal.
#
# Ausstiege:  A  Gegensignal "alles am selben Tag" (4/4-Mail)      B  Gegensignal mit "prior"-Regel (StochRSI/Stoch vor <= 10 Tagen)
#             T  Trailing-Stopp 3 x ATR(14) vom besten Schlusskurs (Elder: Stopp nur nachziehen)
# Einstiege:  S1 4/4 am selben Tag      S2 "prior"-Regel (10 Tage)
#
# Vergleichsmaßstab (wichtig, weil die Haltedauer je Trade verschieden ist): Erwartete Rendite = Ø aller Fenster GLEICHER LÄNGE desselben
# Tickers im gleichen Trendzustand (Kurs über/unter SMA200 am Einstiegstag). Damit wird "Aktien steigen langfristig" und die Trendphase
# herausgerechnet. Überschuss = tatsächliche Rendite des Trades minus diese Erwartung. Offene Positionen am Datenende zählen nicht mit.
# Statistik wie im Sweep: Cluster-t über Einstiegsmonate, Training (< Split) / Test, Verdikt nur wenn beide Zeiträume t > 2.

import argparse
import json
import logging
import math
import os
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from database import get_all_tickers
from engine import download_price_frames
from pooled_backtest import cluster_t
import sweep_backtest as sb

log = logging.getLogger("roundtrip")

SPLIT_DEFAULT = "2022-01-01"
TRAIL_ATR = 3.0
MIN_N_TEST = 60
T_SIG = 2.0
CLIP_PP = 300.0

ENTRIES = {"S1": "4/4 am selben Tag", "S2": "4/4, StochRSI/Stoch vor ≤10 T."}
EXITS = {"A": "Gegensignal 4/4 (selber Tag)", "B": "Gegensignal prior-Regel", "T": "Trailing-Stopp 3×ATR"}
COLS = ["entry_key", "exit_key", "ticker", "side", "entry_date", "exit_date", "days", "ret", "b_ret", "mae", "trend", "open"]


def _gate(P, buy: bool, key: str) -> np.ndarray:
    if key == "S1":
        v = sb.Variant("S1", "", "", all4="same", confirm="none", max_wait=0)
    else:
        v = sb.Variant("S2", "", "", all4="prior", recent_days=10, confirm="none", max_wait=0)
    g = np.asarray(sb.all4_gate(P, v, buy), bool) & P.valid
    return g


def _atr(P) -> np.ndarray:
    pc = np.r_[np.nan, P.c[:-1]]
    tr = np.nanmax(np.vstack([P.h - P.l, np.abs(P.h - pc), np.abs(P.l - pc)]), axis=0)
    return pd.Series(tr).rolling(14, min_periods=14).mean().to_numpy()


class WindowBase:
    """Erwartete Rendite eines Fensters der Länge L im Trendzustand 'up' (Ticker-Schnitt über alle Starttage)."""

    def __init__(self, P, buy: bool):
        self.P, self.buy, self.cache = P, buy, {}
        self.up = (P.c > P.ma) & np.isfinite(P.ma)

    def get(self, L: int, up: bool) -> float:
        key = (L, bool(up))
        if key in self.cache:
            return self.cache[key]
        P = self.P
        m = P.n - L - 1
        val = np.nan
        if m > 60 and L >= 1:
            t = np.arange(m)
            with np.errstate(invalid="ignore", divide="ignore"):
                r = (P.o[t + 1 + L] / P.o[t + 1] - 1) * 100 if L + 1 < P.n else np.full(m, np.nan)
            r = r if self.buy else -r
            ok = np.isfinite(r) & (self.up[t] == bool(up)) & ~P.aw[t + 1]
            if ok.sum() >= 20:
                val = float(np.clip(r[ok], -100, CLIP_PP).mean())
        if not np.isfinite(val):
            val = np.nan
        self.cache[key] = val
        return val


def run_ticker(P, buy: bool) -> list[tuple]:
    n, c, o, h, l = P.n, P.c, P.o, P.h, P.l
    atr = _atr(P)
    sgn = 1.0 if buy else -1.0
    side = "buy" if buy else "sell"
    ent = {k: _gate(P, buy, k) for k in ENTRIES}
    ext = {"A": _gate(P, not buy, "S1"), "B": _gate(P, not buy, "S2")}
    base = WindowBase(P, buy)
    rows = []
    for ek, eg in ent.items():
        for xk in EXITS:
            i = 0
            while i < n - 2:
                if not eg[i] or not np.isfinite(o[i + 1]) or o[i + 1] <= 0 or P.aw[i + 1]:
                    i += 1
                    continue
                e = o[i + 1]
                exit_i, best = None, c[i]
                for j in range(i + 1, n - 1):
                    if xk == "T":
                        best = max(best, c[j]) if buy else min(best, c[j])
                        a = atr[j]
                        hit = np.isfinite(a) and ((c[j] < best - TRAIL_ATR * a) if buy else (c[j] > best + TRAIL_ATR * a))
                    else:
                        hit = bool(ext[xk][j])
                    if hit:
                        exit_i = j
                        break
                if exit_i is None:
                    # Position bis Datenende offen: zum letzten Schlusskurs bewertet und als "offen" markiert. Sie wegzulassen würde
                    # die Verlierer (nie ein Gegensignal) aussortieren und das Ergebnis nach oben verzerren.
                    if n - 1 - (i + 1) < 5 or P.aw[i + 1:n].any() or not np.isfinite(c[-1]):
                        break
                    L = n - 1 - (i + 1)
                    ret = sgn * (c[-1] / e - 1) * 100
                    span = slice(i + 1, n)
                    mae = (min(l[span].min() / e - 1, 0) if buy else min(1 - h[span].max() / e, 0)) * 100
                    up = bool(c[i] > P.ma[i]) if np.isfinite(P.ma[i]) else False
                    rows.append((ek, xk, P.ticker, side, P.dates[i + 1], P.dates[n - 1], L,
                                 float(np.clip(ret, -100, CLIP_PP)), base.get(L, up), float(mae), "up" if up else "down", True))
                    break
                x = o[exit_i + 1]
                if not (np.isfinite(x) and x > 0):
                    i = exit_i + 1
                    continue
                L = exit_i + 1 - (i + 1)
                span = slice(i + 1, exit_i + 2)
                if P.aw[span].any():
                    i = exit_i + 1
                    continue
                ret = sgn * (x / e - 1) * 100
                mae = (min(l[span].min() / e - 1, 0) if buy else min(1 - h[span].max() / e, 0)) * 100
                up = bool(c[i] > P.ma[i]) if np.isfinite(P.ma[i]) else False
                b = base.get(L, up)
                rows.append((ek, xk, P.ticker, side, P.dates[i + 1], P.dates[exit_i + 1], L,
                             float(np.clip(ret, -100, CLIP_PP)), b, float(mae), "up" if up else "down", False))
                i = exit_i + 1
    return rows


def agg(df: pd.DataFrame) -> dict:
    df = df[np.isfinite(df["b_ret"])]
    n = len(df)
    if n == 0:
        return {"n": 0}
    month = pd.to_datetime(df["entry_date"]).dt.to_period("M")
    exc = df["ret"] - df["b_ret"]
    t, m = cluster_t(exc, month)
    return {"n": n, "n_tickers": int(df["ticker"].nunique()), "days": float(df["days"].mean()), "win": float((df["ret"] > 0).mean()) * 100,
            "ret": float(df["ret"].mean()), "ret_med": float(df["ret"].median()), "b_ret": float(df["b_ret"].mean()),
            "exc": float(exc.mean()), "exc_med": float(exc.median()), "t": t, "mae": float(df["mae"].mean()),
            "per_day": float(df["ret"].sum() / df["days"].sum())}


def verdict(tr: dict, te: dict) -> str:
    if tr.get("n", 0) < MIN_N_TEST or te.get("n", 0) < MIN_N_TEST:
        return "zu wenig Trades"
    ok = lambda s: s["exc"] > 0 and s["t"] == s["t"] and s["t"] > T_SIG
    bad = lambda s: s["exc"] < 0 and s["t"] == s["t"] and s["t"] < -T_SIG
    if ok(tr) and ok(te):
        return "✅ Hinweis auf Vorteil (beide Zeiträume)"
    if bad(tr) and bad(te):
        return "⛔ schlechter als Zufall (beide Zeiträume)"
    if ok(te) or ok(tr):
        return "⚠️ nur in einem Zeitraum"
    return "kein Vorteil"


def _f(x, spec="+.1f"):
    return "–" if x is None or (isinstance(x, float) and x != x) else format(x, spec)


def build_report(tr: pd.DataFrame, meta: dict, split: str) -> tuple[str, dict]:
    sp = pd.Timestamp(split)
    tr = tr.copy()
    tr["entry_date"] = pd.to_datetime(tr["entry_date"])
    L = ["# Rundreisen: Einstieg beim Signal, Ausstieg beim Gegensignal", "",
         f"Stand {meta['created']} · {meta['n_tickers']} Ticker · {meta['period']} · Training < {split} / Test ab {split}", "",
         "Einstieg/Ausstieg jeweils zum Open des Folgetags, keine Aufstockung. Positionen ohne Gegensignal bis Datenende (offen) sind enthalten und zum letzten Schlusskurs bewertet; die vorletzte Spalte zeigt zum Vergleich nur die abgeschlossenen. "
         "**Überschuss** = Rendite des Trades minus Ø Rendite gleich langer Fenster desselben Tickers im gleichen Trendzustand (Prozentpunkte je Trade). "
         "Kein Abzug von Kosten.", ""]
    summ = {}
    for side, name, hint in (("buy", "LONG (Kaufsignal → Verkaufssignal)", ""), ("sell", "SHORT (Verkaufssignal → Kaufsignal)", "")):
        t = tr[tr["side"] == side]
        L += [f"## {name}", "",
              "| Einstieg | Ausstieg | Trades Tr./Test (davon offen) | Ø Haltedauer (Tage) | Trefferquote | Ø Rendite | Ø Erwartung | Überschuss Tr. (t) | Überschuss Test (t) | Median-Überschuss | Ø größter Rückschlag | Überschuss nur abgeschlossene Tr./Test | Verdikt |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for ek in ENTRIES:
            for xk in EXITS:
                d = t[(t["entry_key"] == ek) & (t["exit_key"] == xk)]
                a, b, al = agg(d[d["entry_date"] < sp]), agg(d[d["entry_date"] >= sp]), agg(d)
                dc = d[~d["open"]]
                ac, bc = agg(dc[dc["entry_date"] < sp]), agg(dc[dc["entry_date"] >= sp])
                n_open = int(d["open"].sum())
                summ[f"{side}:{ek}:{xk}"] = {"train": a, "test": b, "all": al, "closed_train": ac, "closed_test": bc, "n_open": n_open}
                if al.get("n", 0) == 0:
                    L.append(f"| {ek} | {xk} | 0 | – | – | – | – | – | – | – | – | – | keine Trades |")
                    continue
                cell = lambda s: "–" if s.get("n", 0) == 0 else f"{_f(s['exc'])} ({_f(s['t'], '+.1f')})"
                L.append(f"| {ek} {ENTRIES[ek]} | {xk} {EXITS[xk]} | {a.get('n', 0)} / {b.get('n', 0)} ({n_open}) | {_f(al['days'], '.0f')} | {_f(al['win'], '.0f')} % | "
                         f"{_f(al['ret'])} % | {_f(al['b_ret'])} % | {cell(a)} | {cell(b)} | {_f(al['exc_med'])} | {_f(al['mae'])} % | {cell(ac)} / {cell(bc)} | {verdict(a, b)} |")
        L.append("")
    L += ["## Wie liest man das?", "",
          "- Das ist die Strategie als ganze Rundreise: es gibt keinen festen Horizont, die Haltedauer ergibt sich aus dem Gegensignal.",
          "- **Ø Erwartung** = was ein Zufallseinstieg mit gleich langer Haltedauer im selben Ticker und Trend im Schnitt gebracht hätte. Der **Überschuss** ist der eigentliche Vorteil.",
          "- Ein Vorteil gilt erst, wenn er in Training UND Test mit Cluster-t > 2 auftaucht. Wenige, lange Trades machen die Statistik wackelig (große Streuung).",
          "- Survivorship-Bias der Tickerliste (heutige Titel), keine Kosten, Short ohne Leihkosten, Gegensignale kommen oft spät oder gar nicht (offene Trades sind zum letzten Kurs bewertet)."]
    return "\n".join(L), summ


def run(period: str, out_dir: str, limit: int = 0, tickers: list[str] | None = None, split: str = SPLIT_DEFAULT,
        frames: dict | None = None) -> pd.DataFrame:
    if frames is None:
        tickers = tickers or get_all_tickers()
        if limit:
            tickers = tickers[:limit]
        log.info("Lade %d Ticker (%s) …", len(tickers), period)
        frames, failed = download_price_frames(tickers, period=period, progress_cb=lambda d, t, p: log.info("Download %d/%d", d, t))
    else:
        failed = []
    rows, used = [], 0
    for k, (t, raw) in enumerate(frames.items(), 1):
        try:
            P = sb.prepare(t, raw)
            if P is None:
                continue
            used += 1
            for buy in (True, False):
                rows.extend(run_ticker(P, buy))
        except Exception as e:
            log.warning("%s: %s", t, e)
        if k % 200 == 0:
            log.info("ausgewertet %d, bisher %d Trades", k, len(rows))
    trades = pd.DataFrame(rows, columns=COLS)
    os.makedirs(out_dir, exist_ok=True)
    if trades.empty:
        log.error("Keine Trades – nichts zu schreiben.")
        return trades
    meta = {"created": datetime.now(timezone.utc).strftime("%d.%m.%Y %H:%M UTC"), "period": period, "n_tickers": used, "n_failed": len(failed)}
    report, summ = build_report(trades, meta, split)
    with open(os.path.join(out_dir, "ROUNDTRIP_REPORT.md"), "w", encoding="utf-8") as f:
        f.write(report)
    with open(os.path.join(out_dir, "roundtrip_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summ, f, ensure_ascii=False, indent=1, default=lambda o: None if o != o else float(o))
    trades[(trades["entry_key"] == "S1") & (trades["exit_key"].isin(["A", "B"]))].to_csv(os.path.join(out_dir, "roundtrip_trades_S1.csv"), index=False)
    log.info("Fertig: %d Trades → %s", len(trades), out_dir)
    return trades


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-7s %(message)s")
    ap = argparse.ArgumentParser()
    ap.add_argument("--period", default="10y")
    ap.add_argument("--out", default="roundtrip_results")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--split", default=SPLIT_DEFAULT)
    a = ap.parse_args()
    run(a.period, a.out, a.limit, split=a.split)
