"""
NamSys Inc. (TSXV: CTZ) -- Terminal value at end of FY2030E.

Terminal value = (multiple) x (FY2030E owners' earnings).  NOT discounted to present value.
No NamSys share price, market capitalisation or price-derived input is used anywhere in this file.

Every input below carries a source tag:
  FC   = work_products/forecast_earnings.md  (itself an output of forecast_earnings_calcs.py)
  OE   = work_products/owners_earnings_and_roic.md
  FS25 = primary_sources/FY2025/NamSys_AFS_022426.md
  FSQ2 = primary_sources/2Q2026/FS_Q2_NamSys_Apr_30_26_FINAL.md
  MDA25= primary_sources/FY2025/NamSys_MDA_022426.md
  AM25 = fetched_docs/namsys_2025_annual_meeting_transcript.md
  AM26 = fetched_docs/namsys_2026_annual_meeting_transcript.md
  PEER = work_products/peer_multiples_scrape.py / peer_deal_multiples.py  (stockanalysis.com,
         scraped 17 Sep 2026; deal multiples from the company/press URLs listed in that script)

Run:  uv run python work_products/terminal_value_calcs.py
"""

# ----------------------------------------------------------------------------------
# 1. FY2030E terminal-year inputs  (all from FC section 1)
# ----------------------------------------------------------------------------------
OE_FY2030 = {
    "base":            2_859_320,   # FC s1 headline table
    "bull":            4_649_840,   # FC s1
    "bear_no_cost":    1_505_664,   # FC s1  (bear, no cost response)
    "bear_rightsized": 2_094_988,   # FC s1  (bear, management right-sizes)
}
REV_FY2030_BASE = 11_462_356        # FC s1 base-case revenue table
EBIT_FY2030_BASE = 3_936_580        # FC s1 base-case operating income
DA_FY2025 = 7_465                   # FS25 Note 4 depreciation of property and equipment
TAX_RATE = 0.265                    # MDA25 "The basic rate of 26.50% was applied"

# FY2025 actuals, for the quality/consistency checks
REV_FY2025 = 7_891_605              # FS25 statement of operations
EBIT_FY2025 = 3_146_476             # FS25 / FC s2.1
OE_FY2025 = 2_250_271               # OE s2.1
RECURRING_FY2025 = 7_811_909        # FS25 Note 7 "Software subscriptions, hosted services..."
IC_FY2025 = 991_988                 # OE s3.1 operating invested capital, period end

print("=" * 78)
print("SECTION 1 -- terminal-year earnings object and its relationship to peer metrics")
print("=" * 78)
oe_to_ebit = OE_FY2030["base"] / EBIT_FY2030_BASE
print(f"FY2030E base owners' earnings            : {OE_FY2030['base']:>12,.0f}")
print(f"FY2030E base operating income (EBIT)     : {EBIT_FY2030_BASE:>12,.0f}")
print(f"FY2030E base revenue                     : {REV_FY2030_BASE:>12,.0f}")
print(f"Owners' earnings / EBIT                  : {oe_to_ebit:>12.4f}")
print(f"(1 - statutory tax rate), for comparison : {1-TAX_RATE:>12.4f}")
print(f"EBITDA/EBIT uplift if D&A stays at FY2025 level: "
      f"{(EBIT_FY2030_BASE + DA_FY2025)/EBIT_FY2030_BASE - 1:.3%}  -> EBITDA ~= EBIT")
print()
print("Conversion factor to restate a peer EV/EBIT multiple as a multiple of owners' earnings:")
ebit_to_oe_factor = 1.0 / oe_to_ebit
print(f"  M_owners_earnings = M_EV/EBIT x {ebit_to_oe_factor:.4f}")
print()

# ----------------------------------------------------------------------------------
# 2. Quality metrics that drive the multiple (FY2025 actuals)
# ----------------------------------------------------------------------------------
print("=" * 78)
print("SECTION 2 -- FY2025 quality metrics (the inputs to the qualitative judgement)")
print("=" * 78)
print(f"Operating margin FY2025                  : {EBIT_FY2025/REV_FY2025:>12.1%}")
print(f"Owners' earnings margin FY2025           : {OE_FY2025/REV_FY2025:>12.1%}")
print(f"Recurring share of FY2025 revenue        : {RECURRING_FY2025/REV_FY2025:>12.1%}")
print(f"Operating invested capital / revenue     : {IC_FY2025/REV_FY2025:>12.1%}")
print(f"ROIC on period-end operating IC          : {OE_FY2025/IC_FY2025:>12.0%}")
# Customer concentration, FS25 Note 7 and FSQ2 Note 7
top3_fy2025 = [0.159, 0.123, 0.107]     # FS25 Note 7
top3_h1fy2026 = [0.131, 0.128, 0.114]   # FSQ2 Note 7 (via FC s4.1)
top3_fy2024 = [0.200, 0.089, 0.089]     # FS25 Note 7 comparative
print(f"Top-3 customer share FY2024 / FY2025 / H1FY2026: "
      f"{sum(top3_fy2024):.1%} / {sum(top3_fy2025):.1%} / {sum(top3_h1fy2026):.1%}")
