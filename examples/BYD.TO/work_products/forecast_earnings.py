"""
Boyd Group Services (BYD.TO / BGSI) - 5-year Owners' Earnings forecast (FY2026E-FY2031E), ROIC method.

US$ millions.  Run:  uv run python work_products/forecast_earnings.py
Write-up: work_products/forecast_earnings.md (every number there comes from this script).
The previous margin-method version is kept as forecast_earnings_margin_method.py.

HOW THE MODEL IS LAID OUT
=========================
  PART 1  INPUTS      - one frozen dataclass per input category, each value cited to its source.
                        Judgement calls are marked ASSUMPTION / CALIBRATED / SPECULATION.
  PART 2  SCENARIOS   - the drivers that differ between Bear / Base / Bull.
  PART 3  FORMULAS    - one small function per financial line item.
  PART 4  ONE YEAR    - wires the formulas together for a single year (existing business ->
                        new locations -> corporate deductions -> cash & leverage).
  PART 5  FORECAST    - rolls PART 4 forward 2026 -> 2031 for a scenario.
  PART 6  CHECKS      - back-tests, unit-economics sanity checks, sensitivities (analysis only;
                        nothing here feeds the forecast).
  PART 7  REPORT      - printing.

HOW THE PIECES CONNECT (per year t)
===================================
  same-store sales growth (SSS) = industry claims volume + avg repair cost (TCOR) + Boyd share gain

  (A) EXISTING BUSINESS = legacy Boyd (every location open at 31-Dec-2025) + Joe Hudson's (JH, closed Jan-2026)
      two parts, each grown with SSS:
        legacy Boyd = FY2025 pro-forma sales (2025 acquisitions annualized) x (1 + SSS) each year
        JH          = 2026 disrupted year, then pre-deal run rate x (1 + SSS)
      EBITDA  = legacy sales x legacy margin + JH sales x JH margin + retained cost-program savings
                (legacy & JH margins move each year by operating leverage on SSS)
      rent    = H1-2026 cash rent x 2 in 2026, then prior-year rent x (1 + escalator)   (forecast in $)

  (B) NEW LOCATIONS opened 2026 onward (tuck-in acquisitions + start-ups), their own earnings stream
      mature EBITDA after rent = ROIC x location cost   (ROIC is pre-maintenance-capex, pre-tax)
      ramp: 0 in the year the capex is spent, 1/3 next year, 2/3 the year after, full from year 3;
            after maturity a cohort grows with SSS (it joins the same-store base)
      sales (drive maintenance/software capex only) follow the same ramp

  CORPORATE
      pre-tax OE      = (A) EBITDA - (A) rent + (B) EBITDA after rent
                        - maintenance capex % x total sales - software capex % x total sales - deal cost
      Owners' Earnings = pre-tax OE x (1 - tax rate)
      distributable    = OE - growth capex (units x location cost) - one-off integration costs (after tax)
      cash after financing = distributable - after-tax interest - dividends
      net debt         = prior net debt - cash after financing
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace

YEARS = [2026, 2027, 2028, 2029, 2030, 2031]
FIRST_YEAR = YEARS[0]


# =====================================================================================================
# PART 1 - INPUTS (same in every scenario)
# =====================================================================================================

@dataclass(frozen=True)
class FY2025Base:
    """Reported starting point (FY2025 and H1-2026 actuals)."""
    sales: float = 3142.8                  # FY2025 AFS / OE&ROIC md line 13
    # Revenue "if 2025 acquisitions had been acquired on January 1, 2025" = $3,235,845k (FY2025 AFS l.713).
    # Starting legacy Boyd here annualizes the 43 locations bought during 2025.  Younger locations' later ramp
    # is captured by SSS: SSS "includes only those locations in operation for the full comparative period"
    # (FY2025 MD&A l.232), so a store joins the SSS base after one full year.
    pro_forma_sales: float = 3235.845
    adj_ebitda: float = 376.3              # FY2025 MD&A Adjusted EBITDA
    savings_in_ebitda: float = 40.0        # ~$40M Project 360 savings realized in 2025 (FY2025 MD&A line 111)
    h1_2026_sales: float = 2010.3          # Q2FY26 MD&A line 317
    h1_2026_adj_ebitda: float = 258.3      # Q2FY26 MD&A line 317


@dataclass(frozen=True)
class RentInputs:
    """Cash rent = lease principal + lease interest (IFRS 16 reversed), existing business only.
    New locations' rent is inside their after-rent earnings stream."""
    # H1'26 property + vehicle lease principal and interest; includes JH
    # (Q2FY26 FS, primary_sources/Q2FY26/BoydGroup_Q2.md lines 167-168 principal, 171-172 interest)
    h1_2026_cash_rent: float = 72.637 + 2.901 + 31.872 + 0.531
    # Seasonality check: H1'25 comparative columns of the same lines, and FY2025 cash rent (OE&ROIC md l.100)
    h1_2025_cash_rent: float = 54.892 + 2.815 + 21.555 + 0.462
    fy2025_cash_rent: float = 161.6
    fy2025_rent_ratio: float = 161.6 / 3142.8   # reference only (unit-margin sanity check)


@dataclass(frozen=True)
class JoeHudsonsInputs:
    """Joe Hudson's Collision Center, acquired Jan-2026 (part of the existing business)."""
    pre_deal_sales: float = 722.0          # TTM Jun-25 sales (JH release l.14)
    pre_synergy_margin: float = 0.144      # IFRS-like (pre-rent) Adj. EBITDA margin (JH release l.14)
    # H1'26 sales $342.6M, conversion disruption continuing into Q3 (Q2FY26 MD&A lines 72, 291)
    sales_2026: float = 700.0              # ASSUMPTION: ~H1 x 2 + modest H2 recovery, below the 722 TTM
    margin_2026: float = 0.130             # ASSUMPTION: ~$22M lost sales x ~46% gross margin ~= $10M (~1.4pp)


