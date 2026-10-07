"""
Adobe Inc. (ADBE) - Reported financials summary and current valuation.

All inputs traced to:
  - primary_sources/FY2025/financial_statements.md (FY2025 10-K: FY2023, FY2024, FY2025
    income statement, cash flow statement, balance sheet, segment note (Note 2))
  - primary_sources/2Q2026/financial_statements.md (Q2 FY2026 10-Q: six months ended
    May 29, 2026 and May 30, 2025 income statement, cash flow statement, balance sheet,
    debt note (Note 14), EPS note (Note 12), single-segment note (Note 15))
  - primary_sources/2Q2026/cover_page.md (shares outstanding as of June 11, 2026)
  - primary_sources/FY2025/cover_page.md (shares outstanding as of January 9, 2026)
  - work_products/owners_earnings_and_roic.md (Owners' Earnings and ROIC, already computed)

TTM (trailing twelve months) to Q2 FY2026 = FY2025 + 1H FY2026 - 1H FY2025.

Run: uv run python work_products/financials_summary_calcs.py
"""

# ---------------------------------------------------------------------------
# 1. Raw inputs (all in USD millions unless noted), from primary source statements
# ---------------------------------------------------------------------------

FY2023 = dict(
    revenue=19409, cogs=2354, gross_profit=17055,
    rd=3473, sm=5351, ga=1413, acq_term_fee=0, amort_intangibles_opex=168,
    total_opex=10405, operating_income=6650,
    interest_expense=-113, investment_gains=16, other_income=246, total_nonop=149,
    pretax_income=6799, tax=1371, net_income=5428,
    sbc=1718, da_cfo=872, cfo=7302, capex=360, other_investing_capex=53,
)

FY2024 = dict(
    revenue=21505, cogs=2358, gross_profit=19147,
    rd=3944, sm=5764, ga=1529, acq_term_fee=1000, amort_intangibles_opex=169,
    total_opex=12406, operating_income=6741,
    interest_expense=-169, investment_gains=48, other_income=311, total_nonop=190,
    pretax_income=6931, tax=1371, net_income=5560,
    sbc=1833, da_cfo=857, cfo=8056, capex=183, other_investing_capex=108,
)

FY2025 = dict(
    revenue=23769, cogs=2551, gross_profit=21218,
    rd=4294, sm=6488, ga=1573, acq_term_fee=0, amort_intangibles_opex=157,
    total_opex=12512, operating_income=8706,
    interest_expense=-263, investment_gains=43, other_income=248, total_nonop=28,
    pretax_income=8734, tax=1604, net_income=7130,
    sbc=1942, da_cfo=818, cfo=10031, capex=179, other_investing_capex=134,
)

H1_2025 = dict(
    revenue=11587, cogs=1260, gross_profit=10327,
    rd=2108, sm=3121, ga=744, amort_intangibles_opex=82,
    total_opex=6055, operating_income=4272,
    interest_expense=-130, investment_gains=8, other_income=133, total_nonop=11,
    pretax_income=4283, tax=781, net_income=3502,
    sbc=956, da_cfo=426, cfo=4673, capex=73, other_investing_capex=195,
)

H1_2026 = dict(
    revenue=13016, cogs=1379, gross_profit=11637,
    rd=2308, sm=3592, ga=1009, amort_intangibles_opex=72,
    total_opex=6981, operating_income=4656,
    interest_expense=-128, investment_gains=23, other_income=109, total_nonop=4,
    pretax_income=4660, tax=1059, net_income=3601,
    sbc=1043, da_cfo=367, cfo=5123, capex=95, other_investing_capex=62,
)

# Segment data (FY2023-FY2025 only; Adobe combined into one reportable segment
# from Q1 FY2026 -- primary_sources/2Q2026/financial_statements.md Note 15)
SEGMENTS = {
    "FY2025": {
        "Digital Media": dict(revenue=17649, cogs=841, gross_profit=16808, gm_pct=95),
        "Digital Experience": dict(revenue=5864, cogs=1625, gross_profit=4239, gm_pct=72),
        "Publishing and Advertising": dict(revenue=256, cogs=85, gross_profit=171, gm_pct=67),
    },
    "FY2024": {
        "Digital Media": dict(revenue=15864, cogs=680, gross_profit=15184, gm_pct=96),
        "Digital Experience": dict(revenue=5366, cogs=1589, gross_profit=3777, gm_pct=70),
        "Publishing and Advertising": dict(revenue=275, cogs=89, gross_profit=186, gm_pct=68),
    },
    "FY2023": {
        "Digital Media": dict(revenue=14216, cogs=665, gross_profit=13551, gm_pct=95),
        "Digital Experience": dict(revenue=4893, cogs=1603, gross_profit=3290, gm_pct=67),
        "Publishing and Advertising": dict(revenue=300, cogs=86, gross_profit=214, gm_pct=71),
    },
}