print(f"FY2030E base terminal growth (revenue)   : "
      f"{REV_FY2030_BASE/10_797_518 - 1:>12.1%}   (FY2029E -> FY2030E, FC s1)")
# Verifier round 1, objection 4: the margin gap that justifies the premium over the
# Enghouse/Quorum anchors must be stated on the FY2030E margin actually capitalised,
# not the higher FY2025A margin.
MGN_FY2030 = EBIT_FY2030_BASE / REV_FY2030_BASE
ENGH_EBIT_MGN, QUORUM_EBIT_MGN = 0.186, 0.064   # PEER; DEAL
print(f"\nOperating margin actually capitalised (FY2030E): {MGN_FY2030:.1%}"
      f"   vs FY2025A {EBIT_FY2025/REV_FY2025:.1%}")
print(f"  FY2030E margin / Enghouse 18.6% = {MGN_FY2030/ENGH_EBIT_MGN:.2f}x"
      f"   (on FY2025A it would be {EBIT_FY2025/REV_FY2025/ENGH_EBIT_MGN:.2f}x)")
print(f"  FY2030E margin / Quorum   6.4% = {MGN_FY2030/QUORUM_EBIT_MGN:.2f}x"
      f"   (on FY2025A it would be {EBIT_FY2025/REV_FY2025/QUORUM_EBIT_MGN:.2f}x)")
print()

# ----------------------------------------------------------------------------------
# 3. Anchor A -- peer trading multiples, restated onto owners' earnings
# ----------------------------------------------------------------------------------
print("=" * 78)
print("SECTION 3 -- ANCHOR A: peer trading multiples restated as x owners' earnings")
print("=" * 78)
# (name, EV/EBIT, one-line relevance note).  Source: PEER (stockanalysis.com, 17 Sep 2026)
peers_ev_ebit = [
    ("Enghouse (TSX:ENGH)          ",  7.6, "mature, -4.7% growth, 18.6% EBIT mgn, net cash"),
    ("Open Text (OTEX)             ",  8.8, "mature, +1.5% growth, 22.9% EBIT mgn, levered"),
    ("Dotdigital (AIM:DOTD)        ",  8.1, "microcap SaaS, +2.2% growth, 16.0% EBIT mgn"),
    ("NetSol (NTWK)                ",  7.8, "microcap, +12.4% growth, 7.9% EBIT mgn"),
    ("eGain (EGAN)                 ",  9.0, "microcap SaaS, +3.1% growth, 8.7% EBIT mgn"),
    ("Cerillion (AIM:CER)          ", 11.7, "closest margin analogue: 39.5% EBIT mgn, -6.4% growth"),
    ("Evertz (TSX:ET)              ", 11.7, "Cdn microcap, +3.9% growth (hardware, not SaaS)"),
    ("Intercede (AIM:IGP)          ", 17.4, "microcap, 18.4% EBIT mgn, -1.3% growth"),
    ("ReposiTrak (TRAK)            ", 16.4, "32.2% EBIT mgn, +6.6% growth -- best quality match"),
    ("Mind C.T.I. (MNDO)           ",  2.9, "shrinking microcap -- floor observation"),
    ("Descartes (TSX:DSG)          ", 25.6, "32.0% EBIT mgn but +13.2% growth, large/liquid"),
    ("Constellation (TSX:CSU)      ", 22.7, "serial acquirer, +17.7% growth -- upper bound"),
    ("Glory (TYO:6457)             ",  8.7, "cash-handling hardware incumbent"),
    ("Loomis (STO:LOOMIS)          ", 12.1, "cash-logistics incumbent, capital intensive"),
    ("Brink's (BCO)                ", 13.0, "cash-logistics incumbent, capital intensive"),
]
print(f"{'Peer':<32}{'EV/EBIT':>9}{'-> x OE':>10}   note")
for name, m, note in peers_ev_ebit:
    print(f"{name:<32}{m:>9.1f}{m*ebit_to_oe_factor:>10.1f}   {note}")

