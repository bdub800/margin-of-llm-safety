"""
Adobe Inc. (ADBE) — Owners' Earnings and ROIC calculations.

All inputs are taken from:
  - primary_sources/FY2025/financial_statements.md   (FY2025 10-K, FYE Nov 28 2025)
  - primary_sources/FY2025/md_and_a.md
  - primary_sources/2Q2026/financial_statements.md   (Q2 FY2026 10-Q, period end May 29 2026)
  - primary_sources/2Q2026/md_and_a.md
  - primary_sources/4Q2025|1Q2026|2Q2026/earnings_call_transcript.md
  - stores/knowledge_store.json (market data only)

Run: uv run python work_products/owners_earnings_calcs.py
"""

from textwrap import dedent

M = 1_000_000  # not used for scaling; all figures already in $ millions


def line(label, value, unit="$M", w=58):
    print(f"{label:<{w}} {value:>12,.0f} {unit}")


def pct(label, value, w=58):
    print(f"{label:<{w}} {value:>12.1f} %")


print("=" * 84)
print("SECTION 1 — REPORTED INPUTS (all $ millions, from filings)")
print("=" * 84)

# ---------------------------------------------------------------------------
# Income statement (FY2025 10-K Consolidated Statements of Income)
# ---------------------------------------------------------------------------
revenue = {"FY2023": 19_409, "FY2024": 21_505, "FY2025": 23_769}
ebit = {"FY2023": 6_650, "FY2024": 6_741, "FY2025": 8_706}
net_income = {"FY2023": 5_428, "FY2024": 5_560, "FY2025": 7_130}
pretax = {"FY2023": 6_799, "FY2024": 6_931, "FY2025": 8_734}
tax_provision = {"FY2023": 1_371, "FY2024": 1_371, "FY2025": 1_604}
current_tax = {"FY2023": 1_793, "FY2024": 1_839, "FY2025": 2_118}   # Note 10
cash_taxes_paid = {"FY2023": 1_854, "FY2024": 1_727, "FY2025": 2_219}  # CF supplemental
nonop_net = {"FY2023": 149, "FY2024": 190, "FY2025": 28}
interest_expense = {"FY2023": 113, "FY2024": 169, "FY2025": 263}
interest_income = {"FY2023": 269, "FY2024": 341, "FY2025": 264}     # Note 18

# Non-cash / capital items
ppe_depreciation = {"FY2023": 235, "FY2024": 239, "FY2025": 236}    # Note 6
intangible_amort = {"FY2023": 375, "FY2024": 336, "FY2025": 310}    # Note 8 (total, COGS + opex)
sbc = {"FY2023": 1_718, "FY2024": 1_833, "FY2025": 1_942}           # Note 12
capex = {"FY2023": 360, "FY2024": 183, "FY2025": 179}               # CF investing
cfo = {"FY2023": 7_302, "FY2024": 8_056, "FY2025": 10_031}
d_a_accretion = {"FY2023": 872, "FY2024": 857, "FY2025": 818}       # CF
delta_deferred_rev = {"FY2023": 536, "FY2024": 309, "FY2025": 771}  # CF
advertising = {"FY2023": 970, "FY2024": 1_040, "FY2025": 1_370}     # Note 1

# Non-recurring items hitting operating income
# FY2024: Figma acquisition termination fee $1,000M (income statement line);
#         lease-related asset impairments $78M (CF stmt, recorded in G&A per Note 7)
nonrecurring_ebit = {"FY2023": 0, "FY2024": 1_000 + 78, "FY2025": 0}

# ---------------------------------------------------------------------------
# Q2 FY2026 10-Q (six months ended May 29 2026 vs May 30 2025)
# ---------------------------------------------------------------------------
h1_26 = dict(revenue=13_016, ebit=4_656, pretax=4_660, tax=1_059, net_income=3_601,
             cfo=5_123, capex=95, sbc=1_045, intangible_amort=91,
             delta_deferred_rev=117, nonop_net=4, interest_expense=128,
             interest_income=119, goodwill_impair=70, loss_contingency=92,
             d_a_accretion=367)