@dataclass(frozen=True)
class CostSavingsProgram:
    """Project 360 + JH synergies: cumulative gross savings in the P&L vs the 2024 cost base.
    $40M 2025, +$65M 2026, +$35M ratably 2027-29 (Q2FY26 MD&A lines 70 / 221)."""
    cumulative_savings: dict = field(default_factory=lambda: {
        2025: 40.0, 2026: 105.0, 2027: 116.7, 2028: 128.3, 2029: 140.0, 2030: 140.0, 2031: 140.0})


@dataclass(frozen=True)
class OperatingLeverage:
    """CALIBRATED: yearly change in margin = sensitivity x (SSS - breakeven SSS), capped and floored.
    Anchors: mgmt steady 2-4% SSS -> ~+20bp/yr (FY2025 call l.281);
             FY2024 SSS -1.8% -> margin -1.6pp (FY2024 MD&A l.274, 297)."""
    sensitivity: float = 0.30
    breakeven_sss: float = 0.023
    max_gain_per_year: float = 0.0030      # ASSUMPTION: technician capacity limits the upside
    max_loss_per_year: float = -0.0040     # ASSUMPTION: management cost response limits the downside


@dataclass(frozen=True)
class NewLocationInputs:
    """Locations opened 2026 onward.  Unit count and ROIC are scenario drivers (PART 2)."""
    # Tuck-in: 2025 consideration $120.8M / 43 locations = $2.81M (FY2025 AFS l.663);
    #          H1'26 $18.9M / 7 locations = $2.69M (Q2FY26 interim FS l.261; Q2FY26 MD&A l.55-56)
    tuck_in_cost: float = 2.8
    # 2025 pro-forma acquired revenue = 3,235.8 - 3,142.8 + 31.5 = $124.5M / 43 = $2.90M (FY2025 AFS l.713)
    tuck_in_sales: float = (3235.845 - 3142.8 + 31.508) / 43
    # Start-up leaseholds + equipment, pooled 2022-25 = $133.7M / 79 = $1.69M (new_location_unit_economics.md
    # sec 4.2); mgmt "1,200,000 to $1,400,000 investment" under the outsourced model (Q2FY25 call l.146)
    startup_cost: float = 1.7
    startup_sales: float = 2.95            # mature; avg revenue per location (network $3.10M / JH $2.80M)
    # Share of mature earnings/sales at age 0 (capex year), 1, 2, 3+.  Judge-directed simple ramp, consistent
    # with mgmt "reach maturity by the end of their third year" (Q2FY26 MD&A l.480)
    ramp: tuple = (0.0, 1 / 3, 2 / 3, 1.0)
    cost_inflation: float = 0.03           # ASSUMPTION: unit price / build cost inflation per year

    @property
    def years_to_maturity(self) -> int:
        return len(self.ramp) - 1


@dataclass(frozen=True)
class CorporateInputs:
    software_capex_pct_sales: float = 0.002   # ~0.16-0.26% of sales (OE&ROIC md l.103)
    normalized_deal_cost: float = 5.0         # OE&ROIC md sec 2.5
    tax_rate: float = 0.265                   # OE&ROIC md sec 2.6


@dataclass(frozen=True)
class OneOffCosts:
    """Remaining transformation opex and JH integration capex from Jul-2026 (Q2FY26 MD&A l.223)."""
    remaining_opex: float = 51.5 - 35.6
    remaining_capex: float = 30.0 - 9.8
    share_by_year: dict = field(default_factory=lambda: {2026: 0.6, 2027: 0.4})


@dataclass(frozen=True)
class FinancingInputs:
    net_debt_jun_2026: float = 953.1       # debt net of cash, before leases (Q2FY26 MD&A l.361)
    cash_interest: float = 60.0            # Q2'26 run-rate x 2 (Q2FY26 MD&A l.390)
    dividends: float = 13.0                # H1'26 $6.3M x 2 (Q2FY26 MD&A l.390)
    share_of_2026_remaining: float = 0.5   # only H2-2026 cash flow remains after the Jun-26 net debt figure


@dataclass(frozen=True)
class ValuationInputs:
    """Used only by the checks in PART 6."""
    discount_rate: float = 0.08            # midpoint of 7-9% impairment-test WACC (OE&ROIC md sec 5)
    terminal_growth: float = 0.025
    invested_capital_jun_2026: float = 2902.5   # OE&ROIC md sec 4


BASE_YEAR = FY2025Base()
RENT = RentInputs()
JOE_HUDSONS = JoeHudsonsInputs()
SAVINGS = CostSavingsProgram()
OP_LEVERAGE = OperatingLeverage()
NEW_LOCATIONS = NewLocationInputs()
CORPORATE = CorporateInputs()
ONE_OFFS = OneOffCosts()
FINANCING = FinancingInputs()
VALUATION = ValuationInputs()


# =====================================================================================================
# PART 2 - SCENARIOS (drivers that differ between Bear / Base / Bull)
# =====================================================================================================