# ---------------------------------------------------------------------------
# 2. TTM to Q2 FY2026 = FY2025 + H1 2026 - H1 2025
# ---------------------------------------------------------------------------

def ttm(fy, h1_new, h1_old):
    return {k: fy[k] + h1_new[k] - h1_old[k] for k in fy if k in h1_new and k in h1_old}

TTM = ttm(FY2025, H1_2026, H1_2025)

# ---------------------------------------------------------------------------
# 3. Derived metrics: margins, EBITDA, FCF, unlevered FCF
# ---------------------------------------------------------------------------

def derive(d, label):
    out = dict(d)
    out["gross_margin_pct"] = 100 * d["gross_profit"] / d["revenue"]
    out["operating_margin_pct"] = 100 * d["operating_income"] / d["revenue"]
    out["ebitda"] = d["operating_income"] + d["da_cfo"]
    out["ebitda_margin_pct"] = 100 * out["ebitda"] / d["revenue"]
    out["fcf"] = d["cfo"] - d["capex"]
    out["unlevered_fcf"] = out["fcf"] + (-d["interest_expense"])
    out["net_margin_pct"] = 100 * d["net_income"] / d["revenue"]
    out["label"] = label
    return out

periods = {
    "FY2023": derive(FY2023, "FY2023"),
    "FY2024": derive(FY2024, "FY2024"),
    "FY2025": derive(FY2025, "FY2025"),
    "H1 2025": derive(H1_2025, "H1 2025"),
    "H1 2026": derive(H1_2026, "H1 2026"),
    "TTM Q2FY26": derive(TTM, "TTM Q2FY26"),
}

print("=" * 100)
print("SECTION 1: Financial and operating metrics")
print("=" * 100)
for name, p in periods.items():
    print(f"\n--- {name} ---")
    for k in ["revenue", "gross_profit", "gross_margin_pct", "operating_income",
              "operating_margin_pct", "ebitda", "ebitda_margin_pct", "interest_expense",
              "net_income", "net_margin_pct", "sbc", "cfo", "capex", "fcf", "unlevered_fcf"]:
        v = p[k]
        if "pct" in k:
            print(f"  {k:28s} {v:8.1f}%")
        else:
            print(f"  {k:28s} {v:8,.0f}")

# YoY growth checks
print("\n--- YoY revenue growth ---")
print(f"  FY2024 vs FY2023: {100*(FY2024['revenue']/FY2023['revenue']-1):.1f}%")
print(f"  FY2025 vs FY2024: {100*(FY2025['revenue']/FY2024['revenue']-1):.1f}%")
print(f"  H1 2026 vs H1 2025: {100*(H1_2026['revenue']/H1_2025['revenue']-1):.1f}%")
print(f"  TTM vs FY2025: {100*(TTM['revenue']/FY2025['revenue']-1):.1f}%")

# ---------------------------------------------------------------------------
# 4. Capitalization, cash, debt, and Enterprise Value
# ---------------------------------------------------------------------------
print("\n" + "=" * 100)
print("SECTION 2: Capitalization, Cash, Debt, and Enterprise Value")
print("=" * 100)

STOCK_PRICE = 284.88  # USD, per user prompt, 2026-09-03

# Shares outstanding: most recent primary-source cover page count.
# 2Q FY2026 10-Q cover page: 397.5 million shares as of June 11, 2026
# (primary_sources/2Q2026/cover_page.md, line 63) -- more recent than the
# FY2025 10-K cover page's 410.5 million as of January 9, 2026.
BASIC_SHARES = 397.5

# Dilutive shares: 10-Q Note 12 (EPS reconciliation) discloses "dilutive
# potential common shares from stock plans and programs" of 0.3 million for
# the six months ended May 29, 2026 (weighted-average basis; the closest
# disclosed figure to a point-in-time dilutive add-on).
DILUTIVE_SHARES = 0.3
DILUTED_SHARES = BASIC_SHARES + DILUTIVE_SHARES

MARKET_CAP_BASIC = STOCK_PRICE * BASIC_SHARES
MARKET_CAP_DILUTED = STOCK_PRICE * DILUTED_SHARES

# Cash & liquid investments at Q2 FY2026 (primary_sources/2Q2026/financial_statements.md)
CASH = 4919
ST_INVESTMENTS = 707
CASH_AND_INVESTMENTS = CASH + ST_INVESTMENTS

# Debt at Q2 FY2026 (10-Q Note 14): current debt on balance sheet $1,843M =
# current portion of senior notes (carrying value $1,349M) + commercial paper
# (carrying value $494M); long-term debt (senior notes) $4,802M.
CURRENT_DEBT = 1843
LONGTERM_DEBT = 4802
TOTAL_DEBT = CURRENT_DEBT + LONGTERM_DEBT