h1_25 = dict(revenue=11_587, ebit=4_272, pretax=4_283, tax=781, net_income=3_502,
             cfo=4_673, capex=73, sbc=956, intangible_amort=167,
             delta_deferred_rev=75, nonop_net=11, interest_expense=130,
             interest_income=136, goodwill_impair=0, loss_contingency=0,
             d_a_accretion=426)

# TTM through Q2 FY2026 = FY2025 - 1H FY2025 + 1H FY2026
ttm = {k: revenue["FY2025"] - h1_25["revenue"] + h1_26["revenue"] if k == "revenue" else None
       for k in ["revenue"]}
ttm_revenue = revenue["FY2025"] - h1_25["revenue"] + h1_26["revenue"]
ttm_ebit = ebit["FY2025"] - h1_25["ebit"] + h1_26["ebit"]
ttm_cfo = cfo["FY2025"] - h1_25["cfo"] + h1_26["cfo"]
ttm_capex = capex["FY2025"] - h1_25["capex"] + h1_26["capex"]
ttm_sbc = sbc["FY2025"] - h1_25["sbc"] + h1_26["sbc"]
ttm_intangible_amort = intangible_amort["FY2025"] - h1_25["intangible_amort"] + h1_26["intangible_amort"]
ttm_nonrecurring = h1_26["goodwill_impair"] + h1_26["loss_contingency"]   # both fell in 1H FY2026
ttm_delta_def_rev = delta_deferred_rev["FY2025"] - h1_25["delta_deferred_rev"] + h1_26["delta_deferred_rev"]
ttm_nonop_net = nonop_net["FY2025"] - h1_25["nonop_net"] + h1_26["nonop_net"]
# PP&E depreciation is not separately disclosed in the 10-Q. Net PP&E is essentially
# unchanged ($1,873M -> $1,870M), so FY2025's $236M is carried as the TTM estimate.
ttm_ppe_dep_est = 236

line("TTM revenue (FY25 - 1H25 + 1H26)", ttm_revenue)
line("TTM operating income (EBIT)", ttm_ebit)
line("TTM cash flow from operations", ttm_cfo)
line("TTM capital expenditure", ttm_capex)
line("TTM stock-based compensation", ttm_sbc)
line("TTM amortisation of purchased intangibles", ttm_intangible_amort)
line("TTM non-recurring charges in EBIT (goodwill imp. + FTC contingency)", ttm_nonrecurring)

print()
print("=" * 84)
print("SECTION 2 — MAINTENANCE CAPEX AND NORMALISED TAX RATE (the two judgment calls)")
print("=" * 84)

# --- Maintenance capex --------------------------------------------------------
# Adobe rents essentially all compute (purchase obligations, Note 16), so capex is
# facilities + internal IT. Net PP&E has DECLINED (1,936 -> 1,873 -> 1,870), i.e.
# recent capex is running below depreciation. To avoid flattering owners' earnings
# with a one-year capex dip, maintenance capex = 3-year average actual capex.
maint_capex = (capex["FY2023"] + capex["FY2024"] + capex["FY2025"]) / 3
line("3-yr average actual capex (FY23-FY25) = maintenance capex used", maint_capex)
line("  for reference: FY2025 PP&E depreciation", ppe_depreciation["FY2025"])
line("  for reference: TTM actual capex", ttm_capex)