@dataclass(frozen=True)
class Scenario:
    name: str
    # Same-store sales components, percentage points per year 2026..2031
    claims_volume_pp: tuple                # industry repairable-claims volume
    repair_cost_pp: tuple                  # avg total cost of repair (TCOR)
    share_gain_pp: tuple                   # Boyd share gain vs industry
    savings_retention: float               # share of cost-program savings kept (rest absorbed by inflation)
    maintenance_capex_pct_sales: float
    rent_escalator: float                  # annual growth of existing-business rent $ (ASSUMPTION)
    # (tuck-ins, start-ups) opened per year 2026..2031.  Base 2027+ = 8 start-ups/qtr pipeline x 4 plus a
    # similar number of tuck-ins (mgmt ~50/50 mix).  History, implied growth % and funding check:
    # unit_growth_capital_check.py
    new_units: tuple
    new_location_roic: float               # mature EBITDA after rent / location cost


BEAR = Scenario("Bear",
                claims_volume_pp=(-1.0, -1.5, -1.5, -1.5, -1.5, -1.5),
                repair_cost_pp=(1.0, 1.5, 2.0, 2.0, 2.0, 2.0),
                share_gain_pp=(2.0, 1.0, 1.0, 1.0, 1.0, 1.0),
                savings_retention=0.6, maintenance_capex_pct_sales=0.020, rent_escalator=0.030,
                new_units=((20, 27),) + ((15, 20),) * 5, new_location_roic=0.09)
BASE = Scenario("Base",
                claims_volume_pp=(-1.0,) * 6,
                repair_cost_pp=(1.2, 2.0, 3.0, 3.0, 3.0, 3.0),
                share_gain_pp=(2.0, 1.5, 1.0, 1.0, 1.0, 1.0),
                savings_retention=0.8, maintenance_capex_pct_sales=0.017, rent_escalator=0.025,
                new_units=((25, 27),) + ((30, 32),) * 5, new_location_roic=0.13)
BULL = Scenario("Bull",
                claims_volume_pp=(-1.0, -0.5, -0.5, -0.5, -0.5, -0.5),
                repair_cost_pp=(1.2, 3.0, 4.0, 4.0, 4.0, 4.0),
                share_gain_pp=(2.0, 2.0, 1.5, 1.5, 1.0, 1.0),
                savings_retention=1.0, maintenance_capex_pct_sales=0.016, rent_escalator=0.025,
                new_units=((30, 27),) + ((40, 36),) * 5, new_location_roic=0.17)
EXISTING_ONLY = replace(BASE, name="Existing business only (no locations opened from 2026)",
                        new_units=((0, 0),) * 6)

SCENARIOS = [BEAR, BASE, BULL]
SCENARIO_WEIGHTS = {"Bear": 0.25, "Base": 0.50, "Bull": 0.25}


# =====================================================================================================
# PART 3 - FORMULAS (one function per line item)
# =====================================================================================================

def ramp_share(ramp: tuple, age: int) -> float:
    """Share of mature level reached at a given age (years since opening); 0 before opening."""
    if age < 0:
        return 0.0
    return ramp[min(age, len(ramp) - 1)]


# ---------------------------------------------------------------- revenue drivers

def same_store_sales_growth(scenario: Scenario, year_index: int) -> float:
    return (scenario.claims_volume_pp[year_index]
            + scenario.repair_cost_pp[year_index]
            + scenario.share_gain_pp[year_index]) / 100


def joe_hudsons_sales(year: int, sss: float, prior_sales: float) -> float:
    if year == 2026:
        return JOE_HUDSONS.sales_2026                      # disrupted conversion year
    if year == 2027:
        return JOE_HUDSONS.pre_deal_sales * (1 + sss)      # back to pre-deal run rate
    return prior_sales * (1 + sss)


# ---------------------------------------------------------------- margin drivers

def operating_leverage(sss: float) -> float:
    """Change in EBITDA margin this year from same-store sales growth."""
    ol = OP_LEVERAGE
    change = ol.sensitivity * (sss - ol.breakeven_sss)
    return min(max(change, ol.max_loss_per_year), ol.max_gain_per_year)


def fy2025_underlying_margin(scenario: Scenario) -> float:
    """FY2025 legacy margin excluding the retained share of cost savings (savings are added back separately).
    Applied to the pro-forma sales base, i.e. the annualized 2025 acquisitions are assumed to earn the network
    margin (ASSUMPTION; their in-year result was a $2.0M net loss on $31.5M revenue, FY2025 AFS l.713)."""
    reported = BASE_YEAR.adj_ebitda / BASE_YEAR.sales
    return reported - scenario.savings_retention * BASE_YEAR.savings_in_ebitda / BASE_YEAR.sales


def joe_hudsons_margin(year: int, margin_change: float, prior_margin: float) -> float:
    if year == 2026:
        return JOE_HUDSONS.margin_2026
    if year == 2027:
        return JOE_HUDSONS.pre_synergy_margin + margin_change
    return prior_margin + margin_change


def retained_savings(year: int, scenario: Scenario) -> float:
    return scenario.savings_retention * SAVINGS.cumulative_savings[year]


def existing_business_ebitda(legacy_sales, legacy_margin, jh_sales, jh_margin, savings) -> float:
    return legacy_margin * legacy_sales + jh_margin * jh_sales + savings


# ---------------------------------------------------------------- rent

def existing_rent(year: int, prior_rent: float, scenario: Scenario) -> float:
    """Cash rent in $: 2026 = H1'26 actual x 2; later years = prior year x (1 + escalator)."""
    if year == FIRST_YEAR:
        return 2 * RENT.h1_2026_cash_rent
    return prior_rent * (1 + scenario.rent_escalator)


# ---------------------------------------------------------------- new locations

