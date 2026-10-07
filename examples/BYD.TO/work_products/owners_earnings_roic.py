"""
Boyd Group Services Inc. (BYD.TO / BGSI) - Owners' Earnings and ROIC.

All figures in THOUSANDS of U.S. dollars (Boyd reports in USD), unless noted.

SOURCES (all in primary_sources/):
  FY2023/Boyd_AFS.md        - FY2023 & FY2022 statements of earnings, cash flows, financial position
  FY2023/Boyd_MDA.md        - FY2023 & FY2022 Adjusted EBITDA reconciliation (line 282)
  FY2024/Boyd_AFS.md        - FY2024 & FY2023 statements
  FY2024/Boyd_MDA.md        - FY2024 Adjusted EBITDA (line 198)
  FY2025/BoydGroup_AFS.md   - FY2025 & FY2024 statements + notes 5-32
  FY2025/BoydGroup_MDA.md   - FY2025 Adjusted EBITDA (line 209), capex guidance (line 526)
  Q2FY26/BoydGroup_Q2.md    - Q2/H1 2026 interim statements + notes
  Q2FY26/BoydGroup_MDA.md   - H1 2026 Adjusted EBITDA (line 141), quarterly table (line 350)

Run:  uv run python work_products/owners_earnings_roic.py
"""

from textwrap import indent

TH = 1000.0  # thousands -> millions divisor


# ---------------------------------------------------------------------------
# 1. INPUTS - reported figures, each traceable to a filing line
# ---------------------------------------------------------------------------

PERIODS = ["FY2023", "FY2024", "FY2025", "TTM Jun-2026"]

# Sales. FY23/FY22: FY2023 AFS statement of earnings. FY24/FY25: FY2025 AFS.
# TTM = FY2025 3,142,794 - H1'25 1,558,730 + H1'26 2,010,328 (Q2FY26 statements of earnings)
sales = {
    "FY2023": 2_945_988,
    "FY2024": 3_070_342,
    "FY2025": 3_142_794,
    "TTM Jun-2026": 3_142_794 - 1_558_730 + 2_010_328,
}

# Adjusted EBITDA as reported by the company (EBITDA excl. fair value adjustments and
# acquisition & transformational cost initiatives).
# FY2023 MD&A line 282; FY2024 MD&A line 198; FY2025 MD&A line 209.
# TTM = Q3'25 98,366 + Q4'25 103,609 + Q1'26 122,385 + Q2'26 135,932 (Q2FY26 MD&A line 350)
adj_ebitda = {
    "FY2023": 368_247,
    "FY2024": 334_819,
    "FY2025": 376_306,
    "TTM Jun-2026": 98_366 + 103_609 + 122_385 + 135_932,
}

# Cash lease payments = principal + interest on lease liabilities (property + vehicle/equipment),
# taken from the FINANCING section of the statements of cash flows.
# FY2025 ties to AFS Note 17 "Repayments 161,561"; FY2024 ties to Note 17 "149,656".
lease_principal = {
    "FY2023": 95_441 + 3_863,
    "FY2024": 103_888 + 5_283,
    "FY2025": 111_142 + 5_594,
    "TTM Jun-2026": (111_142 + 5_594) - (54_892 + 2_815) + (72_637 + 2_901),
}
lease_interest = {
    "FY2023": 31_328 + 728,
    "FY2024": 39_464 + 1_021,
    "FY2025": 44_095 + 730,
    "TTM Jun-2026": (44_095 + 730) - (21_555 + 462) + (31_872 + 531),
}

# "Equipment purchases and facility improvements" - investing section of the cash flow
# statement. This is Boyd's non-growth capex line (growth/new-location capex sits inside
# "Acquisition and development of businesses").
capex_equip_actual = {
    "FY2023": 57_482,
    "FY2024": 77_333,
    "FY2025": 54_306,
    "TTM Jun-2026": 54_306 - 25_765 + 24_802,
}

# "Software purchases and licensing" - investing section of the cash flow statement.
capex_software_actual = {
    "FY2023": 1_684,
    "FY2024": 3_124,
    "FY2025": 8_094,
    "TTM Jun-2026": 8_094 - 3_132 + 936,
}

# Income taxes paid (cash), statements of cash flows supplemental disclosure.
cash_taxes_paid = {
    "FY2023": 27_909,
    "FY2024": 12_295,
    "FY2025": 3_669,
    "TTM Jun-2026": 3_669 - 2_555 + 3_260,
}

# Acquisition and transformational cost initiatives (income statement line), for reference.
acq_transform_actual = {
    "FY2023": 4_346,  # labelled "Acquisition and transaction costs" in FY2023
    "FY2024": 9_879,
    "FY2025": 30_488,
    "TTM Jun-2026": 30_488 - 13_773 + 31_264,
}

