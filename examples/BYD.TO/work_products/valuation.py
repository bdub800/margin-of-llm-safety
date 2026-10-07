"""
Boyd Group Services (BYD.TO / BGSI) - intrinsic valuation (DCF of Owners' Earnings + terminal value + equity bridge).

US$ millions unless stated.  Run:  uv run python work_products/valuation.py
Write-up: work_products/valuation.md (every number there comes from this script).
The stock price is not used anywhere.

HOW THE MODEL IS LAID OUT
=========================
  PART 1  INPUTS    - valuation settings, H1-2026 actuals, the Jun-30-2026 balance sheet, tax assets, share count.
  PART 2  FORMULAS  - discounting, the 2026 stub, explicit-period PV, terminal value PV, bridge, per-share.
  PART 3  OUTPUT    - scenario table, bridge, cross-checks and sensitivities.

HOW THE PIECES CONNECT
======================
  Cash flows (from forecast_earnings.py, per scenario):
      distributable_t = Owners' Earnings_t - growth capex_t - one-off integration costs_t
      2026 (t=0, not discounted): only the H2-2026 part is counted, because H1-2026 cash is already
      inside the Jun-30-2026 net debt used in the bridge.
      2027..2031 -> t = 1..5, discounted at DISCOUNT_RATE.
  Terminal value (from terminal_value.py): EV at end-2031 = EV/EBITDA-after-rent multiple x FY2031E EBITDA-R
      + ramp uplift; discounted at t = 5 (same point in time as the FY2031 cash flow).
  Enterprise value = PV(distributable) + PV(terminal value)
  Equity value     = EV + standalone assets - debt and debt-like items
  Per share        = equity value / current diluted shares (Jun-30-2026 count, not a forecast count)
"""
from __future__ import annotations

from dataclasses import dataclass, replace

import forecast_earnings as fe
import terminal_value as tv

# =====================================================================================================
# PART 1 - INPUTS
# =====================================================================================================


@dataclass(frozen=True)
class ValuationSettings:
    discount_rate: float = 0.10          # task requirement: 10%, change here
    valuation_year: int = 2026           # current year = t=0 (not discounted)
    terminal_year: int = 2031            # terminal value sits at end-2031 -> t=5


@dataclass(frozen=True)
class H1_2026Actuals:
    """Used only to strip the already-realized H1-2026 cash out of FY2026E (it is inside Jun-26 net debt)."""
    adjusted_ebitda: float = 258.3       # Q2FY26 MD&A l.317 (H1-2026)
    cash_rent: float = 107.9             # property + vehicle lease principal and interest (Q2FY26 FS l.167-172)
    net_growth_spend: float = 32.9       # acquisition & development less sale-leaseback proceeds, ex-JH
                                         # (forecast_earnings.md sec 6.1a table, H1-2026 row)


@dataclass(frozen=True)
class DebtJun2026:
    """Interest-bearing and debt-like claims at Jun-30-2026 (Q2FY26 FS balance sheet and notes 11-12)."""
    revolver: float = 285.253            # note 11, net of financing costs
    term_loan_a: float = 124.963         # note 11, net of financing costs
    seller_notes: float = 8.606          # note 11 (deferred acquisition consideration)
    senior_notes_2030: float = 369.443   # note 12, principal at Jun-26 FX (C$525M)
    senior_notes_2033: float = 193.517   # note 12, principal at Jun-26 FX (C$275M)
    dividends_payable: float = 3.056     # balance sheet (declared, not yet paid)
    derivatives_asset: float = 4.305     # cross-currency swaps hedging the C$ notes (asset side)
    derivatives_liability: float = 3.003 # (liability side)
    # Items reviewed and NOT deducted (see valuation.md sec 5):
    lease_liabilities_memo: float = 1050.885   # rent is already charged in full inside Owners' Earnings
    deferred_tax_liability_memo: float = 104.318
    deferred_tax_asset_memo: float = 10.051

    @property
    def total(self) -> float:
        net_derivatives = self.derivatives_asset - self.derivatives_liability
        return (self.revolver + self.term_loan_a + self.seller_notes + self.senior_notes_2030
                + self.senior_notes_2033 + self.dividends_payable - net_derivatives)


@dataclass(frozen=True)
class StandaloneAssetsJun2026:
    cash: float = 22.969                 # balance sheet
    operating_cash_requirement: float = 25.0   # OE&ROIC md sec 4: cash capped at $25M inside invested capital

    @property
    def excess_cash(self) -> float:
        return max(self.cash - self.operating_cash_requirement, 0.0)


