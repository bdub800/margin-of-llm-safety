"""
Boyd Group Services (BYD.TO / BGSI) - are the new-location unit assumptions in forecast_earnings.py justified?

US$ millions.  Run:  uv run python work_products/unit_growth_capital_check.py
Write-up: work_products/forecast_earnings.md sec 6.1a (every number there on unit history / funding comes from here).

Back-of-envelope only.  Three questions:
  PART 1  HISTORY    - how many units did Boyd add, what growth rate was that, and what did it cost per unit?
  PART 2  RATES      - what unit growth % do the base-case 52 / 62-per-year counts imply, vs mgmt's 5-7% target?
  PART 3  FUNDING    - can the base case pay for its growth capex after interest and dividends, and what is left
                       for buybacks?  What happens to leverage if Boyd instead grows units at 5% or 7%/yr?
             (r1 additions: ex-lease net debt history 2022-24, and how much NCIB buyback H2-26/2027 could absorb
              if cash taxes stay below the statutory rate as in FY2023-25)
Nothing here feeds the forecast; it imports the forecast model and reads its outputs.
"""
from __future__ import annotations

from dataclasses import dataclass, replace

import forecast_earnings as fe


# =====================================================================================================
# PART 1 - HISTORY (inputs)
# =====================================================================================================

@dataclass(frozen=True)
class UnitYear:
    """One historical period of new-location growth."""
    period: str
    acquired: int                  # collision locations added through acquisition
    startups: int                  # start-up locations opened
    growth_spend: float            # cash flow line "Acquisition and development of businesses (net of cash acquired)"
    sale_leaseback: float          # "Proceeds on sale / leaseback agreements" (land/buildings recycled into leases)
    oe: float | None               # Owners' Earnings for the period (OE&ROIC md line 15); None if not a full year

    @property
    def units(self) -> int:
        return self.acquired + self.startups

    @property
    def net_growth_spend(self) -> float:
        """Growth spend net of sale-leaseback proceeds.  Comparable to the model's unit cost, because the model
        has no sale-leasebacks (start-ups are now developer-funded, FY2025 MD&A l.376)."""
        return self.growth_spend - self.sale_leaseback

    @property
    def net_spend_per_unit(self) -> float:
        return self.net_growth_spend / self.units


HISTORY = [
    # 2023: 78 + 28 (FY2023 MD&A l.33); cash flow lines FY2024 AFS l.291, 294
    UnitYear("2023", 78, 28, growth_spend=180.293, sale_leaseback=2.832, oe=132.4),
    # 2024: 37 + 12 (FY2024 MD&A l.43); FY2025 AFS l.310, 312
    UnitYear("2024", 37, 12, growth_spend=192.486, sale_leaseback=64.854, oe=91.8),
    # 2025: 43 + 27 (FY2025 MD&A l.45-51); FY2025 AFS l.310, 312
    UnitYear("2025", 43, 27, growth_spend=218.537, sale_leaseback=53.252, oe=108.9),
    # H1-2026: 3+8 and 4+6 (Q2FY26 MD&A l.55-56).  Cash line $1,354.8M less JH cash paid $1,304.8M
    # (Q2FY26 FS l.180, 261); sale-leasebacks Q2FY26 FS l.178
    UnitYear("H1-2026", 7, 14, growth_spend=1354.785 - 1304.764, sale_leaseback=17.157, oe=None),
]


@dataclass(frozen=True)
class LocationCounts:
    """Collision location counts."""
    end_2024: int = 984                    # Knowledge Store ID 10
    # 1,301 after JH less 258 JH locations (Knowledge Store ID 6); ties to Q1FY26 call l.71: 1,312 at Q1-26
    # = 1,043 + 258 + 3 acquisitions + 8 start-ups
    end_2025: int = 1301 - 258
    joe_hudsons: int = 258
    aug_11_2026: int = 1323                # Q2FY26 MD&A, location map (46 + 88 + 1,189), "net of one closed location"


COUNTS = LocationCounts()


@dataclass(frozen=True)
class ManagementTargets:
    # "3% to 5% ... from same-store sales growth and an additional 5% to 7% ... through the addition of new
    # locations over the long-term" (FY2025 MD&A l.91); restated as "5%-7% average annual unit growth over the
    # long term" (Q1FY26 call l.69), i.e. a UNIT growth target.
    new_location_growth_low: float = 0.05
    new_location_growth_high: float = 0.07
    startups_per_quarter_pipeline: tuple = (8, 10)     # FY2025 MD&A l.95; "8 or so a quarter" Q2FY26 call l.159
    startup_share_of_new_locations: float = 0.50       # "approximately 50% of new location growth" FY2025 MD&A l.95