# Non-cash D&A, for reference / alternative lease treatment.
dep_ppe = {
    "FY2023": 56_863,
    "FY2024": 75_498,
    "FY2025": 87_851,
    "TTM Jun-2026": 87_851 - 42_394 + 54_792,
}
dep_rou = {
    "FY2023": 109_806,
    "FY2024": 123_512,
    "FY2025": 128_101,
    "TTM Jun-2026": 128_101 - 63_414 + 85_712,
}
amort_intangibles = {
    "FY2023": 26_182,
    "FY2024": 26_309,
    "FY2025": 28_020,
    "TTM Jun-2026": 28_020 - 13_548 + 32_457,
}

# ---------------------------------------------------------------------------
# 2. ASSUMPTIONS (the judgment calls - each is a single adjustable variable)
# ---------------------------------------------------------------------------

# Maintenance capex as % of sales. Management guidance, repeated in FY2025 MD&A line 526 and
# Q2FY26 MD&A line 102: "During 2026, the Company plans to make cash capital expenditures,
# excluding those related to network technology upgrades and acquisition and development of
# new locations, within the range of 1.6% and 1.8% of sales." Midpoint used.
MAINT_CAPEX_PCT = 0.017

# Normalized recurring acquisition transaction costs. Boyd is a perpetual tuck-in acquirer, so
# some deal cost recurs every year even excluding mega-deals. FY2022 actual $1,700 and FY2023
# actual $4,346 (pre-Joe Hudson's, pre-Project 360) bracket the ordinary-course level; $5,000
# is used to reflect a higher recent deal count. JUDGMENT / ESTIMATE.
NORMALIZED_ACQ_COST = 5_000

# Normalized tax rate. AFS Note 10a: combined basic Canadian and U.S. federal, provincial and
# state statutory rate was 26.66% (2025) and 26.53% (2024).
TAX_RATE = 0.265

# Operating cash requirement. Boyd's cash balance sat at $15.1M (Dec-22), $22.5M (Dec-23),
# $20.0M (Dec-24) and $23.0M (Jun-26); the $1,228.6M at Dec-25 was IPO/notes proceeds warehoused
# for the Joe Hudson's closing (AFS Note 6). Cash above this cap is treated as non-operating.
OPERATING_CASH_CAP = 25_000


# ---------------------------------------------------------------------------
# 3. OWNERS' EARNINGS - primary method: leases treated as an operating cost
# ---------------------------------------------------------------------------
# Rationale: Boyd leases essentially its entire shop network and actively converts owned
# property into leases via sale-leasebacks (19 properties / $53.3M in 2025, AFS Note 8). Rent is
# therefore an unavoidable operating cost of the current store base, not a financing decision.
# We deduct the FULL cash lease payment (principal + interest) in place of IFRS 16's
# ROU depreciation + lease finance cost, and correspondingly exclude ROU assets and lease
# liabilities from invested capital and (later) from enterprise value.

rows_oe = {}
for p in PERIODS:
    maint_capex = MAINT_CAPEX_PCT * sales[p]
    lease_cash = lease_principal[p] + lease_interest[p]
    pretax = (
        adj_ebitda[p]
        - lease_cash
        - maint_capex
        - capex_software_actual[p]
        - NORMALIZED_ACQ_COST
    )
    after_tax = pretax * (1 - TAX_RATE)
    rows_oe[p] = {
        "Sales": sales[p],
        "Adjusted EBITDA": adj_ebitda[p],
        "Adj EBITDA margin %": 100 * adj_ebitda[p] / sales[p],
        "(-) Cash lease payments": -lease_cash,
        "(-) Maintenance capex @1.7% sales": -maint_capex,
        "(-) Software & licensing capex": -capex_software_actual[p],
        "(-) Normalized acquisition costs": -NORMALIZED_ACQ_COST,
        "Pre-tax Owners' Earnings": pretax,
        "(-) Normalized tax @26.5%": -pretax * TAX_RATE,
        "Owners' Earnings": after_tax,
        "OE margin %": 100 * after_tax / sales[p],
    }


# ---------------------------------------------------------------------------
# 4. INVESTED CAPITAL
# ---------------------------------------------------------------------------
# Operating capital actually funded by Boyd's own debt + equity. EXCLUDES right-of-use assets
# and lease liabilities (consistent with charging full cash rent above), excess cash, deferred
# tax balances, derivative instruments, and all interest-bearing debt.

