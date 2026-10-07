"""Implied multiples for 2025 take-privates most relevant to NamSys (CTZ) terminal multiple.
All inputs sourced; see comments for URLs. Run: uv run python work_products/peer_deal_multiples.py
"""

def show(name, ev, rev, ebitda=None, ebit=None, cur="C$", note=""):
    print(f"{name}")
    print(f"  EV/Sales      = {cur}{ev:.1f}M / {cur}{rev:.1f}M = {ev/rev:.2f}x")
    if ebitda:
        print(f"  EV/EBITDA     = {cur}{ev:.1f}M / {cur}{ebitda:.1f}M = {ev/ebitda:.1f}x")
    if ebit:
        print(f"  EV/EBIT       = {cur}{ev:.1f}M / {cur}{ebit:.1f}M = {ev/ebit:.1f}x")
    if note:
        print(f"  note: {note}")
    print()


# --- Quorum Information Technologies (TSXV: QIS) -> Valsoft, announced 2025-09-22, closed 2025-12-10
# Transaction value ~C$60M at C$0.80/sh cash; premium ~14% to 2025-09-19 close, ~12% to 10-day VWAP.
#   https://www.valsoftcorp.com/news/valsoft-corporation-announces-agreement-to-acquire-quorum-information-technologies-in-an-all-cash-transaction
# FY2024 revenue C$40.0M, FY2024 record Adjusted EBITDA C$8.3M
#   https://quoruminfotech.com/quorum-announces-q4-and-year-end-2024-results/
# 9M-2025 Adjusted EBITDA = 1.5 (Q1) + 1.8 (Q2) + 1.9 (Q3) = C$5.2M -> annualised ~C$6.9M
#   https://finance.yahoo.com/news/quorum-announces-q2-2025-results-210000095.html
#   https://www.globenewswire.com/news-release/2025/11/19/3191494/0/en/quorum-announces-q3-2025-results.html
# Net cash ~C$0.5M at TTM Sep-2025 (stockanalysis.com), so EV ~= equity value.
q_9m = 1.5 + 1.8 + 1.9
show("Quorum / Valsoft (FY2024 basis)", 60.0, 40.0, ebitda=8.3,
     note="99% recurring SaaS+BDC; 48.7% gross margin, 6.4% op margin (much lower quality than NamSys)")
show("Quorum / Valsoft (2025 run-rate basis)", 60.0, 40.0, ebitda=q_9m * 4 / 3,
     note=f"9M-2025 adj EBITDA C${q_9m:.1f}M annualised")

# --- Logility (NASDAQ: LGTY, formerly American Software AMSWA) -> Aptean/TA+Vista, closed 2025-04-04
# $14.30/sh cash, EV ~US$490M, 27.0% premium to 2025-01-23 close
#   https://www.ta.com/news/aptean-enters-into-definitive-agreement-to-acquire-logility/
# TTM revenue US$101.87M (stockanalysis.com last reported TTM Jan-2025)
show("Logility / Aptean", 490.0, 101.87, cur="US$",
     note="supply-chain VMS, ~7.7% op margin at time of deal; EV/EBITDA not disclosed")

# --- CoreCard (NYSE: CCRD) -> Euronet (EEFT), announced 2025-07-30, closed 2025-10-30
# ~US$248M / $30 per share, stock-for-stock, ~14% premium; press reports 14.85x EBITDA
#   https://www.fintechfutures.com/m-a/euronet-acquires-corecard
#   https://www.insidearbitrage.com/2025/07/euronet-worldwide-acquires-corecard-for-248-million/
# TTM revenue US$64.81M, EBITDA margin 20.99% -> EBITDA ~US$13.6M (stockanalysis.com TTM Jun-2025)
show("CoreCard / Euronet", 248.0, 64.81, ebitda=64.81 * 0.2099, cur="US$",
     note="compare to press-reported 14.85x EBITDA; deal value likely equity value (CoreCard had net cash US$27.5M)")

# --- Sapiens International (NASDAQ: SPNS) -> Advent International, announced 2025-08-13, closed 2025-12-17
# ~US$2.5B equity value at $43.50/sh cash; ~64% premium to the 2025-08-08 close of $26.52
#   https://www.prnewswire.com/news-releases/sapiens-to-be-acquired-advent-25-billion-302528654.html
#   https://www.calcalistech.com/ctechnews/article/q0vo848ts
# Frozen stockanalysis.com values at deal price: EV US$2.39B, TTM rev US$564.33M, EBITDA margin 16.56%
show("Sapiens / Advent", 2390.0, 564.33, ebitda=564.33 * 0.1656, cur="US$",
     note="insurance VMS, 4.7% rev growth, 13.7% op margin; 64% takeover premium = large prior public discount")

print("Takeover premiums observed in 2025 small/mid-cap VMS take-privates:")
for n, prem, src in [("Quorum (TSXV microcap)", 14, "valsoftcorp.com press release"),
                     ("CoreCard (NYSE small cap)", 14, "fintechfutures.com"),
                     ("Logility (Nasdaq small cap)", 27, "ta.com press release"),
                     ("Sapiens (Nasdaq mid cap)", 64, "prnewswire / calcalistech")]:
    print(f"  {n:30s} +{prem:>2d}%   [{src}]")