@dataclass(frozen=True)
class Cohort:
    """Locations opened in one year from 2026 onward."""
    year_opened: int
    tuck_ins: int
    startups: int
    tuck_in_cost: float                    # per location, inflated to the opening year
    startup_cost: float

    @property
    def total_cost(self) -> float:
        return self.tuck_ins * self.tuck_in_cost + self.startups * self.startup_cost

    @property
    def mature_sales_in_2025_prices(self) -> float:
        return self.tuck_ins * NEW_LOCATIONS.tuck_in_sales + self.startups * NEW_LOCATIONS.startup_sales

    @property
    def year_mature(self) -> int:
        return self.year_opened + NEW_LOCATIONS.years_to_maturity


def open_cohort(year: int, scenario: Scenario) -> Cohort:
    tuck_ins, startups = scenario.new_units[YEARS.index(year)]
    inflation = (1 + NEW_LOCATIONS.cost_inflation) ** (year - FIRST_YEAR)
    return Cohort(year, tuck_ins, startups,
                  tuck_in_cost=NEW_LOCATIONS.tuck_in_cost * inflation,
                  startup_cost=NEW_LOCATIONS.startup_cost * inflation)


def cohort_run_rate_ebitda_after_rent(cohort: Cohort, year: int, roic: float, price_index: dict) -> float:
    """What the cohort would earn in `year` if it were already fully ramped: ROIC x cost, and once past its
    maturity year it grows with SSS like any same-store location."""
    growth_since_maturity = 1.0
    if year > cohort.year_mature:
        growth_since_maturity = price_index[year] / price_index[cohort.year_mature]
    return roic * cohort.total_cost * growth_since_maturity


def cohort_run_rate_sales(cohort: Cohort, year: int, price_index: dict) -> float:
    """Mature sales in `year` prices, as if the cohort were already fully ramped."""
    return cohort.mature_sales_in_2025_prices * price_index[year]


def cohort_ebitda_after_rent(cohort: Cohort, year: int, roic: float, price_index: dict) -> float:
    """Run-rate earnings x ramp share for the cohort's age."""
    return (cohort_run_rate_ebitda_after_rent(cohort, year, roic, price_index)
            * ramp_share(NEW_LOCATIONS.ramp, year - cohort.year_opened))


def cohort_sales(cohort: Cohort, year: int, price_index: dict) -> float:
    """Run-rate sales x same ramp as earnings."""
    return (cohort_run_rate_sales(cohort, year, price_index)
            * ramp_share(NEW_LOCATIONS.ramp, year - cohort.year_opened))


# ---------------------------------------------------------------- corporate deductions

def capex_rate(scenario: Scenario) -> float:
    """Maintenance + software capex as % of sales."""
    return scenario.maintenance_capex_pct_sales + CORPORATE.software_capex_pct_sales


def after_tax(pre_tax: float) -> float:
    return pre_tax * (1 - CORPORATE.tax_rate)


def one_off_costs_after_tax(year: int) -> float:
    share = ONE_OFFS.share_by_year.get(year, 0.0)
    return share * (after_tax(ONE_OFFS.remaining_opex) + ONE_OFFS.remaining_capex)


def one_off_capex(year: int) -> float:
    return ONE_OFFS.share_by_year.get(year, 0.0) * ONE_OFFS.remaining_capex


def cash_after_financing(distributable: float) -> float:
    return distributable - after_tax(FINANCING.cash_interest) - FINANCING.dividends


# =====================================================================================================
# PART 4 - ONE YEAR OF THE MODEL
# =====================================================================================================

@dataclass
class ExistingBusinessYear:
    legacy_sales: float                    # FY2025 pro-forma legacy Boyd grown with SSS
    jh_sales: float
    legacy_margin: float                   # excluding cost-program savings
    jh_margin: float                       # excluding cost-program savings
    savings: float                         # retained cost-program savings ($)
    ebitda: float
    rent: float

    @property
    def sales(self) -> float:
        return self.legacy_sales + self.jh_sales

    @property
    def margin(self) -> float:
        return self.ebitda / self.sales

    @property
    def rent_ratio(self) -> float:
        return self.rent / self.sales


@dataclass
class NewLocationsYear:
    units_opened: int
    growth_capex: float
    ebitda_after_rent: float
    sales: float
    rent_memo: float                       # new-location sales x network rent ratio (memo only)
    # Memo: all locations opened 2026..this year, valued as if already fully ramped (nothing feeds OE)
    units_open_to_date: int
    run_rate_sales: float
    run_rate_ebitda_after_rent: float

    @property
    def ebitda_memo(self) -> float:
        return self.ebitda_after_rent + self.rent_memo


@dataclass
class ForecastYear:
    year: int
    sss: float
    price_index: float                     # cumulative SSS index vs FY2025
    existing: ExistingBusinessYear
    new: NewLocationsYear
    maintenance_capex: float
    software_capex: float
    ebitda_after_rent: float
    pre_tax_oe: float
    owners_earnings: float
    oe_existing: float                     # OE split by stream (each bears capex on its own sales)
    oe_new: float
    oe_new_run_rate: float                 # memo: new-location OE if every cohort opened to date were mature
    one_offs: float
    distributable: float
    cash_after_financing: float
    net_debt: float

    @property
    def sales(self) -> float:
        return self.existing.sales + self.new.sales

    @property
    def ebitda_memo(self) -> float:
        return self.existing.ebitda + self.new.ebitda_memo

    @property
    def leverage(self) -> float:
        return self.net_debt / self.ebitda_after_rent