BS = {
    # Dec-2022 and Dec-2023 from FY2023 AFS statement of financial position
    "Dec-2022": dict(cash=15_068, ar=139_266, tax_recov=5_666, inventory=78_784, prepaid=36_520,
                     ppe=314_564, intangibles=332_939, goodwill=601_706, other_lt=6_067,
                     ap_accrued=307_729, unearned_rebates=5_194, rou=568_437,
                     dta=3_815, deriv=0, total_assets=2_102_832),
    "Dec-2023": dict(cash=22_511, ar=145_793, tax_recov=7_721, inventory=78_532, prepaid=41_728,
                     ppe=438_981, intangibles=342_781, goodwill=633_986, other_lt=11_720,
                     ap_accrued=339_823, unearned_rebates=4_579, rou=654_347,
                     dta=4_316, deriv=0, total_assets=2_382_416),
    # Dec-2024 and Dec-2025 from FY2025 AFS statement of financial position
    "Dec-2024": dict(cash=19_997, ar=120_616, tax_recov=12_307, inventory=73_134, prepaid=44_663,
                     ppe=529_673, intangibles=336_943, goodwill=643_864, other_lt=12_051,
                     ap_accrued=306_942, unearned_rebates=3_964, rou=668_101,
                     dta=2_840, deriv=0, total_assets=2_464_189),
    "Dec-2025": dict(cash=1_228_614, ar=137_474, tax_recov=10_196, inventory=68_284, prepaid=53_789,
                     ppe=581_146, intangibles=356_347, goodwill=702_460, other_lt=12_616,
                     ap_accrued=339_276, unearned_rebates=3_349, rou=689_247,
                     dta=12_625, deriv=7_153, total_assets=3_859_951),
    # Jun-2026 from Q2FY26 interim statement of financial position
    "Jun-2026": dict(cash=22_969, ar=175_219, tax_recov=9_276, inventory=78_003, prepaid=61_389,
                     ppe=714_219, intangibles=1_029_812, goodwill=1_227_770, other_lt=13_998,
                     ap_accrued=427_093, unearned_rebates=3_041, rou=951_087,
                     dta=10_051, deriv=4_305, total_assets=4_298_098),
}


def invested_capital(b):
    op_cash = min(b["cash"], OPERATING_CASH_CAP)
    # Working capital uses only genuinely CURRENT items. "Unearned rebates" is presented in the
    # NON-CURRENT liabilities block of the balance sheet (FY2025 AFS: it sits below the
    # $476,679 current-liabilities subtotal), so it is shown on its own line below, not here.
    nwc = (b["ar"] + b["tax_recov"] + b["inventory"] + b["prepaid"] - b["ap_accrued"])
    ic = op_cash + nwc - b["unearned_rebates"] + b["ppe"] + b["intangibles"] + b["goodwill"] + b["other_lt"]
    return {
        "Operating cash": op_cash,
        "Net operating working capital ex-cash": nwc,
        "(-) Unearned rebates (non-current op. liability)": -b["unearned_rebates"],
        "PP&E": b["ppe"],
        "Intangible assets": b["intangibles"],
        "Goodwill": b["goodwill"],
        "Other long-term assets": b["other_lt"],
        "Invested capital (ex-leases)": ic,
        "Invested capital ex-goodwill & intangibles": ic - b["goodwill"] - b["intangibles"],
        "Right of use assets (memo)": b["rou"],
        "Invested capital incl. leased assets": ic + b["rou"],
    }


IC = {d: invested_capital(b) for d, b in BS.items()}

IC_PAIRS = {
    "FY2023": ("Dec-2022", "Dec-2023"),
    "FY2024": ("Dec-2023", "Dec-2024"),
    "FY2025": ("Dec-2024", "Dec-2025"),
    "TTM Jun-2026": ("Dec-2025", "Jun-2026"),
}


def avg_ic(period, key):
    a, b = IC_PAIRS[period]
    return (IC[a][key] + IC[b][key]) / 2


# ---------------------------------------------------------------------------
# 5. ROIC
# ---------------------------------------------------------------------------

roic = {}
for p in PERIODS:
    oe = rows_oe[p]["Owners' Earnings"]
    ic_avg = avg_ic(p, "Invested capital (ex-leases)")
    ic_tang = avg_ic(p, "Invested capital ex-goodwill & intangibles")

    # Alternative treatment (b): capitalize leases. Replace cash rent with ROU depreciation,
    # treat lease interest as financing (excluded from OE), and include ROU assets in capital.
    pretax_b = (adj_ebitda[p] - dep_rou[p] - MAINT_CAPEX_PCT * sales[p]
                - capex_software_actual[p] - NORMALIZED_ACQ_COST)
    oe_b = pretax_b * (1 - TAX_RATE)
    ic_b = avg_ic(p, "Invested capital incl. leased assets")

    roic[p] = {
        "Owners' Earnings": oe,
        "Avg invested capital (ex-leases)": ic_avg,
        "ROIC %": 100 * oe / ic_avg,
        "Avg IC ex-goodwill/intangibles": ic_tang,
        "ROIC on tangible capital %": 100 * oe / ic_tang,
        "OE (leases capitalized)": oe_b,
        "Avg IC incl. leased assets": ic_b,
        "ROIC % (leases capitalized)": 100 * oe_b / ic_b,
    }


