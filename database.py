# database.py — Globale Aktien-Datenbank v2.1 (Erweitert & Aktualisiert)
# Abdeckung: USA (S&P500, NASDAQ, Dow Jones, Russell, REITs, CEF/BDC) | UK (FTSE100)
# China/Asien (A/H-Shares, HK, ADR, Indonesien, etc.) | Südkorea (KOSPI) | Japan (Nikkei)
# Europa (DAX/MDAX/SDAX, CAC40, IBEX35, FTSE MIB, AEX, SMI, Skandinavien)
# Sektoren: Energy, Mining, Healthcare, Financials, Tech, Consumer, REIT, Utilities, Sin-Stocks, Emerging Markets

TICKER_LISTS = {

    # ═══════════════════════════════════════════════════════
    # USA — S&P 500 nach Sektoren
    # ═══════════════════════════════════════════════════════
    "SP500_TECH": [
        "AAPL", "MSFT", "NVDA", "GOOGL", "GOOG", "META", "AVGO",
        "ORCL", "ADBE", "CRM", "AMD", "QCOM", "TXN", "INTU", "AMAT",
        "LRCX", "KLAC", "SNPS", "CDNS", "MCHP", "INTC", "IBM",
        "CSCO", "ACN", "FTNT", "PANW", "CRWD", "ZS", "DDOG", "MU",
        "SMCI", "VRT", "ANET", "NET", "OKTA", "SNOW", "MDB", "PLTR",
    ],
    "SP500_FINANCIALS": [
        "JPM", "BAC", "WFC", "C", "GS", "MS", "BLK", "SCHW",
        "AXP", "V", "MA", "PYPL", "COF", "USB", "PNC", "TFC",
        "BK", "STT", "FITB", "KEY", "RF", "HBAN",
        "AFL", "MET", "PRU", "ALL", "AIG", "CB", "PGR", "TRV",
        "CME", "ICE", "NDAQ", "SPGI", "MCO", "USB-PP", "KEY-PJ",
        "KEY-PI", "WFC-PC", "WFC-PY", "BAC-PK", "BAC-PL", "BAC-PB",
        "MS-PE", "MS-PI", "MS-PO", "MS-PA", "STT-PG", "HIG-PG",
    ],
    "SP500_HEALTHCARE": [
        "JNJ", "LLY", "UNH", "ABBV", "MRK", "PFE", "TMO", "ABT",
        "DHR", "BMY", "AMGN", "GILD", "VRTX", "REGN", "BIIB",
        "SYK", "BSX", "MDT", "BDX", "EW", "ISRG", "ZBH",
        "HCA", "CI", "CVS", "MCK", "ABC", "CAH", "IDXX",
        "IQV", "ILMN", "A", "WAT", "PRGO", "VTRS", "ZTS",
    ],
    "SP500_CONSUMER_STAPLES": [
        "PG", "KO", "PEP", "WMT", "COST", "MDLZ", "PM", "MO",
        "KHC", "GIS", "K", "CPB", "HRL", "CAG", "MKC",
        "CL", "CHD", "CLX", "EL", "KR", "DLTR", "DG",
        "HSY", "SJM", "TSN", "KMB",
    ],
    "SP500_CONSUMER_DISC": [
        "AMZN", "TSLA", "HD", "MCD", "NKE", "LOW", "SBUX", "TJX",
        "BKNG", "MAR", "HLT", "YUM", "CMG", "DPZ", "QSR",
        "F", "GM", "PHM", "DHI", "LEN", "NVR", "TOL",
        "ROST", "RL", "PVH", "EBAY", "ETSY", "RH", "WSM",
        "LEN-B", "BBY", "ULTA", "DRI", "POOL", "TSCO",
    ],
    "SP500_ENERGY": [
        "XOM", "CVX", "COP", "EOG", "SLB", "HAL", "MPC", "PSX",
        "VLO", "DVN", "FANG", "APA", "CTRA", "OXY", "PBR",
        "MRO", "HES", "BKR", "NOV", "CHRD", "MTDR", "PR", "SM",
        "EPD", "MPLX", "PAGP", "SUN", "EQT", "SWN", "OKE",
    ],
    "SP500_INDUSTRIALS": [
        "GE", "HON", "UPS", "BA", "LMT", "RTX", "NOC", "GD",
        "CAT", "DE", "EMR", "ETN", "ITW", "PH", "IR", "ROK",
        "AME", "FTV", "XYL", "IDEX", "ROP",
        "UNP", "CSX", "NSC", "FDX", "PCAR", "GWW", "WM",
        "RSG", "FAST", "CTAS", "URI",
    ],
    "SP500_MATERIALS": [
        "LIN", "APD", "ECL", "SHW", "PPG", "NEM", "FCX", "NUE",
        "STLD", "AA", "CF", "MOS", "DOW", "LYB",
        "ALB", "MP", "CTVA", "FMC", "IFF", "AVY", "PKG",
        "EMN", "WLK", "BALL", "CE", "PKG",
    ],
    "SP500_UTILITIES": [
        "NEE", "DUK", "SO", "D", "AEP", "EXC", "SRE", "PCG",
        "AWK", "WEC", "ES", "FE", "CNP", "AES", "NRG", "ETR",
        "EIX", "PPL", "DTE", "AEE", "CMS", "LNT",
        "ED", "PCG-PA", "XEL", "PEG", "ATO",
    ],
    "SP500_REITS": [
        "AMT", "PLD", "CCI", "EQIX", "PSA", "O", "DLR", "VICI",
        "SPG", "AVB", "EQR", "MAA", "UDR", "CPT", "ESS",
        "WY", "ARE", "BXP", "KIM", "REG", "FRT", "HST",
        "OHI", "WPC", "NNN", "EXR", "WELL", "SBAC", "VTR",
        "DLR-PJ", "DLR-PL", "PSA-PQ", "PSA-PK", "SLG", "SLG-PI",
        "KRC", "HIW", "DOC", "CUZ", "REXR", "FRT",
    ],

    # ═══════════════════════════════════════════════════════
    # USA — DOW JONES 30
    # ═══════════════════════════════════════════════════════
    "DOW_JONES_30": [
        "AAPL", "AMGN", "AXP", "BA", "CAT", "CRM", "CSCO",
        "CVX", "DIS", "DOW", "GS", "HD", "HON", "IBM",
        "INTC", "JNJ", "JPM", "KO", "MCD", "MMM",
        "MRK", "MSFT", "NKE", "PG", "TRV", "UNH",
        "V", "VZ", "WBA", "WMT",
    ],

    # ═══════════════════════════════════════════════════════
    # USA — NASDAQ GROWTH & DISRUPTIVE TECH
    # ═══════════════════════════════════════════════════════
    "NASDAQ_GROWTH_TECH": [
        "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
        "AVGO", "NFLX", "ADBE", "AMD", "QCOM", "TXN", "INTU", "AMAT",
        "ISRG", "BKNG", "VRTX", "PANW", "MU", "SNPS", "CDNS", "KLAC",
        "MELI", "PYPL", "SNOW", "PLTR", "SMCI", "VRT", "DECK",
        "SOFI", "AFRM", "COIN", "DKNG", "RBLX", "SNAP",
        "ZM", "DOCU", "OKTA", "NET", "CFLT", "MDB",
        "HOOD", "IONQ", "RXRX", "SOUN", "BBAI",
    ],

    # ═══════════════════════════════════════════════════════
    # USA — BDCs, CEFs, PREFERRED & INCOME STOCKS (NEU & INTEGRIERT)
    # ═══════════════════════════════════════════════════════
    "USA_INCOME_CEF_BDC_REIT": [
        "IEP", "DHT", "PDI", "DX", "FSK", "AGNC", "STWD", "OTF",
        "PTY", "MPL", "PFL", "BXSL", "BHFAP", "OBDC", "RITM", "HTGC",
        "TRMD", "JPC", "RVT", "NMT", "NZF", "AMBP", "CLM", "BSM",
        "USAC", "NLY-PG", "SBSW", "SBR", "NAD", "NEA", "TIMB", "KYN",
        "CSQ", "AXS-PE", "RLJ-PA", "VNO-PM", "EPR", "CALM", "PBC",
        "TFSL", "ADX", "GIS", "RNR-PF", "ACGLO", "MAA", "OMF", "INSW",
        "UTG", "VALE", "EVT", "FCPT", "WFC-PC", "ATH-PA", "SCHW-PD",
        "STT-PG", "MET-PE", "HIW", "SFD", "ARE", "GDV", "TU", "KRC",
        "LINE", "BCE", "EIX", "KSPI", "OHI", "NNN", "WPC", "MET-PA",
        "MTN", "MO", "CMCSA", "MAIN", "RLX", "BBDO", "CL", "HR",
        "LCII", "SUNC", "BCH", "UGI", "SUN", "OGE", "CCI", "LTC",
        "BEP", "VNOM", "LAZ", "RIO", "BEPC", "APLE", "EMN", "SLG",
        "AU", "CQP", "CNXC", "VIPS", "FG", "TRN", "C", "BHP",
        "MC", "PRU", "LNT", "IRT", "TAP", "FIS", "ES", "KMB",
        "KRG", "NSP", "BX", "BXP", "CLX", "REXR", "SMG", "AES",
        "ULTA", "HASI", "SMA", "DOC", "CUZ", "ARES", "AESI", "DOW",
        "NVO", "OKE", "GGAL", "LXP", "AXIA", "NE", "VMRK", "CIB",
        "BTI", "NWN", "FE", "PBA", "BBY", "KHC", "REYN", "WF",
        "BOH", "EVRG", "BP", "STEP", "WIT", "WSBC", "AMT", "PSA",
        "NGG", "SIRI", "KGS", "SR", "HPQ", "VICR", "WAFD", "WPP",
        "ESS", "PFE", "PEG", "CG", "PB", "SJM", "GRFS", "BVN",
        "BAP", "DOX", "FRME", "PECO", "RHP", "TIGO", "ELS", "FAF",
        "USB", "TSN", "MDC", "WLK", "CPB", "TRNO", "INGR", "KMI",
        "CMS", "HSY", "CHRD", "EGP", "GPC", "PTEN", "BNS", "IVT",
        "CHT", "EQNR", "CNA", "NTR", "TM", "UBSI", "ACN", "BF-A",
        "LVS", "FITB", "CPT", "FITBP", "NEE", "EDR", "SRE", "DRH",
        "INDB", "BAH", "BKU", "BZ", "CVX", "MCD", "TMUS", "UNH",
        "DRI", "POOL", "RTO", "BRO", "IRM", "KFY", "MFC", "ALV",
        "AMCR", "RDN", "HD", "SHEL", "FFIN", "MDU", "YMM", "IVZ",
        "TSCO", "FBP", "FHN", "HOMB", "MAS", "CWA", "FNB", "SWK",
        "JNJ", "BMO", "HLNE", "UCBI", "TXN", "AEO", "GEF", "SBAC",
        "KDP", "LW", "CVS", "SHO", "CHCO", "CRBG", "DTM", "YUMC",
        "IDA", "MGY", "MTDR", "VTRS", "AFL", "EOG", "ALLE", "FHI",
        "KMT", "LEN", "SSB", "DPZ", "AOS", "FBIN", "LOW", "PR",
        "SBUX", "WMG", "CURB", "BAC", "HON", "ABT", "CATY", "OTTR",
        "RBC", "RY", "CBT", "ITW", "MTC", "RGA", "FUTU", "MFG",
        "GIL", "HAS", "MS", "PRK", "AIG", "BR", "AMX", "VTR",
        "ABBV", "EWBC", "SLB", "K", "AMGN", "DLB", "UBS", "GNTX",
        "KO", "PUK", "PG", "SLM", "SM", "ADM", "MRK", "TRI",
        "CPK", "KSS", "AAP", "VNO", "AVY", "SLGN", "DEO", "SU",
        "GILD", "IT", "HRI", "MMS", "CNI", "NTRS", "RRR", "ACT",
        "ACM", "PHIN", "VFC", "NMRK", "RQL", "PRDO", "RCI", "GS",
        "JPM", "UNP", "FCNCA", "FUL", "CMI", "PSO", "SFBS", "AZN",
        "CTSH", "MKTX", "NRG", "AHR", "BANF", "SIGI", "CLBK", "SHAW",
        "CVE", "NOV", "OSK", "R", "VIRT", "BAM", "NXPI", "TFII",
        "CCL", "BLK", "LPX", "NSC", "WM", "BKH", "BUD", "FDX",
        "INTU", "THG", "ATAT", "TNET", "XYL", "LOGI", "HCA", "UMBF",
        "WTFC", "WTTR", "LII", "CSL", "TAC", "EMR", "FDS", "WELL",
        "CBC", "DGX", "GGG", "GRMN", "EVR", "DCI", "SCHW", "AMP",
        "ATKR", "RJF", "DHI", "CSX", "EMBJ", "NOC", "PLMR", "SNDR",
        "CXT", "DLO", "TEX", "LIN", "MWA", "WFRD", "KNX", "PCAR",
        "YOU", "EQT", "ROK", "SAP", "BALL", "RS", "PH", "BWA",
        "MSA", "SYK", "BTE", "CHD", "MEOH", "WMS", "RSG", "STE",
        "PLUS", "AGCO", "NHC", "SNT", "CCK", "NDSN", "RLI", "GWW",
        "AON", "MSI", "TROW", "TFX", "TNK", "VRSK", "WSFS", "SIMO",
        "SLDE", "DE", "ASO", "HUBB", "CHH", "EBAY", "ECL", "ZBH",
        "J", "KLIC", "ABM", "AMER",
    ],

    # ═══════════════════════════════════════════════════════
    # USA — SIN STOCKS / TABAK / ALKOHOL / SWEETS
    # ═══════════════════════════════════════════════════════
    "SIN_STOCKS_SWEETS_ENERGY": [
        "PM", "MO", "BTI", "BATS.L", "IMB.L", "2914.T", "UVV",
        "DEO", "RI.PA", "BF-B", "STZ", "BUD", "HEIA.AS", "HEIO.AS",
        "CARL-B.CO", "TAP", "CAMP.MI", "LVMH.PA",
        "MDLZ", "BN.PA", "UMG.AS", "DIS", "HSY", "NESN.SW", "LINDT.SW",
        "MNST", "CELH", "KDP", "BF-B", "CPR.MI",
    ],

    # ═══════════════════════════════════════════════════════
    # GROSSBRITANNIEN — FTSE 100
    # ═══════════════════════════════════════════════════════
    "FTSE100": [
        "AZN.L",  "HSBA.L", "ULVR.L", "GSK.L",  "RIO.L",
        "BP.L",   "SHEL.L", "BATS.L", "REL.L",  "NG.L",
        "DGE.L",  "IMB.L",  "LSEG.L", "LLOY.L", "BARC.L",
        "NWG.L",  "STAN.L", "PRU.L",  "LGEN.L", "AV.L",
        "MNG.L",  "RR.L",   "BA.L",   "MNDI.L", "SMDS.L",
        "CRH.L",  "ANTO.L", "AAL.L",  "GLEN.L", "BHP.L",
        "SVT.L",  "UU.L",   "SSE.L",  "BDEV.L", "PSN.L",
        "TW.L",   "BKG.L",  "SGRO.L", "BLND.L", "LAND.L",
        "WPP.L",  "OCDO.L", "MKS.L",  "NEXT.L", "JD.L",
        "HBR.L",  "IMI.L",  "EXPN.L", "HLMA.L", "WEIR.L",
        "TSCO.L", "SBRY.L", "KGF.L",  "AUTO.L", "III.L", "RKT.L",
        "LDSCY",  "VODPF",  "VOD",    "RTO",    "PUK",   "GSK",
    ],

    # ═══════════════════════════════════════════════════════
    # CHINA / ASIEN — ADRs & HK (inkl. Ping An / PNGAY)
    # ═══════════════════════════════════════════════════════
    "CHINA_TECH_INTERNET": [
        "BABA",    "TCEHY",   "JD",      "BIDU",    "PDD",
        "NTES",    "BILI",    "IQ",      "VIPS",    "MOMO",
        "YMM",     "FINV",    "ZH",      "TIGR",    "FUTU",
        "LKNCY",   "TUYA",    "KC",      "PNGAY",   "HTHT",
        "9988.HK", "0700.HK", "9618.HK", "9888.HK", "9999.HK",
        "9626.HK", "0992.HK", "CSDXF",   "LNGVO",
    ],
    "CHINA_FINANCE_ENERGY_EV": [
        "NIO",     "XPEV",    "LI",      "BEKE",    "YUMC",
        "TAL",     "EDU",     "GOTU",    "DAO",
        "0939.HK", "1398.HK", "3988.HK", "0941.HK", "0728.HK",
        "0762.HK", "2628.HK", "0386.HK", "0857.HK", "1088.HK",
        "0175.HK", "9868.HK", "2015.HK",
    ],

    # ═══════════════════════════════════════════════════════
    # SÜDKOREA — KOSPI
    # ═══════════════════════════════════════════════════════
    "KOSPI_KOREA": [
        "005930.KS", "000660.KS", "005380.KS", "000270.KS", "005490.KS",
        "051910.KS", "006400.KS", "035420.KS", "035720.KS", "012330.KS",
        "066570.KS", "003550.KS", "028260.KS", "086790.KS", "105560.KS",
        "055550.KS", "032830.KS", "017670.KS", "030200.KS", "015760.KS",
        "096770.KS", "010950.KS", "034220.KS", "009150.KS", "011200.KS",
        "018260.KS", "032640.KS", "011070.KS", "042700.KS", "247540.KS",
        "086280.KS", "KEP", "WF",
    ],

    # ═══════════════════════════════════════════════════════
    # JAPAN — NIKKEI 225 & INTERNATIONAL ADRs
    # ═══════════════════════════════════════════════════════
    "NIKKEI_SELECTION": [
        "7203.T",  "6758.T",  "9984.T",  "6861.T",  "8306.T",
        "9432.T",  "6367.T",  "6501.T",  "4519.T",  "9433.T",
        "8035.T",  "6594.T",  "4543.T",  "7751.T",  "7267.T",
        "6702.T",  "8411.T",  "7741.T",  "4063.T",  "9983.T",
        "2914.T",  "7974.T",  "4661.T",  "6954.T",  "6971.T",
        "5108.T",  "8801.T",  "3382.T",  "2502.T",  "4901.T",
        "TKOMY",   "NTDOY",   "MTSFY",   "ALPMY",   "PCRHY",
        "DFKUY",   "EBCO",    "SNYYF",   "YACAF",   "OPHYY",
    ],

    # ═══════════════════════════════════════════════════════
    # DEUTSCHLAND — DAX / MDAX / SDAX
    # ═══════════════════════════════════════════════════════
    "DAX": [
        "ADS.DE", "AIR.DE", "ALV.DE", "BAS.DE", "BAYN.DE", "BEI.DE",
        "BMW.DE", "CBK.DE", "CON.DE", "1COV.DE", "DTG.DE", "DBK.DE",
        "DB1.DE", "DHL.DE", "DTE.DE", "EOAN.DE", "ENR.DE", "FRE.DE",
        "HEI.DE", "HEN3.DE", "HNR1.DE", "IFX.DE", "MBG.DE", "MRK.DE",
        "MTX.DE", "MUV2.DE", "P911.DE", "PAH3.DE", "PUM.DE", "RHM.DE",
        "RWE.DE", "SAP.DE", "SRT3.DE", "SHL.DE", "SIE.DE", "SY1.DE",
        "TKA.DE", "VNA.DE", "VOW3.DE", "ZAL.DE", "BSRRF", "BMWYY",
        "FMS",
    ],
    "MDAX": [
        "BC8.DE", "BNR.DE", "BOSS.DE", "DEQ.DE", "DUE.DE", "EVD.DE",
        "EVK.DE", "FPE.DE", "FRA.DE", "FME.DE", "GXI.DE", "HNR1.DE",
        "HHE.DE", "HOT.DE", "JUN3.DE", "KRN.DE", "LAN.DE", "LEG.DE",
        "NDX1.DE", "NEM.DE", "PUM.DE", "SAF.DE", "SDF.DE",
        "SIX2.DE", "SZG.DE", "TAG.DE", "TLX.DE", "VNA.DE",
        "WAF.DE", "WCH.DE",
    ],
    "SDAX": [
        "1U1.DE",  "B7A.DE",  "BIL.DE",  "BVB.DE",  "C3X.DE",
        "CEC.DE",  "DIC.DE",  "DWNI.DE", "FIE.DE",  "FRA.DE",
        "FNTN.DE", "GFT.DE",  "GNL.DE",  "HHFA.DE", "HLAG.DE",
        "HDD.DE",  "HORN.DE", "IVU.DE",  "JEN.DE",  "JOST.DE",
        "KLO.DE",  "KWS.DE",  "MLP.DE",  "O2D.DE",  "PBB.DE",
        "PNE3.DE", "PSM.DE",  "QIA.DE",  "SAF.DE",  "SDF.DE",
        "STR.DE",  "TAG.DE",  "TTK.DE",  "VAR1.DE", "VIP.DE",
        "WUW.DE",  "TUI1.DE", "LXS.DE",
    ],

    # ═══════════════════════════════════════════════════════
    # FRANKREICH — CAC 40
    # ═══════════════════════════════════════════════════════
    "CAC40": [
        "AI.PA",    "AIR.PA",   "ALO.PA",   "CS.PA",    "BN.PA",
        "DSY.PA",   "ENGI.PA",  "EL.PA",    "RMS.PA",   "KER.PA",
        "OR.PA",    "LR.PA",    "MC.PA",    "ML.PA",    "ORA.PA",
        "RI.PA",    "PUB.PA",   "RNO.PA",   "SAF.PA",   "SGO.PA",
        "SAN.PA",   "SU.PA",    "GLE.PA",   "STLA.PA",  "STMPA.PA",
        "HO.PA",    "TTE.PA",   "CA.PA",    "BNP.PA",   "ACA.PA",
        "VIE.PA",   "DG.PA",    "WLN.PA",   "EN.PA",    "FR.PA",
        "LI.PA",    "URW.PA",   "MT.AS",    "CRARY",    "PRNDY",
        "BNPQY",    "BOUYY",    "VCISY",    "SCGLY",    "PPRUY",
        "SOCNF",    "HDELY",    "EADSY",
    ],

    # ═══════════════════════════════════════════════════════
    # SPANIEN — IBEX 35
    # ═══════════════════════════════════════════════════════
    "IBEX35": [
        "ACS.MC",  "ACX.MC",  "AMS.MC",  "ANA.MC",  "BBVA.MC",
        "BKT.MC",  "CABK.MC", "CLNX.MC", "COL.MC",  "ELE.MC",
        "ENG.MC",  "FER.MC",  "GRF.MC",  "IAG.MC",  "IBE.MC",
        "IDR.MC",  "ITX.MC",  "MAP.MC",  "MEL.MC",  "MRL.MC",
        "NTGY.MC", "RED.MC",  "REP.MC",  "SAB.MC",  "SAN.MC",
        "TEF.MC",  "VIS.MC",  "IDEXY",
    ],

    # ═══════════════════════════════════════════════════════
    # ITALIEN — FTSE MIB
    # ═══════════════════════════════════════════════════════
    "FTSE_MIB": [
        "A2A.MI",   "AMP.MI",   "BAMI.MI",  "BZU.MI",  "CNHI.MI",
        "ENEL.MI",  "ENI.MI",   "FCMA.MI",  "G.MI",    "HER.MI",
        "IG.MI",    "INW.MI",   "ISP.MI",   "LDO.MI",  "MB.MI",
        "MONC.MI",  "PIRC.MI",  "PRY.MI",   "RACE.MI", "REC.MI",
        "SRG.MI",   "STM.MI",   "TEN.MI",   "TIT.MI",  "TRN.MI",
        "UCG.MI",   "UNI.MI",   "SAPMY",    "EURBF",   "GLOF",
    ],

    # ═══════════════════════════════════════════════════════
    # NIEDERLANDE — AEX
    # ═══════════════════════════════════════════════════════
    "AEX_NETHERLANDS": [
        "ADYEN.AS", "AD.AS",   "AGN.AS",  "AKZA.AS", "MT.AS",
        "ASML.AS",  "HEIA.AS", "HEIO.AS", "IMCD.AS", "INGA.AS",
        "PHIA.AS",  "PRX.AS",  "RAND.AS", "REN.AS",  "SHELL.AS",
        "NN.AS",    "WKL.AS",  "UMG.AS",  "BESI.AS", "LIGHT.AS",
        "ADRNY",    "AKZOY",   "AAMWY",   "NXPI",
    ],

    # ═══════════════════════════════════════════════════════
    # SCHWEIZ — SMI
    # ═══════════════════════════════════════════════════════
    "SMI_SWITZERLAND": [
        "NESN.SW",  "ROG.SW",   "NOVN.SW",  "ABBN.SW",  "ADEN.SW",
        "ALC.SW",   "CFR.SW",   "CSGN.SW",  "GEBN.SW",  "GIVN.SW",
        "HOLN.SW",  "KNIN.SW",  "LONN.SW",  "PGHN.SW",  "SGSN.SW",
        "SIKA.SW",  "SLHN.SW",  "SRENH.SW", "UBSG.SW",  "ZURN.SW",
        "LINDT.SW", "BALN.SW",  "LOGI",
    ],

    # ═══════════════════════════════════════════════════════
    # SKANDINAVIEN — OMX Nordic
    # ═══════════════════════════════════════════════════════
    "NORDIC_OMXS": [
        "VOLV-B.ST", "ERIC-B.ST", "ASSA-B.ST", "SEB-A.ST",  "SHB-A.ST",
        "SWED-A.ST", "ATCO-A.ST", "SAND.ST",   "SKF-B.ST",  "ALFA.ST",
        "INVE-B.ST", "ESSITY-B.ST","NDA-SE.ST", "LOOMIS.ST", "HEXA-B.ST",
        "NIBE-B.ST", "HUFV-A.ST", "HUSQ-B.ST", "KINV-B.ST", "SINCH.ST",
        "NOVO-B.CO", "CARL-B.CO", "MAERSK-B.CO","ORSTED.CO","DEMANT.CO",
        "COLOB.CO",  "GN.CO",     "ROCK-B.CO", "EQNR",      "AKRBP.OL",
        "VAR.OL",    "DNO.OL",    "MOWI.OL",   "TEL.OL",    "ORK.OL",
        "SALM.OL",   "YAR.OL",    "KNEBV.HE",  "NESTE.HE",  "FORTUM.HE",
        "WRT1V.HE",  "OUT1V.HE",  "ATLKY",     "AMKBY",     "VLVLY",
        "RYAAY",     "NVO",
    ],

    # ═══════════════════════════════════════════════════════
    # EMERGING MARKETS — Breite Auswahl (Brasilien, Indien, etc.)
    # ═══════════════════════════════════════════════════════
    "EMERGING_MARKETS": [
        "PBR",    "VALE",   "ITUB",   "BBD",    "ABEV",
        "BRFS",   "EMBR3.SA","PETR4.SA","INFY",   "WIT",
        "HDB",    "IBN",    "TTM",    "SIFY",   "VEDL",
        "NPN.JO", "AGL.JO", "FSR.JO", "SBK.JO", "TKFEN.IS",
        "BIMAS.IS","EREGL.IS","AMXL.MX","FEMSAUBD.MX","TLKM",
        "BSRR",   "2222.SR","CHKP",   "NICE",   "CHL",
        "ESLT",   "BSBR",   "BBDO",   "UNLRF",  "BCRFY",
        "FMTYP",  "TIMB",   "GGAL",   "CIB",    "IMPUY",
        "HMY",    "GARPF",  "EMBJ",   "WMLWY",  "BVN",
        "BAP",    "AGNC",
    ],
}