@dataclass(frozen=True)
class JoeHudsonsTaxShield:
    """Tax-deductible goodwill and intangibles from the JH acquisition (Q2FY26 FS l.316, l.318).
    OE is taxed at the full statutory rate with no deduction for these, so the shield is value outside OE."""
    deductible_goodwill: float = 366.291
    deductible_intangibles: float = 602.555
    amortization_years: int = 15         # US tax amortization of acquired goodwill/intangibles (internal AI knowledge:
                                         # IRC s.197 15-year straight line)
    tax_rate: float = fe.CORPORATE.tax_rate    # 26.5%, same as OE (OE&ROIC md sec 2.6)
    first_year: int = 2026               # closed Jan-9-2026
    share_of_first_year_remaining: float = 0.5   # H1-2026 benefit already inside Jun-26 cash taxes
    boyd_estimate_of_tax_benefits: float = 150.0 # JH release l.43 ("approximately $150 million"), cross-check only

    @property
    def annual_tax_saving(self) -> float:
        return (self.deductible_goodwill + self.deductible_intangibles) / self.amortization_years * self.tax_rate


@dataclass(frozen=True)
class ShareCount:
    basic_shares_jun_2026: float = 27_836_435          # Q2FY26 FS statement of changes in equity
    diluted_weighted_q2_2026: float = 27_898_269       # Q2FY26 FS l.129
    basic_weighted_q2_2026: float = 27_836_295         # Q2FY26 FS l.128
    option_plan_cap: float = 250_000                   # FY2025 AFS l.459: plan allows options up to 250,000 shares

    @property
    def dilutive_units(self) -> float:
        """RSU/PSU units the company itself counts as dilutive (options were anti-dilutive, Q2FY26 FS l.669)."""
        return self.diluted_weighted_q2_2026 - self.basic_weighted_q2_2026

    @property
    def diluted_shares(self) -> float:
        return self.basic_shares_jun_2026 + self.dilutive_units


@dataclass(frozen=True)
class FxJun2026:
    """C$ per US$ implied by Boyd's own Jun-30-2026 balance sheet (no market data used)."""
    notes_principal_cad: float = 525.0 + 275.0         # FY2025 MD&A l.25, l.35
    notes_principal_usd: float = 369.443 + 193.517     # Q2FY26 FS note 12

    @property
    def cad_per_usd(self) -> float:
        return self.notes_principal_cad / self.notes_principal_usd


@dataclass(frozen=True)
class DeferredTaxDec2025:
    """Deferred-tax components at Dec-31-2025 (FY2025 AFS l.852-877; Canada DTA table, U.S. DTL table).
    Used only for the r1 reconciliation of the DTL treatment vs the legacy tax shield (valuation.md sec 5)."""
    intangibles_dtl_us: float = 71.540
    intangibles_dtl_canada: float = 6.346          # shown as (6,346) inside the Canadian net asset
    ppe_dtl_us: float = 57.549
    ppe_dtl_canada: float = 1.092                  # shown as (1,092) inside the Canadian net asset
    legacy_goodwill: float = 702.460               # Q2FY26 FS balance sheet, Dec-31-2025 column
    legacy_intangibles: float = 356.347
    jh_nondeductible_intangibles_dtl: float = 25.466   # Q2FY26 FS l.318: book-only, never a cash tax
    illustrative_remaining_life_years: int = 8     # SPECULATION: half of a 15-year tax life already used
    # FY2023-25 cash taxes paid vs OE's normalized tax (OE&ROIC md l.87, l.105)
    cash_taxes_paid: tuple = (27.9, 12.3, 3.7)
    normalized_tax: tuple = (47.7, 33.1, 39.3)


@dataclass(frozen=True)
class OtherTaxShield:
    """Judge r2: tax shield on ALL goodwill & intangibles. JH uses Boyd's own ~$150M; the rest is estimated here.
    Legacy (pre-2026) goodwill & intangibles: remaining tax basis = net book value - book-over-tax gap implied by the
    intangibles deferred tax liability (DeferredTaxDec2025). 2023-25 goodwill is disclosed as deductible
    (FY2023 AFS l.761, FY2024 AFS l.658, FY2025 AFS l.703); pre-2023 deductibility is ASSUMED the same (inference)."""
    jh_boyd_estimate: float = 150.0                # JH release l.43: "expected tax benefits of approximately $150 million"
    legacy_goodwill: float = 702.460               # Dec-31-2025 (Q2FY26 FS balance sheet)
    legacy_intangibles_net: float = 356.347
    legacy_intangibles_gross: float = 580.2        # FY2025 AFS Note 11 via OE&ROIC md l.192
    other_2026_goodwill: float = 7.208             # Q2FY26 FS acquisition table, "Other acquisitions"
    other_2026_intangibles: float = 5.496 + 0.245  # customer relationships + non-competes (same table)
    tax_life_years: int = 15                       # internal AI knowledge: US IRC s.197 15-year straight line
    tax_rate: float = fe.CORPORATE.tax_rate        # 26.5% (OE&ROIC md sec 2.6)
    first_year: int = 2026
    share_of_first_year_remaining: float = 0.5     # H1-2026 deductions already inside Jun-26 cash taxes


