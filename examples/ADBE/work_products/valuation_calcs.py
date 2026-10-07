"""
Adobe Inc. (ADBE) - Valuation: PV of forecast owners' earnings + PV of terminal
value, plus standalone (non-operating) assets, less all debt-like items,
per current diluted share count.

Convention (per brief): the CURRENT fiscal year (FY2026, in progress as of the
2026-09-01 valuation date) is t=0 and is NOT discounted; FY2027 is t=1, ...,
FY2030 is t=4. The terminal value is realised at the end of FY2030, i.e. at
the same point in time as the FY2030 cash flow, so it is discounted at the
same t=4 factor.

Inputs are taken unchanged from:
  - work_products/forecast_earnings.md / forecast_earnings_calcs.py
    (owners' earnings by scenario, FY2026E-FY2030E; probability weights)
  - work_products/terminal_value.md / terminal_value_calcs.py
    (terminal multiples and terminal values by scenario, at FY2030 year-end)
  - work_products/owners_earnings_and_roic.md / owners_earnings_calcs.py
    (Q2 FY2026 excess cash and short-term investments = standalone assets)
  - primary_sources/2Q2026/financial_statements.md
    (Q2 FY2026 10-Q balance sheet: debt, operating lease liabilities, diluted
    share count)

Run: uv run python work_products/valuation_calcs.py

REVISED after r1 verifier review (pv/sotp/r1_review.md, response in
pv/sotp/r1_response.md): (1) the debt bridge now includes the PV of hosting
purchase obligations alongside operating lease liabilities, applying one rule
symmetrically instead of two conflicting ones; (2) the diluted share count
now uses the more current Q2 FY2026 spot count (399.0M actual shares
outstanding + 0.1M current dilutive effect) instead of the quarter's backward-
looking three-month weighted average (402.5M).
"""

DISCOUNT_RATE = 0.15  # variable, per brief - easy to change

YEARS = [2026, 2027, 2028, 2029, 2030]
T = {y: i for i, y in enumerate(YEARS)}  # FY2026 -> t=0, ..., FY2030 -> t=4

# ---------------------------------------------------------------------------
# 1. Owners' earnings paths, $M, by scenario (forecast_earnings_calcs.py
#    Section 9 printed output, reproduced exactly - see forecast_earnings.md §1)
# ---------------------------------------------------------------------------
OE = {
    "SEVERE": {2026: 6_886, 2027: 6_903, 2028: 6_639, 2029: 6_330, 2030: 6_022},
    "BEAR":   {2026: 7_426, 2027: 7_739, 2028: 7_941, 2029: 8_064, 2030: 8_105},
    "BASE":   {2026: 7_729, 2027: 8_475, 2028: 9_278, 2029: 10_055, 2030: 10_745},
    "BULL":   {2026: 7_891, 2027: 9_062, 2028: 10_394, 2029: 11_722, 2030: 13_035},
}
WEIGHT = {"SEVERE": 0.15, "BEAR": 0.25, "BASE": 0.40, "BULL": 0.20}

# Probability-weighted OE path (forecast_earnings_calcs.py Section 9 output,
# forecast_earnings.md does not print this path but the underlying calc does)
OE_WEIGHTED = {y: sum(WEIGHT[s] * OE[s][y] for s in OE) for y in YEARS}

# ---------------------------------------------------------------------------
# 2. Terminal value at FY2030 year-end, $M, by scenario (terminal_value.md §1,
#    terminal_value_calcs.py Section 4 printed output)
# ---------------------------------------------------------------------------
TERMINAL_MULTIPLE = {"SEVERE": 7, "BEAR": 11, "BASE": 15, "BULL": 22}
TV = {s: TERMINAL_MULTIPLE[s] * OE[s][2030] for s in OE}
TV_WEIGHTED = sum(WEIGHT[s] * TV[s] for s in OE)

# ---------------------------------------------------------------------------
# 3. Standalone (non-operating) assets and all debt-like items, both as of
#    the Q2 FY2026 10-Q (period ended May 29 2026) - the most current balance
#    sheet available (Q3 FY2026 reports Sept 10 2026, after this valuation).
# ---------------------------------------------------------------------------
# Standalone assets: excess cash and short-term investments not needed to
# operate the business (owners_earnings_and_roic.md §4; owners_earnings_calcs.py
# Section 5 "Q2 FY2026" block). Total cash+STI $5,626M less an assumed 2% of
# TTM revenue operating cash need ($504M) = $5,122M.
STANDALONE_ASSETS = 5_122

# All debt-like items, at carrying value, Q2 FY2026 10-Q balance sheet
# (primary_sources/2Q2026/financial_statements.md):
DEBT_CURRENT = 1_843      # commercial paper $494M carrying + current senior notes $1,349M carrying
DEBT_LONGTERM = 4_802     # long-term senior notes, carrying value
LEASE_CURRENT = 91        # operating lease liabilities, current
LEASE_LONGTERM = 329      # operating lease liabilities, long-term