def forecast_existing_business(year, scenario, sss, prior: ExistingBusinessYear) -> ExistingBusinessYear:
    legacy_sales = prior.legacy_sales * (1 + sss)
    jh_sales = joe_hudsons_sales(year, sss, prior.jh_sales)

    margin_change = operating_leverage(sss)
    legacy_margin = prior.legacy_margin + margin_change
    jh_margin = joe_hudsons_margin(year, margin_change, prior.jh_margin)
    savings = retained_savings(year, scenario)
    ebitda = existing_business_ebitda(legacy_sales, legacy_margin, jh_sales, jh_margin, savings)

    rent = existing_rent(year, prior.rent, scenario)
    return ExistingBusinessYear(legacy_sales, jh_sales, legacy_margin, jh_margin, savings, ebitda, rent)


def forecast_new_locations(year, scenario, cohorts: list[Cohort], price_index: dict, rent_ratio_: float):
    """`cohorts` must already include this year's cohort."""
    this_year = cohorts[-1]
    ebitda_after_rent = sum(cohort_ebitda_after_rent(c, year, scenario.new_location_roic, price_index)
                            for c in cohorts)
    sales = sum(cohort_sales(c, year, price_index) for c in cohorts)
    return NewLocationsYear(
        units_opened=this_year.tuck_ins + this_year.startups,
        growth_capex=this_year.total_cost,
        ebitda_after_rent=ebitda_after_rent, sales=sales, rent_memo=rent_ratio_ * sales,
        units_open_to_date=sum(c.tuck_ins + c.startups for c in cohorts),
        run_rate_sales=sum(cohort_run_rate_sales(c, year, price_index) for c in cohorts),
        run_rate_ebitda_after_rent=sum(cohort_run_rate_ebitda_after_rent(c, year, scenario.new_location_roic,
                                                                         price_index) for c in cohorts))


def forecast_year(year, scenario, sss, price_index, existing: ExistingBusinessYear,
                  new: NewLocationsYear, prior_net_debt: float) -> ForecastYear:
    total_sales = existing.sales + new.sales
    maintenance_capex = scenario.maintenance_capex_pct_sales * total_sales
    software_capex = CORPORATE.software_capex_pct_sales * total_sales
    ebitda_after_rent = existing.ebitda - existing.rent + new.ebitda_after_rent

    pre_tax_oe = ebitda_after_rent - maintenance_capex - software_capex - CORPORATE.normalized_deal_cost
    owners_earnings = after_tax(pre_tax_oe)
    oe_existing = after_tax(existing.ebitda - existing.rent - capex_rate(scenario) * existing.sales
                            - CORPORATE.normalized_deal_cost)
    oe_new = after_tax(new.ebitda_after_rent - capex_rate(scenario) * new.sales)
    oe_new_run_rate = after_tax(new.run_rate_ebitda_after_rent - capex_rate(scenario) * new.run_rate_sales)

    one_offs = one_off_costs_after_tax(year)
    distributable = owners_earnings - new.growth_capex - one_offs
    cash = cash_after_financing(distributable)
    share_of_year = FINANCING.share_of_2026_remaining if year == FIRST_YEAR else 1.0
    net_debt = prior_net_debt - cash * share_of_year

    return ForecastYear(year, sss, price_index[year], existing, new, maintenance_capex, software_capex,
                        ebitda_after_rent, pre_tax_oe, owners_earnings, oe_existing, oe_new, oe_new_run_rate, one_offs,
                        distributable, cash, net_debt)


# =====================================================================================================
# PART 5 - FORECAST A SCENARIO 2026 -> 2031
# =====================================================================================================

def fy2025_starting_point(scenario: Scenario) -> ExistingBusinessYear:
    return ExistingBusinessYear(legacy_sales=BASE_YEAR.pro_forma_sales, jh_sales=0.0,
                                legacy_margin=fy2025_underlying_margin(scenario), jh_margin=0.0, savings=0.0,
                                ebitda=0.0, rent=RENT.fy2025_cash_rent)


def forecast(scenario: Scenario) -> list[ForecastYear]:
    existing = fy2025_starting_point(scenario)
    net_debt = FINANCING.net_debt_jun_2026
    price_index = {}                       # cumulative SSS index vs FY2025, by year
    cohorts: list[Cohort] = []
    results = []
    running_index = 1.0
    for i, year in enumerate(YEARS):
        sss = same_store_sales_growth(scenario, i)
        running_index *= 1 + sss
        price_index[year] = running_index

        existing = forecast_existing_business(year, scenario, sss, existing)
        cohorts.append(open_cohort(year, scenario))
        new = forecast_new_locations(year, scenario, cohorts, price_index, existing.rent_ratio)
        result = forecast_year(year, scenario, sss, price_index, existing, new, net_debt)

        net_debt = result.net_debt
        results.append(result)
    return results


def probability_weighted(results: dict, metric) -> list[float]:
    return [sum(SCENARIO_WEIGHTS[name] * metric(results[name][i]) for name in SCENARIO_WEIGHTS)
            for i in range(len(YEARS))]


# =====================================================================================================
# PART 6 - CHECKS (analysis only; nothing here feeds the forecast)
# =====================================================================================================

def rent_check():
    """Is H1 x 2 a fair full-year rent?  Test on 2025, and show the 2026 starting point."""
    fy25_from_h1 = 2 * RENT.h1_2025_cash_rent
    print(f"Rent check: H1'25 x 2 = {fy25_from_h1:.1f} vs FY2025 actual {RENT.fy2025_cash_rent:.1f} "
          f"({fy25_from_h1 / RENT.fy2025_cash_rent - 1:+.1%}); FY2026E = H1'26 {RENT.h1_2026_cash_rent:.1f} x 2 "
          f"= {2 * RENT.h1_2026_cash_rent:.1f}")