# ---------------------------------------------------------------------------
# 6. CROSS-CHECK: reported cash flow from operations -> normalized Owners' Earnings
# ---------------------------------------------------------------------------
# One reconciliation, running from Boyd's reported cash flow from operations - using ACTUAL
# cash lease payments, ACTUAL capex and ACTUAL taxes - across to the normalized Owners'
# Earnings figure. Every reconciling item is a disclosed number, and the reconciliation foots
# to zero by arithmetic, not by a plug. Reading it tells you exactly what the normalization
# is worth, line by line.
#
# Boyd reports ALL interest and ALL lease principal in FINANCING activities (AFS Note 2u), so
# reported CFO is before rent and before interest.

cfo = {"FY2023": 357_545, "FY2024": 313_325, "FY2025": 352_989,
       "TTM Jun-2026": 352_989 - 170_593 + 224_591}
wc_change = {"FY2023": 19_072, "FY2024": -5_909, "FY2025": 5_752,
             "TTM Jun-2026": 5_752 - 18_791 - 6_375}
# Equity-settled share-based payment added back as non-cash in CFO. Not separately disclosed
# in FY2023 (subsumed in "Other"); FY2024 per FY2025 AFS comparative column.
sbc_addback = {"FY2023": 0, "FY2024": 928, "FY2025": 4_319,
               "TTM Jun-2026": 4_319 - 1_877 + 4_689}
# "Other" non-cash add-back line in CFO (mainly losses on disposal, which sit in operating
# expenses and are therefore already inside Adjusted EBITDA).
other_addback = {"FY2023": 444, "FY2024": 1_033, "FY2025": 2_928,
                 "TTM Jun-2026": 2_928 - 1 + 3_425}
# CURRENT income tax expense from the statement of earnings - not cash tax paid. The working
# capital line already carries the income-taxes-payable movement, so adding back the current
# expense (rather than the cash payment) avoids double-counting that movement.
current_tax = {"FY2023": 25_872, "FY2024": 7_667, "FY2025": 5_828,
               "TTM Jun-2026": 5_828 - 10_634 + 4_201}

recon = {}
for p_ in PERIODS:
    lease_cash = lease_principal[p_] + lease_interest[p_]
    d = {}
    d["Cash flow from operations (reported)"] = cfo[p_]
    d["(-) Cash lease payments (ACTUAL)"] = -lease_cash
    d["(-) Equipment purchases & facility improvements (ACTUAL)"] = -capex_equip_actual[p_]
    d["(-) Software purchases and licensing (ACTUAL)"] = -capex_software_actual[p_]
    d["= Cash flow after rent and actual capex"] = (
        cfo[p_] - lease_cash - capex_equip_actual[p_] - capex_software_actual[p_])
    d["(-) Working capital swing (OE normalizes to nil)"] = -wc_change[p_]
    d["(-) Equity-settled SBC added back in CFO"] = -sbc_addback[p_]
    d["(-) Other non-cash items added back in CFO"] = -other_addback[p_]
    d["(+) Actual acquisition & transformational costs"] = acq_transform_actual[p_]
    d["(-) Normalized recurring acquisition cost"] = -NORMALIZED_ACQ_COST
    d["(+) Capex: actual less assumed maintenance"] = (
        capex_equip_actual[p_] - MAINT_CAPEX_PCT * sales[p_])
    d["(+) Current income tax expense (added back)"] = current_tax[p_]
    d["(-) Normalized income tax @26.5%"] = -rows_oe[p_]["Pre-tax Owners' Earnings"] * TAX_RATE
    d["= Owners' Earnings (normalized)"] = sum(
        v for k, v in d.items() if not k.startswith("="))
    d["Check: less primary method (must be nil)"] = (
        d["= Owners' Earnings (normalized)"] - rows_oe[p_]["Owners' Earnings"])
    recon[p_] = d


# ---------------------------------------------------------------------------
# 7. SENSITIVITY: maintenance capex is the swing assumption
# ---------------------------------------------------------------------------