# ═══════════════════════════════════════════════════════════════
# WÄHRUNGS-MAPPING nach Ticker-Suffix
# ═══════════════════════════════════════════════════════════════
CURRENCY_MAP = {
    ".DE": "€",  ".PA": "€",  ".MC": "€",  ".MI": "€",
    ".AS": "€",  ".VI": "€",  ".LS": "€",  ".HE": "€",
    ".L":  "£",
    ".SW": "CHF",
    ".OL": "NOK", ".ST": "SEK", ".CO": "DKK",
    ".T":  "¥",   ".HK": "HK$", ".KS": "₩",
    ".JO": "ZAR", ".SA": "BRL", ".MX": "MXN",
    ".IS": "TRY", ".SR": "SAR",
}


def get_currency(ticker: str) -> str:
    """Gibt das Währungssymbol für einen Ticker zurück."""
    upper = ticker.upper()
    for suffix, symbol in CURRENCY_MAP.items():
        if upper.endswith(suffix.upper()):
            return symbol
    return "$"  # Default: US-Dollar


def get_all_tickers() -> list:
    """Gibt alle einzigartigen Ticker in fester Reihenfolge zurück."""
    seen   = set()
    result = []
    for tickers in TICKER_LISTS.values():
        for t in tickers:
            if t not in seen:
                seen.add(t)
                result.append(t)
    return sorted(result)