TARGETS = ManagementTargets()


@dataclass(frozen=True)
class FundingInputs:
    # Marginal cost of extra debt if Boyd grew faster than the base case: the 5.5% senior notes coupon
    # (FY2025 AFS l.962).  Used only for the 5% / 7% variants below (ASSUMPTION: revolver cost is similar).
    marginal_debt_rate: float = 0.055
    leverage_target: float = 2.7           # JH release l.47: "return ... to current levels of 2.7x"


FUNDING = FundingInputs()


@dataclass(frozen=True)
class DebtAndTaxHistory:
    """For the reinvestment-history and NCIB checks (r1 response)."""
    # "Total debt, net of cash before lease liabilities" (excludes leases, same basis as the model's $953.1M)
    # end-2022 and end-2023: FY2023 MD&A l.432; end-2024: FY2024 MD&A l.350
    net_debt_ex_leases: tuple = (("end-2022", 345.103), ("end-2023", 399.194), ("end-2024", 487.286))
    # FY2023-25 cash taxes paid vs normalized 26.5% tax on pre-tax OE (OE&ROIC md l.87 and OE table)
    cash_taxes_paid: tuple = (27.9, 12.3, 3.7)
    normalized_taxes: tuple = (47.7, 33.1, 39.3)


DEBT_TAX = DebtAndTaxHistory()


# =====================================================================================================
# PART 2 - FORMULAS
# =====================================================================================================

def closures_2025() -> int:
    return COUNTS.end_2024 + HISTORY[2].units - COUNTS.end_2025


def opening_location_counts(new_units_by_year: list[int]) -> list[int]:
    """Locations at the start of each forecast year: end-2025 + JH, then + prior-year openings.
    Closures are ignored (2025 had some, see closures_2025), so these rates are GROSS unit growth."""
    counts = [COUNTS.end_2025 + COUNTS.joe_hudsons]
    for units in new_units_by_year[:-1]:
        counts.append(counts[-1] + units)
    return counts


def units_for_growth_rate(rate: float) -> tuple:
    """(tuck-ins, start-ups) per year that grow the unit count at `rate`, split 50/50 per mgmt.
    2026 is held at the base case (23 opened by Aug-11 plus 13 start-ups already scheduled)."""
    units = [fe.BASE.new_units[0]]
    count = COUNTS.end_2025 + COUNTS.joe_hudsons + sum(fe.BASE.new_units[0])
    for _ in fe.YEARS[1:]:
        total = round(rate * count)
        startups = round(total * TARGETS.startup_share_of_new_locations)
        units.append((total - startups, startups))
        count += total
    return tuple(units)


def after_tax_interest() -> float:
    return fe.after_tax(fe.FINANCING.cash_interest)


def cash_before_growth(y: fe.ForecastYear) -> float:
    """OE less one-offs, after-tax interest and dividends: what is left to fund growth, buybacks or debt paydown."""
    return y.owners_earnings - y.one_offs - after_tax_interest() - fe.FINANCING.dividends


def debt_capacity_at_target(results: list[fe.ForecastYear], i: int) -> float:
    """Extra debt Boyd could take in year i while holding leverage at the target: target x growth in
    (EBITDA - rent).  Only meaningful once leverage is at or below the target."""
    return FUNDING.leverage_target * (results[i].ebitda_after_rent - results[i - 1].ebitda_after_rent)


def variant_with_interest_on_extra_debt(variant: list[fe.ForecastYear], base: list[fe.ForecastYear]) -> list[float]:
    """fe.forecast holds interest flat at $60M.  For a faster-growth variant, add after-tax interest on the extra
    debt it carries vs the base case, compounding year by year.  Returns corrected leverage by year."""
    extra_debt = 0.0
    leverage = []
    for v, b in zip(variant, base):
        share_of_year = fe.FINANCING.share_of_2026_remaining if v.year == fe.FIRST_YEAR else 1.0
        extra_interest = fe.after_tax(extra_debt * FUNDING.marginal_debt_rate) * share_of_year
        extra_debt += (b.cash_after_financing - v.cash_after_financing) * share_of_year + extra_interest
        leverage.append((b.net_debt + extra_debt) / v.ebitda_after_rent)
    return leverage


