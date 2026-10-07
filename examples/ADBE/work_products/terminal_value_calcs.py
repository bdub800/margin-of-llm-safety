"""
Adobe Inc. (ADBE) -- Terminal value at end of FY2030 (the last projected year).

Terminal value = terminal multiple x FY2030E owners' earnings.
NO discounting to present value (out of scope for this step).
NO per-share terminal values (explicitly out of scope).

Run:  uv run python work_products/terminal_value_calcs.py

INPUTS AND THEIR SOURCES
------------------------
FY2030E owners' earnings by scenario   work_products/forecast_earnings.md sec.1 (scenario table)
FY2030E revenue / EBITA (base)         work_products/forecast_earnings.md sec.1
FY2025A / TTM owners' earnings, ROIC   work_products/owners_earnings_and_roic.md sec.1
ADBE market cap, EV, trading ratios    fetched_docs/adbe_statistics_aug2026.md (stockanalysis.com,
                                       Aug 31 2026), fetched_docs/adbe_ratio_history_aug2026.md
Peer trading multiples                 fetched_docs/peer_multiples_compare_2026.md and
                                       fetched_docs/peer_multiples_disruption_set_2026.md
                                       (stockanalysis.com, Aug 31 2026)
Scenario probabilities                 work_products/forecast_earnings.md sec.1 -- ANALYST JUDGMENT
Scenario terminal multiples            ANALYST JUDGMENT, justified in terminal_value.md sec.4
"""

from statistics import median

L = print


def rule(t):
    L("\n" + "=" * 78)
    L(t)
    L("=" * 78)


# =====================================================================
# 0. INPUTS
# =====================================================================

# --- Forecast output: FY2030E owners' earnings ($M) by scenario -------
# work_products/forecast_earnings.md sec.1 "The four scenarios"
SCEN = {
    #  name        FY2030E OE ($M)   prob (judgment)   5yr OE CAGR
    "SEVERE": {"oe": 6_022, "p": 0.15, "cagr": -0.033},
    "BEAR":   {"oe": 8_105, "p": 0.25, "cagr": 0.026},
    "BASE":   {"oe": 10_745, "p": 0.40, "cagr": 0.086},
    "BULL":   {"oe": 13_035, "p": 0.20, "cagr": 0.129},
}

FY2030E_REVENUE_BASE = 35_267.0     # $M, forecast_earnings.md sec.1
FY2030E_EBITA_BASE = 13_607.0       # $M, forecast_earnings.md sec.1
FY2030E_SBC_BASE = 2_892.0          # $M, forecast_earnings.md sec.8
FY2026E_OE = 7_729.0                # $M, forecast_earnings.md sec.1
FY2025A_OE = 7_119.0                # $M, owners_earnings_and_roic.md sec.1
TTM_OE_Q2FY26 = 7_490.0             # $M, owners_earnings_and_roic.md sec.1

# --- Adobe market data, Aug 31 2026 (fetched_docs/adbe_statistics_aug2026.md) ---
ADBE_MKT_CAP = 116_280.0            # $M
ADBE_EV = 117_740.0                 # $M
ADBE_NET_DEBT = 1_450.0             # $M (net cash -1.45bn)
ADBE_TTM_NET_INCOME = 7_230.0       # $M
ADBE_TTM_REVENUE = 25_200.0         # $M
ADBE_TTM_FCF = 10_280.0             # $M
ADBE_PE_TTM = 16.67
ADBE_FWD_PE = 11.24
ADBE_EV_EBITDA = 12.03
ADBE_EV_EBIT = 12.65
ADBE_EV_SALES = 4.64

# --- ADBE own P/E history (fetched_docs/adbe_ratio_history_aug2026.md) ---
ADBE_PE_HIST = {"FY2021": 60.84, "FY2022": 33.39, "FY2023": 51.37,
                "FY2024": 40.85, "FY2025": 18.80, "Aug-2026": 16.67}
ADBE_EV_EBIT_HIST = {"FY2021": 50.30, "FY2022": 25.85, "FY2023": 41.42,
                     "FY2024": 28.86, "FY2025": 15.47, "Aug-2026": 12.65}