# --- Normalised tax rate ------------------------------------------------------
# Two anchors disagree, and the gap is a timing item:
#   GAAP effective tax rate: 20% (FY23), 20% (FY24), 18% (FY25), 23% (1H FY26),
#     ~22.5% guided FY2026 (4Q25 + 2Q26 transcripts).
#   Cash/current tax rate: much higher because Sec.174 forced capitalisation of
#     domestic R&D (deferred tax asset "capitalized expenses" $2,065M at FY2025).
#   The One Big Beautiful Bill Act restores immediate R&D expensing from FY2026 and
#     Adobe "anticipate[s] a reduction to our effective rates for cash taxes paid"
#     (2Q2026 md_and_a.md), so the cash rate should converge DOWN toward the GAAP rate.
gaap_etr = {"FY2023": 0.20, "FY2024": 0.20, "FY2025": 0.18, "FY2026E": 0.225}
cash_rate = {y: cash_taxes_paid[y] / pretax[y] for y in cash_taxes_paid}
current_rate = {y: current_tax[y] / pretax[y] for y in current_tax}
for y in cash_rate:
    pct(f"  cash taxes paid / pre-tax income, {y}", 100 * cash_rate[y])
for y in current_rate:
    pct(f"  current tax provision / pre-tax income, {y}", 100 * current_rate[y])
avg_gaap = sum(gaap_etr.values()) / len(gaap_etr)
pct("  average GAAP ETR, FY2023-FY2026E", 100 * avg_gaap)

TAX_BASE = 0.21     # base case
TAX_LOW = 0.18      # management's non-GAAP / 3-yr projected rate
TAX_HIGH = 0.25     # recent cash-tax experience persisting
pct("NORMALISED TAX RATE USED (base)", 100 * TAX_BASE)

print()
print("=" * 84)
print("SECTION 3 — METHOD A: OWNERS' EARNINGS FROM NORMALISED OPERATING EARNINGS")
print("=" * 84)
print(dedent("""
    Construction (unlevered, per the brief: interest expense added back and interest
    income removed, so financing is handled separately on the balance sheet):

      Operating income (EBIT)
      + non-recurring charges booked in operating expenses
      + amortisation of PURCHASED intangibles   (not an economic cost: the acquired
          asset base is maintained by R&D and S&M that are already expensed; the
          corresponding capital stays in invested capital)
      + PP&E depreciation
      - maintenance capex
      = pre-tax owners' earnings
      x (1 - normalised tax rate)
      = OWNERS' EARNINGS

    Stock-based compensation is deliberately NOT added back. It is a real cost to
    owners and is already deducted inside EBIT.
"""))


def method_a(ebit_v, nonrec_v, intang_v, dep_v, maint_v, tax_rate):
    pretax_oe = ebit_v + nonrec_v + intang_v + dep_v - maint_v
    return pretax_oe, pretax_oe * (1 - tax_rate)


oe_a = {}
for y in ["FY2023", "FY2024", "FY2025"]:
    p, o = method_a(ebit[y], nonrecurring_ebit[y], intangible_amort[y],
                    ppe_depreciation[y], maint_capex, TAX_BASE)
    oe_a[y] = o
    print(f"\n{y}:")
    line("  operating income (EBIT)", ebit[y])
    line("  + non-recurring charges in EBIT", nonrecurring_ebit[y])
    line("  + amortisation of purchased intangibles", intangible_amort[y])
    line("  + PP&E depreciation", ppe_depreciation[y])
    line("  - maintenance capex", -maint_capex)
    line("  = pre-tax owners' earnings", p)
    line(f"  - normalised tax @ {TAX_BASE:.0%}", -p * TAX_BASE)
    line("  = OWNERS' EARNINGS", o)
    pct("    as % of revenue", 100 * o / revenue[y])

p_ttm, oe_ttm = method_a(ttm_ebit, ttm_nonrecurring, ttm_intangible_amort,
                         ttm_ppe_dep_est, maint_capex, TAX_BASE)
oe_a["TTM_Q2FY26"] = oe_ttm
print("\nTTM through Q2 FY2026:")
line("  operating income (EBIT)", ttm_ebit)
line("  + goodwill impairment ($70M) + FTC loss contingency ($92M)", ttm_nonrecurring)
line("  + amortisation of purchased intangibles", ttm_intangible_amort)
line("  + PP&E depreciation (estimate, see note)", ttm_ppe_dep_est)
line("  - maintenance capex", -maint_capex)
line("  = pre-tax owners' earnings", p_ttm)
line(f"  - normalised tax @ {TAX_BASE:.0%}", -p_ttm * TAX_BASE)
line("  = OWNERS' EARNINGS", oe_ttm)
pct("    as % of revenue", 100 * oe_ttm / ttm_revenue)

