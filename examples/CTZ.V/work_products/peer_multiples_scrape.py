"""Scrape stockanalysis.com for peer trading multiples (NamSys/CTZ peer-comp work).
Pulls the /statistics/ page (multiples, margins, market cap) and the /financials/ page
(TTM revenue growth) for each peer. Data as of run date.
Run: uv run python work_products/peer_multiples_scrape.py
"""
import re, subprocess, concurrent.futures as cf

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

PEERS = [
    # (group, label, stockanalysis slug)
    ("A", "CSU.TO  Constellation Software", "quote/tsx/CSU"),
    ("A", "TOI.V   Topicus.com",            "quote/tsxv/TOI"),
    ("A", "LMN.V   Lumine Group",           "quote/tsxv/LMN"),
    ("A", "ENGH.TO Enghouse Systems",       "quote/tsx/ENGH"),
    ("A", "SYZ.TO  Sylogist",               "quote/tsx/SYZ"),
    ("A", "VHI.TO  VitalHub",               "quote/tsx/VHI"),
    ("A", "TCS.TO  Tecsys",                 "quote/tsx/TCS"),
    ("A", "ET.TO   Evertz Technologies",    "quote/tsx/ET"),
    ("A", "DSG.TO  Descartes Systems",      "quote/tsx/DSG"),
    ("B", "BCO     Brink's",                "stocks/BCO"),
    ("B", "LOOMIS  Loomis AB",              "quote/sto/LOOMIS"),
    ("B", "6457    Glory Ltd",              "quote/tyo/6457"),
    ("B", "PMTS    CPI Card Group",         "stocks/PMTS"),
    ("B", "EEFT    Euronet Worldwide",      "stocks/EEFT"),
    ("B", "NATL    NCR Atleos",             "stocks/NATL"),
    ("C", "AMSWA   American Software",      "stocks/AMSWA"),
    ("C", "EGAN    eGain",                  "stocks/EGAN"),
    ("C", "SLP     Simulations Plus",       "stocks/SLP"),
    ("C", "TRAK    ReposiTrak",             "stocks/TRAK"),
    ("C", "CCRD    CoreCard",               "stocks/CCRD"),
    ("C", "CER.L   Cerillion",              "quote/lon/CER"),
    ("C", "NET.L   Netcall",                "quote/lon/NET"),
    ("C", "CRW.L   Craneware",              "quote/lon/CRW"),
    ("C", "TRCS.L  Tracsis",                "quote/lon/TRCS"),
    # Added 2026-09-17 in response to verifier round 1, objection 1: these four rows
    # appear in work_products/terminal_value.md s4.1 but were previously missing from
    # this list, so the committed script could not reproduce them.
    ("C", "MNDO    Mind C.T.I.",             "stocks/MNDO"),
    ("C", "NTWK    NetSol Technologies",     "stocks/NTWK"),
    ("C", "DOTD.L  Dotdigital",              "quote/lon/DOTD"),
    ("C", "IGP.L   Intercede",               "quote/lon/IGP"),
]

KEYS = ["Market Cap", "Enterprise Value", "Revenue", "PE Ratio", "Forward PE",
        "EV / Sales", "EV / EBITDA", "EV / EBIT", "EV / FCF", "Gross Margin",
        "Operating Margin", "EBITDA Margin", "Profit Margin", "Net Cash",
        "Return on Invested Capital (ROIC)", "Dividend Yield", "Average Volume (20 Days)"]


def fetch(url):
    return subprocess.run(["curl", "-sL", "-m", "45", "-A", UA, url],
                          capture_output=True, text=True).stdout


def table_rows(html):
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    out = []
    for m in re.finditer(r"<tr[^>]*>(.*?)</tr>", h, flags=re.S | re.I):
        cells = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", c)).replace("&nbsp;", " ").strip()
                 for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", m.group(1), flags=re.S | re.I)]
        cells = [c for c in cells if c]
        if len(cells) >= 2:
            out.append(cells)
    return out


def one(peer):
    grp, label, slug = peer
    stats = {c[0]: c[1] for c in reversed(table_rows(fetch(f"https://stockanalysis.com/{slug}/statistics/")))}
    fin = table_rows(fetch(f"https://stockanalysis.com/{slug}/financials/"))
    ttm, growth = "", ""
    for c in fin:
        if c[0].startswith("Period Ending") and not ttm:
            ttm = c[1]
        if c[0] == "Revenue Growth" and not growth:
            growth = c[1]
    lines = [f"\n### [{grp}] {label}   https://stockanalysis.com/{slug}/statistics/",
             f"  TTM period: {ttm} | TTM Revenue Growth YoY: {growth or 'n/a'}"]
    for k in KEYS:
        if k in stats:
            lines.append(f"  {k:36s} {stats[k]}")
    return "\n".join(lines)


if __name__ == "__main__":
    with cf.ThreadPoolExecutor(8) as ex:
        for r in ex.map(one, PEERS):
            print(r)
