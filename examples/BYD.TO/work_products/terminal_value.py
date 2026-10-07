"""
Boyd Group Services (BYD.TO / BGSI) - terminal value at end-2031 (undiscounted).

    TV_2031 = EV/EBITDA-after-rent multiple x FY2031E EBITDA after rent  +  ramp uplift

US$ millions.  Run:  uv run python work_products/terminal_value.py
Write-up: work_products/terminal_value.md (every number there comes from this script).

Nothing here uses Boyd's own share price.  The multiple comes from collision-repair valuation evidence only
(private-market / PE / Joe Hudson's deal multiples and the one listed pure-play), placed by qualitative judgment.
r3/r4 (judge): the multiple is applied directly to EBITDA after rent - the basis the evidence is quoted on - with no
conversion to Owners' Earnings (OE), so no tax / maintenance-capex assumptions are stacked on the multiple.
OE appears only in the secondary cross-checks.

  PART 1  INPUTS    - forecast results (Bear / Base / Bull / No growth capex), peer evidence, AMA Group, Joe Hudson's,
                      Boyd's impairment test, chosen multiples, cross-check steady-state assumptions
  PART 2  FORMULAS  - ramp uplift, terminal value, value of 2026-31 growth, cross-check formulas
  PART 3  OUTPUT    - (1) terminal-year inputs  (2) peer evidence  (3) terminal values  (4) no-growth-capex comparison
                      (5) cross-checks: formula, TV / invested capital, impairment test, margin normalization
"""
from __future__ import annotations

from dataclasses import dataclass

import forecast_earnings as fe


# =====================================================================================================
# PART 1 - INPUTS
# =====================================================================================================

# ---- Forecast results (forecast_earnings.py).  "No growth" = EXISTING_ONLY: base drivers, no locations opened
#      from 2026, so no growth capex (forecast_earnings.md sec 1, "Existing business only" rows).
NO_GROWTH = "No growth"
SCENARIO_DEFS = {"Bear": fe.BEAR, "Base": fe.BASE, "Bull": fe.BULL, NO_GROWTH: fe.EXISTING_ONLY}
RESULTS = {name: fe.forecast(s) for name, s in SCENARIO_DEFS.items()}
TERMINAL = {name: years[-1] for name, years in RESULTS.items()}      # FY2031E ForecastYear per scenario
WEIGHTS = fe.SCENARIO_WEIGHTS                                          # Bear 25% / Base 50% / Bull 25%

DISCOUNT_RATE = 0.08    # midpoint of Boyd's 7-9% impairment-test WACC (FY2025 AFS l.966); used only to compound
                        # 2026-31 cash flows in the growth-vs-no-growth check


@dataclass(frozen=True)
class PeerEvidence:
    """Collision-repair valuation datapoints, EV / EBITDA after rent (basis assumed where sources do not state it;
    confirmed only for Joe Hudson's).  Listed non-peers (LKQ, DRVN, MNRO, CPRT, VVV) were dropped in r2."""
    label: str
    low: float
    high: float
    source: str


PEER_EVIDENCE = [
    PeerEvidence("Single shops", 3.0, 5.0, "KS 11, 28"),
    PeerEvidence("Small / medium MSOs bought by consolidators", 5.0, 7.0, "KS 20, 28"),
    PeerEvidence("Market average, 2025 (weak claims year)", 7.0, 7.0, "KS 19"),
    PeerEvidence("MSOs with strong DRP relationships", 7.0, 10.0, "KS 11"),
    PeerEvidence("Platform-grade MSOs", 8.0, 12.0, "KS 11"),
    PeerEvidence("PE platform recap (illustrative)", 10.0, 10.0, "KS 21"),
    PeerEvidence("PE platforms raising capital, 2024", 12.0, 14.0, "KS 20, 21"),
    PeerEvidence("Joe Hudson's to TSG, 2019 ('north of 13x')", 13.0, 13.0, "KS 25"),
    PeerEvidence("Joe Hudson's to Boyd, 2025, run-rate pre-synergy", 13.3, 13.3, "JH release l.43"),
    PeerEvidence("Joe Hudson's to Boyd, 2025, run-rate + synergies", 9.3, 9.3, "JH release l.43"),
]