sens = {}
for pct in (0.014, 0.017, 0.020, 0.025):
    row = {}
    for p in PERIODS:
        pretax = (adj_ebitda[p] - (lease_principal[p] + lease_interest[p]) - pct * sales[p]
                  - capex_software_actual[p] - NORMALIZED_ACQ_COST)
        oe = pretax * (1 - TAX_RATE)
        row[p] = (oe, 100 * oe / avg_ic(p, "Invested capital (ex-leases)"))
    sens[pct] = row


# ---------------------------------------------------------------------------
# 8. NON-OPERATING ITEMS EXCLUDED FROM OE (carry forward to valuation)
# ---------------------------------------------------------------------------

non_operating_jun2026 = {
    "Cash (Q2FY26 BS)": 22_969,
    "Long-term debt incl. current portion (7,200 + 411,622)": -(7_200 + 411_622),
    "Senior unsecured notes": -557_205,
    "Derivative financial instruments, net asset (4,305 - 3,003)": 4_305 - 3_003,
    "Net deferred income tax liability (104,318 - 10,051)": -(104_318 - 10_051),
    "Dividends payable": -3_056,
    "Lease liabilities, total (MEMO ONLY - excluded, rent charged in OE)": -(159_574 + 891_311),
}


# ---------------------------------------------------------------------------
# OUTPUT
# ---------------------------------------------------------------------------

def fmt(v, dec=1):
    return f"{v/TH:>10,.{dec}f}"


def table(title, rowdict_by_period, keys, pct_keys=()):
    print(f"\n{title}")
    print("-" * (46 + 13 * len(PERIODS)))
    print(f"{'(US$ millions)':<44}" + "".join(f"{p:>13}" for p in PERIODS))
    for k in keys:
        cells = ""
        for p in PERIODS:
            v = rowdict_by_period[p][k]
            cells += f"{v:>13,.1f}" if k in pct_keys else f"{v/TH:>13,.1f}"
        print(f"{k:<44}{cells}")


print("=" * 110)
print("BOYD GROUP SERVICES INC. - OWNERS' EARNINGS AND ROIC   (US$ millions unless noted)")
print("=" * 110)

table("OWNERS' EARNINGS (leases treated as an operating cost)", rows_oe,
      ["Sales", "Adjusted EBITDA", "Adj EBITDA margin %", "(-) Cash lease payments",
       "(-) Maintenance capex @1.7% sales", "(-) Software & licensing capex",
       "(-) Normalized acquisition costs", "Pre-tax Owners' Earnings",
       "(-) Normalized tax @26.5%", "Owners' Earnings", "OE margin %"],
      pct_keys={"Adj EBITDA margin %", "OE margin %"})

print("\nINVESTED CAPITAL BY BALANCE SHEET DATE (US$ millions)")
print("-" * 110)
keys_ic = ["Operating cash", "Net operating working capital ex-cash",
           "(-) Unearned rebates (non-current op. liability)", "PP&E", "Intangible assets",
           "Goodwill", "Other long-term assets", "Invested capital (ex-leases)",
           "Invested capital ex-goodwill & intangibles", "Right of use assets (memo)",
           "Invested capital incl. leased assets"]
dates = list(BS.keys())
print(f"{'':<44}" + "".join(f"{d:>13}" for d in dates))
for k in keys_ic:
    print(f"{k:<44}" + "".join(f"{IC[d][k]/TH:>13,.1f}" for d in dates))

table("ROIC", roic,
      ["Owners' Earnings", "Avg invested capital (ex-leases)", "ROIC %",
       "Avg IC ex-goodwill/intangibles", "ROIC on tangible capital %",
       "OE (leases capitalized)", "Avg IC incl. leased assets", "ROIC % (leases capitalized)"],
      pct_keys={"ROIC %", "ROIC on tangible capital %", "ROIC % (leases capitalized)"})

print("\nCROSS-CHECK: reported cash flow from operations -> normalized Owners' Earnings")
print("-" * 110)
print(f"{'(US$ millions)':<58}" + "".join(f"{p:>13}" for p in PERIODS))
for k in recon["FY2025"]:
    print(f"{k:<58}" + "".join(f"{recon[p][k]/TH:>13,.1f}" for p in PERIODS))

print("\nSENSITIVITY OF OE / ROIC TO MAINTENANCE CAPEX ASSUMPTION")
print("-" * 110)
print(f"{'Maint capex % of sales':<28}" + "".join(f"{p:>26}" for p in PERIODS))
for pct, row in sens.items():
    cells = "".join(f"{row[p][0]/TH:>16,.1f} ({row[p][1]:>4.1f}%)" for p in PERIODS)
    print(f"{pct*100:>6.1f}%{'':<21}{cells}")