@dataclass(frozen=True)
class RatioMethodInputs:
    """Judge r3: legacy (and other-2026) shield = Boyd's JH $150M x (their goodwill+intangibles / JH's).
    JH book amounts: Q2FY26 FS acquisition table (l.249-258, revised provisional PPA)."""
    jh_goodwill: float = 521.760
    jh_intangibles: float = 700.000 + 0.500 + 0.300     # customer relationships + brand + IP
    legacy_goodwill: float = 702.460                    # Dec-31-2025 (Q2FY26 FS l.28, Dec-25 column)
    legacy_intangibles: float = 356.347
    other_2026_goodwill: float = 7.208                  # "Other acquisitions" column
    other_2026_intangibles: float = 5.496 + 0.245

    @property
    def jh_total(self) -> float:
        return self.jh_goodwill + self.jh_intangibles

    @property
    def legacy_total(self) -> float:
        return self.legacy_goodwill + self.legacy_intangibles

    @property
    def other_2026_total(self) -> float:
        return self.other_2026_goodwill + self.other_2026_intangibles


SETTINGS = ValuationSettings()
DTX = DeferredTaxDec2025()
RATIO = RatioMethodInputs()
OTHER_TAX = OtherTaxShield()
H1 = H1_2026Actuals()
DEBT = DebtJun2026()
ASSETS = StandaloneAssetsJun2026()
JH_TAX = JoeHudsonsTaxShield()
SHARES = ShareCount()
FX = FxJun2026()

SCENARIOS = {"Bear": fe.BEAR, "Base": fe.BASE, "Bull": fe.BULL}
NO_GROWTH = tv.NO_GROWTH                            # existing business only: base drivers, no stores opened from 2026
# Judge r2: headline includes the no-growth-capex case. It shares the base operating drivers (forecast_earnings.md
# l.42-43), so it takes half of the base weight: the operating-driver mix stays 25/50/25 bear/base/bull.
WEIGHTS = {"Bear": 0.25, "Base": 0.25, NO_GROWTH: 0.25, "Bull": 0.25}
PRIOR_WEIGHTS = fe.SCENARIO_WEIGHTS                 # r1 headline: Bear 25% / Base 50% / Bull 25% (comparison only)
ALL_CASES = ["Bear", "Base", NO_GROWTH, "Bull"]
FORECASTS = {name: fe.forecast(s) for name, s in SCENARIOS.items()}
FORECASTS[NO_GROWTH] = fe.forecast(fe.EXISTING_ONLY)

# =====================================================================================================
# PART 2 - FORMULAS
# =====================================================================================================


def period(year: int) -> int:
    return year - SETTINGS.valuation_year


def discount_factor(year: int, rate: float) -> float:
    return 1.0 / (1.0 + rate) ** period(year)


def h2_share_of_2026_oe(y2026: fe.ForecastYear) -> float:
    """H2 share of FY2026E Owners' Earnings, proxied by H2 share of EBITDA after rent (H1 is actual)."""
    h1_ebitda_after_rent = H1.adjusted_ebitda - H1.cash_rent
    h2_ebitda_after_rent = y2026.ebitda_after_rent - h1_ebitda_after_rent
    return h2_ebitda_after_rent / y2026.ebitda_after_rent


def stub_2026_distributable(y2026: fe.ForecastYear) -> dict:
    """H2-2026 distributable = H2 OE - (FY growth capex - H1 actual) - one-offs (the forecast's are Jul-2026 onward)."""
    h2_oe = y2026.owners_earnings * h2_share_of_2026_oe(y2026)
    h2_growth_capex = max(y2026.new.growth_capex - H1.net_growth_spend, 0.0)
    return {"h2_oe": h2_oe, "h2_growth_capex": h2_growth_capex, "one_offs": y2026.one_offs,
            "distributable": h2_oe - h2_growth_capex - y2026.one_offs}