# REVISED after r1 review (Objection 1, CONCEDED): the FY2025 10-K's $6,821M of
# off-balance-sheet hosting purchase obligations (PV $6,259M @ 5%,
# owners_earnings_and_roic.md §4.1) are now INCLUDED as debt-like, matching the
# treatment of operating lease liabilities below and the brief's explicit
# instruction to include "off-balance sheets commitments/obligations." The
# prior exclusion argued this double-counts opex already embedded in the OE
# forecast - true in principle, but that argument applies equally to lease
# payments (also fully embedded in EBIT, never excluded from OE the way debt
# interest is) and the document applied it to one item and not the other
# without reconciling why. Resolved here by applying ONE rule symmetrically:
# both are on the brief's explicit list and both are now included. See
# pv/sotp/r1_response.md Objection 1, and SECTION 5 below for the disclosed
# reverse sensitivity (excluding both, the alternative internally-consistent
# rule) so the reader can see both defensible answers.
PV_HOSTING = 6_259

# Legal contingencies (securities class action, derivative actions): Adobe
# states it is "unable to estimate a reasonably possible financial loss or
# range of financial loss, if any" (primary_sources/2Q2026/financial_statements.md,
# Note 13). Not quantifiable from any source, so NOT included as a debt-like
# deduction - flagged as an unquantified risk, not a modelled one.

TOTAL_DEBT_LIKE = DEBT_CURRENT + DEBT_LONGTERM + LEASE_CURRENT + LEASE_LONGTERM + PV_HOSTING

# REVISED after r1 review (Objection 2, CONCEDED): the prior figure (402.5M,
# the Q2 FY2026 three-month weighted-average diluted share count) was mislabeled
# as "the most current actual figure available" - it is not. The SAME 10-Q
# balance sheet reports 399.0M shares actually outstanding as of May 29 2026
# (a point-in-time spot count), which is lower and more current than a
# three-month backward-looking average taken while Adobe was continuously
# retiring shares (primary_sources/2Q2026/financial_statements.md, cover/
# balance sheet). To keep the "diluted" requirement in the brief while using
# the most current spot count, this adds the CURRENT dilutive effect from Note
# 12 (three months ended May 29 2026: diluted weighted-average 402.5M less
# basic weighted-average 402.4M = 0.1M of dilutive potential shares - small,
# because 12.1M of potential shares are currently anti-dilutive) to the 399.0M
# spot count: 399.0 + 0.1 = 399.1M.
DILUTED_SHARES = 399.1


def pv(cashflow_by_year, rate):
    return sum(cashflow_by_year[y] / (1 + rate) ** T[y] for y in YEARS)


def equity_bridge(pv_oe, pv_tv, label):
    ev = pv_oe + pv_tv
    equity = ev + STANDALONE_ASSETS - TOTAL_DEBT_LIKE
    per_share = equity / DILUTED_SHARES
    print(f"{label:<28} PV(OE) {pv_oe:>9,.0f}   PV(TV) {pv_tv:>9,.0f}   "
          f"EV {ev:>9,.0f}   Equity {equity:>9,.0f}   /share ${per_share:>7.2f}")
    return equity, per_share


print("=" * 100)
print("SECTION 1 - OWNERS' EARNINGS PATHS AND TERMINAL VALUES BY SCENARIO ($M)")
print("=" * 100)
for s in OE:
    print(f"{s:<8} weight {WEIGHT[s]:.0%}  OE: " +
          "  ".join(f"{OE[s][y]:>7,.0f}" for y in YEARS) +
          f"   TV(FY2030) {TV[s]:>9,.0f}  ({TERMINAL_MULTIPLE[s]}x)")
print(f"{'WEIGHTED':<8}        OE: " +
      "  ".join(f"{OE_WEIGHTED[y]:>7,.0f}" for y in YEARS) +
      f"   TV(FY2030) {TV_WEIGHTED:>9,.0f}")

print()
print("=" * 100)
print(f"SECTION 2 - DISCOUNTING at r = {DISCOUNT_RATE:.0%} "
      "(FY2026E = t=0, undiscounted; FY2030E TV discounted at t=4)")
print("=" * 100)
print("Discount factors:", {y: round(1 / (1 + DISCOUNT_RATE) ** T[y], 4) for y in YEARS})
print()

print("--- Scenario-by-scenario (own OE path, own terminal multiple) ---")
scenario_equity = {}
for s in OE:
    pv_oe_s = pv(OE[s], DISCOUNT_RATE)
    pv_tv_s = TV[s] / (1 + DISCOUNT_RATE) ** T[2030]
    eq, ps = equity_bridge(pv_oe_s, pv_tv_s, s)
    scenario_equity[s] = (eq, ps)