# =====================================================================================================
# PART 3 - REPORT
# =====================================================================================================

def print_history():
    print("HISTORY: new collision locations and growth spend")
    print(f"{'Period':8}{'acq':>5}{'start':>6}{'total':>6}{'spend':>8}{'SLB':>7}{'net':>7}{'net/unit':>9}"
          f"{'OE':>7}{'net/OE':>8}")
    for h in HISTORY:
        oe = f"{h.oe:7.1f}{h.net_growth_spend / h.oe:8.0%}" if h.oe else f"{'':7}{'':8}"
        print(f"{h.period:8}{h.acquired:5}{h.startups:6}{h.units:6}{h.growth_spend:8.1f}{h.sale_leaseback:7.1f}"
              f"{h.net_growth_spend:7.1f}{h.net_spend_per_unit:9.2f}" + oe)
    pooled = sum(h.net_growth_spend for h in HISTORY) / sum(h.units for h in HISTORY)
    full_years = HISTORY[:3]
    print(f"Pooled 2023-H1'26 net spend per unit: {pooled:.2f}; avg units/yr 2023-25: "
          f"{sum(h.units for h in full_years) / 3:.0f} (acq {sum(h.acquired for h in full_years) / 3:.0f}, "
          f"start-ups {sum(h.startups for h in full_years) / 3:.0f})")
    print(f"Gross unit growth: 2024 {HISTORY[1].units}/(984-49 = {COUNTS.end_2024 - HISTORY[1].units}, before "
          f"2024 closures) = {HISTORY[1].units / (COUNTS.end_2024 - HISTORY[1].units):.1%}; "
          f"2025 {HISTORY[2].units}/{COUNTS.end_2024} = {HISTORY[2].units / COUNTS.end_2024:.1%} gross, "
          f"closures {closures_2025()}, net {(COUNTS.end_2025 - COUNTS.end_2024) / COUNTS.end_2024:.1%}")


def print_unit_rates(base: list[fe.ForecastYear]):
    units = [sum(u) for u in fe.BASE.new_units]
    opening = opening_location_counts(units)
    print("\nBASE CASE unit growth implied by the unit counts")
    print(f"{'Year':6}{'opening':>9}{'units':>7}{'unit %':>8}{'rev. added':>11}{'% prior sales':>14}"
          f"{'5% units':>9}{'7% units':>9}{'capex/unit':>11}")
    prior_sales = fe.BASE_YEAR.sales + fe.JOE_HUDSONS.pre_deal_sales   # 2025 pro-forma incl. JH TTM
    for year, y, n, count in zip(fe.YEARS, base, units, opening):
        cohort = fe.open_cohort(year, fe.BASE)
        revenue_added = cohort.mature_sales_in_2025_prices * y.price_index
        print(f"{year:<6}{count:9}{n:7}{n / count:8.1%}{revenue_added:11.0f}{revenue_added / prior_sales:14.1%}"
              f"{round(0.05 * count):9}{round(0.07 * count):9}{cohort.total_cost / n:11.2f}")
        prior_sales = y.sales
    for scenario in (fe.BEAR, fe.BULL):
        s_units = [sum(u) for u in scenario.new_units]
        s_opening = opening_location_counts(s_units)
        print(f"{scenario.name}: {s_units[1]}/yr from 2027 = {s_units[1] / s_opening[1]:.1%} (2027) -> "
              f"{s_units[-1] / s_opening[-1]:.1%} (2031)")
    low, high = TARGETS.startups_per_quarter_pipeline
    print(f"Pipeline build: start-ups {4 * low}-{4 * high}/yr (8-10/qtr) x 1/{TARGETS.startup_share_of_new_locations:.0%}"
          f" share -> {4 * low / TARGETS.startup_share_of_new_locations:.0f}-"
          f"{4 * high / TARGETS.startup_share_of_new_locations:.0f} total units/yr")


