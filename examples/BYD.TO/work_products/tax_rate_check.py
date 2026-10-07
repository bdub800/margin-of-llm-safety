"""
Is the 26.5% tax rate in forecast_earnings.py reasonable against Boyd's actual taxes?
US$ millions.  Run:  uv run python work_products/tax_rate_check.py
"""
from dataclasses import dataclass

import forecast_earnings as fe


@dataclass(frozen=True)
class TaxYear:
    period: str
    earnings_before_tax: float     # IFRS, after interest
    current_tax: float
    deferred_tax: float
    cash_tax_paid: float
    pre_tax_oe: float | None       # OE&ROIC md OE table (unlevered, normalized)

    @property
    def book_rate(self) -> float:
        return (self.current_tax + self.deferred_tax) / self.earnings_before_tax

    @property
    def cash_rate_on_pre_tax_oe(self) -> float:
        return self.cash_tax_paid / self.pre_tax_oe


HISTORY = [
    # FY2023 AFS l.221-224, 297 (2022 comparative column); no OE computed for 2022
    TaxYear("2022", 58.727, 5.712, 12.053, 3.857, None),
    # FY2024 AFS l.203-206, 300; OE&ROIC pre-tax OE 180.1
    TaxYear("2023", 119.521, 25.872, 6.993, 27.909, 180.1),
    # FY2025 AFS l.239-242, 318; pre-tax OE 124.8
    TaxYear("2024", 31.660, 7.667, -0.551, 12.295, 124.8),
    # FY2025 AFS l.239-242, 318; pre-tax OE 148.2
    TaxYear("2025", 28.724, 5.828, 4.476, 3.669, 148.2),
    # TTM Jun-26 cash tax = FY25 3.669 - H1'25 2.555 + H1'26 3.260 (Q2FY26 FS l.190); pre-tax OE 198.5.
    # Book lines not meaningful for TTM (H1'26 EBT is a loss, Q2FY26 FS l.120), so book fields set to FY2025.
    TaxYear("TTM Jun-26", 28.724, 5.828, 4.476, 3.669 - 2.555 + 3.260, 198.5),
]
STATUTORY_2025 = 0.2666             # FY2025 AFS l.832


if __name__ == "__main__":
    print(f"{'Period':11}{'book ETR':>9}{'cash tax':>9}{'pre-tax OE':>11}{'cash/OE':>8}")
    for t in HISTORY:
        cash_rate = f"{t.cash_rate_on_pre_tax_oe:8.1%}" if t.pre_tax_oe else f"{'':8}"
        oe = f"{t.pre_tax_oe:11.1f}" if t.pre_tax_oe else f"{'':11}"
        book = f"{t.book_rate:9.1%}" if t.period != "TTM Jun-26" else f"{'':9}"
        print(f"{t.period:11}{book}{t.cash_tax_paid:9.1f}{oe}{cash_rate}")
    books = HISTORY[1:4]
    pooled_book = sum(t.current_tax + t.deferred_tax for t in books) / sum(t.earnings_before_tax for t in books)
    pooled_cash = sum(t.cash_tax_paid for t in books) / sum(t.pre_tax_oe for t in books)
    print(f"Pooled FY2023-25: book ETR {pooled_book:.1%}; cash tax / pre-tax OE {pooled_cash:.1%}; "
          f"model {fe.CORPORATE.tax_rate:.1%}; statutory 2025 {STATUTORY_2025:.2%}")

    base = fe.forecast(fe.BASE)
    ttm_cash_rate = HISTORY[-1].cash_rate_on_pre_tax_oe
    print("\nBase: modeled tax vs tax at historical cash rates (difference = cash the model does not count)")
    for y in base:
        modeled = y.pre_tax_oe * fe.CORPORATE.tax_rate
        at_pooled = y.pre_tax_oe * pooled_cash
        at_ttm = y.pre_tax_oe * ttm_cash_rate
        print(f"  {y.year}: pre-tax OE {y.pre_tax_oe:5.0f}  modeled tax {modeled:5.1f}  at pooled cash rate "
              f"{at_pooled:5.1f} (+{modeled - at_pooled:4.1f})  at TTM cash rate {at_ttm:5.1f} (+{modeled - at_ttm:4.1f})")

    # SPECULATION: rough value of the tax shield the model ignores, if the pooled-rate gap (~$40-70M/yr, taking
    # 2026-27 average) persists for 10 years and then stops (US tax goodwill amortizes over 15 years - internal
    # AI model knowledge; 10 years allows for runoff of older deals).  Discounted at the model's 8%.
    gap = sum(y.pre_tax_oe * (fe.CORPORATE.tax_rate - pooled_cash) for y in base[:2]) / 2
    years, rate = 10, fe.VALUATION.discount_rate
    annuity = (1 - (1 + rate) ** -years) / rate
    print(f"\nRough shield value: {gap:.0f}/yr x {years}-yr annuity at {rate:.0%} ({annuity:.2f}) = {gap * annuity:.0f}")
    interest_shield = fe.FINANCING.cash_interest * fe.CORPORATE.tax_rate
    print(f"Part of the gap is the interest deduction (financing, not operations): {interest_shield:.1f}/yr")
    operating_gap = gap - interest_shield
    print(f"Operating shield only (gap less interest deduction): {operating_gap:.0f}/yr -> value {operating_gap * annuity:.0f}")