def h2_2026_cross_check(base: list[ForecastYear]):
    fy26 = base[0]
    h2_sales = fy26.sales - BASE_YEAR.h1_2026_sales
    h2_margin = (fy26.ebitda_memo - BASE_YEAR.h1_2026_adj_ebitda) / h2_sales
    print(f"\nFY2026E base: sales {fy26.sales:.0f}, EBITDA {fy26.ebitda_memo:.0f} "
          f"({fy26.ebitda_memo / fy26.sales:.1%}); implied H2 sales {h2_sales:.0f}, H2 margin {h2_margin:.1%} "
          f"(H1 actual {BASE_YEAR.h1_2026_adj_ebitda / BASE_YEAR.h1_2026_sales:.1%})")
    # Seasonality: FY2025 H2/H1 sales ratio (H1'25 $1,558.7M, Q2FY26 FS l.109; FY2025 $3,142.8M)
    h1_2025 = 1558.730
    h2_over_h1 = (BASE_YEAR.sales - h1_2025) / h1_2025
    seasonal_h2 = BASE_YEAR.h1_2026_sales * h2_over_h1
    gap = seasonal_h2 - h2_sales
    # OE on the missing sales at the 2028E network after-rent margin less 1.9% capex, after tax (rough)
    oe_gap = after_tax(gap * (0.088 - capex_rate(BASE)))
    print(f"  Seasonality: FY2025 H2/H1 = {h2_over_h1:.3f} -> H2'26 ~{seasonal_h2:.0f}; model H2 is {gap:.0f} lower "
          f"({gap / fy26.sales:.1%} of FY sales); rough OE effect ~{oe_gap:.1f}")


def blended_unit(scenario: Scenario) -> tuple[float, float]:
    """(cost, mature sales) per location for the scenario's steady-state (2027+) unit mix."""
    tuck_ins, startups = scenario.new_units[1]
    n = tuck_ins + startups
    nl = NEW_LOCATIONS
    return ((tuck_ins * nl.tuck_in_cost + startups * nl.startup_cost) / n,
            (tuck_ins * nl.tuck_in_sales + startups * nl.startup_sales) / n)


def existing_after_rent_margin(year: ForecastYear) -> float:
    return year.existing.margin - year.existing.rent_ratio


def unit_margin_sanity_check(results: dict):
    """Unit margins implied by a given ROIC: EBITDA after rent / sales = ROIC x cost / sales.
    Pre-rent margin = after-rent margin + network rent ratio (reference)."""
    base_2028 = results["Base"][2]                     # a post-savings year
    rent = base_2028.existing.rent_ratio
    network_after_rent = existing_after_rent_margin(base_2028)
    print(f"\nReference, base 2028E existing business: pre-rent EBITDA {base_2028.existing.margin:.1%}, "
          f"rent {rent:.2%}, after rent {network_after_rent:.1%}")
    fy25_margin = BASE_YEAR.adj_ebitda / BASE_YEAR.sales
    print(f"FY2025 network: pre-rent {fy25_margin:.1%}, rent {RENT.fy2025_rent_ratio:.2%}, after rent "
          f"{fy25_margin - RENT.fy2025_rent_ratio:.1%}; JH pre-synergy 14.4% pre-rent, rent 5.7% (JH release l.14, 37)")

    nl = NEW_LOCATIONS
    tuck_ins, startups = BASE.new_units[1]
    blend_cost, blend_sales = blended_unit(BASE)
    unit_types = {"Tuck-in": (nl.tuck_in_cost, nl.tuck_in_sales),
                  "Start-up": (nl.startup_cost, nl.startup_sales),
                  f"Blend {tuck_ins}/{startups}": (blend_cost, blend_sales),
                  "Start-up @ $1.3M": (1.3, nl.startup_sales),
                  "Start-up @ $2.0M": (2.0, nl.startup_sales)}
    print(f"\n{'Unit':20}{'cost':>6}{'rev':>6}{'cost/rev':>9} | ROIC ->  after-rent margin / implied pre-rent margin")
    for label, (cost, sales) in unit_types.items():
        cells = []
        for roic in (0.09, 0.13, 0.17, 0.20):
            after_rent = roic * cost / sales
            cells.append(f"{roic:.0%}: {after_rent:5.1%}/{after_rent + rent:5.1%}")
        print(f"{label:20}{cost:6.2f}{sales:6.2f}{cost / sales:9.2f} | " + "  ".join(cells))

    print("\nROIC at which a new unit merely matches the base 2028E existing network after-rent margin:")
    for label, (cost, sales) in unit_types.items():
        print(f"  {label:20} {network_after_rent * sales / cost:.1%}")

    print("\nIf both unit types earn the same after-rent margin, ROIC by type (blended ROIC = scenario ROIC):")
    for s in SCENARIOS:
        unit_after_rent = s.new_location_roic * blend_cost / blend_sales
        print(f"  {s.name:5} ROIC {s.new_location_roic:.0%}: unit after-rent margin {unit_after_rent:.1%}, "
              f"pre-rent {unit_after_rent + rent:.1%} (rent {rent:.1%}; start-up rent +1pp -> "
              f"{unit_after_rent + rent + 0.01:.1%}); tuck-in ROIC {unit_after_rent * nl.tuck_in_sales / nl.tuck_in_cost:.1%}, "
              f"start-up ROIC {unit_after_rent * nl.startup_sales / nl.startup_cost:.1%}")

    # How the bull and base ROICs were constructed
    bull_tuck_ins, bull_startups = BULL.new_units[1]
    bull_unit_margin = existing_after_rent_margin(results["Bull"][2]) + 0.02   # +2pp density premium (SPECULATION)
    bull_roic = (bull_unit_margin * (bull_tuck_ins * nl.tuck_in_sales + bull_startups * nl.startup_sales)
                 / (bull_tuck_ins * nl.tuck_in_cost + bull_startups * 1.3))    # start-ups at mgmt's $1.3M
    print(f"\nBull construct: after-rent {bull_unit_margin:.1%} (bull 2028E network +2pp), start-ups at $1.3M "
          f"-> blended ROIC {bull_roic:.1%}")
    base_unit_margin = network_after_rent + 0.01                               # +1pp premium (SPECULATION)
    print(f"Base construct: after-rent {base_unit_margin:.1%} (base 2028E network +1pp) -> blended ROIC "
          f"{base_unit_margin * blend_sales / blend_cost:.1%}")
    for name in ("Bear", "Bull"):
        m = existing_after_rent_margin(results[name][2])
        print(f"  {name} 2028E existing after-rent margin {m:.1%}; parity ROIC for blend "
              f"{m * blend_sales / blend_cost:.1%}")