# --- Peer trailing P/E, Aug 31 2026 -----------------------------------
# fetched_docs/peer_multiples_compare_2026.md
MATURE_SW_PE = {"MSFT": 28.61, "CRM": 23.72, "INTU": 21.75,
                "ADSK": 33.78, "ORCL": 25.87, "SAP": 28.77}
# fetched_docs/peer_multiples_disruption_set_2026.md
DISRUPTED_SW_PE = {"DBX": 19.65, "ZM": 9.01, "DOCU": 41.56, "GEN": 18.03}
# Shutterstock: no meaningful P/E (loss-making); priced on sales
SSTK_MKT_CAP = 210.23   # $M
SSTK_REVENUE = 901.29   # $M

# --- Scenario terminal multiples: ANALYST JUDGMENT --------------------
# Applied to FY2030E owners' earnings, which are UNLEVERED (pre-interest),
# so the product is an ENTERPRISE value.
MULT = {"SEVERE": 7.0, "BEAR": 11.0, "BASE": 15.0, "BULL": 22.0}

# =====================================================================
# 1. What does Adobe trade at TODAY on an owners'-earnings basis?
# =====================================================================
rule("1. ADBE's own trading multiple on owners' earnings, Aug 31 2026")

for label, oe in [("FY2025A OE", FY2025A_OE), ("TTM-to-Q2FY26 OE", TTM_OE_Q2FY26),
                  ("FY2026E OE", FY2026E_OE)]:
    L(f"  Mkt cap / {label:<18} = {ADBE_MKT_CAP/oe:6.2f}x   "
      f"EV / {label:<18} = {ADBE_EV/oe:6.2f}x")

# Basis reconciliation: is an OE multiple comparable to a peer P/E?
L(f"\n  Basis check -- ADBE TTM owners' earnings ${TTM_OE_Q2FY26:,.0f}M vs "
  f"TTM GAAP net income ${ADBE_TTM_NET_INCOME:,.0f}M")
L(f"  Difference: {(TTM_OE_Q2FY26/ADBE_TTM_NET_INCOME - 1)*100:+.1f}%  "
  "-> for ADBE an OE multiple and a P/E are near-interchangeable in level.")
L(f"  (Sanity: implied P/E on TTM net income = {ADBE_MKT_CAP/ADBE_TTM_NET_INCOME:.2f}x "
  f"vs stockanalysis.com reported {ADBE_PE_TTM:.2f}x)")

# =====================================================================
# 2. Peer multiple anchors
# =====================================================================
rule("2. Peer trading multiples (trailing P/E), Aug 31 2026")

mat = sorted(MATURE_SW_PE.values())
L(f"  Mature large-cap software {list(MATURE_SW_PE)}")
L(f"    median {median(mat):.1f}x   range {mat[0]:.1f}x - {mat[-1]:.1f}x")
dis = sorted(DISRUPTED_SW_PE.values())
L(f"  Ex-growth / disruption-discounted software {list(DISRUPTED_SW_PE)}")
L(f"    median {median(dis):.1f}x   range {dis[0]:.1f}x - {dis[-1]:.1f}x")
L(f"  Shutterstock (AI-substituted content franchise): no P/E; "
  f"mkt cap/revenue = {SSTK_MKT_CAP/SSTK_REVENUE:.2f}x")
L(f"  ADBE today: {ADBE_PE_TTM:.2f}x -- a "
  f"{(1 - ADBE_PE_TTM/median(mat))*100:.0f}% discount to the mature-software median.")

L("\n  ADBE's own P/E history: " +
  "  ".join(f"{k} {v:.1f}x" for k, v in ADBE_PE_HIST.items()))
hist5 = [v for k, v in ADBE_PE_HIST.items() if k.startswith("FY")]
L(f"  FY2021-FY2025 median {median(hist5):.1f}x -> today {ADBE_PE_TTM:.1f}x "
  f"({(ADBE_PE_TTM/median(hist5) - 1)*100:.0f}% de-rating).")