print("\nGrowth in owners' earnings:")
pct("  FY2023 -> FY2024", 100 * (oe_a["FY2024"] / oe_a["FY2023"] - 1))
pct("  FY2024 -> FY2025", 100 * (oe_a["FY2025"] / oe_a["FY2024"] - 1))
pct("  FY2025 -> TTM Q2 FY2026", 100 * (oe_a["TTM_Q2FY26"] / oe_a["FY2025"] - 1))

print("\nTax-rate sensitivity on the TTM figure:")
for r in [TAX_LOW, TAX_BASE, TAX_HIGH]:
    line(f"  owners' earnings @ {r:.0%} normalised tax", p_ttm * (1 - r))

print()
print("=" * 84)
print("SECTION 4 — METHOD B: CROSS-CHECK FROM CASH FLOW")
print("=" * 84)
print(dedent("""
    Start at reported CFO and strip out the three things that make CFO NOT owners'
    earnings: (1) SBC is added back inside CFO but is a real cost to owners;
    (2) the growth in the deferred-revenue float is customer cash, not earnings, and
    only recurs while the book keeps growing; (3) net non-operating income must come
    out to keep the measure unlevered. Then deduct maintenance capex.
"""))


def method_b(cfo_v, maint_v, sbc_v, ddr_v, nonop_v, label):
    oe = cfo_v - maint_v - sbc_v - ddr_v - nonop_v
    print(f"\n{label}:")
    line("  cash flow from operations", cfo_v)
    line("  - maintenance capex", -maint_v)
    line("  - stock-based compensation (real cost to owners)", -sbc_v)
    line("  - increase in deferred revenue (growth float, not earnings)", -ddr_v)
    line("  - net non-operating income (keep measure unlevered)", -nonop_v)
    line("  = OWNERS' EARNINGS (cash method, at ACTUAL cash tax rates)", oe)
    return oe


oe_b = {}
for y in ["FY2023", "FY2024", "FY2025"]:
    oe_b[y] = method_b(cfo[y], maint_capex, sbc[y], delta_deferred_rev[y], nonop_net[y], y)
oe_b["TTM_Q2FY26"] = method_b(ttm_cfo, maint_capex, ttm_sbc, ttm_delta_def_rev,
                              ttm_nonop_net, "TTM through Q2 FY2026")

print("\nNOTE: FY2024 cash method is depressed by the $1.0bn Figma termination fee,")
print("which was a cash operating outflow that year (FY2025 md_and_a.md).")

print("\nA vs B reconciliation ($M):")
for y in ["FY2023", "FY2024", "FY2025", "TTM_Q2FY26"]:
    print(f"  {y:<12} Method A {oe_a[y]:>8,.0f}   Method B {oe_b[y]:>8,.0f}   "
          f"diff {oe_b[y]-oe_a[y]:>+7,.0f}  ({100*(oe_b[y]-oe_a[y])/oe_a[y]:>+5.1f}%)")
print(dedent("""
  Exact algebraic bridge (Method B minus Method A), $M. The identity is:
     B - A = (other D&A not in Method A) + other non-cash items
             + (working-capital change excluding deferred revenue)
             - non-recurring add-backs
             - actual current tax + normalised tax
"""))