mature_micro_software = [7.6, 8.8, 8.1, 7.8, 9.0, 11.7, 11.7]
quality_micro_software = [11.7, 16.4, 17.4]
cash_ecosystem = [8.7, 12.1, 13.0]
def rng(xs):
    return (min(xs) * ebit_to_oe_factor, sum(xs)/len(xs) * ebit_to_oe_factor,
            max(xs) * ebit_to_oe_factor)
for label, xs in [("Mature low-growth microcap software", mature_micro_software),
                  ("High-margin microcap software      ", quality_micro_software),
                  ("Cash-ecosystem incumbents          ", cash_ecosystem)]:
    lo, mid, hi = rng(xs)
    print(f"\n{label}: {lo:.1f}x - {hi:.1f}x owners' earnings (mean {mid:.1f}x)")
print()

# ----------------------------------------------------------------------------------
# 4. Anchor B -- M&A / take-private multiples
# ----------------------------------------------------------------------------------
print("=" * 78)
print("SECTION 4 -- ANCHOR B: take-private multiples restated as x owners' earnings")
print("=" * 78)
# EBITDA ~= EBIT for NamSys (Section 1), so EV/EBITDA maps with the same factor.
deals = [
    ("Quorum Info Tech (TSXV:QIS) -> Valsoft, Dec-25", 7.2, 8.7,
     "TSXV, 99% recurring VMS, C$40M rev, 6.4% EBIT mgn"),
    ("CoreCard (CCRD) -> Euronet, Oct-25          ", 14.85, 18.2,
     "US$248M deal, payments software"),
    ("Sapiens (SPNS) -> Advent, Dec-25            ", 25.6, 25.6,
     "US$2.5B, insurance VMS, mid-cap"),
]
print(f"{'Deal':<48}{'EV/EBITDA range':>18}{'-> x OE':>18}")
for name, lo, hi, note in deals:
    print(f"{name:<48}{lo:>8.1f} - {hi:<7.1f}"
          f"{lo*ebit_to_oe_factor:>9.1f} - {hi*ebit_to_oe_factor:<7.1f}")
    print(f"{'':<48}{note}")
print()

# ----------------------------------------------------------------------------------
# 5. Anchor C -- Gordon growth cross-check.  Because operating invested capital is
#    negligible and there is no debt, ~100% of owners' earnings is distributable
#    (OE s5), so multiple = 1 / (r - g) with no reinvestment wedge.
# ----------------------------------------------------------------------------------
print("=" * 78)
print("SECTION 5 -- ANCHOR C: Gordon growth cross-check, multiple = 1/(r-g)")
print("=" * 78)
# r components.  The short risk-free proxy is SOURCED: NamSys's own cashable GICs
# yielded 2.00%-2.45% (FSQ2 Note 15).  The premia are ANALYST JUDGEMENT, flagged as such.
rf = 0.0225                  # midpoint of 2.00%-2.45% cashable GIC yields, FSQ2 Note 15
print(f"Short risk-free proxy (FSQ2 Note 15 GIC yields, midpoint): {rf:.2%}")
print("Equity risk premium + size/illiquidity/concentration premium: ANALYST JUDGEMENT")
rs = [0.100, 0.110, 0.120, 0.130]
gs = [0.000, 0.010, 0.020, 0.030, 0.040]
print(f"\n{'r \\ g':>8}" + "".join(f"{g:>9.1%}" for g in gs))
for r in rs:
    row = f"{r:>8.1%}"
    for g in gs:
        row += f"{1.0/(r-g):>9.1f}"
    print(row)
print("\nImplied perpetual owners'-earnings growth at selected multiples:")
for m in [9, 10, 12, 15, 18]:
    print(f"  {m:>2}x OE -> (r - g) = {1/m:.2%};  g = {0.115 - 1/m:>6.2%} at r = 11.5%;"
          f"  g = {0.125 - 1/m:>6.2%} at r = 12.5%")
print()