print("\nNON-OPERATING ITEMS AT JUN-30-2026 EXCLUDED FROM OWNERS' EARNINGS (US$ millions)")
print("-" * 110)
for k, v in non_operating_jun2026.items():
    print(f"{k:<74}{v/TH:>12,.1f}")
net_no = sum(v for k, v in non_operating_jun2026.items() if "MEMO" not in k)
print(f"{'NET non-operating position (excl. leases) - deduct from equity value':<74}{net_no/TH:>12,.1f}")


# ---------------------------------------------------------------------------
# 9. DERIVED RATIOS QUOTED IN work_products/owners_earnings_and_roic.md
# ---------------------------------------------------------------------------
print("\nDERIVED RATIOS QUOTED IN THE WRITE-UP")
print("-" * 110)
_oe25 = rows_oe["FY2025"]["Owners' Earnings"]
_lease25 = lease_principal["FY2025"] + lease_interest["FY2025"]
print(f"{'FY2025 Owners Earnings as % of Adjusted EBITDA':<70}"
      f"{100*_oe25/adj_ebitda['FY2025']:>10.1f}%")
print(f"{'FY2025 cash rent as % of Adjusted EBITDA':<70}"
      f"{100*_lease25/adj_ebitda['FY2025']:>10.1f}%")
print(f"{'FY2025 rent + maintenance capex (US$m)':<70}"
      f"{(_lease25 + MAINT_CAPEX_PCT*sales['FY2025'])/TH:>10,.1f}")
for d in BS:
    gw_int = BS[d]["goodwill"] + BS[d]["intangibles"]
    print(f"{'Goodwill + intangibles at ' + d + ' (US$m)':<70}{gw_int/TH:>10,.1f}")
_syn = 65_000  # Q2FY26 MD&A: $30m more in 2026 + $35m 2027-2029, still to be realized
print(f"{'Remaining annualized synergy, after tax, as pp of TTM ROIC':<70}"
      f"{100*_syn*(1-TAX_RATE)/avg_ic('TTM Jun-2026', 'Invested capital (ex-leases)'):>10.1f}pp")
print(f"{'Pro-forma TTM ROIC incl. remaining synergies':<70}"
      f"{100*(_oe25*0+roic['TTM Jun-2026']['Owners’ Earnings'.replace(chr(8217), chr(39))]+_syn*(1-TAX_RATE))/avg_ic('TTM Jun-2026', 'Invested capital (ex-leases)'):>10.1f}%")
print(f"{'FY2025 ROU assets vs owned PP&E (US$m)':<70}"
      f"{BS['Dec-2025']['rou']/TH:>10,.1f} vs {BS['Dec-2025']['ppe']/TH:,.1f}")
print(f"{'Total lease liabilities at Jun-30-2026 (US$m)':<70}{(159_574+891_311)/TH:>10,.1f}")
# tangible ROIC at the punitive 2.5% maintenance capex assumption
for p in ("FY2024", "FY2025", "TTM Jun-2026"):
    oe_25 = sens[0.025][p][0]
    print(f"{'Tangible ROIC at 2.5% maint capex - ' + p:<70}"
          f"{100*oe_25/avg_ic(p, 'Invested capital ex-goodwill & intangibles'):>10.1f}%")


# ---------------------------------------------------------------------------
# 10. HOW AVERAGE INVESTED CAPITAL IS DERIVED (shown explicitly for the write-up)
# ---------------------------------------------------------------------------
# Convention: simple two-point average of the opening and closing balance sheet for each
# period. Boyd reports a balance sheet only at Dec-31 and Jun-30, so a two-point average is
# the finest granularity the filings support; a monthly-weighted average is not computable.
print("\nDERIVATION OF AVERAGE INVESTED CAPITAL (US$ millions)")
print("-" * 110)
for key, short in [("Invested capital (ex-leases)", "IC ex-leases"),
                   ("Invested capital ex-goodwill & intangibles", "IC ex-GW & intangibles"),
                   ("Invested capital incl. leased assets", "IC incl. leased assets")]:
    print(f"\n{short}")
    print(f"  {'Period':<16}{'Opening':>12}{'Closing':>12}{'Average':>12}   formula")
    for p in PERIODS:
        a, b = IC_PAIRS[p]
        o, c_ = IC[a][key], IC[b][key]
        print(f"  {p:<16}{o/TH:>12,.1f}{c_/TH:>12,.1f}{(o + c_) / 2 / TH:>12,.1f}"
              f"   ({a} + {b}) / 2")