@dataclass(frozen=True)
class AmaGroup:
    """AMA Group (ASX: AMA), Australia's listed collision-repair consolidator - the only listed pure-play besides
    Boyd.  A$M.  Knowledge Store ID 26.  EBITDA is 'normalised pre-AASB 16', i.e. after rent."""
    market_cap: float = 238.42        # as of 2026-09-25 (search summary of stockanalysis.com; moderate confidence)
    net_debt: float = 18.4            # FY26 year-end, assumed ex-leases (pre-AASB 16 basis)
    ebitda_fy26: float = 68.0
    ebitda_fy27_guide_low: float = 75.0
    ebitda_fy27_guide_high: float = 80.0

    @property
    def enterprise_value(self) -> float:
        return self.market_cap + self.net_debt


@dataclass(frozen=True)
class JoeHudsonsDeal:
    """fetched_docs/boyd_joe_hudsons_acquisition_announcement.md, lines 13-16, 37, 43, 45.
    Boyd's disclosed multiples are on RUN-RATE-adjusted JHCC Adj. EBITDA (after rent), not raw TTM (r1)."""
    purchase_price: float = 1300.0
    expected_tax_benefits: float = 150.0
    ebitda_after_rent_ttm: float = 63.0          # US GAAP JHCC Adj. EBITDA (operating leases in opex), line 37
    ebitda_pre_rent_ttm: float = 104.0           # adjusted to approximate IFRS lease treatment, line 37
    synergies_low: float = 35.0                  # line 45
    synergies_high: float = 45.0
    disclosed_multiple_run_rate: float = 13.3            # "13.3x ... assuming run-rate adjustments", line 43
    disclosed_multiple_run_rate_synergies: float = 9.3   # "approximately 9.3x" with run-rate synergies, line 43

    @property
    def net_price(self) -> float:
        return self.purchase_price - self.expected_tax_benefits

    @property
    def ebitda_after_rent_run_rate(self) -> float:
        return self.net_price / self.disclosed_multiple_run_rate

    @property
    def implied_synergies(self) -> float:
        return self.net_price / self.disclosed_multiple_run_rate_synergies - self.ebitda_after_rent_run_rate

    @property
    def max_multiple_if_pre_rent(self) -> float:
        """If the 13.3x were on pre-rent EBITDA, it could not exceed this - so the disclosed basis is after rent."""
        return self.net_price / self.ebitda_pre_rent_ttm


@dataclass(frozen=True)
class ImpairmentTest:
    """Boyd's goodwill test: 'terminal growth rate of 3% and a weighted average cost of capital of 7% to 9%'
    (FY2025 AFS, line 966)."""
    terminal_growth: float = 0.03
    wacc_low: float = 0.07
    wacc_high: float = 0.09


# Historical Owners' Earnings (owners_earnings_and_roic.md, line 15) - used only to show earnings volatility.
HISTORICAL_OE = {"FY2023": 132.4, "FY2024": 91.8, "FY2025": 108.9, "TTM Jun-2026": 145.9}

# ---- THE CHOSEN MULTIPLES: EV / EBITDA after rent (judgment within the peer evidence; terminal_value.md sec 6-7).
#      Bear 6x (r4, was 7x): structural weakness, priced like the 5-7x MSO band; the 7x 2025 average was paid on
#      trough EBITDA expecting recovery, and 7x implied TV/OE of 15.4x (= formula at 6.8%) given bear capex.
#      No growth capex: same network economics and the same post-2031 growth option for a 2031 buyer -> base 8.5x.
CHOSEN_MULTIPLE = {"Bear": 6.0, "Base": 8.5, "Bull": 10.0, NO_GROWTH: 8.5}