def print_funding(base: list[fe.ForecastYear]):
    print("\nBASE CASE funding: can OE pay for growth after interest and dividends?")
    print(f"{'Year':6}{'OE':>6}{'1-offs':>7}{'int.':>6}{'div.':>6}{'avail.':>8}{'growth':>8}{'cover':>7}"
          f"{'surplus':>9}{'lev.':>6}{'capex/OE':>9}{'+debt@2.7x':>11}")
    for i, y in enumerate(base):
        avail = cash_before_growth(y)
        capacity = f"{debt_capacity_at_target(base, i):11.0f}" if i > 0 else f"{'':11}"
        print(f"{y.year:<6}{y.owners_earnings:6.0f}{-y.one_offs:7.0f}{-after_tax_interest():6.0f}"
              f"{-fe.FINANCING.dividends:6.0f}{avail:8.0f}{-y.new.growth_capex:8.0f}"
              f"{avail / y.new.growth_capex:7.0%}{y.cash_after_financing:9.0f}{y.leverage:6.2f}"
              f"{y.new.growth_capex / y.owners_earnings:9.0%}" + capacity)
    later = base[2:]
    print(f"Cumulative surplus 2028-31 (available for buybacks if net debt held at YE-2027 "
          f"{base[1].net_debt:.0f}): {sum(y.cash_after_financing for y in later):.0f}; "
          f"leverage in 2031 on that path: {base[1].net_debt / base[-1].ebitda_after_rent:.2f}x")


def print_growth_rate_variants(base: list[fe.ForecastYear]):
    print("\nVARIANTS: unit growth at mgmt's 5% / 7% (50/50 mix, 2026 unchanged, interest on extra debt at 5.5%)")
    for rate in (TARGETS.new_location_growth_low, TARGETS.new_location_growth_high):
        scenario = replace(fe.BASE, name=f"Base, units at {rate:.0%}", new_units=units_for_growth_rate(rate))
        results = fe.forecast(scenario)
        leverage = variant_with_interest_on_extra_debt(results, base)
        units = [sum(u) for u in scenario.new_units]
        print(f"  {rate:.0%}: units {units}; growth capex {[round(y.new.growth_capex) for y in results]}")
        print(f"      cash after int. & div. (before extra interest) {[round(y.cash_after_financing) for y in results]}")
        print(f"      leverage {[round(x, 2) for x in leverage]} vs base {[round(y.leverage, 2) for y in base]}")
        print(f"      OE 2031E {results[-1].owners_earnings:.0f} vs base {base[-1].owners_earnings:.0f}; "
              f"new-loc run-rate OE 2031E {results[-1].oe_new_run_rate:.0f} vs base {base[-1].oe_new_run_rate:.0f}")


def print_debt_history():
    first, last = DEBT_TAX.net_debt_ex_leases[0], DEBT_TAX.net_debt_ex_leases[-1]
    gap = sum(h.net_growth_spend - h.oe for h in HISTORY[:2])
    print(f"\nNet debt before leases: " + ", ".join(f"{d} {v:.1f}" for d, v in DEBT_TAX.net_debt_ex_leases)
          + f"; increase {last[1] - first[1]:.1f}.  2023-24 net growth spend in excess of OE: {gap:.1f}")


def print_ncib_check(base: list[fe.ForecastYear]):
    """How much buyback could H2-2026 + 2027 absorb with no change to the leverage path, if cash taxes stay at
    their FY2023-25 ratio to normalized tax?  And what does each $100M of buyback do to YE-2027 leverage?"""
    cash_tax_ratio = sum(DEBT_TAX.cash_taxes_paid) / sum(DEBT_TAX.normalized_taxes)
    extra_cash = []
    for y in base[:2]:
        share_of_year = fe.FINANCING.share_of_2026_remaining if y.year == fe.FIRST_YEAR else 1.0
        normalized_tax = y.pre_tax_oe * fe.CORPORATE.tax_rate
        extra_cash.append((1 - cash_tax_ratio) * normalized_tax * share_of_year)
    per_100m = 100 / base[1].ebitda_after_rent
    print(f"\nNCIB check: FY2023-25 cash tax / normalized tax = {cash_tax_ratio:.0%}; extra cash vs model "
          f"H2-26 {extra_cash[0]:.0f} + 2027 {extra_cash[1]:.0f} = {sum(extra_cash):.0f}; "
          f"each $100M of buyback by YE-2027 adds {per_100m:.2f}x -> {base[1].leverage + per_100m:.2f}x; "
          f"growth capex H2-26 + 2027 = {fe.FINANCING.share_of_2026_remaining * base[0].new.growth_capex + base[1].new.growth_capex:.0f}")


if __name__ == "__main__":
    base = fe.forecast(fe.BASE)
    print_history()
    print_unit_rates(base)
    print_funding(base)
    print_growth_rate_variants(base)
    print_debt_history()
    print_ncib_check(base)
