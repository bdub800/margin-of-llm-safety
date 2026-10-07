"""
NamSys Inc. (CTZ.V) -- Owners' Earnings and ROIC
Companion calculation script for work_products/owners_earnings_and_roic.md

ALL INPUTS ARE TAKEN DIRECTLY FROM primary_sources/ (audited annual financial
statements FY2023/FY2024/FY2025 and the unaudited Q2 FY2026 interim statements).
Every input is tagged with its source file and line reference in comments.
All amounts in Canadian dollars.
"""

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# 1. REPORTED INPUTS
# ---------------------------------------------------------------------------
# FY2022, FY2023: primary_sources/FY2023/Namsys_-_Annual_FS_-_Feb262024.md
# FY2024        : primary_sources/FY2024/NamSys_AFS_021925.md
# FY2025        : primary_sources/FY2025/NamSys_AFS_022426.md
# H1 FY2026/H1 FY2025: primary_sources/2Q2026/FS_Q2_NamSys_Apr_30_26_FINAL.md


@dataclass
class Period:
    name: str
    revenue: float
    operating_income: float     # after bad debt expense, after SBC, after depreciation
    bad_debt: float             # reported bad debt expense (inside operating income)
    sbc: float                  # reported share-based compensation (inside operating income)
    depreciation: float         # depreciation of PP&E (+ ROU asset where applicable)
    capex: float                # purchase of property and equipment
    interest_income: float
    fx_gain: float              # gain (loss) on foreign exchange
    pretax_income: float
    tax_expense: float
    net_income: float
    ocf: float                  # cash flows from operating activities
    # operating balance sheet at period END
    receivables: float
    prepaid: float
    ppe: float
    payables: float
    deferred_revenue: float
    cash: float
    st_investments: float
    cogs: float
    opex: float                 # total expenses (selling + G&A + bad debt)
    gna: float                  # general and administration expense line
    # "Adjustments to determine taxable income" per the Note 9 tax-rate reconciliation
    tax_recon_adj: float
    # Off-balance-sheet office lease commitment DISCLOSED AT THIS BALANCE SHEET DATE
    lease_commitment: float


FY2022 = Period(
    name="FY2022", revenue=5_394_781, operating_income=1_753_157,
    bad_debt=2_546, sbc=0.0,
    # PP&E depreciation only. The $10,768 of right-of-use asset depreciation is NOT
    # added back: it is the economic cost of renting premises (cash lease payment of
    # $11,250 sat in financing activities in FY2022), i.e. a real recurring operating
    # cost, not a non-economic accounting charge.
    depreciation=12_028,
    capex=9_311, interest_income=5_812, fx_gain=139_768,
    pretax_income=1_898_682, tax_expense=504_242, net_income=1_394_440, ocf=962_018,
    receivables=1_038_800, prepaid=114_670, ppe=33_466,
    payables=433_360, deferred_revenue=222_349,
    cash=4_708_122, st_investments=800_000,
    cogs=2_248_149, opex=1_393_475, gna=1_060_340,
    tax_recon_adj=1_091,        # FY2023 AFS Note 9, 2022 column
    # No office-lease commitment disclosed at Oct 31, 2022 in the sources available
    # (the FY2022 IFRS-16 right-of-use lease had run off: $11,250 of cash lease
    # payments and $10,768 of ROU depreciation during FY2022, no ROU asset on the
    # Oct-31-22 balance sheet). The FY2022 AFS itself is not in primary_sources.
    lease_commitment=0.0,
)

FY2023 = Period(
    name="FY2023", revenue=6_093_020, operating_income=2_107_434,
    bad_debt=23_004, sbc=191_468, depreciation=7_191, capex=4_982,
    interest_income=195_112, fx_gain=-5_780,
    pretax_income=2_296_766, tax_expense=681_891, net_income=1_614_875, ocf=1_659_749,
    receivables=1_181_189, prepaid=139_050, ppe=31_257,
    payables=423_386, deferred_revenue=287_783,
    cash=1_119_089, st_investments=6_099_223,
    cogs=2_440_520, opex=1_545_066, gna=1_140_611,
    tax_recon_adj=73_248,       # FY2023 AFS Note 9
    lease_commitment=7_474,     # FY2023 AFS Note 13: Jan 1 2024 - Dec 31 2024 lease
)