def get_tickers_by_group(group: str) -> list:
    """Gibt die Ticker einer bestimmten Gruppe zurück."""
    return TICKER_LISTS.get(group, [])


def get_all_groups() -> list:
    """Gibt alle Gruppen-Namen zurück."""
    return list(TICKER_LISTS.keys())


def get_ticker_count() -> int:
    """Gibt die Anzahl einzigartiger Ticker zurück."""
    return len(get_all_tickers())


_TICKER_TO_GROUP = None

def get_group_for_ticker(ticker: str) -> str | None:
    """Gibt die (erste) Gruppe zurück, in der ein Ticker geführt wird."""
    global _TICKER_TO_GROUP
    if _TICKER_TO_GROUP is None:
        _TICKER_TO_GROUP = {}
        for group, tickers in TICKER_LISTS.items():
            for t in tickers:
                _TICKER_TO_GROUP.setdefault(t, group)
    return _TICKER_TO_GROUP.get(ticker)


# ─────────────────────────────────────────────────────────────────────────────
# REGIONEN & FILTER
# ─────────────────────────────────────────────────────────────────────────────
_EU_ASIA_SUFFIXES = (".DE", ".PA", ".MC", ".MI", ".AS", ".VI", ".LS", ".HE", ".L",
                     ".SW", ".OL", ".ST", ".CO", ".IS", ".JO", ".SR",
                     ".T", ".HK", ".KS")

REGION_LABELS = {"eu_asia": "Europa/Asien", "us": "USA/Amerika", "all": "Alle Märkte"}


def get_region(ticker: str) -> str:
    """'eu_asia' oder 'us' (Ticker ohne Börsen-Suffix = US-Listing)."""
    return "eu_asia" if ticker.upper().endswith(_EU_ASIA_SUFFIXES) else "us"


def get_tickers_by_region(region: str) -> list:
    if region == "all":
        return get_all_tickers()
    return [t for t in get_all_tickers() if get_region(t) == region]


def get_groups_for_ticker(ticker: str) -> list:
    """ALLE Gruppen, in denen ein Ticker geführt wird."""
    return [g for g, ts in TICKER_LISTS.items() if ticker in ts]
