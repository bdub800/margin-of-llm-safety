"""
NamSys Inc. (TSXV: CTZ) -- Present-value equity valuation.

Method (per user brief): PV of five years of forecast owners' earnings (FY2026E-FY2030E),
plus PV of terminal value at end of FY2030E, plus standalone/excess assets, minus all debt-
like items, divided by current diluted shares outstanding. Discount rate is a variable, set
to 10%. Convention: the current fiscal year (FY2026, in progress as of the Sep 17, 2026
preparation date) is t=0 and is NOT discounted; FY2027E is t=1; ... FY2030E is t=4. The
terminal value is a value AS OF the end of FY2030E, i.e. the same time point as the FY2030E
cash flow, so it is discounted at the same t=4 factor.

This exercise is deliberately stock-price-blind: no NamSys quote, market capitalisation or
price-derived multiple is used anywhere.

CORRECTED per verifier round 1 (pv/sotp/r1_review.md, objection 1; see pv/sotp/r1_response.md
for the full back-and-forth). The standalone-assets balance MUST be the most recent ACTUAL
balance (April 30, 2026 -- the latest on file), not an earlier one: rolling it back to
October 31, 2025 would re-credit today's shareholder with the $4,027,790 special dividend
already paid out and pocketed by shareholders of record in March 2026, while still dividing
by TODAY's (post-buyback, smaller) share count -- a different and larger error than the one
being fixed. The correct fix instead nets the double-counted flow OUT of the t=0 term: the
April 30, 2026 balance already contains the $1,497,265 of operating cash NamSys generated in
H1 FY2026 (FSQ2 Statements of Cash Flows), so that amount is subtracted from each scenario's
undiscounted FY2026E owners' earnings at t=0 before it is added again as part of the flow.

Every input below carries a source tag:
  FC   = work_products/forecast_earnings.md       (owners' earnings by scenario, FY2026E-FY2030E)
  TV   = work_products/terminal_value.md           (terminal multiple and value at end of FY2030E)
  OE   = work_products/owners_earnings_and_roic.md (net cash / standalone assets; no debt)
  FSQ2 = primary_sources/2Q2026/FS_Q2_NamSys_Apr_30_26_FINAL.md   (diluted share count, cash flows)
  MDQ2 = primary_sources/2Q2026/MDA_Q2_NamSys_Apr_30_26_FINAL.md  (diluted share count)

Run: uv run python work_products/valuation_calcs.py
"""

# ----------------------------------------------------------------------------------
# 1. Inputs
# ----------------------------------------------------------------------------------

DISCOUNT_RATE = 0.10   # <-- variable, per brief. Change here to re-run at a different rate.

# Owners' earnings by scenario and forecast year, FC section 1 headline table (as reported).
OE_PATH_ASREPORTED = {
    "base": {
        2026: 2_375_755, 2027: 2_413_913, 2028: 2_548_061, 2029: 2_716_487, 2030: 2_859_320,
    },
    "bull": {
        2026: 2_497_370, 2027: 2_875_019, 2028: 3_456_739, 2029: 4_050_655, 2030: 4_649_840,
    },
    "bear_rightsized": {   # "management right-sizes" bear variant, FC s1 / s8
        2026: 2_186_559, 2027: 2_104_052, 2028: 1_804_902, 2029: 2_033_866, 2030: 2_094_988,
    },
    "bear_no_cost": {      # "no cost response" bear variant, FC s1 / s8
        2026: 2_186_559, 2027: 1_910_394, 2028: 1_467_614, 2029: 1_469_920, 2030: 1_505_664,
    },
}

# H1 FY2026 operating cash flow ALREADY generated and sitting inside the April 30, 2026
# standalone-assets balance (FSQ2 Statements of Cash Flows, six months ended Apr 30 2026,
# line 162: "CASH FLOWS FROM (USED IN) OPERATING ACTIVITIES" = 1,497,265). This is a single
# historical, already-realised dollar figure -- it does not vary by forecast scenario, since
# it already happened before any scenario branches. It is netted out of each scenario's t=0
# FY2026E flow once, so it is not counted a second time via the balance-sheet add-back.
H1_FY26_OPERATING_CASHFLOW_ALREADY_IN_BALANCE = 1_497_265   # FSQ2, six months ended Apr 30 2026

OE_PATH = {
    name: {yr: (val - H1_FY26_OPERATING_CASHFLOW_ALREADY_IN_BALANCE if yr == 2026 else val)
           for yr, val in path.items()}
    for name, path in OE_PATH_ASREPORTED.items()
}

# Terminal value at the end of FY2030E (TV s1), NOT yet discounted.
# Scenario-consistent diagonal (multiple co-moves with the scenario, TV s1):
TV_DIAGONAL = {
    "base": 34_311_840,             # 12x FY2030E base owners' earnings
    "bull": 69_747_600,             # 15x FY2030E bull owners' earnings
    "bear_rightsized": 16_759_904,  # 8x FY2030E bear (rightsized) owners' earnings
    "bear_no_cost": 12_045_312,     # 8x FY2030E bear (no cost response) owners' earnings
}