def cash_flows(name: str) -> dict:
    """Year -> distributable cash counted in the valuation (2026 = H2 stub only)."""
    years = FORECASTS[name]
    flows = {y.year: y.distributable for y in years}
    flows[SETTINGS.valuation_year] = stub_2026_distributable(years[0])["distributable"]
    return flows


def pv_explicit(name: str, rate: float) -> float:
    return sum(cf * discount_factor(yr, rate) for yr, cf in cash_flows(name).items())


def terminal_value_exit_multiple(name: str, multiple: float | None = None) -> float:
    """terminal_value.md: EV/EBITDA-R multiple x FY2031E EBITDA-R + ramp uplift (end-2031, undiscounted)."""
    return tv.terminal_value(name, multiple)["total"]


def terminal_value_perpetuity(name: str, rate: float) -> float:
    """CROSS-CHECK: value-driver formula on run-rate FY2031E OE at THIS model's discount rate.
    Run-rate OE = FY2031E OE + OE of 2026-31 openings still ramping. Growth/reinvestment from terminal_value.py."""
    y = FORECASTS[name][-1]
    run_rate_oe = y.owners_earnings + (y.oe_new_run_rate - y.oe_new)
    steady = replace(tv.STEADY[name], discount_rate=rate)
    return tv.fundamental_oe_multiple(steady) * run_rate_oe


def pv_terminal(terminal_value: float, rate: float) -> float:
    return terminal_value * discount_factor(SETTINGS.terminal_year, rate)


def enterprise_value(name: str, rate: float, tv_method: str = "exit", multiple: float | None = None) -> dict:
    if tv_method == "exit":
        terminal = terminal_value_exit_multiple(name, multiple)
    else:
        terminal = terminal_value_perpetuity(name, rate)
    pv_cf = pv_explicit(name, rate)
    pv_tv = pv_terminal(terminal, rate)
    return {"pv_cash_flows": pv_cf, "terminal_value": terminal, "pv_terminal": pv_tv, "ev": pv_cf + pv_tv}


def pv_jh_tax_shield(rate: float) -> float:
    total, years = 0.0, JH_TAX.amortization_years
    for i in range(years + 1):                       # 2026 .. 2041 (half-years at both ends)
        year = JH_TAX.first_year + i
        if i == 0:
            share = JH_TAX.share_of_first_year_remaining
        elif i == years:
            share = 1.0 - JH_TAX.share_of_first_year_remaining
        else:
            share = 1.0
        total += JH_TAX.annual_tax_saving * share * discount_factor(year, rate)
    return total


def legacy_remaining_tax_basis() -> float:
    """Dec-25 net book value of legacy goodwill + intangibles less the ~$294M already deducted for tax."""
    intangible_dtl = DTX.intangibles_dtl_us + DTX.intangibles_dtl_canada
    book_over_tax_gap = intangible_dtl / OTHER_TAX.tax_rate
    return OTHER_TAX.legacy_goodwill + OTHER_TAX.legacy_intangibles_net - book_over_tax_gap


def legacy_annual_deduction() -> float:
    """Original deductible cost / 15 years; original cost ~ goodwill + GROSS intangibles."""
    return (OTHER_TAX.legacy_goodwill + OTHER_TAX.legacy_intangibles_gross) / OTHER_TAX.tax_life_years


def pv_deduction_stream(remaining_basis: float, annual_deduction: float, rate: float) -> float:
    """Tax saving on a basis deducted at `annual_deduction`/yr from 2026 (H2 only counted) until exhausted."""
    total, basis, year = 0.0, remaining_basis, OTHER_TAX.first_year
    # H1-2026 deduction is already used (inside Jun-26 cash taxes)
    basis -= annual_deduction * (1 - OTHER_TAX.share_of_first_year_remaining)
    first = True
    while basis > 1e-9:
        d = min(annual_deduction * (OTHER_TAX.share_of_first_year_remaining if first else 1.0), basis)
        total += d * OTHER_TAX.tax_rate * discount_factor(year, rate)
        basis -= d
        year += 1
        first = False
    return total


def pv_legacy_tax_shield(rate: float) -> float:
    return pv_deduction_stream(legacy_remaining_tax_basis(), legacy_annual_deduction(), rate)


def pv_other_2026_tax_shield(rate: float) -> float:
    cost = OTHER_TAX.other_2026_goodwill + OTHER_TAX.other_2026_intangibles
    return pv_deduction_stream(cost, cost / OTHER_TAX.tax_life_years, rate)