def bridge(y, d_a_v, ppe_v, intang_v, other_noncash, wc_total, ddr_v, nonrec_v,
           current_tax_v, pretax_oe_v, label):
    other_amort = d_a_v - ppe_v - intang_v
    wc_ex_dr = wc_total - ddr_v
    norm_tax = TAX_BASE * pretax_oe_v
    tot = other_amort + other_noncash + wc_ex_dr - nonrec_v - current_tax_v + norm_tax
    print(f"\n  {label}:")
    line("    + amortisation in D&A that Method A does not add back", other_amort)
    print("      (principally capitalised sales-commission amortisation)")
    line("    + other non-cash items", other_noncash)
    line("    + working-capital change excluding deferred revenue", wc_ex_dr)
    line("    - non-recurring add-backs made in Method A", -nonrec_v)
    line("    - actual current-year tax", -current_tax_v)
    line(f"    + normalised tax @ {TAX_BASE:.0%} added back", norm_tax)
    line("    = Method B minus Method A", tot)
    return tot


# FY2025 working-capital change (CF stmt): -275 -90 +64 +180 -45 +771
bridge("FY2025", 818, 236, 310, 48, (-275 - 90 + 64 + 180 - 45 + 771), 771, 0,
       1_604 + 512, 9_011, "FY2025")
# 1H FY2026 WC change: +368 -377 +15 -215 -53 +117 ; 1H FY2025: +334 -221 +7 -92 -61 +75
wc_ttm = ((-275 - 90 + 64 + 180 - 45 + 771)
          - (334 - 221 + 7 - 92 - 61 + 75)
          + (368 - 377 + 15 - 215 - 53 + 117))
# Other non-cash: FY2025 $48M, less 1H FY2025 $35M, plus 1H FY2026 $76M, plus the
# $70M goodwill impairment which the 1H FY2026 cash-flow statement adds back separately.
oth_nc_ttm = 48 - 35 + 76 + 70
dt_ttm = -512 - (-288) + 111
bridge("TTM", 818 - 426 + 367, 236, ttm_intangible_amort, oth_nc_ttm, wc_ttm,
       ttm_delta_def_rev, ttm_nonrecurring,
       (1_604 - 781 + 1_059) - dt_ttm, p_ttm, "TTM through Q2 FY2026")
print(dedent("""
  Two things dominate the gap: (a) Method A adds back only PP&E depreciation and
  purchased-intangible amortisation, while CFO also adds back amortisation of
  capitalised sales commissions — but the cash cost of those commissions sits in the
  working-capital line, so the two largely cancel; and (b) Adobe's actual cash/current
  tax rate (24-27% of pre-tax income) has run above the 21% normalised rate, because
  Sec.174 forced capitalisation of domestic R&D. FY2023 and FY2024 diverge more: FY2024
  carries the $1.0bn Figma termination fee as a cash outflow that Method A normalises
  out, and FY2023's current tax rate was 26.4%.
"""))

# FCF for reference (this INCLUDES the float, and does NOT charge SBC)
print("Reference: conventional free cash flow (CFO - actual capex), for comparison only:")
for y in ["FY2023", "FY2024", "FY2025"]:
    line(f"  FCF {y}", cfo[y] - capex[y])
line("  FCF TTM Q2 FY2026", ttm_cfo - ttm_capex)

print()
print("=" * 84)
print("SECTION 5 — INVESTED CAPITAL")
print("=" * 84)
print(dedent("""
    Invested capital = net operating assets:
      total assets
        - cash, equivalents and short-term investments in EXCESS of operating needs
        - net deferred income tax assets (a tax-timing asset, not operating capital)
        - operating lease right-of-use assets (per the brief)
        - non-interest-bearing operating liabilities (payables, accruals, DEFERRED
          REVENUE, income taxes payable, other liabilities), excluding lease liabilities
      Operating cash need assumed at 2% of revenue (assumption; Adobe is a
      subscription business collecting in advance, so true operating cash need is small).
"""))

OPERATING_CASH_PCT = 0.02