# Operating lease liabilities at Q2 FY2026 (balance sheet): current $91M +
# long-term $329M. Included in EV per brief instruction to treat leases as debt.
LEASE_LIAB_CURRENT = 91
LEASE_LIAB_LT = 329
TOTAL_LEASE_LIAB = LEASE_LIAB_CURRENT + LEASE_LIAB_LT

# No defined-benefit pension plan disclosed in Adobe's filings (not found in
# primary_sources) -- no pension shortfall adjustment made.

NET_DEBT = TOTAL_DEBT + TOTAL_LEASE_LIAB - CASH_AND_INVESTMENTS

EV_BASIC = MARKET_CAP_BASIC + NET_DEBT
EV_DILUTED = MARKET_CAP_DILUTED + NET_DEBT

print(f"Stock price: ${STOCK_PRICE}")
print(f"Basic shares: {BASIC_SHARES:.1f}M | Diluted shares: {DILUTED_SHARES:.1f}M")
print(f"Market cap (basic): ${MARKET_CAP_BASIC:,.0f}M | (diluted): ${MARKET_CAP_DILUTED:,.0f}M")
print(f"Cash + ST investments: ${CASH_AND_INVESTMENTS:,.0f}M")
print(f"Total debt (senior notes + CP): ${TOTAL_DEBT:,.0f}M")
print(f"Total operating lease liabilities: ${TOTAL_LEASE_LIAB:,.0f}M")
print(f"Net debt (incl. leases, less cash & ST investments): ${NET_DEBT:,.0f}M")
print(f"EV (basic): ${EV_BASIC:,.0f}M | EV (diluted): ${EV_DILUTED:,.0f}M")

# ---------------------------------------------------------------------------
# 5. Valuation multiples on TTM metrics
# ---------------------------------------------------------------------------
print("\n" + "=" * 100)
print("SECTION 3: Valuation (LTM to Q2 FY2026)")
print("=" * 100)

TTM_D = periods["TTM Q2FY26"]
ltm_ebit = TTM_D["operating_income"]
ltm_ebitda = TTM_D["ebitda"]
ltm_ufcf = TTM_D["unlevered_fcf"]

# Owners' earnings, TTM Method A, from work_products/owners_earnings_and_roic.md Section 1
OWNERS_EARNINGS_TTM = 7490

print(f"LTM EBIT: ${ltm_ebit:,.0f}M")
print(f"LTM EBITDA: ${ltm_ebitda:,.0f}M")
print(f"LTM unlevered FCF: ${ltm_ufcf:,.0f}M")
print(f"LTM Owners' earnings (Method A, from owners_earnings_and_roic.md): ${OWNERS_EARNINGS_TTM:,.0f}M")

for label, ev in [("Basic", EV_BASIC), ("Diluted", EV_DILUTED)]:
    print(f"\n--- EV ({label}) = ${ev:,.0f}M ---")
    print(f"  EV/EBIT              = {ev/ltm_ebit:.1f}x")
    print(f"  EV/EBITDA            = {ev/ltm_ebitda:.1f}x")
    print(f"  EV/unlevered FCF     = {ev/ltm_ufcf:.1f}x")
    print(f"  EV/Owners' Earnings  = {ev/OWNERS_EARNINGS_TTM:.1f}x")

# P/E for reference
ltm_net_income = TTM_D["net_income"]
print(f"\nLTM net income: ${ltm_net_income:,.0f}M")
print(f"P/E (basic, on LTM net income): {MARKET_CAP_BASIC/ltm_net_income:.1f}x")
print(f"P/E (diluted, on LTM net income): {MARKET_CAP_DILUTED/ltm_net_income:.1f}x")

# ---------------------------------------------------------------------------
# 6. Sensitivity: EV including PV of off-balance-sheet hosting commitments
# ---------------------------------------------------------------------------
print("\n" + "=" * 100)
print("SECTION 4: Sensitivity -- EV including hosting-commitment PV (not base case)")
print("=" * 100)
# PV of $6,821M undiscounted hosting/data-center purchase obligations (FY2025
# 10-K Note 16), discounted at 5% -- taken unchanged from
# work_products/owners_earnings_and_roic.md Section 4.1.
HOSTING_PV = 6259
ev_basic_incl_hosting = EV_BASIC + HOSTING_PV
ev_diluted_incl_hosting = EV_DILUTED + HOSTING_PV
print(f"EV (basic) incl. hosting PV: ${ev_basic_incl_hosting:,.0f}M ({100*(ev_basic_incl_hosting/EV_BASIC-1):.1f}% higher)")
print(f"EV (diluted) incl. hosting PV: ${ev_diluted_incl_hosting:,.0f}M ({100*(ev_diluted_incl_hosting/EV_DILUTED-1):.1f}% higher)")