def mature_unit_oe_yield(scenario: Scenario, cost: float, sales: float) -> float:
    """OE / location cost once mature: (ROIC x cost - capex on sales) after tax."""
    return after_tax(scenario.new_location_roic * cost - capex_rate(scenario) * sales) / cost


def growth_capex_value():
    """Mature OE yield and value per $1 of growth capex (simple growing perpetuity, ignores the ramp)."""
    v = VALUATION
    nl = NEW_LOCATIONS
    print(f"\nMature unit OE yield (after maint+software capex and tax) and value per $1 at "
          f"{v.discount_rate:.0%} disc., {v.terminal_growth:.1%} growth:")
    units = {"blend": blended_unit(BASE), "tuck-in": (nl.tuck_in_cost, nl.tuck_in_sales),
             "start-up": (nl.startup_cost, nl.startup_sales)}
    for s in SCENARIOS:
        for label, (cost, sales) in units.items():
            oe_yield = mature_unit_oe_yield(s, cost, sales)
            print(f"  {s.name:5} {label:9} ROIC {s.new_location_roic:.0%}: OE yield {oe_yield:5.1%}, "
                  f"value/$1 {oe_yield / (v.discount_rate - v.terminal_growth):4.2f}")


def sensitivities():
    """One-at-a-time changes to the base case; effect on FY2029E OE."""
    fy2029 = YEARS.index(2029)
    base_oe = forecast(BASE)[fy2029].owners_earnings
    b = BASE
    tests = {
        "TCOR +1pp/yr from 2027": replace(b, repair_cost_pp=(1.2,) + tuple(t + 1 for t in b.repair_cost_pp[1:])),
        "TCOR -1pp/yr from 2027": replace(b, repair_cost_pp=(1.2,) + tuple(t - 1 for t in b.repair_cost_pp[1:])),
        "Share gain 0 from 2027": replace(b, share_gain_pp=(2.0,) + (0.0,) * 5),
        "Claims -2%/yr (vs -1%)": replace(b, claims_volume_pp=(-1.0,) + (-2.0,) * 5),
        "Savings retention 1.0 (vs 0.8)": replace(b, savings_retention=1.0),
        "Savings retention 0.6": replace(b, savings_retention=0.6),
        "Maint capex 2.0% (vs 1.7%)": replace(b, maintenance_capex_pct_sales=0.020),
        "Rent escalator 3.0% (vs 2.5%)": replace(b, rent_escalator=0.030),
        "New-location ROIC 20% (mgmt)": replace(b, new_location_roic=0.20),
        "New-location ROIC 10%": replace(b, new_location_roic=0.10),
        "No new locations from 2026": EXISTING_ONLY,
    }
    print(f"\nSensitivity of base FY2029E OE ({base_oe:.0f}):")
    for label, scenario in tests.items():
        oe = forecast(scenario)[fy2029].owners_earnings
        print(f"  {label:32} {oe:6.0f}  ({oe - base_oe:+5.0f}, {oe / base_oe - 1:+.0%})")


def roic_on_total_invested_capital(base: list[ForecastYear]):
    """OE / average invested capital; IC grows by growth capex and one-off capex (H2 only in 2026)."""
    invested_capital = VALUATION.invested_capital_jun_2026
    print("\nBase ROIC on total invested capital (OE / average IC):")
    for y in base:
        opening = invested_capital
        share_of_year = FINANCING.share_of_2026_remaining if y.year == FIRST_YEAR else 1.0
        invested_capital += y.new.growth_capex * share_of_year + one_off_capex(y.year)
        average = (opening + invested_capital) / 2
        print(f"  {y.year}: avg IC {average:6.0f}  OE {y.owners_earnings:5.0f}  ROIC {y.owners_earnings / average:.1%}")


def terminal_year_checks(results: dict):
    print("\nRun-rate check for the terminal year (2026-31 cohorts as if fully mature, 2031 prices):")
    for s in SCENARIOS:
        r = results[s.name]
        run_rate = r[-1].oe_new_run_rate
        print(f"  {s.name}: 2031E new-location OE {r[-1].oe_new:.0f} vs run-rate once mature {run_rate:.0f} "
              f"(uplift {run_rate - r[-1].oe_new:+.0f}); cumulative growth capex "
              f"{sum(y.new.growth_capex for y in r):.0f}")

    cumulative_cost = sum(open_cohort(year, BASE).total_cost for year in YEARS)
    uplift_at_20pct = after_tax((0.20 - BASE.new_location_roic) * cumulative_cost)
    print("  Base with ROIC 20% (mgmt):")
    print(f"    run-rate OE uplift vs 13%: {uplift_at_20pct:.0f}")
    print("  Base new-location stream detail: " + "; ".join(
        f"{y.year}: EAR {y.new.ebitda_after_rent:.1f}, capex+tax {y.oe_new - y.new.ebitda_after_rent:.1f}, "
        f"OE {y.oe_new:.1f}" for y in results["Base"]))

    # Break-even ROIC: mature OE yield = discount rate - growth
    v = VALUATION
    cost, sales = blended_unit(BASE)
    required_yield = v.discount_rate - v.terminal_growth
    t = CORPORATE.tax_rate
    breakeven = (required_yield * cost + capex_rate(BASE) * sales * (1 - t)) / ((1 - t) * cost)
    print(f"  Break-even ROIC (OE yield = {v.discount_rate:.0%} - {v.terminal_growth:.1%} = {required_yield:.1%}): "
          f"{breakeven:.1%}")