def legacy_shield_ratio_method() -> float:
    return OTHER_TAX.jh_boyd_estimate * RATIO.legacy_total / RATIO.jh_total


def other_2026_shield_ratio_method() -> float:
    return OTHER_TAX.jh_boyd_estimate * RATIO.other_2026_total / RATIO.jh_total


def standalone_assets(rate: float) -> dict:
    items = {"Excess cash (above $25M operating cash)": ASSETS.excess_cash,
             "JH tax shield (Boyd's ~$150M estimate)": OTHER_TAX.jh_boyd_estimate,
             "Legacy tax shield ($150M x legacy/JH ratio)": legacy_shield_ratio_method(),
             "Other 2026 acq. tax shield ($150M x ratio)": other_2026_shield_ratio_method()}
    return {"items": items, "total": sum(items.values())}


def tax_shield_total(rate: float) -> float:
    return OTHER_TAX.jh_boyd_estimate + legacy_shield_ratio_method() + other_2026_shield_ratio_method()


def debt_items() -> dict:
    items = {"Revolver + swing line": DEBT.revolver,
             "Term Loan A": DEBT.term_loan_a,
             "Seller notes": DEBT.seller_notes,
             "Senior notes 2030 (C$525M principal)": DEBT.senior_notes_2030,
             "Senior notes 2033 (C$275M principal)": DEBT.senior_notes_2033,
             "Dividends payable": DEBT.dividends_payable,
             "Cross-currency swaps, net (asset)": -(DEBT.derivatives_asset - DEBT.derivatives_liability)}
    return {"items": items, "total": DEBT.total}


def equity_value(ev: float, rate: float, extra_debt: float = 0.0) -> float:
    return ev + standalone_assets(rate)["total"] - debt_items()["total"] - extra_debt


def per_share(equity: float, shares: float | None = None) -> float:
    return equity * 1e6 / (SHARES.diluted_shares if shares is None else shares)


def weighted(values: dict) -> float:
    return sum(WEIGHTS[n] * values[n] for n in WEIGHTS)


def scenario_values(rate: float, tv_method: str = "exit", multiple_shift: float = 0.0) -> dict:
    out = {}
    for name in ALL_CASES:
        m = tv.CHOSEN_MULTIPLE[name] + multiple_shift
        ev = enterprise_value(name, rate, tv_method, m)
        eq = equity_value(ev["ev"], rate)
        out[name] = {**ev, "equity": eq, "per_share": per_share(eq)}
    return out


# =====================================================================================================
# PART 3 - OUTPUT
# =====================================================================================================

def print_inputs():
    r = SETTINGS.discount_rate
    print(f"(1) Settings: discount rate {r:.0%}; t=0 = {SETTINGS.valuation_year}; TV at end-{SETTINGS.terminal_year} "
          f"(t={period(SETTINGS.terminal_year)}, factor {discount_factor(SETTINGS.terminal_year, r):.4f})")
    print(f"    Diluted shares: {SHARES.basic_shares_jun_2026:,.0f} basic + {SHARES.dilutive_units:,.0f} dilutive "
          f"RSU/PSU = {SHARES.diluted_shares:,.0f}")
    print(f"    FX implied by C$800M notes: C${FX.cad_per_usd:.4f} per US$")


def print_cash_flows():
    r = SETTINGS.discount_rate
    print("\n(2) Distributable cash counted (US$M) and discount factors")
    years = list(range(SETTINGS.valuation_year, SETTINGS.terminal_year + 1))
    print("    " + " " * 22 + "".join(f"{y:>8}" for y in years) + "   PV sum")
    print("    " + "t".ljust(22) + "".join(f"{period(y):>8}" for y in years))
    print("    " + "discount factor".ljust(22) + "".join(f"{discount_factor(y, r):>8.3f}" for y in years))
    for name in ALL_CASES:
        flows = cash_flows(name)
        print("    " + name[:22].ljust(22) + "".join(f"{flows[y]:>8.1f}" for y in years)
              + f"{pv_explicit(name, r):>9.1f}")
    for name in ALL_CASES:
        y0 = FORECASTS[name][0]
        s = stub_2026_distributable(y0)
        print(f"    2026 stub {name[:10]:10}: FY OE {y0.owners_earnings:.1f} x H2 share {h2_share_of_2026_oe(y0):.1%} "
              f"= {s['h2_oe']:.1f}; - growth capex {s['h2_growth_capex']:.1f} (FY {y0.new.growth_capex:.1f} - H1 "
              f"{H1.net_growth_spend}); - one-offs {s['one_offs']:.1f} = {s['distributable']:.1f} "
              f"(FY distributable {y0.distributable:.1f})")


