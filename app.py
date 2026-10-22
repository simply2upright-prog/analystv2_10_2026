# app.py — v5: mit erweiterten Marktkapitalisierungs- und Volumen-Metriken

import streamlit as st
import pandas as pd
import numpy as np
import base64
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from database import get_all_tickers, get_tickers_by_group, get_all_groups, get_currency, get_ticker_count, get_group_for_ticker
from engine import (get_analysis, send_mail_report, classify_signal,
                    get_futures_analysis, FUTURES_TICKERS,
                    get_all_futures_groups, get_futures_by_group,
                    analyze_trend_hit_rate)
from detail_engine import get_detail_analysis, compute_hit_rate
from engine import MIN_HISTORY_N, FORWARD_DAYS
from ticker_search import search_ticker, label_to_ticker, get_display_name

APP_URL = "https://stockupdate-65qjxum6gq2gpjpr5exqfd.streamlit.app"

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="In8Invest Scanner", page_icon="📊", layout="wide")

try:
    def _b64(p):
        with open(p,"rb") as f: return base64.b64encode(f.read()).decode()
    st.markdown(f'<div style="margin-bottom:8px"><img src="data:image/png;base64,{_b64("Icon in8invest.png")}" width="160"></div>',
                unsafe_allow_html=True)
except: pass

st.title("📊 Strategie Scanner")
st.caption(f"🌍 Datenbank: {get_ticker_count()} Ticker · {len(get_all_groups())} Märkte & Sektoren")

# ─── QUERY PARAMS — Deep-Link aus Email (?ticker=XXX) ─────────────────────────
params         = st.query_params
deep_link_ticker = params.get("ticker", None)

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if "results"    not in st.session_state: st.session_state.results    = pd.DataFrame()
if "det_ticker" not in st.session_state: st.session_state.det_ticker = deep_link_ticker or ""

# Wenn Deep-Link vorhanden, direkt Tab 2 aktiv machen
default_tab = 1 if deep_link_ticker else 0  # 0-indexed

# ─── HELPER: Ampel-Badge ──────────────────────────────────────────────────────
def _sig_badge(sig: dict) -> str:
    return (f"<span style='background:{sig['color']};color:#fff;padding:3px 10px;"
            f"border-radius:12px;font-size:12px;font-weight:700'>{sig['emoji']} {sig['label']}</span>")

def _ind_badge(v, low, high, fmt="{:.3f}", invert=False) -> str:
    if v is None: return "<span style='color:#888'>N/A</span>"
    try:
        fv = float(v)
        if fv <= low:    c,t = ("#1a9e3f","OS") if not invert else ("#c0392b","OB")
        elif fv >= high: c,t = ("#c0392b","OB") if not invert else ("#1a9e3f","OS")
        else:             c,t = "#7f8c8d","—"
        b = f"<span style='background:{c};color:#fff;padding:1px 6px;border-radius:3px;font-size:11px;font-weight:700'>{t}</span>"
        return f"{b} {fmt.format(fv)}"
    except: return str(v)

def _fnum(v, fmt="{:.2f}", suffix="") -> str:
    """Sicheres Zahlenformat - zeigt 'N/A' statt Crash/„nan“ bei fehlenden Werten."""
    if v is None: return "N/A"
    try:
        fv = float(v)
        if not np.isfinite(fv): return "N/A"
        return f"{fmt.format(fv)}{suffix}"
    except Exception:
        return "N/A"

def _macd_badge(turn) -> str:
    if turn == "up":   return "<span style='background:#0d7a2e;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700'>DREHT ↑ (Trigger)</span>"
    if turn == "down": return "<span style='background:#8e1f14;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700'>DREHT ↓ (Trigger)</span>"
    return "<span style='background:#7f8c8d;color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700'>KEINE UMKEHR</span>"