# The ex-goodwill/intangibles base is the same invested capital less the two acquisition
# accounts, at each balance sheet date.
print("\nDerivation of 'IC ex-goodwill & intangibles' at each date (US$ millions)")
print(f"  {'Date':<12}{'IC ex-leases':>14}{'(-) Goodwill':>14}{'(-) Intangibles':>17}{'= Tangible IC':>15}")
for d in BS:
    print(f"  {d:<12}{IC[d]['Invested capital (ex-leases)']/TH:>14,.1f}"
          f"{-BS[d]['goodwill']/TH:>14,.1f}{-BS[d]['intangibles']/TH:>17,.1f}"
          f"{IC[d]['Invested capital ex-goodwill & intangibles']/TH:>15,.1f}")


# ---------------------------------------------------------------------------
# 11. LINE-BY-LINE BUILD OF INVESTED CAPITAL FROM THE FACE OF THE BALANCE SHEET
# ---------------------------------------------------------------------------
print("\nINVESTED CAPITAL - LINE BY LINE FROM THE BALANCE SHEET (US$ millions)")
print("-" * 110)
_d = list(BS.keys())
_rows = [
    ("(+) Cash, capped at operating requirement", lambda b: min(b["cash"], OPERATING_CASH_CAP)),
    ("(+) Accounts receivable", lambda b: b["ar"]),
    ("(+) Income taxes recoverable", lambda b: b["tax_recov"]),
    ("(+) Inventory", lambda b: b["inventory"]),
    ("(+) Prepaid expenses", lambda b: b["prepaid"]),
    ("(+) Property, plant and equipment", lambda b: b["ppe"]),
    ("(+) Intangible assets", lambda b: b["intangibles"]),
    ("(+) Goodwill", lambda b: b["goodwill"]),
    ("(+) Other long-term assets", lambda b: b["other_lt"]),
    ("(-) Accounts payable and accrued liabilities", lambda b: -b["ap_accrued"]),
    ("(-) Unearned rebates", lambda b: -b["unearned_rebates"]),
]
print(f"{'':<46}" + "".join(f"{x:>13}" for x in _d))
for lab, fn in _rows:
    print(f"{lab:<46}" + "".join(f"{fn(BS[x])/TH:>13,.1f}" for x in _d))
print(f"{'= INVESTED CAPITAL (ex-leases)':<46}"
      + "".join(f"{IC[x]['Invested capital (ex-leases)']/TH:>13,.1f}" for x in _d))
print(f"{'  check: sum of rows above':<46}"
      + "".join(f"{sum(fn(BS[x]) for _, fn in _rows)/TH:>13,.1f}" for x in _d))

print("\nTIE-OUT TO REPORTED TOTAL ASSETS (US$ millions)")
print("-" * 110)
_ex = [
    ("Total assets (reported)", lambda b: b["total_assets"]),
    ("(-) Cash above operating requirement", lambda b: -max(0, b["cash"] - OPERATING_CASH_CAP)),
    ("(-) Right of use assets", lambda b: -b["rou"]),
    ("(-) Deferred income tax asset", lambda b: -b["dta"]),
    ("(-) Derivative financial instruments", lambda b: -b["deriv"]),
    ("= Operating assets included", lambda b: (
        b["total_assets"] - max(0, b["cash"] - OPERATING_CASH_CAP) - b["rou"]
        - b["dta"] - b["deriv"])),
    ("(-) Accounts payable and accrued liabilities", lambda b: -b["ap_accrued"]),
    ("(-) Unearned rebates", lambda b: -b["unearned_rebates"]),
    ("= INVESTED CAPITAL (ex-leases)", lambda b: (
        b["total_assets"] - max(0, b["cash"] - OPERATING_CASH_CAP) - b["rou"] - b["dta"]
        - b["deriv"] - b["ap_accrued"] - b["unearned_rebates"])),
]
print(f"{'':<46}" + "".join(f"{x:>13}" for x in _d))
for lab, fn in _ex:
    print(f"{lab:<46}" + "".join(f"{fn(BS[x])/TH:>13,.1f}" for x in _d))
print(f"{'  difference vs section 11 build (must be nil)':<46}"
      + "".join(f"{(_ex[-1][1](BS[x]) - IC[x]['Invested capital (ex-leases)'])/TH:>13,.1f}"
                for x in _d))


# ---------------------------------------------------------------------------
# 12. MEMO: ACTUAL CASH TAX PAID vs. ADJUSTED EBITDA AFTER RENT
# ---------------------------------------------------------------------------
# Shows how little cash tax Boyd has actually paid relative to its operating cash earnings,
# to contextualize the 26.5% statutory rate used in Owners' Earnings. FY2022 is included here
# (memo only) because the data is in the FY2023 AFS comparative column and it lengthens the
# history; it is not used anywhere else in the model.
from dataclasses import dataclass