# Base-case terminal value across the full defensible multiple range (TV s1 / s5), for sensitivity.
TV_BASE_BY_MULTIPLE = {
    9:  25_733_880,
    12: 34_311_840,
    15: 42_889_800,
}

# Standalone assets: cash + short-term investments at the most recent actual balance sheet
# date, April 30, 2026 (OE s4 / s1: $940,082 cash + $6,425,965 short-term investments =
# $7,366,047). This must be the CURRENT actual balance, not an earlier one: rolling it back to
# October 31, 2025 ($10,175,672) would re-credit today's shareholder with the $4,027,790
# special dividend already paid to, and pocketed by, shareholders of record in March 2026
# (FSQ2 Note 6) -- that cash has left the company and is not available to a buyer of the stock
# today, even though today's (denominator) share count already reflects the buybacks funded
# from that same balance. See the OE_PATH construction above for how the resulting overlap
# with the undiscounted FY2026E flow is instead removed on the FLOW side. No debt of any kind
# ("no debt outstanding" -- OE s2, point 1, citing FY2025 MD&A). No pension plan, no disclosed
# off-balance-sheet debt-like commitments other than the contingent employee termination
# commitment discussed below (s3 of this script).
CASH_AND_STI_APR26 = 940_082 + 6_425_965    # = 7,366,047, OE s4 / s1
DEBT = 0                                    # OE s2: "no debt outstanding and incurred no interest expense"

# Current diluted shares outstanding: latest disclosed weighted-average diluted count,
# three months ended April 30, 2026 (the most recent single quarter on file; Q3 FY2026 had
# not yet been filed as of this document's date -- FC s2.5). MDQ2 line 114.
DILUTED_SHARES = 27_459_593

# ----------------------------------------------------------------------------------
# 2. Core PV function
# ----------------------------------------------------------------------------------

def pv_operating_business(oe_by_year, terminal_value, r):
    """PV at t=0 (start of FY2026E) of five years of owners' earnings plus terminal value.

    t=0: FY2026E (current year, not discounted)
    t=1: FY2027E
    t=2: FY2028E
    t=3: FY2029E
    t=4: FY2030E, and the terminal value is also discounted at t=4 (same time point).
    """
    years = [2026, 2027, 2028, 2029, 2030]
    pv_earnings = 0.0
    detail = []
    for t, yr in enumerate(years):
        cf = oe_by_year[yr]
        df = 1.0 / (1.0 + r) ** t
        pv = cf * df
        pv_earnings += pv
        detail.append((yr, t, cf, df, pv))
    pv_tv = terminal_value / (1.0 + r) ** 4   # same t=4 discount factor as FY2030E
    return pv_earnings, pv_tv, detail


def full_valuation(oe_by_year, terminal_value, r, cash=CASH_AND_STI_APR26, debt=DEBT,
                    shares=DILUTED_SHARES):
    pv_earnings, pv_tv, detail = pv_operating_business(oe_by_year, terminal_value, r)
    pv_operating = pv_earnings + pv_tv
    equity_value = pv_operating + cash - debt
    per_share = equity_value / shares
    return {
        "pv_earnings": pv_earnings,
        "pv_tv": pv_tv,
        "pv_operating": pv_operating,
        "cash": cash,
        "debt": debt,
        "equity_value": equity_value,
        "per_share": per_share,
        "detail": detail,
    }


# ----------------------------------------------------------------------------------
# 3. Base case, full detail, at the 10% discount rate
# ----------------------------------------------------------------------------------
print("=" * 88)
print("SECTION 1 -- BASE CASE, detailed PV build, r = 10%")
print("=" * 88)
print(f"FY2026E base owners' earnings, as reported (FC s1) : {OE_PATH_ASREPORTED['base'][2026]:>14,.0f}")
print(f"- H1 FY2026 operating cash flow already in balance : {H1_FY26_OPERATING_CASHFLOW_ALREADY_IN_BALANCE:>14,.0f}")
print(f"= FY2026E flow used at t=0 (this script)            : {OE_PATH['base'][2026]:>14,.0f}")
print()
base = full_valuation(OE_PATH["base"], TV_DIAGONAL["base"], DISCOUNT_RATE)
print(f"{'Year':<6}{'t':<4}{'Owners earnings':>18}{'Discount factor':>18}{'PV':>16}")
for yr, t, cf, df, pv in base["detail"]:
    print(f"{yr:<6}{t:<4}{cf:>18,.0f}{df:>18.4f}{pv:>16,.0f}")
print(f"\nSum PV of FY2026E-FY2030E owners' earnings : {base['pv_earnings']:>14,.0f}")
print(f"PV of terminal value (12x FY2030E OE, disc. at t=4): {base['pv_tv']:>14,.0f}")
print(f"= PV of operating business                  : {base['pv_operating']:>14,.0f}")
print(f"+ Standalone assets (cash + STI, Apr 30 2026): {base['cash']:>14,.0f}")
print(f"- Debt (none)                                : {base['debt']:>14,.0f}")
print(f"= Equity value                               : {base['equity_value']:>14,.0f}")
print(f"/ Diluted shares outstanding                  : {DILUTED_SHARES:>14,.0f}")
print(f"= Value per diluted share                     : {base['per_share']:>14,.2f}")