@dataclass(frozen=True)
class SteadyState:
    """CROSS-CHECK ONLY: post-2031 economics for the value-driver formula on OE (terminal_value.md sec 8)."""
    discount_rate: float            # 8% = Boyd impairment-test midpoint
    growth_no_capital: float        # claims volume + repair-cost inflation (forecast_earnings.py Scenario, 2028-31)
    growth_share: float             # share gains that need new capacity
    new_capacity_oe_yield: float    # after-tax OE yield on new capacity (forecast_earnings.md sec 6.4)

    @property
    def growth(self) -> float:
        return self.growth_no_capital + self.growth_share


# Bear: claims -1.5 + TCOR 2.0 = 0.5%; Base: -1.0 + 3.0 = 2.0%; Bull: -0.5 + 4.0 = 3.5% capped to 2.5% so total g = 3%
# (Boyd's impairment-test rate).  +0.5pp share gains bought with new capacity; none in the no-growth-capex case.
STEADY = {
    "Bear": SteadyState(0.08, 0.005, 0.005, 0.045),
    "Base": SteadyState(0.08, 0.020, 0.005, 0.077),
    "Bull": SteadyState(0.08, 0.025, 0.005, 0.108),
    NO_GROWTH: SteadyState(0.08, 0.020, 0.000, 0.077),
}


# =====================================================================================================
# PART 2 - FORMULAS
# =====================================================================================================

def ramp_gap(y: fe.ForecastYear) -> float:
    """EBITDA after rent already paid for but not yet earned in 2031: new locations' run-rate less actual."""
    return y.new.run_rate_ebitda_after_rent - y.new.ebitda_after_rent


def ramp_uplift(y: fe.ForecastYear, multiple: float) -> float:
    """r5 (judge): same multiple x ramp gap.  No adjustment for the 1-3 years before the gap is fully earned."""
    return multiple * ramp_gap(y)


def terminal_value(name: str, multiple: float | None = None) -> dict:
    y = TERMINAL[name]
    m = CHOSEN_MULTIPLE[name] if multiple is None else multiple
    on_ebitda = m * y.ebitda_after_rent
    uplift = ramp_uplift(y, m)
    return {"ebitda": y.ebitda_after_rent, "multiple": m, "on_ebitda": on_ebitda, "gap": ramp_gap(y),
            "uplift": uplift, "total": on_ebitda + uplift, "oe": y.owners_earnings}


def probability_weighted(tvs: dict, key: str) -> float:
    return sum(WEIGHTS[n] * tvs[n][key] for n in WEIGHTS)


def future_value_2031(flows_by_year: dict) -> float:
    """Compound end-of-year cash flows to end-2031 at DISCOUNT_RATE."""
    return sum(cf * (1 + DISCOUNT_RATE) ** (2031 - yr) for yr, cf in flows_by_year.items())


def invested_capital_end_2031(years: list[fe.ForecastYear]) -> float:
    """Jun-2026 IC plus growth capex (H2 only in 2026) and one-off integration capex, as in the forecast."""
    ic = fe.VALUATION.invested_capital_jun_2026
    for y in years:
        share = fe.FINANCING.share_of_2026_remaining if y.year == fe.FIRST_YEAR else 1.0
        ic += y.new.growth_capex * share + fe.one_off_capex(y.year)
    return ic


# ---- cross-check formulas (OE basis) ----
def reinvestment_rate(s: SteadyState) -> float:
    return s.growth_share / s.new_capacity_oe_yield


def fundamental_oe_multiple(s: SteadyState) -> float:
    """(1 + g)(1 - reinvestment) / (r - g), on trailing FY2031E OE."""
    return (1 + s.growth) * (1 - reinvestment_rate(s)) / (s.discount_rate - s.growth)


def implied_discount_rate(oe_multiple: float, s: SteadyState) -> float:
    return s.growth + (1 + s.growth) * (1 - reinvestment_rate(s)) / oe_multiple


# =====================================================================================================
# PART 3 - OUTPUT
# =====================================================================================================