@dataclass
class CashTaxInputs:
    period: str
    adjusted_ebitda: float        # company-reported Adjusted EBITDA
    cash_lease_payments: float    # lease principal + lease interest, financing section of CFS
    cash_income_tax_paid: float   # "Income taxes paid", supplemental line of CFS
    source: str


cash_tax_history = [
    CashTaxInputs("FY2022", 273_500, 92_203 + 3_047 + 21_363 + 432, 3_857,
                  "Adj EBITDA: FY2023 MD&A line 282; leases: FY2023 AFS lines 277-281; "
                  "tax: FY2023 AFS line 297"),
] + [
    CashTaxInputs(p, adj_ebitda[p], lease_principal[p] + lease_interest[p], cash_taxes_paid[p],
                  src)
    for p, src in [
        ("FY2023", "tax: FY2023 AFS line 297"),
        ("FY2024", "tax: FY2024 AFS line 300"),
        ("FY2025", "tax: FY2025 AFS line 318"),
        ("TTM Jun-2026", "tax: FY2025 AFS line 318 less H1'25 plus H1'26, Q2FY26 line 190"),
    ]
]


def adjusted_ebitda_after_rent(x: CashTaxInputs) -> float:
    return x.adjusted_ebitda - x.cash_lease_payments


def cash_tax_as_pct_of_ebitda_after_rent(x: CashTaxInputs) -> float:
    return x.cash_income_tax_paid / adjusted_ebitda_after_rent(x)


def normalized_tax_as_pct_of_ebitda_after_rent(x: CashTaxInputs) -> float | None:
    """The normalized tax charged in the OE bridge, on the same base, for comparison."""
    if x.period not in rows_oe:
        return None
    return -rows_oe[x.period]["(-) Normalized tax @26.5%"] / adjusted_ebitda_after_rent(x)


print("\nMEMO: ACTUAL CASH TAX PAID vs. ADJUSTED EBITDA AFTER RENT (US$ millions)")
print("-" * 110)
print(f"{'':<46}" + "".join(f"{x.period:>13}" for x in cash_tax_history))
print(f"{'Adjusted EBITDA':<46}" + "".join(f"{x.adjusted_ebitda/TH:>13,.1f}" for x in cash_tax_history))
print(f"{'(-) Cash lease payments':<46}" + "".join(f"{-x.cash_lease_payments/TH:>13,.1f}" for x in cash_tax_history))
print(f"{'= Adjusted EBITDA after rent':<46}" + "".join(f"{adjusted_ebitda_after_rent(x)/TH:>13,.1f}" for x in cash_tax_history))
print(f"{'Cash income taxes paid (actual)':<46}" + "".join(f"{x.cash_income_tax_paid/TH:>13,.1f}" for x in cash_tax_history))
print(f"{'Cash tax paid % of Adj. EBITDA after rent':<46}" + "".join(f"{100*cash_tax_as_pct_of_ebitda_after_rent(x):>12.1f}%" for x in cash_tax_history))
print(f"{'Normalized OE tax % of same base (compare)':<46}" + "".join(
    f"{'n/a':>13}" if normalized_tax_as_pct_of_ebitda_after_rent(x) is None
    else f"{100*normalized_tax_as_pct_of_ebitda_after_rent(x):>12.1f}%" for x in cash_tax_history))


OE_KEY = "Owners' Earnings"


def owners_earnings_if_cash_tax_used(period: str) -> float:
    """Sensitivity: pre-tax OE less ACTUAL cash tax paid, instead of the 26.5% normalized tax."""
    return rows_oe[period]["Pre-tax Owners' Earnings"] - cash_taxes_paid[period]


print(f"{'OE if actual cash tax replaced normalized tax':<46}{'n/a':>13}" + "".join(
    f"{owners_earnings_if_cash_tax_used(p)/TH:>13,.1f}" for p in PERIODS))
print(f"{'OE as reported (normalized tax)':<46}{'n/a':>13}" + "".join(
    f"{rows_oe[p][OE_KEY]/TH:>13,.1f}" for p in PERIODS))

# Debt interest is tax-deductible, so Boyd's cash tax is a LEVERED figure, while Owners'
# Earnings is pre-interest and so needs an UNLEVERED tax. FY2025 interest on long-term debt
# per FY2025 AFS statement of cash flows (financing section).
FY2025_INTEREST_ON_LONG_TERM_DEBT = 32_707
print(f"{'FY2025 tax shield on debt interest @26.5%':<46}"
      f"{FY2025_INTEREST_ON_LONG_TERM_DEBT * TAX_RATE / TH:>13,.1f}")