# =====================================================================
# 3. Gordon-growth cross-check on the multiple
# =====================================================================
rule("3. Cross-check: what multiple does a simple perpetuity imply?")
# Value = OE x (1 - g/ROIC) / (r - g).  Reinvestment drag is tiny because
# ROIC is ~70% (owners_earnings_and_roic.md sec.1).
ROIC = 0.70
L(f"  Using Value/OE = (1 - g/ROIC)/(r - g), ROIC = {ROIC:.0%}\n")
L("      g \\ r      8.0%    9.0%   10.0%   11.0%")
for g in [-0.03, 0.00, 0.01, 0.02, 0.03, 0.04]:
    row = f"    {g:+.0%}   "
    for r in [0.08, 0.09, 0.10, 0.11]:
        row += f"  {(1 - g/ROIC)/(r - g):6.1f}x"
    L(row)
L("\n  Reinvestment drag at g=3%: 1 - 0.03/0.70 = "
  f"{1 - 0.03/ROIC:.3f} -- i.e. ~96% of owners' earnings are distributable.")
L("  ROIC (~70%) is nowhere near binding on growth; it is a quality signal,")
L("  not a constraint. (owners_earnings_and_roic.md sec.1)")

# =====================================================================
# 4. Terminal value by scenario
# =====================================================================
rule("4. TERMINAL VALUE AT FY2030 (enterprise basis, undiscounted)")

L(f"  {'Scenario':<10}{'Prob':>7}{'FY30E OE $M':>14}{'Mult':>8}{'TV $M':>14}{'Wtd TV $M':>13}")
tv_w = 0.0
oe_w = 0.0
for k, d in SCEN.items():
    tv = d["oe"] * MULT[k]
    tv_w += d["p"] * tv
    oe_w += d["p"] * d["oe"]
    L(f"  {k:<10}{d['p']:>7.0%}{d['oe']:>14,.0f}{MULT[k]:>7.1f}x{tv:>14,.0f}{d['p']*tv:>13,.0f}")
L("  " + "-" * 66)
L(f"  {'WEIGHTED':<10}{'':>7}{oe_w:>14,.0f}{tv_w/oe_w:>7.1f}x{tv_w:>14,.0f}")

L(f"\n  Base-case terminal value      = ${SCEN['BASE']['oe']*MULT['BASE']/1000:,.1f}bn "
  f"({MULT['BASE']:.0f}x ${SCEN['BASE']['oe']/1000:,.2f}bn)")
L(f"  Probability-weighted TV       = ${tv_w/1000:,.1f}bn")
L(f"  Implied blended multiple on the probability-weighted OE of "
  f"${oe_w/1000:,.2f}bn = {tv_w/oe_w:.1f}x")

# Where does the weighted value come from?
L("\n  Contribution to probability-weighted TV:")
for k, d in SCEN.items():
    L(f"    {k:<8}{d['p']*d['oe']*MULT[k]/tv_w:>7.0%}")
L("  NOTE the right-tail dependence: the 20%-probability BULL case supplies")
L(f"  {SCEN['BULL']['p']*SCEN['BULL']['oe']*MULT['BULL']/tv_w:.0%} of the weighted terminal value.")

# The error avoided: blended-OE x blended-multiple would NOT equal this
naive = oe_w * MULT["BASE"]
L(f"\n  Contrast -- the common error of applying ONE multiple to blended earnings:")
L(f"    {MULT['BASE']:.0f}x x ${oe_w:,.0f}M = ${naive/1000:,.1f}bn "
  f"({(naive/tv_w - 1)*100:+.1f}% vs the correctly weighted ${tv_w/1000:,.1f}bn)")

# =====================================================================
# 5. Cross-checks on the base-case terminal value
# =====================================================================
rule("5. Cross-checks on the BASE-case terminal value")
tv_base = SCEN["BASE"]["oe"] * MULT["BASE"]
L(f"  Base TV ${tv_base:,.0f}M implies, on FY2030E base-case financials:")
L(f"    EV / revenue  = {tv_base/FY2030E_REVENUE_BASE:5.2f}x   "
  f"(ADBE today {ADBE_EV_SALES:.2f}x)")
L(f"    EV / EBITA    = {tv_base/FY2030E_EBITA_BASE:5.2f}x   "
  f"(ADBE today EV/EBIT {ADBE_EV_EBIT:.2f}x, EV/EBITDA {ADBE_EV_EBITDA:.2f}x)")