def print_terminal_year():
    oe = list(HISTORICAL_OE.items())
    print("Historical OE (year-on-year change): " +
          ", ".join(f"{label} {cur:.1f} ({cur / prev - 1:+.0%})" for (_, prev), (label, cur) in zip(oe, oe[1:])))
    print("\n(1) FY2031E terminal-year inputs (forecast_earnings.py):")
    print(f"  {'':10} {'Sales':>6} {'EBITDA-R':>8} {'of which new':>12} {'ramp gap':>8} {'OE':>5} {'Ex. margin':>10}")
    for name, y in TERMINAL.items():
        print(f"  {name:10} {y.sales:6.0f} {y.ebitda_after_rent:8.1f} {y.new.ebitda_after_rent:12.1f} "
              f"{ramp_gap(y):8.1f} {y.owners_earnings:5.1f} {y.existing.margin:10.1%}")


def print_peer_evidence():
    print("\n(2) Collision-repair valuation evidence, EV / EBITDA after rent:")
    for e in PEER_EVIDENCE:
        rng = f"{e.low:.1f}x" if e.low == e.high else f"{e.low:.1f}-{e.high:.1f}x"
        print(f"  {e.label:50} {rng:>10}  ({e.source})")
    ama = AmaGroup()
    print(f"  AMA Group (ASX): EV A${ama.enterprise_value:.0f}M -> FY26 {ama.enterprise_value / ama.ebitda_fy26:.1f}x, "
          f"FY27 guide {ama.enterprise_value / ama.ebitda_fy27_guide_high:.1f}-"
          f"{ama.enterprise_value / ama.ebitda_fy27_guide_low:.1f}x")
    jh = JoeHudsonsDeal()
    print(f"  Joe Hudson's: net price ${jh.net_price:.0f}M; run-rate EBITDA-R {jh.ebitda_after_rent_run_rate:.1f} "
          f"(raw TTM {jh.ebitda_after_rent_ttm:.0f}, adj. {jh.ebitda_after_rent_run_rate - jh.ebitda_after_rent_ttm:+.1f}); "
          f"implied synergies {jh.implied_synergies:.1f} (disclosed {jh.synergies_low:.0f}-{jh.synergies_high:.0f}); "
          f"on raw TTM {jh.net_price / jh.ebitda_after_rent_ttm:.1f}x pre-synergy; "
          f"max if pre-rent basis {jh.max_multiple_if_pre_rent:.1f}x")


def print_terminal_values():
    print("\n(3) Terminal value at end-2031 (undiscounted), US$M:")
    print(f"  {'':10} {'EBITDA-R':>8} {'Mult.':>6} {'on EBITDA-R':>11} {'+ramp':>6} {'TV':>7} {'TV/OE':>6}")
    tvs = {name: terminal_value(name) for name in TERMINAL}
    for name, tv in tvs.items():
        print(f"  {name:10} {tv['ebitda']:8.1f} {tv['multiple']:5.1f}x {tv['on_ebitda']:11.0f} {tv['uplift']:6.0f} "
              f"{tv['total']:7.0f} {tv['total'] / tv['oe']:5.1f}x")
    pw = {k: probability_weighted(tvs, k) for k in ("ebitda", "on_ebitda", "uplift", "total", "oe")}
    print(f"  {'P-wtd':10} {pw['ebitda']:8.1f} {pw['on_ebitda'] / pw['ebitda']:5.1f}x {pw['on_ebitda']:11.0f} "
          f"{pw['uplift']:6.0f} {pw['total']:7.0f} {pw['total'] / pw['oe']:5.1f}x   (Bear/Base/Bull 25/50/25)")

    print("  Base sensitivity to the multiple:")
    for m in (7.0, 7.5, 8.0, 8.5, 9.0, 9.3, 10.0):
        print(f"    {m:4.1f}x -> base {terminal_value('Base', m)['total']:6.0f}   no growth "
              f"{terminal_value(NO_GROWTH, m)['total']:6.0f}")
    return tvs