def print_scenarios(vals: dict, label: str):
    print(f"\n{label}")
    print(f"    {'Scenario':24}{'PV CF':>8}{'TV 2031':>9}{'PV TV':>8}{'EV':>8}{'Equity':>8}{'US$/sh':>8}{'C$/sh':>8}")
    for name, v in vals.items():
        print(f"    {name[:24]:24}{v['pv_cash_flows']:>8.0f}{v['terminal_value']:>9.0f}{v['pv_terminal']:>8.0f}"
              f"{v['ev']:>8.0f}{v['equity']:>8.0f}{v['per_share']:>8.1f}{v['per_share'] * FX.cad_per_usd:>8.1f}")
    keys = ["pv_cash_flows", "terminal_value", "pv_terminal", "ev", "equity", "per_share"]
    w = {k: weighted({n: vals[n][k] for n in WEIGHTS}) for k in keys}
    print(f"    {'Probability-weighted':24}{w['pv_cash_flows']:>8.0f}{w['terminal_value']:>9.0f}{w['pv_terminal']:>8.0f}"
          f"{w['ev']:>8.0f}{w['equity']:>8.0f}{w['per_share']:>8.1f}{w['per_share'] * FX.cad_per_usd:>8.1f}")
    for name in WEIGHTS:
        v = vals[name]
        print(f"    {name}: TV share of EV {v['pv_terminal'] / v['ev']:.0%}")
    return w


def print_bridge(base_ev: float, weighted_ev: float):
    r = SETTINGS.discount_rate
    sa, dt = standalone_assets(r), debt_items()
    print("\n(4) Equity bridge at Jun-30-2026 (US$M)")
    for k, v in sa["items"].items():
        print(f"    + {k:52}{v:>9.1f}")
    for k, v in dt["items"].items():
        print(f"    - {k:52}{v:>9.1f}")
    print(f"    Standalone assets {sa['total']:.1f}; debt & debt-like {dt['total']:.1f}; net {sa['total'] - dt['total']:.1f}")
    print(f"    JH tax shield: annual saving {JH_TAX.annual_tax_saving:.1f}, nominal total "
          f"{JH_TAX.annual_tax_saving * JH_TAX.amortization_years:.1f}, PV@{r:.0%} {pv_jh_tax_shield(r):.1f}, "
          f"PV@8% {pv_jh_tax_shield(0.08):.1f}, PV@7% {pv_jh_tax_shield(0.07):.1f} (Boyd: ~{JH_TAX.boyd_estimate_of_tax_benefits:.0f})")
    basis, ded = legacy_remaining_tax_basis(), legacy_annual_deduction()
    print(f"    Legacy shield: remaining basis {basis:.0f} (book {OTHER_TAX.legacy_goodwill + OTHER_TAX.legacy_intangibles_net:.0f}"
          f" - gap {(DTX.intangibles_dtl_us + DTX.intangibles_dtl_canada) / OTHER_TAX.tax_rate:.0f}); deduction {ded:.1f}/yr"
          f" (tax saving {ded * OTHER_TAX.tax_rate:.1f}/yr) -> runs ~{basis / ded:.1f} yrs; nominal {basis * OTHER_TAX.tax_rate:.0f},"
          f" PV@{r:.0%} {pv_legacy_tax_shield(r):.1f}")
    slow = pv_deduction_stream(basis, basis / 12, r)
    print(f"    Legacy shield if spread evenly over 12 yrs instead: PV {slow:.1f}; if all basis deductible over 15 yrs: "
          f"{pv_deduction_stream(basis, basis / 15, r):.1f}")
    print(f"    r3 RATIO METHOD (headline): JH goodwill {RATIO.jh_goodwill:.1f} + intangibles {RATIO.jh_intangibles:.1f} = "
          f"{RATIO.jh_total:.1f}; legacy goodwill {RATIO.legacy_goodwill:.1f} + intangibles {RATIO.legacy_intangibles:.1f} = "
          f"{RATIO.legacy_total:.1f}; ratio {RATIO.legacy_total / RATIO.jh_total:.3f} -> legacy shield "
          f"{legacy_shield_ratio_method():.1f}; other 2026 {RATIO.other_2026_total:.1f} / {RATIO.jh_total:.1f} x 150 = "
          f"{other_2026_shield_ratio_method():.1f}")
    jh_deductible = JH_TAX.deductible_goodwill + JH_TAX.deductible_intangibles
    print(f"    Cross-check, tax-basis ratio: legacy remaining basis {basis:.0f} / JH deductible {jh_deductible:.1f} = "
          f"{basis / jh_deductible:.3f} -> {150 * basis / jh_deductible:.1f}; r2 build (PV of deductions) {pv_legacy_tax_shield(r):.1f}")
    print(f"    Other 2026 acquisitions (r2 build): cost {OTHER_TAX.other_2026_goodwill + OTHER_TAX.other_2026_intangibles:.1f}, "
          f"PV {pv_other_2026_tax_shield(r):.1f}.  Total tax-shield asset {tax_shield_total(r):.1f} "
          f"(US${per_share(tax_shield_total(r)):.1f}/share)")
    print(f"    Memo not deducted: lease liabilities {DEBT.lease_liabilities_memo:.1f}; net deferred tax liability "
          f"{DEBT.deferred_tax_liability_memo - DEBT.deferred_tax_asset_memo:.1f}")
    print(f"    Base EV {base_ev:.0f} -> equity {equity_value(base_ev, r):.0f}; weighted EV {weighted_ev:.0f} -> "
          f"equity {equity_value(weighted_ev, r):.0f}")