L(f"    Owners' earnings yield = {1/MULT['BASE']:.1%}   "
  f"(ADBE today earnings yield 6.26%, FCF yield 8.90%)")
L("  All three land within a few percent of where ADBE trades TODAY.")
L("  => The base terminal multiple is equivalent to assuming Adobe in FY2030")
L("     is valued on the SAME terms as the market applies in Aug 2026.")

L(f"\n  SBC check: FY2030E SBC ${FY2030E_SBC_BASE:,.0f}M is already expensed inside")
L(f"  owners' earnings ({FY2030E_SBC_BASE/SCEN['BASE']['oe']:.0%} of base-case OE). "
  "No add-back, no double-count.")

# =====================================================================
# 6. Sensitivity
# =====================================================================
rule("6. Sensitivity of the weighted terminal value")

L("  (a) Base multiple varied, others held:")
for m in [12, 13, 14, 15, 16, 17, 18]:
    mm = dict(MULT); mm["BASE"] = m
    t = sum(d["p"] * d["oe"] * mm[k] for k, d in SCEN.items())
    L(f"      BASE {m:>2}x -> weighted TV ${t/1000:6.1f}bn  ({(t/tv_w-1)*100:+5.1f}%)")

L("\n  (b) Bull multiple varied (tests the right-tail dependence):")
for m in [16, 18, 20, 22, 25, 27]:
    mm = dict(MULT); mm["BULL"] = m
    t = sum(d["p"] * d["oe"] * mm[k] for k, d in SCEN.items())
    L(f"      BULL {m:>2}x -> weighted TV ${t/1000:6.1f}bn  ({(t/tv_w-1)*100:+5.1f}%)")

L("\n  (c) All multiples scaled together:")
for s in [0.8, 0.9, 1.0, 1.1, 1.2]:
    t = sum(d["p"] * d["oe"] * MULT[k] * s for k, d in SCEN.items())
    L(f"      x{s:.1f} -> weighted TV ${t/1000:6.1f}bn")

L("\n  (d) Probabilities: shift 10pp from BASE to SEVERE (pessimist's weights):")
alt = {"SEVERE": 0.25, "BEAR": 0.25, "BASE": 0.30, "BULL": 0.20}
t = sum(alt[k] * d["oe"] * MULT[k] for k, d in SCEN.items())
L(f"      weighted TV ${t/1000:.1f}bn  ({(t/tv_w-1)*100:+.1f}%)")
L("      shift 10pp from SEVERE+BEAR to BULL (optimist's weights):")
alt2 = {"SEVERE": 0.10, "BEAR": 0.20, "BASE": 0.40, "BULL": 0.30}
t2 = sum(alt2[k] * d["oe"] * MULT[k] for k, d in SCEN.items())
L(f"      weighted TV ${t2/1000:.1f}bn  ({(t2/tv_w-1)*100:+.1f}%)")

# =====================================================================
# 7. Equity bridge flag (NOT resolved here -- for the valuation step)
# =====================================================================
rule("7. Flag for the next step: this TV is an ENTERPRISE value")
cum_oe = 7_729 + 8_475 + 9_278 + 10_055 + 10_745          # forecast sec.1
cum_bb = 8_500 + 7_628 + 8_350 + 9_049 + 9_670            # forecast sec.8
L(f"  Owners' earnings are unlevered (pre-interest), so multiple x OE = ENTERPRISE value.")
L(f"  Net debt today = ${ADBE_NET_DEBT:,.0f}M (fetched_docs/adbe_statistics_aug2026.md).")
L(f"  Cumulative FY2026E-FY2030E owners' earnings = ${cum_oe:,.0f}M")
L(f"  Cumulative FY2026E-FY2030E buyback spend    = ${cum_bb:,.0f}M "
  f"({cum_bb/cum_oe:.0%} of OE)")
L("  => The forecast's buyback plan is roughly self-funded out of owners'")
L("     earnings, so FY2030 net debt should be of a similar order to today's")
L("     ~$1.5bn -- immaterial (~1%) against a ~$150bn enterprise value.")
L("     APPROXIMATE: ignores cash interest and cash-vs-normalised tax timing.")