FY2024 = Period(
    name="FY2024", revenue=6_840_146, operating_income=2_572_018,
    bad_debt=0.0, sbc=114_174, depreciation=7_023, capex=8_259,
    interest_income=291_840, fx_gain=25_590,
    pretax_income=2_889_448, tax_expense=798_973, net_income=2_090_475, ocf=2_508_076,
    receivables=975_812, prepaid=171_893, ppe=32_493,
    payables=428_543, deferred_revenue=440_985,
    cash=817_800, st_investments=7_229_551,
    cogs=2_570_778, opex=1_697_350, gna=1_255_163,
    tax_recon_adj=33_269,       # FY2024 AFS Note 9
    lease_commitment=8_927,     # FY2024 AFS Note 13: Feb 1 2025 - Jan 31 2026 lease
)

FY2025 = Period(
    name="FY2025", revenue=7_891_605, operating_income=3_146_476,
    bad_debt=51_330, sbc=47_030, depreciation=7_465, capex=9_661,
    interest_income=265_771, fx_gain=-10_945,
    pretax_income=3_401_302, tax_expense=915_193, net_income=2_486_109, ocf=2_196_505,
    receivables=1_241_499, prepaid=162_679, ppe=34_689,
    payables=544_985, deferred_revenue=301_975,
    cash=846_423, st_investments=9_329_249,
    cogs=2_813_196, opex=1_931_933, gna=1_165_985,
    tax_recon_adj=13_848,       # FY2025 AFS Note 9
    lease_commitment=9_195,     # FY2025 AFS Note 13: Feb 1 2026 - Jan 31 2027 lease
)

# TTM = FY2025 + H1 FY2026 - H1 FY2025.  Balance sheet is as at April 30, 2026.
TTM = Period(
    name="TTM Apr-26",
    revenue=7_891_605 + 4_267_406 - 3_951_863,
    operating_income=3_146_476 + 1_779_560 - 1_626_795,
    bad_debt=51_330 + 0 - 50_746,
    sbc=47_030 + 4_894 - 27_020,
    depreciation=7_465 + 3_623 - 3_449,
    capex=9_661 + 3_595 - 3_998,
    interest_income=265_771 + 111_013 - 132_073,
    fx_gain=-10_945 + (-102_941) - (-34_680),
    pretax_income=3_401_302 + 1_787_632 - 1_724_188,
    tax_expense=915_193 + 475_568 - 464_842,
    net_income=2_486_109 + 1_312_064 - 1_259_346,
    ocf=2_196_505 + 1_497_265 - 1_223_129,
    receivables=1_381_988, prepaid=146_330, ppe=34_661,
    payables=360_682, deferred_revenue=707_554,
    cash=940_082, st_investments=6_425_965,
    cogs=2_813_196 + 1_596_137 - 1_364_558,
    opex=1_931_933 + 891_709 - 960_510,
    gna=1_165_985 + 582_407 - 574_253,
    tax_recon_adj=13_848 + 1_846 - 7_932,   # Q2-26 FS Note 9 discloses the interim
                                            # reconciliation: H1-26 1,846 / H1-25 7,932
    lease_commitment=6_896,     # Q2-26 MD&A contractual obligations at Apr 30, 2026
)

PERIODS = [FY2022, FY2023, FY2024, FY2025, TTM]