def invested_capital(total_assets, cash, sti, dta, rou, nibcl, rev, label):
    op_cash = OPERATING_CASH_PCT * rev
    excess_cash = cash + sti - op_cash
    ic = total_assets - excess_cash - dta - rou - nibcl
    print(f"\n{label}:")
    line("  total assets", total_assets)
    line("  - excess cash and short-term investments", -excess_cash)
    line("     (memo: operating cash retained @ 2% of revenue)", op_cash)
    line("  - net deferred income tax assets", -dta)
    line("  - operating lease right-of-use assets", -rou)
    line("  - non-interest-bearing operating liabilities", -nibcl)
    line("  = INVESTED CAPITAL", ic)
    return ic


# FY2024 balance sheet (Nov 29 2024)
nibcl_fy24 = 361 + 2_336 + (6_131 + 128) + (119 + 548) + 446
ic_fy24 = invested_capital(30_230, 7_613, 273, 1_657, 281, nibcl_fy24,
                           revenue["FY2024"], "FY2024 (Nov 29 2024 balance sheet)")

# FY2025 balance sheet (Nov 28 2025)
nibcl_fy25 = 417 + 2_648 + (6_905 + 125) + (153 + 469) + 508
ic_fy25 = invested_capital(29_496, 5_431, 1_164, 2_186, 312, nibcl_fy25,
                           revenue["FY2025"], "FY2025 (Nov 28 2025 balance sheet)")

# Q2 FY2026 balance sheet (May 29 2026)
nibcl_q226 = 499 + 2_455 + (7_152 + 98) + (38 + 536) + 572
ic_q226 = invested_capital(29_933, 4_919, 707, 1_998, 299, nibcl_q226,
                           ttm_revenue, "Q2 FY2026 (May 29 2026 balance sheet)")

print("\nComposition check — invested capital is essentially acquisition goodwill:")
line("  FY2025 goodwill + other intangibles, net", 12_857 + 495)
line("  FY2025 invested capital", ic_fy25)
line("  => invested capital EXCLUDING goodwill and intangibles", ic_fy25 - (12_857 + 495))
line("  Q2 FY2026 goodwill + other intangibles, net", 14_041 + 1_012)
line("  => Q2 FY2026 invested capital ex-goodwill/intangibles",
     ic_q226 - (14_041 + 1_012))

# Off-balance-sheet purchase obligations, PV'd
po = {2026: 2_083, 2027: 1_901, 2028: 1_623, 2029: 1_196, 2030: 12, 2031: 6}  # Note 16
DISC = 0.05
pv_po = sum(v / (1 + DISC) ** (i + 0.5) for i, v in enumerate(po.values()))
print()
line("FY2025 non-cancellable purchase obligations, undiscounted (Note 16)", sum(po.values()))
line(f"  present value @ {DISC:.0%}, mid-year convention", pv_po)

print()
print("=" * 84)
print("SECTION 6 — ROIC")
print("=" * 84)


def roic(oe, ic_open, ic_close, label):
    avg = (ic_open + ic_close) / 2
    r = oe / avg
    print(f"\n{label}:")
    line("  owners' earnings", oe)
    line("  average invested capital", avg)
    pct("  ROIC", 100 * r)
    return r


roic(oe_a["FY2025"], ic_fy24, ic_fy25, "FY2025 (Method A owners' earnings)")
roic(oe_a["TTM_Q2FY26"], ic_fy25, ic_q226, "TTM Q2 FY2026 (Method A owners' earnings)")

print("\nConservative variant — add the PV of off-balance-sheet hosting/data-centre")
print("commitments to invested capital WITHOUT adding the associated cost back to")
print("earnings. This double-counts and is therefore a FLOOR on ROIC, not an estimate:")
roic(oe_a["FY2025"], ic_fy24 + pv_po, ic_fy25 + pv_po,
     "FY2025 incl. PV of purchase obligations")
roic(oe_a["TTM_Q2FY26"], ic_fy25 + pv_po, ic_q226 + pv_po,
     "TTM Q2 FY2026 incl. PV of purchase obligations")