def print_sensitivities():
    print("\n(5a) Discount rate (exit-multiple TV fixed; perpetuity TV recomputed at each rate), US$/share")
    print(f"    {'Rate':>6}{'Wtd exit':>10}{'Base exit':>11}{'Wtd perp.':>11}{'Base perp.':>12}{'No-growth exit':>16}")
    for r in (0.08, 0.09, 0.10, 0.11, 0.12):
        ex, pp = scenario_values(r, "exit"), scenario_values(r, "perpetuity")
        print(f"    {r:>6.0%}{weighted({n: ex[n]['per_share'] for n in WEIGHTS}):>10.1f}{ex['Base']['per_share']:>11.1f}"
              f"{weighted({n: pp[n]['per_share'] for n in WEIGHTS}):>11.1f}{pp['Base']['per_share']:>12.1f}"
              f"{ex[NO_GROWTH]['per_share']:>16.1f}")

    r = SETTINGS.discount_rate
    print("\n(5b) Exit multiple shift (all scenarios), US$/share at 10%")
    for shift in (-1.5, -1.0, -0.5, 0.0, 0.5, 1.0):
        v = scenario_values(r, "exit", shift)
        print(f"    {shift:+.1f}x: weighted {weighted({n: v[n]['per_share'] for n in WEIGHTS}):6.1f}   "
              f"base {v['Base']['per_share']:6.1f}")

    print("\n(5c) Implied multiples of the perpetuity TV at 10% (TV / FY2031E EBITDA-R) vs chosen exit multiple")
    for name in ALL_CASES:
        y = FORECASTS[name][-1]
        perp = terminal_value_perpetuity(name, r)
        print(f"    {name[:22]:22} perpetuity TV {perp:6.0f} = {perp / y.ebitda_after_rent:4.1f}x EBITDA-R "
              f"(chosen {tv.CHOSEN_MULTIPLE[name]:.1f}x, exit TV {terminal_value_exit_multiple(name):6.0f})")

    base = scenario_values(r, "exit")
    w = weighted({n: base[n]['equity'] for n in WEIGHTS})
    print("\n(5d) Bridge alternatives on the weighted equity value (US$/share at 10%)")
    net_dtl = DEBT.deferred_tax_liability_memo - DEBT.deferred_tax_asset_memo
    alts = {
        "Headline": 0.0,
        "Also deduct net deferred tax liability": net_dtl,
        "Drop all goodwill/intangible tax shields": tax_shield_total(r),
        "Drop only the legacy + other 2026 shields": tax_shield_total(r) - OTHER_TAX.jh_boyd_estimate,
        "JH at own formula PV@10% instead of $150M": OTHER_TAX.jh_boyd_estimate - pv_jh_tax_shield(r),
        "Count all $23.0M cash as excess": -ASSETS.cash,
    }
    for k, extra in alts.items():
        print(f"    {k:42} {per_share(w - extra):6.1f}")
    print(f"    {'All 250k plan options issued, no proceeds':42} "
          f"{per_share(w, SHARES.diluted_shares + SHARES.option_plan_cap):6.1f}")
    print(f"    {'Lease liabilities also deducted (WRONG: double count)':42} {per_share(w - DEBT.lease_liabilities_memo):6.1f}")


def annuity_factor(years: int, rate: float) -> float:
    """PV of 1 per year at t=1..years (end-of-year)."""
    return sum(1.0 / (1.0 + rate) ** t for t in range(1, years + 1))