# ---------------------------------------------------------------------------
# 2. NORMALISING ASSUMPTIONS (each justified in the write-up)
# ---------------------------------------------------------------------------
TAX_RATE = 0.265          # FY2025 MD&A: "The basic rate of 26.50% was applied"
# Normalised bad debt = simple average of reported FY2022-FY2025 bad debt expense
NORM_BAD_DEBT = (2_546 + 23_004 + 0 + 51_330) / 4
# Normalised SBC = average reported FY2023-FY2025 (the only years with a live grant),
# cross-checked against the Dec-2022 grant fair value of $357,566 amortised over 3 yrs.
NORM_SBC = (191_468 + 114_174 + 47_030) / 3
SBC_GRANT_CHECK = 357_566 / 3
# Operating cash requirement = 1 month of cash operating costs
OPERATING_CASH_MONTHS = 1.0
# Off-balance-sheet office lease: the FY2025 AFS Note 13 wording ("Monthly lease
# payments total $9,195 over the 12 month term") reads as $9,195/month. It is not:
# the Q2-26 MD&A contractual obligations table shows $6,896 remaining at Apr-30-26
# with 9 of 12 months to run, i.e. 9,195 x 9/12 = 6,896  =>  $9,195 is the TOTAL
# 12-month obligation. Each period now uses the commitment DISCLOSED AT ITS OWN
# balance sheet date (Period.lease_commitment) rather than a flat $9,195.
LEASE_CHECK = 9_195.0 * 9 / 12

# ---------------------------------------------------------------------------
# 3. OWNERS' EARNINGS
# ---------------------------------------------------------------------------
# Start at operating income (already excludes interest income and interest expense;
# the company has no debt).  FX gain/loss sits below operating income and is
# normalised to nil.  Then:
#   + reported bad debt      - normalised bad debt
#   + reported SBC           - normalised SBC
#   + depreciation           - maintenance capex (actual PP&E capex)
# Tax: 26.5% applied to the normalised base GROSSED UP for SBC, because stock-option
# SBC is not deductible in Canada (see reconciliation cross-check below).


def other_perm_diff(p: Period):
    """Permanent tax differences NOT explained by non-deductible stock-option SBC.

    The Note 9 reconciliation line 'Adjustments to determine taxable income' is the
    total gap between 26.5% x pre-tax income and reported tax expense. Non-deductible
    SBC explains most of it in FY2022/FY2024/FY2025/TTM but only ~69% of it in FY2023.
    The unexplained residual is carried as an explicit extra tax cost rather than
    assumed away."""
    return p.tax_recon_adj - p.sbc * TAX_RATE


def owners_earnings(p: Period):
    pre_tax = (
        p.operating_income
        + p.bad_debt - NORM_BAD_DEBT
        + p.sbc - NORM_SBC
        + p.depreciation - p.capex
    )
    taxable = pre_tax + NORM_SBC          # add back non-deductible SBC
    tax = TAX_RATE * taxable + other_perm_diff(p)
    return {
        "pretax": pre_tax,
        "tax": tax,
        "oe": pre_tax - tax,
        "margin": (pre_tax - tax) / p.revenue,
    }


# Cross-check that SBC non-deductibility explains the tax reconciliation
# ("Adjustments to determine taxable income", FY2025 AFS Note 9)
TAX_RECON_CHECK = {
    "FY2025": {"reported_adj": 13_848, "sbc_x_rate": 47_030 * TAX_RATE},
    "FY2024": {"reported_adj": 33_269, "sbc_x_rate": 114_174 * TAX_RATE},
}

# ---------------------------------------------------------------------------
# 4. INVESTED CAPITAL
# ---------------------------------------------------------------------------
# Operating invested capital = operating cash + receivables + prepaids + PP&E
#   - trade & other payables - deferred revenue + capitalised off-BS office lease.
# EXCLUDED: short-term investments and surplus cash (non-operating), income taxes
# receivable/payable and deferred income tax assets (tax accounts, not operating
# capital).  Employee termination commitments ($1.1M) are a contingent liability,
# not capital deployed -- shown separately as a sensitivity.