print("\nTax-rate sensitivity on TTM ROIC (average IC excluding purchase obligations):")
avg_ic_ttm = (ic_fy25 + ic_q226) / 2
for r in [TAX_LOW, TAX_BASE, TAX_HIGH]:
    pct(f"  ROIC @ {r:.0%} normalised tax", 100 * p_ttm * (1 - r) / avg_ic_ttm)

print("\nSensitivity to the operating-cash assumption (TTM, base tax):")
for opc in [0.00, 0.02, 0.05]:
    ic1 = 29_496 - (5_431 + 1_164 - opc * revenue["FY2025"]) - 2_186 - 312 - nibcl_fy25
    ic2 = 29_933 - (4_919 + 707 - opc * ttm_revenue) - 1_998 - 299 - nibcl_q226
    pct(f"  ROIC with operating cash @ {opc:.0%} of revenue",
        100 * oe_a["TTM_Q2FY26"] / ((ic1 + ic2) / 2))

print()
print("=" * 84)
print("SECTION 7 — PER-SHARE AND SANITY CHECKS")
print("=" * 84)

diluted_shares = {"FY2023": 459.1, "FY2024": 449.7, "FY2025": 427.0}
ttm_diluted = 427.0 - 433.2 + 406.6   # FY2025 - 1H FY2025 + 1H FY2026
for y in ["FY2023", "FY2024", "FY2025"]:
    print(f"  {y}: owners' earnings per diluted share = "
          f"${oe_a[y]/diluted_shares[y]:.2f}  (on {diluted_shares[y]:.1f}M shares)")
print(f"  TTM : owners' earnings per diluted share = "
      f"${oe_a['TTM_Q2FY26']/ttm_diluted:.2f}  (on {ttm_diluted:.1f}M shares)")

print("\nSBC sanity check — is GAAP SBC expense a fair proxy for the cost to owners?")
shares_issued_fy25 = 3.6 + 0.1 + 1.1   # RSUs + performance shares + ESPP, Note 12
avg_price_proxy = 400.0                # RSU weighted-average grant date FV FY2025 $407.67
line("  gross shares delivered under stock plans FY2025 (millions)", shares_issued_fy25, "M sh")
line(f"  x ~${avg_price_proxy:.0f}/share  = economic cost of dilution",
     shares_issued_fy25 * avg_price_proxy)
line("  GAAP SBC expense FY2025", sbc["FY2025"])

print("\nBuyback vs owners' earnings (the sustainability test):")
buybacks = {"FY2023": 4_400, "FY2024": 9_500, "FY2025": 11_281}
for y in ["FY2023", "FY2024", "FY2025"]:
    print(f"  {y}: repurchases ${buybacks[y]:,}M = {buybacks[y]/oe_a[y]:.2f}x owners' earnings")
h1_buyback = 4_589
print(f"  1H FY2026: repurchases ${h1_buyback:,}M = "
      f"{h1_buyback/(oe_a['TTM_Q2FY26']/2):.2f}x half of TTM owners' earnings")

print("\nAdvertising step-up sensitivity (NOT in base owners' earnings):")
ad_step = advertising["FY2025"] - advertising["FY2024"]
line("  FY2025 advertising expense (Note 1)", advertising["FY2025"])
line("  FY2024 advertising expense", advertising["FY2024"])
line("  year-on-year step-up", ad_step)
line(f"  if treated as growth investment, after-tax add-back @ {TAX_BASE:.0%}",
     ad_step * (1 - TAX_BASE))
pct("  as % of FY2025 owners' earnings", 100 * ad_step * (1 - TAX_BASE) / oe_a["FY2025"])

print("\nValuation cross-check (market data: Knowledge Store ID 7 / ID 8):")
for mcap, tag in [(108_700, "$108.7bn (stockanalysis, Aug 27 2026)"),
                  (112_130, "$112.1bn (tradingeconomics, Aug 2026)")]:
    net_debt = (6_150 + 494) - (4_919 + 707)   # Q2 FY2026 debt at par + CP, less cash + STI
    ev = mcap + net_debt
    print(f"  mkt cap {tag}: EV ${ev:,.0f}M -> EV / TTM owners' earnings = "
          f"{ev/oe_a['TTM_Q2FY26']:.1f}x  (unlevered yield {100*oe_a['TTM_Q2FY26']/ev:.1f}%)")