# =====================================================================================================
# PART 7 - REPORT
# =====================================================================================================

REPORT_ROWS = [  # (label, value, multiplier, decimals)
    ("SSS %",                     lambda y: y.sss, 100, 1),
    ("Existing-business sales",   lambda y: y.existing.sales, 1, 0),
    ("  of which JH",             lambda y: y.existing.jh_sales, 1, 0),
    ("  of which legacy Boyd",    lambda y: y.existing.legacy_sales, 1, 0),
    ("Existing Adj. EBITDA",      lambda y: y.existing.ebitda, 1, 0),
    ("  margin %",                lambda y: y.existing.margin, 100, 1),
    ("Existing cash rent",        lambda y: y.existing.rent, 1, 0),
    ("  rent % sales",            lambda y: y.existing.rent_ratio, 100, 2),
    ("New-location sales",        lambda y: y.new.sales, 1, 0),
    ("New-loc EBITDA after rent", lambda y: y.new.ebitda_after_rent, 1, 0),
    ("New-loc units open (cum.)", lambda y: y.new.units_open_to_date, 1, 0),
    ("  run-rate sales (memo)",   lambda y: y.new.run_rate_sales, 1, 0),
    ("  run-rate EAR (memo)",     lambda y: y.new.run_rate_ebitda_after_rent, 1, 1),
    ("  run-rate OE (memo)",      lambda y: y.oe_new_run_rate, 1, 1),
    ("  OE still ramping (memo)", lambda y: y.oe_new_run_rate - y.oe_new, 1, 1),
    ("Total sales",               lambda y: y.sales, 1, 0),
    ("Total Adj. EBITDA (memo)",  lambda y: y.ebitda_memo, 1, 0),
    ("  margin % (memo)",         lambda y: y.ebitda_memo / y.sales, 100, 1),
    ("Maint capex (all sales)",   lambda y: y.maintenance_capex, 1, 0),
    ("Software capex",            lambda y: y.software_capex, 1, 0),
    ("Pre-tax OE",                lambda y: y.pre_tax_oe, 1, 0),
    ("Owners' Earnings",          lambda y: y.owners_earnings, 1, 0),
    ("  from existing business",  lambda y: y.oe_existing, 1, 0),
    ("  from new locations",      lambda y: y.oe_new, 1, 0),
    ("  OE margin %",             lambda y: y.owners_earnings / y.sales, 100, 1),
    ("Growth capex",              lambda y: y.new.growth_capex, 1, 0),
    ("One-offs (after tax)",      lambda y: y.one_offs, 1, 0),
    ("Distributable",             lambda y: y.distributable, 1, 0),
    ("After interest & dividends", lambda y: y.cash_after_financing, 1, 0),
    ("Net debt (ex-leases) YE",   lambda y: y.net_debt, 1, 0),
    ("Net debt/(EBITDA-rent)",    lambda y: y.leverage, 1, 2),
]


def print_scenario(scenario: Scenario, results: list[ForecastYear]):
    print(f"\n=== {scenario.name} (new-location ROIC {scenario.new_location_roic:.0%}) ===")
    print(f"{'':30}" + "".join(f"{y:>8}" for y in YEARS))
    for label, value, multiplier, decimals in REPORT_ROWS:
        print(f"{label:30}" + "".join(f"{value(y) * multiplier:8.{decimals}f}" for y in results))


def print_summary(results: dict, existing_only: list[ForecastYear]):
    weighted_oe = probability_weighted(results, lambda y: y.owners_earnings)
    weighted_dist = probability_weighted(results, lambda y: y.distributable)
    print("\nProbability-weighted (25/50/25):")
    for year, oe, dist in zip(YEARS, weighted_oe, weighted_dist):
        print(f"  {year}: OE {oe:6.1f}   distributable {dist:6.1f}")
    for name, r in list(results.items()) + [("ExistingOnly", existing_only)]:
        cagr = (r[-1].owners_earnings / r[0].owners_earnings) ** (1 / 5) - 1
        print(f"{name}: OE 2026E {r[0].owners_earnings:.0f} -> 2031E {r[-1].owners_earnings:.0f}; CAGR 26-31 "
              f"{cagr:.1%}; sum distributable {sum(y.distributable for y in r):.0f}")


if __name__ == "__main__":
    rent_check()
    results = {s.name: forecast(s) for s in SCENARIOS}
    for s in SCENARIOS:
        print_scenario(s, results[s.name])
    existing_only = forecast(EXISTING_ONLY)
    print_scenario(EXISTING_ONLY, existing_only)

    h2_2026_cross_check(results["Base"])
    print_summary(results, existing_only)
    unit_margin_sanity_check(results)
    growth_capex_value()
    sensitivities()
    roic_on_total_invested_capital(results["Base"])
    terminal_year_checks(results)