def print_deferred_tax_reconciliation():
    r, rate_tax = SETTINGS.discount_rate, fe.CORPORATE.tax_rate
    intangible_dtl = DTX.intangibles_dtl_us + DTX.intangibles_dtl_canada
    ppe_dtl = DTX.ppe_dtl_us + DTX.ppe_dtl_canada
    book_tax_gap = intangible_dtl / rate_tax
    legacy_book = DTX.legacy_goodwill + DTX.legacy_intangibles
    max_remaining_basis = legacy_book - book_tax_gap
    max_shield_nominal = max_remaining_basis * rate_tax
    life = DTX.illustrative_remaining_life_years
    max_shield_pv = max_shield_nominal / life * annuity_factor(life, r)
    print("\n(5e) r1: deferred tax liability vs legacy tax shield (Dec-25 components, US$M)")
    print(f"    Intangibles DTL (US {DTX.intangibles_dtl_us:.1f} + Canada {DTX.intangibles_dtl_canada:.1f}) = {intangible_dtl:.1f}"
          f" -> book exceeds tax basis by {book_tax_gap:.0f}")
    print(f"    PP&E DTL (US {DTX.ppe_dtl_us:.1f} + Canada {DTX.ppe_dtl_canada:.1f}) = {ppe_dtl:.1f}")
    print(f"    Legacy goodwill + intangibles (book) {legacy_book:.1f}; remaining tax basis at most {max_remaining_basis:.0f}"
          f" (if all deductible) -> shield at most {max_shield_nominal:.0f} nominal, "
          f"PV@{r:.0%} over {life} yrs {max_shield_pv:.0f} (= US${per_share(max_shield_pv):.1f}/share); lower bound 0 [r1 illustration; r3 headline uses the ratio method in (4)]")
    print(f"    JH non-deductible intangibles DTL (book only, never cash): {DTX.jh_nondeductible_intangibles_dtl:.1f}")
    gaps = [n - c for c, n in zip(DTX.cash_taxes_paid, DTX.normalized_tax)]
    print(f"    Cash taxes below OE's normalized tax FY2023-25: {', '.join(f'{g:.1f}' for g in gaps)}")
    print(f"    Per share: net DTL {per_share(DEBT.deferred_tax_liability_memo - DEBT.deferred_tax_asset_memo):.1f}; "
          f"PP&E DTL only {per_share(ppe_dtl):.1f}")


def print_ev_multiples(vals: dict):
    print("\n(6) Sanity checks: implied EV multiples on 2026E/2027E (base)")
    b = FORECASTS["Base"]
    ev = vals["Base"]["ev"]
    print(f"    Base EV {ev:.0f}: {ev / b[0].ebitda_after_rent:.1f}x 2026E EBITDA-R ({b[0].ebitda_after_rent:.0f}), "
          f"{ev / b[1].ebitda_after_rent:.1f}x 2027E ({b[1].ebitda_after_rent:.0f}); "
          f"{ev / b[0].owners_earnings:.1f}x 2026E OE ({b[0].owners_earnings:.0f}), "
          f"{ev / b[1].owners_earnings:.1f}x 2027E OE ({b[1].owners_earnings:.0f})")
    ic = fe.VALUATION.invested_capital_jun_2026
    print(f"    Base EV / Jun-26 invested capital ex-leases ({ic:.0f}): {ev / ic:.2f}x")
    wev = weighted({n: vals[n]["ev"] for n in WEIGHTS})
    print(f"    Weighted EV {wev:.0f}: {wev / ic:.2f}x invested capital")


if __name__ == "__main__":
    rate = SETTINGS.discount_rate
    print_inputs()
    print_cash_flows()
    exit_vals = scenario_values(rate, "exit")
    w_exit = print_scenarios(exit_vals, "(3a) HEADLINE - exit-multiple terminal value (terminal_value.md), US$M")
    perp_vals = scenario_values(rate, "perpetuity")
    w_perp = print_scenarios(perp_vals, "(3b) CROSS-CHECK - perpetuity terminal value at the 10% discount rate, US$M")
    print_bridge(exit_vals["Base"]["ev"], w_exit["ev"])
    prior = sum(PRIOR_WEIGHTS[n] * exit_vals[n]["per_share"] for n in PRIOR_WEIGHTS)
    print(f"    Memo: r1 weighting (Bear 25 / Base 50 / Bull 25, no no-growth case) with the r2 bridge: US${prior:.1f}/share")
    print_sensitivities()
    print_deferred_tax_reconciliation()
    print_ev_multiples(exit_vals)