# ----------------------------------------------------------------------------------
# 4. Scenario table at r = 10%, each with its own scenario-consistent terminal multiple
# ----------------------------------------------------------------------------------
print()
print("=" * 88)
print("SECTION 2 -- Scenario table, r = 10%, scenario-consistent terminal multiple (TV s1 diagonal)")
print("=" * 88)
scenario_results = {}
for name in ["bull", "base", "bear_rightsized", "bear_no_cost"]:
    res = full_valuation(OE_PATH[name], TV_DIAGONAL[name], DISCOUNT_RATE)
    scenario_results[name] = res
    print(f"{name:<18} PV earnings {res['pv_earnings']:>12,.0f}  PV TV {res['pv_tv']:>12,.0f}  "
          f"Equity value {res['equity_value']:>13,.0f}  Per share {res['per_share']:>7.2f}")

# ----------------------------------------------------------------------------------
# 5. Base-case sensitivity: discount rate x terminal multiple
# ----------------------------------------------------------------------------------
print()
print("=" * 88)
print("SECTION 3 -- Base-case sensitivity: per-share value by discount rate and terminal multiple")
print("=" * 88)
rates = [0.08, 0.09, 0.10, 0.11, 0.12]
multiples = [9, 12, 15]
header = "r \\ multiple".ljust(14) + "".join(f"{m}x".rjust(10) for m in multiples)
print(header)
sensitivity_table = {}
for r in rates:
    row = []
    for m in multiples:
        res = full_valuation(OE_PATH["base"], TV_BASE_BY_MULTIPLE[m], r)
        row.append(res["per_share"])
    sensitivity_table[r] = row
    print(f"{r:<14.0%}" + "".join(f"{v:>10.2f}" for v in row))

# ----------------------------------------------------------------------------------
# 6. Decomposition of base-case per-share value: how much is the five explicit years,
#    how much is the terminal value, how much is standalone cash
# ----------------------------------------------------------------------------------
print()
print("=" * 88)
print("SECTION 4 -- Base case: composition of value per share, r = 10%")
print("=" * 88)
pv_earn_ps = base["pv_earnings"] / DILUTED_SHARES
pv_tv_ps = base["pv_tv"] / DILUTED_SHARES
cash_ps = base["cash"] / DILUTED_SHARES
total_ps = base["per_share"]
print(f"PV of FY2026E-FY2030E owners' earnings : {pv_earn_ps:>7.2f}  ({pv_earn_ps/total_ps:>5.1%} of total)")
print(f"PV of terminal value                    : {pv_tv_ps:>7.2f}  ({pv_tv_ps/total_ps:>5.1%} of total)")
print(f"Standalone cash + short-term investments: {cash_ps:>7.2f}  ({cash_ps/total_ps:>5.1%} of total)")
print(f"Total value per diluted share            : {total_ps:>7.2f}")

# ----------------------------------------------------------------------------------
# 7. Contingent item flagged but NOT deducted: the $1.1M employee termination commitment
#    (OE s3.1: "payable only on termination without cause", not capital deployed in the
#    business, and not a certain/contractual debt obligation). Shown here as a what-if.
# ----------------------------------------------------------------------------------
print()
print("=" * 88)
print("SECTION 5 -- What-if: employee termination commitment treated as debt-like (NOT base case)")
print("=" * 88)
TERMINATION_COMMITMENT = 1_100_000   # FS25 AFS Note 13; OE s3.1
what_if = full_valuation(OE_PATH["base"], TV_DIAGONAL["base"], DISCOUNT_RATE,
                          debt=TERMINATION_COMMITMENT)
print(f"Equity value if $1.1M commitment deducted as debt: {what_if['equity_value']:>14,.0f}")
print(f"Per-share value in that case                      : {what_if['per_share']:>14.2f}")
print(f"Base-case per-share value (commitment NOT deducted): {base['per_share']:>14.2f}")
print(f"Difference                                         : {what_if['per_share'] - base['per_share']:>14.2f}")

# ----------------------------------------------------------------------------------
# 8. Cross-check: share count sensitivity (six-month weighted average vs three-month)
# ----------------------------------------------------------------------------------
print()
print("=" * 88)
print("SECTION 6 -- Cross-check: diluted share count choice")
print("=" * 88)
SHARES_H1_FY26 = 27_498_422   # six months ended Apr 30 2026, FSQ2 line 85
res_h1 = full_valuation(OE_PATH["base"], TV_DIAGONAL["base"], DISCOUNT_RATE, shares=SHARES_H1_FY26)
print(f"Per-share value using Q2-only diluted count ({DILUTED_SHARES:,}): {base['per_share']:.2f}")
print(f"Per-share value using H1 diluted count       ({SHARES_H1_FY26:,}): {res_h1['per_share']:.2f}")
print(f"Difference is {(base['per_share']-res_h1['per_share'])/res_h1['per_share']:.2%} -- immaterial, "
      f"choice of share count does not move the conclusion.")