def invested_capital(p: Period, cash_months=OPERATING_CASH_MONTHS):
    cash_opcosts = p.cogs + p.opex - p.sbc - p.depreciation
    op_cash = min(cash_opcosts * cash_months / 12.0, p.cash + p.st_investments)
    ic = (
        op_cash + p.receivables + p.prepaid + p.ppe
        - p.payables - p.deferred_revenue
        + p.lease_commitment
    )
    return {"op_cash": op_cash, "ic": ic}


# ---------------------------------------------------------------------------
# 5. OUTPUT
# ---------------------------------------------------------------------------
def fmt(x):
    return f"{x:>12,.0f}"


if __name__ == "__main__":
    print("=" * 100)
    print("CHECKS")
    print("=" * 100)
    print(f"Normalised bad debt (avg FY22-25)      : {NORM_BAD_DEBT:,.0f}")
    print(f"Normalised SBC (avg FY23-25)           : {NORM_SBC:,.0f}")
    print(f"  cross-check: FY2023 grant FV / 3 yrs : {SBC_GRANT_CHECK:,.0f}")
    print(f"Lease: 9,195 x 9/12                    : {LEASE_CHECK:,.0f}  "
          f"(Q2-26 MD&A reports 6,896 remaining -> 9,195 is the ANNUAL total)")
    print("Tax reconciliation: how much of Note 9's 'Adjustments to determine taxable")
    print("income' is explained by non-deductible stock-option SBC?")
    for p_ in PERIODS:
        print(f"   {p_.name:<12} reported adj {p_.tax_recon_adj:>9,.0f}   "
              f"SBC x 26.5% {p_.sbc*TAX_RATE:>9,.0f}   "
              f"unexplained residual {other_perm_diff(p_):>9,.0f}   "
              f"({p_.sbc*TAX_RATE/p_.tax_recon_adj*100 if p_.tax_recon_adj else 0:>5.0f}% explained)")
    print()

    print("=" * 100)
    print("OWNERS' EARNINGS BRIDGE")
    print("=" * 100)
    hdr = f"{'':<42}" + "".join(f"{p.name:>14}" for p in PERIODS)
    print(hdr)
    rows = [
        ("Revenue", lambda p: p.revenue),
        ("Operating income (reported)", lambda p: p.operating_income),
        ("+ reported bad debt expense", lambda p: p.bad_debt),
        ("- normalised bad debt", lambda p: -NORM_BAD_DEBT),
        ("+ reported share-based comp", lambda p: p.sbc),
        ("- normalised share-based comp", lambda p: -NORM_SBC),
        ("+ depreciation", lambda p: p.depreciation),
        ("- maintenance capex (actual)", lambda p: -p.capex),
        ("= Normalised pre-tax owners' earnings", lambda p: owners_earnings(p)["pretax"]),
        ("- normalised tax @26.5% (SBC non-ded.)",
         lambda p: -(TAX_RATE * (owners_earnings(p)["pretax"] + NORM_SBC))),
        ("- other permanent tax differences", lambda p: -other_perm_diff(p)),
        ("= OWNERS' EARNINGS", lambda p: owners_earnings(p)["oe"]),
    ]
    for label, fn in rows:
        print(f"{label:<42}" + "".join(fmt(fn(p)) for p in PERIODS))
    print(f"{'OE margin (% of revenue)':<42}"
          + "".join(f"{owners_earnings(p)['margin']*100:>13.1f}%" for p in PERIODS))
    print(f"{'Memo: reported net income':<42}" + "".join(fmt(p.net_income) for p in PERIODS))
    print(f"{'Memo: interest income excluded':<42}" + "".join(fmt(p.interest_income) for p in PERIODS))
    print(f"{'Memo: FX gain/(loss) excluded':<42}" + "".join(fmt(p.fx_gain) for p in PERIODS))

    print()
    print("=" * 100)
    print("CASH-FLOW SANITY CHECK (does owners' earnings show up as cash?)")
    print("=" * 100)
    for p in PERIODS:
        after_tax_interest = p.interest_income * (1 - TAX_RATE)
        fcf = p.ocf - p.capex - after_tax_interest
        oe = owners_earnings(p)["oe"]
        print(f"{p.name:<12} OCF {fmt(p.ocf)}  - capex {fmt(p.capex)}"
              f"  - after-tax interest {fmt(after_tax_interest)}"
              f"  = op.FCF {fmt(fcf)}   vs OE {fmt(oe)}   "
              f"cash conv. {fcf/oe*100:>6.0f}%")
    print("4-yr cumulative FY2022-FY2025:")
    cum_fcf = sum(p.ocf - p.capex - p.interest_income * (1 - TAX_RATE)
                  for p in [FY2022, FY2023, FY2024, FY2025])
    cum_oe = sum(owners_earnings(p)["oe"] for p in [FY2022, FY2023, FY2024, FY2025])
    print(f"   cumulative operating FCF {fmt(cum_fcf)} vs cumulative OE {fmt(cum_oe)}"
          f"  -> {cum_fcf/cum_oe*100:.0f}%")

    print()
    print("=" * 100)
    print("INVESTED CAPITAL AND ROIC")
    print("=" * 100)
    print(hdr)
    ic_rows = [
        ("Operating cash (1 month of cash opex)", lambda p: invested_capital(p)["op_cash"]),
        ("+ Trade and other receivables", lambda p: p.receivables),
        ("+ Prepaid expenses", lambda p: p.prepaid),
        ("+ Property and equipment", lambda p: p.ppe),
        ("- Trade and other payables", lambda p: -p.payables),
        ("- Deferred revenue", lambda p: -p.deferred_revenue),
        ("+ Capitalised office lease (as disclosed)", lambda p: p.lease_commitment),
        ("= INVESTED CAPITAL (period end)", lambda p: invested_capital(p)["ic"]),
    ]
    for label, fn in ic_rows:
        print(f"{label:<42}" + "".join(fmt(fn(p)) for p in PERIODS))
    print(f"{'Memo: excess cash + ST investments':<42}"
          + "".join(fmt(p.cash + p.st_investments - invested_capital(p)["op_cash"]) for p in PERIODS))

    print()
    print(f"{'ROIC on period-end IC':<42}"
          + "".join(f"{owners_earnings(p)['oe']/invested_capital(p)['ic']*100:>13.0f}%"
                    for p in PERIODS))
    print(f"{'ROIC on 2-pt average IC':<42}" + f"{'n/a':>14}"
          + "".join(f"{owners_earnings(b)['oe']/((invested_capital(a)['ic']+invested_capital(b)['ic'])/2)*100:>13.0f}%"
                    for a, b in zip(PERIODS[:-1], PERIODS[1:])))

    print()
    print("Incremental ROIC, FY2022 -> FY2025 (period-end IC):")
    d_oe = owners_earnings(FY2025)["oe"] - owners_earnings(FY2022)["oe"]
    d_ic = invested_capital(FY2025)["ic"] - invested_capital(FY2022)["ic"]
    print(f"   delta OE {fmt(d_oe)}   delta IC {fmt(d_ic)}   incremental ROIC "
          f"{d_oe/d_ic*100:,.0f}%")

    print()
    print("=" * 100)
    print("SENSITIVITIES ON FY2025 ROIC")
    print("=" * 100)
    oe25 = owners_earnings(FY2025)["oe"]
    base_ic = invested_capital(FY2025)["ic"]
    scen = [
        ("Base: 1 month operating cash", base_ic),
        ("Zero operating cash", base_ic - invested_capital(FY2025)["op_cash"]),
        ("3 months operating cash", invested_capital(FY2025, 3.0)["ic"]),
        ("Note 12 policy, broad reading: 6 mths TOTAL cash opex",
         invested_capital(FY2025, 6.0)["ic"]),
        ("Note 12 policy, literal reading: 6 mths of the G&A line only",
         base_ic - invested_capital(FY2025)["op_cash"] + FY2025.gna / 2),
        ("Base + $1.1M termination commitment", base_ic + 1_100_000),
        ("Base + 3 yrs of ALL COGS compensation capitalised (upper bound)",
         base_ic + (1_739_266 + 1_690_129 + 1_690_129)),
    ]
    for label, ic in scen:
        print(f"  {label:<62} IC {fmt(ic)}   ROIC {oe25/ic*100:>8.0f}%")

    print()
    print("=" * 100)
    print("PER-SHARE (FY2025 and TTM)")
    print("=" * 100)
    for p, dil in [(FY2025, 27_601_426), (TTM, 27_498_422)]:
        oe = owners_earnings(p)["oe"]
        print(f"  {p.name:<12} OE {fmt(oe)}  / diluted shares {dil:,}"
              f"  = ${oe/dil:.3f} per diluted share")
    net_cash_25 = 846_423 + 9_329_249
    net_cash_ttm = 940_082 + 6_425_965
    print(f"  Net cash Oct-31-25 {fmt(net_cash_25)} = ${net_cash_25/27_601_426:.2f}/dil. sh")
    print(f"  Net cash Apr-30-26 {fmt(net_cash_ttm)} = ${net_cash_ttm/27_498_422:.2f}/dil. sh")

    print()
    print("=" * 100)
    print("GROWTH / DSO DIAGNOSTICS")
    print("=" * 100)
    for p in PERIODS:
        print(f"  {p.name:<12} revenue {fmt(p.revenue)}   "
              f"trade+other receivables {fmt(p.receivables)}   "
              f"DSO(on total rev) {p.receivables/p.revenue*365:>5.1f} days   "
              f"IC as % of revenue {invested_capital(p)['ic']/p.revenue*100:>5.1f}%")
    for a, b in zip(PERIODS[:-1], PERIODS[1:]):
        print(f"  {a.name} -> {b.name}: revenue growth "
              f"{(b.revenue/a.revenue-1)*100:>5.1f}%,  OE growth "
              f"{(owners_earnings(b)['oe']/owners_earnings(a)['oe']-1)*100:>5.1f}%")

    print()
    print("=" * 100)
    print("FIGURES QUOTED IN THE WRITE-UP PROSE")
    print("=" * 100)
    oe22, oe25 = owners_earnings(FY2022)["oe"], owners_earnings(FY2025)["oe"]
    print(f"  OE CAGR FY2022->FY2025                 : {((oe25/oe22)**(1/3)-1)*100:.1f}%")
    print(f"  Revenue CAGR FY2022->FY2025            : {((FY2025.revenue/FY2022.revenue)**(1/3)-1)*100:.1f}%")
    print(f"  TTM FX loss, after tax                 : {TTM.fx_gain*(1-TAX_RATE):,.0f}")
    print(f"  TTM OE if FX loss were included        : {owners_earnings(TTM)['oe']+TTM.fx_gain*(1-TAX_RATE):,.0f}")
    print(f"  TTM SBC normalisation, pre-tax         : {NORM_SBC-TTM.sbc:,.0f}")
    for p_ in (FY2025, TTM):
        d = p_.bad_debt - NORM_BAD_DEBT
        print(f"  Bad debt normalisation {p_.name:<11}, pre-tax : {d:>+9,.0f}  "
              f"({'raises' if d > 0 else 'reduces'} owners' earnings)")
    print(f"  Trade-receivable DSO FY2025 (1,164,580): {1_164_580/FY2025.revenue*365:.1f} days")
    print(f"  Trade-receivable DSO FY2024 (  857,096): {857_096/FY2024.revenue*365:.1f} days")
    print(f"  H1-26 vs H1-25 COGS compensation       : {(1_016_795/844_523-1)*100:.1f}%")
    print(f"  H1-26 vs H1-25 revenue                 : {(4_267_406/3_951_863-1)*100:.1f}%")
    print(f"  H1 gross margin 2026 / 2025            : {2_671_269/4_267_406*100:.1f}% / {2_587_305/3_951_863*100:.1f}%")