print()
print("=" * 84)
print("SECTION 8 — VERIFICATION OF FIGURES QUOTED IN THE WRITE-UP")
print("=" * 84)

gw_int = {"FY2024": 12_788 + 782, "FY2025": 12_857 + 495, "Q2FY26": 14_041 + 1_012}
for k, v in gw_int.items():
    line(f"  goodwill + other intangibles, net, {k}", v)
line("  FY2024 invested capital EXCLUDING goodwill/intangibles", ic_fy24 - gw_int["FY2024"])
line("  FY2025 invested capital EXCLUDING goodwill/intangibles", ic_fy25 - gw_int["FY2025"])
line("  Q2 FY2026 invested capital EXCLUDING goodwill/intangibles", ic_q226 - gw_int["Q2FY26"])

print("\n  Variant: net deferred tax assets INCLUDED in invested capital")
ic24_dta, ic25_dta, ic26_dta = ic_fy24 + 1_657, ic_fy25 + 2_186, ic_q226 + 1_998
line("    FY2025 invested capital incl. DTA", ic25_dta)
pct("    FY2025 ROIC incl. DTA", 100 * oe_a["FY2025"] / ((ic24_dta + ic25_dta) / 2))
pct("    TTM ROIC incl. DTA", 100 * oe_a["TTM_Q2FY26"] / ((ic25_dta + ic26_dta) / 2))

print("\n  Variant: deferred-revenue float COUNTED as owners' earnings")
float_ttm = ttm_delta_def_rev * (1 - TAX_BASE)
line("    after-tax float add-back (TTM)", float_ttm)
line("    owners' earnings including float", oe_a["TTM_Q2FY26"] + float_ttm)
pct("    TTM ROIC including float", 100 * (oe_a["TTM_Q2FY26"] + float_ttm) / avg_ic_ttm)

print("\n  Variant: purchased-intangible amortisation NOT added back")
line("    after-tax reduction (TTM)", ttm_intangible_amort * (1 - TAX_BASE))
pct("    as % of TTM owners' earnings",
    100 * ttm_intangible_amort * (1 - TAX_BASE) / oe_a["TTM_Q2FY26"])

print("\n  Variant: 'purchases of long-term investments, intangibles and other assets'")
print("           treated in full as capital spending (FY2025: $134M)")
line("    after-tax reduction", 134 * (1 - TAX_BASE))
pct("    as % of TTM owners' earnings", 100 * 134 * (1 - TAX_BASE) / oe_a["TTM_Q2FY26"])

print("\n  Causal-model reconciliation (work_products/causal_model.md Stage 4)")
line("    causal model 'SBC-adjusted owners' earnings', FY2025", 7_910)
line("    less increase in deferred revenue", -delta_deferred_rev["FY2025"])
line("    = comparable to this document's Method A", 7_910 - delta_deferred_rev["FY2025"])
line("    this document's Method A, FY2025", oe_a["FY2025"])
pct("    difference", 100 * ((7_910 - delta_deferred_rev["FY2025"]) / oe_a["FY2025"] - 1))

print("\n  Semrush capital deployed vs return (Q2 FY2026 10-Q Note 3)")
line("    goodwill recognised", 1_251)
line("    identifiable intangible assets", 582)
line("    = increase in invested capital", 1_251 + 582)
line("    memo: acquired ARR (Knowledge Store ID 4)", 480)
line("    memo: expected FY2026 revenue contribution (GUIDANCE)", 280)

print("\n  Net debt at Q2 FY2026")
line("    senior notes at par + commercial paper", 6_150 + 494)
line("    less cash and short-term investments", -(4_919 + 707))
line("    = net debt", (6_150 + 494) - (4_919 + 707))