def print_no_growth_comparison(tvs: dict):
    """What the 2026-31 growth programme is worth at end-2031, base vs no growth capex."""
    base, none = RESULTS["Base"], RESULTS[NO_GROWTH]
    d_tv = tvs["Base"]["total"] - tvs[NO_GROWTH]["total"]
    d_dist = {b.year: b.distributable - n.distributable for b, n in zip(base, none)}
    capex = {b.year: b.new.growth_capex for b in base}
    print("\n(4) Base vs no growth capex, end-2031:")
    print(f"  Extra TV from 2026-31 locations: {d_tv:.0f} "
          f"(on 2031 new-loc EBITDA-R {tvs['Base']['on_ebitda'] - tvs[NO_GROWTH]['on_ebitda']:.0f} + ramp "
          f"{tvs['Base']['uplift'] - tvs[NO_GROWTH]['uplift']:.0f})")
    print(f"  Distributable 2026-31: base {sum(b.distributable for b in base):.0f}, no growth "
          f"{sum(n.distributable for n in none):.0f}, difference {sum(d_dist.values()):.0f} "
          f"(growth capex {sum(capex.values()):.0f})")
    fv = future_value_2031(d_dist)
    print(f"  Difference compounded to end-2031 at {DISCOUNT_RATE:.0%}: {fv:.0f}")
    print(f"  Net value of the growth programme at end-2031: {d_tv + fv:+.0f}")
    print(f"  Invested capital end-2031: base {invested_capital_end_2031(base):.0f}, no growth "
          f"{invested_capital_end_2031(none):.0f}")


def print_cross_checks(tvs: dict):
    print("\n(5a) Value-driver formula on OE (cross-check): TV/OE implied by the chosen EBITDA-R multiples")
    for name, s in STEADY.items():
        implied = tvs[name]["total"] / tvs[name]["oe"]
        print(f"  {name:10} formula at 8%: {fundamental_oe_multiple(s):5.1f}x (g {s.growth:.1%}, reinvest "
              f"{reinvestment_rate(s):4.1%}); chosen TV/OE {implied:5.1f}x = formula at r {implied_discount_rate(implied, s):.2%}")
    b = STEADY["Base"]
    print("  Base formula sensitivity (rows r, columns total g):")
    growths = (0.015, 0.020, 0.025, 0.030)
    for r in (0.08, 0.09, 0.10):
        row = " ".join(f"{fundamental_oe_multiple(SteadyState(r, g - b.growth_share, b.growth_share, b.new_capacity_oe_yield)):6.1f}x"
                       for g in growths)
        print(f"    r {r:.0%}: {row}   (g = {', '.join(f'{g:.1%}' for g in growths)})")

    print("\n(5b) TV vs invested capital, end-2031:")
    for name in TERMINAL:
        ic = invested_capital_end_2031(RESULTS[name])
        tv = tvs[name]["total"]
        print(f"  {name:10} IC {ic:6.0f}  OE/IC {TERMINAL[name].owners_earnings / ic:5.1%}  TV/IC {tv / ic:4.2f}x  "
              f"TV-IC {tv - ic:+6.0f}")

    it = ImpairmentTest()
    print(f"\n(5c) Boyd impairment test (g {it.terminal_growth:.0%}, WACC {it.wacc_low:.0%}-{it.wacc_high:.0%}): "
          f"cash-flow multiple {(1 + it.terminal_growth) / (it.wacc_high - it.terminal_growth):.1f}x to "
          f"{(1 + it.terminal_growth) / (it.wacc_low - it.terminal_growth):.1f}x")

    y = TERMINAL["Base"]
    lost = (y.existing.margin - 0.14) * y.existing.sales
    m = CHOSEN_MULTIPLE["Base"]
    print(f"\n(5d) Base existing margin {y.existing.margin:.1%} normalized to 14.0%: EBITDA-R {y.ebitda_after_rent:.0f} -> "
          f"{y.ebitda_after_rent - lost:.0f} ({-lost / y.ebitda_after_rent:+.0%}); TV lower by {m * lost:.0f}")


if __name__ == "__main__":
    print_terminal_year()
    print_peer_evidence()
    terminal_values = print_terminal_values()
    print_no_growth_comparison(terminal_values)
    print_cross_checks(terminal_values)