# ----------------------------------------------------------------------------------
# 6. Selected multiple and terminal value
# ----------------------------------------------------------------------------------
print("=" * 78)
print("SECTION 6 -- TERMINAL VALUE AT END OF FY2030 (October 31, 2030). NOT discounted.")
print("=" * 78)
MULT_LOW, MULT_BASE, MULT_HIGH = 9.0, 12.0, 15.0
print(f"{'Multiple on FY2030E owners earnings':<40}"
      f"{MULT_LOW:>12.1f}x{MULT_BASE:>12.1f}x{MULT_HIGH:>12.1f}x")
print("-" * 78)
for k, v in OE_FY2030.items():
    print(f"{k+' (FY2030E OE '+format(v, ',')+')':<40}"
          f"{v*MULT_LOW:>13,.0f}{v*MULT_BASE:>13,.0f}{v*MULT_HIGH:>13,.0f}")
print()
tv_base = OE_FY2030["base"] * MULT_BASE
print(f"HEADLINE: base case, {MULT_BASE:.0f}x x {OE_FY2030['base']:,.0f} "
      f"= {tv_base:,.0f} CAD of operating-business value at 31-Oct-2030")
print()

# Scenario-consistent ("diagonal") multiples: the multiple and the earnings path are
# not independent, so a single multiple across scenarios overstates the spread's
# credibility in the bull case and understates the damage in the bear case.
diag = {"bull": 15.0, "base": 12.0, "bear_rightsized": 8.0, "bear_no_cost": 8.0}
print("Scenario-consistent pairing (multiple co-moves with the scenario's implied quality):")
for k in ["bull", "base", "bear_rightsized", "bear_no_cost"]:
    print(f"  {k:<18} {diag[k]:>5.1f}x x {OE_FY2030[k]:>10,.0f} = {diag[k]*OE_FY2030[k]:>12,.0f}")
print()

# ----------------------------------------------------------------------------------
# 7. Cross-checks on the selected base multiple
# ----------------------------------------------------------------------------------
print("=" * 78)
print("SECTION 7 -- cross-checks on the 12x base multiple")
print("=" * 78)
print(f"Implied EV / FY2030E revenue             : {tv_base/REV_FY2030_BASE:>12.2f}x")
print(f"Implied EV / FY2030E EBIT                : {tv_base/EBIT_FY2030_BASE:>12.2f}x")
print(f"Implied EV / FY2030E EBITDA              : "
      f"{tv_base/(EBIT_FY2030_BASE+DA_FY2025):>12.2f}x")
print(f"Implied owners'-earnings yield           : {OE_FY2030['base']/tv_base:>12.2%}")
print(f"Implied multiple on FY2025A owners' earn.: {tv_base/OE_FY2025:>12.2f}x  "
      f"(i.e. what FY2025 earnings would be worth at the FY2030 value)")
# Peer EV/Sales at comparable margin, for the EV/Sales cross-check (PEER)
print("\nPeer EV/Sales at stated EBIT margin (PEER, 17-Sep-2026):")
for name, evs, mgn in [("Cerillion (AIM:CER)", 4.62, 0.395), ("ReposiTrak (TRAK)", 5.27, 0.322),
                       ("Descartes (TSX:DSG)", 8.19, 0.320), ("Dotdigital (AIM:DOTD)", 1.29, 0.160),
                       ("Enghouse (TSX:ENGH)", 1.41, 0.186),
                       ("Quorum take-private", 1.50, 0.064)]:
    print(f"  {name:<24}{evs:>6.2f}x sales at {mgn:>5.1%} EBIT margin")
print(f"  {'NamSys FY2030E at 12x OE':<24}{tv_base/REV_FY2030_BASE:>6.2f}x sales at "
      f"{EBIT_FY2030_BASE/REV_FY2030_BASE:>5.1%} EBIT margin")
print()

# ----------------------------------------------------------------------------------
# 8. What is NOT in the terminal value
# ----------------------------------------------------------------------------------
print("=" * 78)
print("SECTION 8 -- explicitly excluded from the terminal value above")
print("=" * 78)
NET_CASH_APR2026 = 7_370_000   # OE s1/s4, ~$7.37M cash + short-term investments, 30-Apr-2026
print(f"Net cash and short-term investments at 30-Apr-2026 (OE s1): ~{NET_CASH_APR2026:,.0f}")
print("Excluded because owners' earnings exclude interest income (OE s4); the financial")
print("portfolio is a separate asset and would be added alongside, not capitalised at 12x.")
print("Also excluded: any acquisition NamSys might complete (AM26 -- strategy unsuccessful")
print("to date), and the $1,100,000 employee termination commitment (FS25 Note 13),")
print("which is contingent, not an operating liability.")