# ─── TABS ─────────────────────────────────────────────────────────────────────
def render_side_analysis(side, entry_sigs, sig_history, df_full, cur, sel_tf):
    """Trefferquoten-Analyse für EINE Seite ('buy' = Boden, 'sell' = Top): Gauge, Tabelle, Details."""
    is_buy = side == "buy"
    w_move   = "Trendwende (+5% oder +10%)" if is_buy else "Rückgang (−5% oder −10%)"
    lbl_ok   = "✅ Trendwenden" if is_buy else "✅ Kursrückgänge"
    lbl_bad  = "❌ Kein Boden" if is_buy else "❌ Kein Top"
    col_fav  = "Max Gewinn" if is_buy else "Max Rückgang"
    col_adv  = "Max Verlust" if is_buy else "Max Anstieg"

    if not entry_sigs:
        st.info("Noch keine historischen " + ("Einstiegs" if is_buy else "Verkaufs") +
                "signale im Datenzeitraum erkennbar.")
    else:
        st.markdown("#### 🎯 Trefferquote: " + ("Hat der Boden gehalten?" if is_buy else "Hat das Top gehalten?"))
        st.caption(f"{len(entry_sigs)} unabhängige historische Signale (je Extrem-Phase eines, Einstieg zum nächsten "
                   f"Open) · prüft, ob innerhalb von {FORWARD_DAYS} Tagen eine {w_move} stattfand. "
                   f"Ohne Gebühren/Spreads.")
        hr = compute_hit_rate(entry_sigs, df_full, forward_days=FORWARD_DAYS, side=side)

        if hr["total"] > 0:
            rate_pct = hr["rate"] * 100
            base, edge = hr.get("baseline"), hr.get("edge")
            if hr["total"] < MIN_HISTORY_N:
                rate_color, rate_label = "#8a94a6", f"⚪ Zu wenige Signale (n={hr['total']})"
            elif edge is not None:
                ep = edge * 100
                if ep >= 10:
                    rate_color, rate_label = "#1a9e3f", "🟢 Deutlich besser als Zufall"
                elif ep > 0:
                    rate_color, rate_label = "#f39c12", "🟡 Kaum besser als Zufall"
                else:
                    rate_color, rate_label = "#c0392b", "🔴 Nicht besser als Zufall"
            else:
                rate_color, rate_label = "#f39c12", "🟡 Ohne Zufalls-Vergleich"
            thr_val = base * 100 if base is not None else 65

            hc1, hc2 = st.columns([1, 2])
            with hc1:
                fig_hr = go.Figure(go.Indicator(
                    mode="gauge+number", value=rate_pct,
                    number={"suffix": "%", "font": {"size": 48, "color": rate_color, "family": "Arial Black"}},
                    title={"text": f"Trefferquote<br><span style='font-size:13px;color:{rate_color}'>{rate_label}</span>",
                           "font": {"size": 15, "color": "white"}},
                    gauge={"axis": {"range": [0, 100]}, "bar": {"color": rate_color}, "bgcolor": "#161b22",
                           "steps": [{"range": [0, 45], "color": "#2d1b1b"},
                                     {"range": [45, 65], "color": "#2d2a1b"},
                                     {"range": [65, 100], "color": "#1b2d1b"}],
                           "threshold": {"line": {"color": "white", "width": 3}, "value": thr_val}}))
                fig_hr.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": "white"}, height=280)
                st.plotly_chart(fig_hr, use_container_width=True, key=f"hr_gauge_{side}")
                if base is not None:
                    st.caption(f"Weiße Linie = Zufallsquote dieses Tickers ({base*100:.0f}%): so oft erreicht "
                               f"JEDER beliebige Tag {FORWARD_DAYS} Tage später dieselbe Bewegung.")

            with hc2:
                hm1, hm2, hm3, hm4 = st.columns(4)
                hm1.metric("Signale", hr["total"])
                hm2.metric(lbl_ok, hr["hits"], delta=f"+{hr['hits']}", delta_color="normal")
                hm3.metric(lbl_bad, hr["misses"], delta=f"-{hr['misses']}", delta_color="inverse")
                if base is not None:
                    hm4.metric("Zufallsquote", f"{base*100:.0f}%",
                               delta=f"{edge*100:+.0f} Pkt Edge" if edge is not None else None,
                               delta_color="normal")

                if hr["details"]:
                    row_colors = {"strong": "#1a4d2e", "weak": "#4d3d00", "fail": "#4d1a1a",
                                  "sideways": "#2d2d2d", "new": "#1a2d4d"}
                    rows_html = ""
                    for d in hr["details"]:
                        rc = d.get("result_code", "sideways")
                        bg = row_colors.get(rc, "#222")
                        mg, ml = d.get("max_gain_pct"), d.get("max_loss_pct")
                        if is_buy:
                            mg_str = f"+{mg:.1f}%" if mg is not None else "–"
                            ml_str = f"{ml:.1f}%" if ml is not None else "–"
                        else:   # Verkauf: günstig = Kurs fällt, ungünstig = Kurs steigt
                            mg_str = f"−{mg:.1f}%" if mg is not None else "–"
                            ml_str = f"+{abs(ml):.1f}%" if ml is not None else "–"
                        date_str = d["entry_date"].strftime("%d.%m.%Y") if hasattr(d["entry_date"], "strftime") else str(d["entry_date"])
                        txt_col = "4ade80" if "strong" in rc else "fbbf24" if "weak" in rc else "f87171" if "fail" in rc else "94a3b8"
                        rows_html += (
                            f"<tr style='background:{bg}'>"
                            f"<td style='padding:7px 10px;color:#ccc'>{date_str}</td>"
                            f"<td style='padding:7px 10px;color:#ccc;text-align:right'>{d['entry_price']:.2f} {cur}</td>"
                            f"<td style='padding:7px 10px;font-weight:700;color:#{txt_col}'>{d['result']}</td>"
                            f"<td style='padding:7px 10px;color:#4ade80;text-align:right'>{mg_str}</td>"
                            f"<td style='padding:7px 10px;color:#f87171;text-align:right'>{ml_str}</td></tr>")
                    st.markdown(
                        f"<div style='overflow-x:auto'><table style='border-collapse:collapse;width:100%;font-size:12px;font-family:sans-serif'>"
                        f"<thead><tr style='background:#1e2235;color:#8892a4;font-size:10px;text-transform:uppercase'>"
                        f"<th style='padding:8px 10px'>{'Einstieg' if is_buy else 'Verkauf'}</th>"
                        f"<th style='padding:8px 10px;text-align:right'>Preis</th>"
                        f"<th style='padding:8px 10px'>Ergebnis</th>"
                        f"<th style='padding:8px 10px;text-align:right'>{col_fav}</th>"
                        f"<th style='padding:8px 10px;text-align:right'>{col_adv}</th>"
                        f"</tr></thead><tbody>{rows_html}</tbody></table></div>", unsafe_allow_html=True)

        with st.expander(f"📋 {len(entry_sigs)} historische " + ("Einstiegs" if is_buy else "Verkaufs") + "signale im Detail", expanded=False):
            if is_buy:
                st.caption("Trigger 'MACD' = Histogramm hat nach oben gedreht (eigentliches Kaufsignal). "
                           "Trigger 'Preis' = MACD hat im Fenster nicht gedreht, der Kurs liegt aber bereits +2% über dem laufenden Tief.")
            else:
                st.caption("Trigger 'MACD' = Histogramm hat nach unten gedreht (eigentliches Verkaufssignal). "
                           "Trigger 'Preis' = MACD hat im Fenster nicht gedreht, der Kurs liegt aber bereits 2% unter dem laufenden Hoch.")
            rows = []
            for e in entry_sigs[-12:]:
                f = lambda x: x.strftime("%d.%m.%Y") if hasattr(x, "strftime") else str(x)
                rows.append({"Signal-Datum": f(e["signal_date"]), "Signal-Preis": f"{e['signal_price']:.2f} {cur}",
                             "Trigger": e.get("trigger", "–"),
                             ("Einstieg-Datum" if is_buy else "Verkauf-Datum"): f(e["entry_date"]),
                             ("Einstieg-Preis" if is_buy else "Verkauf-Preis"): f"{e['entry_price']:.2f} {cur}",
                             "Vorlauf": f"{e['days_to_entry']} Tage"})
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
            ei1, ei2, ei3 = st.columns(3)
            ei1.metric("Ø Vorlauf Signal→Ausführung", f"{round(np.mean([e['days_to_entry'] for e in entry_sigs]), 1)} Tage")
            ei2.metric("Ø Bestätigungs-Anstieg" if is_buy else "Ø Bestätigungs-Rückgang",
                       f"{'+' if is_buy else '−'}{abs(round(np.mean([e['upside_pct'] for e in entry_sigs]), 1))}%")
            ei3.metric("Signale gesamt", len(entry_sigs))

    if sig_history:
        with st.expander(f"📅 {len(sig_history)} historische Rohtreffer ({'Kauf' if is_buy else 'Verkauf'}, Zeitraum: {sel_tf})", expanded=False):
            st.dataframe(pd.DataFrame([{
                "Datum": s["date"].strftime("%d.%m.%Y") if hasattr(s["date"], "strftime") else str(s["date"]),
                "Preis": f"{s['price']:.2f} {cur}", "StochRSI": s["StochRSI"], "CCI": s["CCI"],
                "MACD": s.get("MACD_Turn") or "–", "Score": f"{s['score']}/4"} for s in sig_history]),
                hide_index=True, use_container_width=True)


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🚀 Scanner", "📊 Detail-Analyse", "📐 Formations-Check",
    "🛢️ Rohstoffe & Futures", "📅 Automation"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — SCANNER
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.header("Globaler Markt-Scanner")
    c1, c2 = st.columns([4, 1])
    sel_grp   = c1.selectbox("📂 Markt / Index / Sektor:", ["🌍 Alle Gruppen"] + get_all_groups(), key="scan_grp")
    min_score = c2.selectbox("Min. Score:", [1, 2, 3, 4])

    if st.button("🔥 SCAN STARTEN"):
        tickers = get_all_tickers() if sel_grp == "🌍 Alle Gruppen" else get_tickers_by_group(sel_grp)
        raw, prog, stat = [], st.progress(0), st.empty()
        for i, t in enumerate(tickers):
            stat.text(f"Scanne {i+1}/{len(tickers)}: {t}")
            res = get_analysis(t)
            if res: raw.append(res)
            prog.progress((i+1)/len(tickers))
        df = pd.DataFrame(raw)
        if not df.empty:
            df["_group"] = df["Ticker"].apply(get_group_for_ticker)
            grp_avg = df.dropna(subset=["Ret_20d"]).groupby("_group")["Ret_20d"].mean()
            df["RelStrength"] = df.apply(
                lambda r: round(r["Ret_20d"] - grp_avg.get(r["_group"], np.nan), 2)
                if pd.notna(r.get("Ret_20d")) and r["_group"] in grp_avg.index else None, axis=1)
            df = df.drop(columns=["_group"])
            df = df[df["Score"] >= min_score].sort_values(
                ["Score","HitRate"], ascending=[False,False], na_position="last").reset_index(drop=True)
            st.session_state.results = df
            stat.success(f"✅ {len(df)} Signale in {len(tickers)} Titeln.")
        else:
            stat.warning("Keine Signale.")

    if not st.session_state.results.empty:
        df_show = st.session_state.results.copy()
        st.markdown("##### Ergebnisse — 🟢 OVERSOLD · 🔴 OVERBOUGHT · ⚪ NEUTRAL")

        def _trend_html(t):
            if t == "up":   return "<span style='color:#1a9e3f;font-weight:700'>📈</span>"
            if t == "down": return "<span style='color:#c0392b;font-weight:700'>📉</span>"
            return "<span style='color:#888'>–</span>"

        def _hitrate_html(r):
            hr, n = r.get('HitRate'), r.get('HitRate_N', 0)
            if hr is None or (isinstance(hr, float) and pd.isna(hr)):
                return f"<span style='color:#888;font-size:11px'>zu wenig ({int(n) if pd.notna(n) else 0})</span>"
            color = "#0d7a2e" if hr >= 70 else ("#f39c12" if hr >= 50 else "#c0392b")
            return f"<span style='color:{color};font-weight:700'>{int(hr)}%</span> <span style='color:#888;font-size:10px'>({int(n)})</span>"

        def _relstrength_html(r):
            rs = r.get('RelStrength')
            if rs is None or (isinstance(rs, float) and pd.isna(rs)):
                return "<span style='color:#888'>–</span>"
            color = "#0d7a2e" if rs >= 0 else "#c0392b"
            return f"<span style='color:{color};font-weight:700'>{rs:+.1f}%</span>"

        def _row_html(r):
            sv, sf, ss, cv = r.get('StochRSI'), r.get('Stoch_Fast'), r.get('Stoch_Slow'), r.get('CCI')
            macd_turn = r.get('MACD_Turn')
            sig  = classify_signal(sv, sf, ss, cv, macd_turn)
            sc   = int(r.get('Score', 0))
            sc_c = {4:"#0d7a2e",3:"#1a9e3f",2:"#f39c12",1:"#7f8c8d"}.