print()
print("--- Probability-weighted (weighted OE path + weighted TV, discounted once) ---")
pv_oe_w = pv(OE_WEIGHTED, DISCOUNT_RATE)
pv_tv_w = TV_WEIGHTED / (1 + DISCOUNT_RATE) ** T[2030]
eq_w, ps_w = equity_bridge(pv_oe_w, pv_tv_w, "WEIGHTED (direct)")

print()
print("--- Cross-check: probability-weighted average of the four scenario equity values ---")
eq_w_check = sum(WEIGHT[s] * scenario_equity[s][0] for s in OE)
ps_w_check = sum(WEIGHT[s] * scenario_equity[s][1] for s in OE)
print(f"weighted-avg of scenario equity values = {eq_w_check:>9,.0f}   "
      f"weighted-avg of scenario /share = ${ps_w_check:>7.2f}")
print(f"(should equal the direct weighted calc above, since discounting is linear: "
      f"{eq_w:,.0f} vs {eq_w_check:,.0f}, diff {abs(eq_w-eq_w_check):.1f}; "
      f"${ps_w:.2f} vs ${ps_w_check:.2f})")

print()
print("=" * 100)
print("SECTION 3 - THE EQUITY BRIDGE (Q2 FY2026 balance sheet, $M)")
print("=" * 100)
print(f"Standalone assets (excess cash + short-term investments)      {STANDALONE_ASSETS:>8,.0f}")
print(f"Total debt-like items:")
print(f"  Debt, current (incl. commercial paper), carrying value      {DEBT_CURRENT:>8,.0f}")
print(f"  Debt, long-term, carrying value                             {DEBT_LONGTERM:>8,.0f}")
print(f"  Operating lease liabilities, current                        {LEASE_CURRENT:>8,.0f}")
print(f"  Operating lease liabilities, long-term                      {LEASE_LONGTERM:>8,.0f}")
print(f"  Off-balance-sheet hosting purchase obligations, PV @ 5%     {PV_HOSTING:>8,.0f}")
print(f"  = Total debt-like items                                     {TOTAL_DEBT_LIKE:>8,.0f}")
print(f"Net standalone assets less debt                              "
      f"{STANDALONE_ASSETS - TOTAL_DEBT_LIKE:>8,.0f}")
print(f"Current diluted shares (399.0M spot outstanding + 0.1M current "
      f"dilutive effect)             {DILUTED_SHARES:>8,.1f}M")

print()
print("=" * 100)
print("SECTION 4 - SENSITIVITY TO DISCOUNT RATE (probability-weighted path)")
print("=" * 100)
for r in [0.10, 0.125, 0.15, 0.175, 0.20]:
    pv_oe_r = pv(OE_WEIGHTED, r)
    pv_tv_r = TV_WEIGHTED / (1 + r) ** T[2030]
    ev_r = pv_oe_r + pv_tv_r
    eq_r = ev_r + STANDALONE_ASSETS - TOTAL_DEBT_LIKE
    ps_r = eq_r / DILUTED_SHARES
    tv_share_of_ev = pv_tv_r / ev_r
    print(f"r = {r:>5.1%}   PV(OE) {pv_oe_r:>9,.0f}   PV(TV) {pv_tv_r:>9,.0f}   "
          f"EV {ev_r:>9,.0f}   /share ${ps_r:>7.2f}   TV share of EV {tv_share_of_ev:>5.0%}")

print()
print("=" * 100)
print("SECTION 5 - ALTERNATIVE, INTERNALLY-CONSISTENT TREATMENTS OF THE DEBT BRIDGE")
print("(disclosed per r1_response.md Objection 1 - the headline above applies ONE rule")
print(" symmetrically: both leases and hosting commitments are on the brief's explicit")
print(" list, so both are included. These are the other internally-consistent choices.)")
print("=" * 100)
LEASES = LEASE_CURRENT + LEASE_LONGTERM
FUNDED_DEBT = DEBT_CURRENT + DEBT_LONGTERM


def bridge_variant(label, debt_total):
    eq = eq_w + TOTAL_DEBT_LIKE - debt_total   # eq_w already nets TOTAL_DEBT_LIKE; back it out and swap in debt_total
    ps = eq / DILUTED_SHARES
    print(f"{label:<62} debt {debt_total:>7,.0f}   equity {eq:>9,.0f}   /share ${ps:>7.2f}")
    return ps


print(f"{'(headline) funded debt + leases + hosting, all included':<62} "
      f"debt {TOTAL_DEBT_LIKE:>7,.0f}   equity {eq_w:>9,.0f}   /share ${ps_w:>7.2f}")
bridge_variant("funded debt + leases only, hosting excluded (r0 draft's rule)",
               FUNDED_DEBT + LEASES)
ps_pure = bridge_variant(
    "funded debt only, leases AND hosting excluded (pure double-count-avoidance rule)",
    FUNDED_DEBT)
print(f"\nRange across defensible bridge conventions: "
      f"${min(ps_pure, ps_w):.2f} to ${max(ps_pure, ps_w):.2f} per share "
      f"(all else held at the probability-weighted DCF).")
