# NamSys Inc. (TSXV: CTZ) — Present-Value Equity Valuation

*Prepared September 17, 2026; revised September 17, 2026 after verifier round 1 (`pv/sotp/r1_review.md`, `pv/sotp/r1_response.md`) to remove a double-count between the standalone cash balance and the undiscounted FY2026E flow — see §3.3 and §9. All figures in Canadian dollars unless stated. Fiscal year ends October 31. Every number in this document is an output of `work_products/valuation_calcs.py`; run it with `uv run python work_products/valuation_calcs.py`. Each input in that script carries a source tag in a comment. This document is stock-price-blind: no NamSys quote, market capitalisation or price-derived multiple is used anywhere, and none of the inputs below were chosen or adjusted with reference to the trading price.*

Source tags used throughout:

| Tag     | Source                                                     |
|---------|--------------------------------------------------------------|
| `FC`    | `work_products/forecast_earnings.md` (owners' earnings by scenario, FY2026E–FY2030E) |
| `TV`    | `work_products/terminal_value.md` (terminal multiple and value at end of FY2030E)     |
| `OE`    | `work_products/owners_earnings_and_roic.md` (net cash / standalone assets; no debt)   |
| `FSQ2`  | `primary_sources/2Q2026/FS_Q2_NamSys_Apr_30_26_FINAL.md`                              |
| `MDQ2`  | `primary_sources/2Q2026/MDA_Q2_NamSys_Apr_30_26_FINAL.md`                              |

---

## 1. Headline

**Base case: ~$1.46 per diluted share**, built as the present value of five years of forecast owners' earnings (FY2026E–FY2030E) plus the present value of a terminal value at the end of FY2030E, plus standalone net cash, less debt (nil), divided by 27,459,593 current diluted shares.

| Scenario                     | Equity value    | Per diluted share |
|-------------------------------|-----------------|--------------------|
| Bull                          | $67,694,384     | **$2.47**          |
| **Base**                      | **$39,974,178** | **$1.46**          |
| Bear, management right-sizes  | $25,865,989     | **$0.94**          |
| Bear, no cost response        | $21,364,839     | **$0.78**          |

This is a **valuation exercise only**, deliberately blind to where CTZ.V actually trades. It says nothing about margin of safety or whether the stock is cheap or expensive at today's price — that comparison is outside the scope of this document.

---

## 2. Method

Per the brief: valuation equals the projected future owners' earnings discounted to present value, plus the terminal value also discounted to present value, plus standalone assets, minus all debt-like items, expressed per current diluted share.

**Discounting convention.** The discount rate is a variable set to 10% (`DISCOUNT_RATE` in the script — change it there to re-run at a different rate). The current fiscal year is treated as t=0 and is **not** discounted; each subsequent year is discounted one more period. NamSys's fiscal year ends October 31, and this document is prepared September 17, 2026 — i.e. inside FY2026, which is therefore the "current year." So:

| t | Fiscal year | Discount factor at r=10% |
|---|-------------|---------------------------|
| 0 | FY2026E     | 1.0000                    |
| 1 | FY2027E     | 0.9091                    |
| 2 | FY2028E     | 0.8264                    |
| 3 | FY2029E     | 0.7513                    |
| 4 | FY2030E     | 0.6830                    |

The terminal value (`TV`) is, by construction, the value of the operating business **as of the end of FY2030E** (`TV` document header: "terminal value at October 31, 2030"), i.e. the same point in time as the FY2030E cash flow. It is therefore discounted at the **same t=4 factor**, not t=5.

**What feeds the discounted stream.** Owners' earnings, not revenue or net income — reported operating income normalised for bad debt and share-based compensation, plus depreciation less maintenance capex, taxed at the 26.5% statutory rate, with interest income on the financial portfolio deliberately excluded (`OE` §2, carried forward unchanged in `FC` §2.1). This is the correct object to discount because, as established in `OE` §3–§5, NamSys's operating invested capital is negligible (~$1M against ~$2.3M of annual owners' earnings) and essentially 100% of owners' earnings is distributable each year without impairing the business — so there is no reinvestment wedge between "earnings" and "cash available to owners," and no separate free-cash-flow adjustment is needed on top of the owners'-earnings figure already built for this purpose.

**Why five years plus a terminal value, not a longer explicit forecast.** `FC` already builds and defends a five-year driver-based forecast (endpoints × rate → revenue; headcount × compensation → cost) out to FY2030E; extending it further would not add information, only compounding uncertainty on assumptions (headcount path, Mexican-account durability, FX) that `FC` §10 already flags as unresolvable much past a few years. `TV` then separately reasons about the durability of the business *beyond* FY2030 and selects a multiple, rather than extending the explicit driver forecast — the standard and more defensible way to handle a perpetuity question.

---

## 3. The three components, base case

### 3.1 PV of FY2026E–FY2030E owners' earnings

**FY2026E is adjusted before it enters the t=0 flow, to avoid double-counting against the standalone-cash balance in §3.3.** The reported FY2026E base-case owners' earnings is $2,375,755 (`FC` §1). NamSys's own H1 FY2026 cash-flow statement shows $1,497,265 of operating cash already generated in the first six months of FY2026 (`FSQ2` Statements of Cash Flows, six months ended April 30, 2026), and that cash is already sitting inside the April 30, 2026 balance added as a standalone asset in §3.3. Adding the *whole* $2,375,755 undiscounted at t=0 on top of a balance that already contains $1,497,265 of this year's cash generation would count that portion twice. The fix nets it out on the flow side: $2,375,755 − $1,497,265 = **$878,490** is what is actually used at t=0. (This netting is applied identically to every scenario's FY2026E figure in §5, since the $1,497,265 already happened and does not vary by scenario.)

| Year  | t | Owners' earnings used | Discount factor | PV        |
|-------|---|-----------------------------------|------------------|-----------|
| FY2026E (net of H1 overlap) | 0 | 878,490 | 1.0000 | 878,490  |
| FY2027E | 1 | 2,413,913 | 0.9091 | 2,194,466  |
| FY2028E | 2 | 2,548,061 | 0.8264 | 2,105,836  |
| FY2029E | 3 | 2,716,487 | 0.7513 | 2,040,937  |
| FY2030E | 4 | 2,859,320 | 0.6830 | 1,952,954  |
| **Sum** |   |           |        | **9,172,683** |

### 3.2 PV of terminal value

`TV` §1/§5 selects **12× FY2030E owners' earnings** as the base-case terminal multiple (defensible range 9×–15×), on the reasoning that NamSys combines genuinely high quality (99% recurring revenue, near-zero account churn, ~40% operating margin, three-digit ROIC, no debt — `TV` §3.1) with genuine fragility (37–39% of revenue in three customers in every disclosed period, a documented bank-merger displacement mechanism, a saturated US client tier, weak pricing power — `TV` §3.2), reconciled against peer trading multiples, comparable take-private transactions, and a Gordon-growth cross-check (`TV` §4). That gives:

- FY2030E base-case owners' earnings: $2,859,320 (`FC` §1)
- Terminal value at October 31, 2030: 12 × $2,859,320 = **$34,311,840** (`TV` §1)
- Discounted at the same t=4 factor as the FY2030E cash flow: $34,311,840 × 0.6830 = **$23,435,448**

### 3.3 Standalone assets and debt

**Standalone assets:** cash of $940,082 plus short-term investments (cashable GICs) of $6,425,965, totalling **$7,366,047** at April 30, 2026 — the most recent balance-sheet date available, since Q3 FY2026 had not yet been filed as of this document's date (`OE` §4, `FC` §2.5). These are genuinely surplus to the operating business: they are excluded from operating invested capital in `OE` §3.1, they earn a sub-inflation 2.0%–2.45% (`OE` §4), and owners' earnings deliberately exclude the interest they generate (`OE` §2.2(a)).

**This must be the current (April 30, 2026) balance, not an earlier one, and the overlap with the FY2026E flow is instead removed on the flow side (§3.1).** An earlier draft of this document used this same April 30, 2026 figure but paired it with the *full, unadjusted* FY2026E owners' earnings at t=0, which double-counted the H1 FY2026 cash already inside the balance — flagged correctly by the verifier (`pv/sotp/r1_review.md`, objection 1) and fixed as shown in §3.1. The alternative fix of rolling the *balance* back to the October 31, 2025 figure ($10,175,672, per `OE` §4) instead of adjusting the flow was considered and rejected: NamSys paid a $4,027,790 special dividend in March 2026 (`FSQ2` Note 6), which is *already in the hands of* whoever held shares at the record date. A buyer of the stock today does not receive that dividend, so crediting today's valuation with the pre-dividend balance while dividing by today's (post-buyback) share count would overstate value by re-including cash that has already left the company and been paid out — a different and larger error than the one being corrected. Keeping the actual current balance and netting the overlap out of the flow (as done in §3.1) is the internally consistent fix.

**Debt:** **nil**. "Other than trade and other payables, the Company has no debt outstanding and incurred no interest expense in respect of outstanding debt in the current or comparative periods" (FY2025 MD&A, quoted at `OE` §2, point 1). There is no pension plan, no capitalised operating lease debt of any size (the office lease is $6,896–$9,195 across all periods and is already absorbed inside operating invested capital in `OE` §3.1, not treated as debt), and no disclosed off-balance-sheet financing obligation.

**One contingent item, deliberately not deducted.** NamSys carries a $1,100,000 employee termination commitment to three employees, payable only if those employees are terminated without cause (FY2025 AFS Note 13; unchanged at April 30, 2026, per `OE` §3.1). This is not a certain, contractual debt obligation — it is a contingent severance commitment that a reasonable analyst could read either way. §5 below shows the effect of treating it as debt: it costs $0.04 per share, which does not change the conclusion in either direction. I flag it rather than silently including or excluding it.

### 3.4 Diluted share count

**27,459,593** — the weighted-average diluted share count for the three months ended April 30, 2026, the latest disclosed figure at the time of writing (`MDQ2`, line 114; Q3 FY2026 had not yet been filed). Per the brief, this is the **current** count, not a forecast, so the most recent quarter is used rather than an older or six-month-average figure. (An earlier draft characterized the NCIB buyback program as "ongoing" as the reason for preferring the more recent quarter; the verifier correctly flagged that the only disclosed NCIB authorization ran "commencing March 27, 2025 and ending on March 26, 2026" — `MDQ2`, *Outstanding Securities Data* — which had already expired by this document's September 17, 2026 preparation date, with no renewal found in the sources reviewed. That characterization is dropped; it was never load-bearing.) Section 6 of the script shows the six-month H1 FY2026 count (27,498,422) instead moves the answer by 0.14% — immaterial, so the choice of count does not affect the conclusion regardless of buyback status.

---

## 4. Full build and result

| Component                                              | Amount          |
|---------------------------------------------------------|-----------------|
| PV of FY2026E–FY2030E owners' earnings (FY2026E net of H1 overlap, §3.1) | $9,172,683 |
| + PV of terminal value (12× FY2030E OE, discounted at t=4)| $23,435,448     |
| = PV of operating business                                | **$32,608,131** |
| + Standalone assets (cash + short-term investments, Apr 30 2026) | $7,366,047 |
| − Debt                                                    | $0              |
| = **Equity value**                                        | **$39,974,178** |
| ÷ Diluted shares outstanding                              | 27,459,593      |
| = **Value per diluted share**                             | **$1.46**       |

**Composition of the $1.46.** $0.33 (23%) is the five explicit forecast years; $0.85 (59%) is the discounted terminal value; $0.27 (18%) is standalone cash and short-term investments. **Nearly 60% of the answer is the terminal-value judgement call, not the five-year forecast** — this is a direct consequence of a business whose owners' earnings are ~$2.3–2.9M/yr against a terminal multiple in the low teens; it is not an artefact of the method, and it is exactly why `TV` spends as much space as it does defending the multiple.

---

## 5. Scenarios

Each scenario carries its own owners'-earnings path (`FC` §1, §8) **and** its own scenario-consistent terminal multiple (`TV` §1 diagonal — the multiple and the earnings path are not independent: a scenario in which earnings compound faster is also one in which the business has become demonstrably less concentrated, and vice versa; `TV` §1).

Each scenario's FY2026E figure is likewise reduced by the same $1,497,265 of already-realized H1 FY2026 operating cash (§3.1) before entering its t=0 flow, since that cash is a historical fact common to all four scenarios and is already embedded in the (scenario-independent) April 30, 2026 standalone-asset balance.

| Scenario                     | Terminal multiple | PV earnings   | PV terminal value | Equity value    | Per diluted share |
|-------------------------------|--------------------|---------------|---------------------|------------------|---------------------|
| Bull                          | 15×                | $12,689,788   | $47,638,549         | $67,694,384      | **$2.47**           |
| **Base**                      | **12×**            | **$9,172,683** | **$23,435,448**    | **$39,974,178**  | **$1.46**           |
| Bear, management right-sizes  | 8×                 | $7,052,702    | $11,447,240         | $25,865,989      | **$0.94**           |
| Bear, no cost response        | 8×                 | $5,771,681    | $8,227,110          | $21,364,839      | **$0.78**           |

The scenario definitions are unchanged from `FC` §8: the bull case requires a second Mexico-sized international account landing from FY2028 (`FC` §4.4, §8); the bear cases both assume the legacy US account is lost outright via the bank-merger displacement mechanism NamSys itself discloses (`MDA25` Risk Factors, quoted at `TV` §3.2), differing only in whether management right-sizes headcount in response (`FC` §8). All four scenarios hold USD/CAD flat as a deliberate no-view assumption (`FC` §2.2) — currency is the single largest swing factor in the underlying earnings (`FC` §7: ~2.6× elasticity, so a ±10% move shifts FY2030E owners' earnings ±26%) and is sensitized separately in `FC`, not re-litigated here.

---

## 6. Sensitivity: discount rate × terminal multiple (base-case earnings path)

| r \ multiple | 9×    | 12×   | 15×   |
|--------------|-------|-------|-------|
| 8%           | 1.31  | 1.53  | 1.76  |
| 9%           | 1.27  | 1.49  | 1.72  |
| **10%**      | **1.24** | **1.46** | **1.67** |
| 11%          | 1.21  | 1.42  | 1.62  |
| 12%          | 1.18  | 1.38  | 1.58  |

Across the full defensible band — 9×–15× terminal multiple (`TV` §5) and 8%–12% discount rate — base-case value per share ranges from **$1.18 to $1.76**, a band of about ±20% around the $1.46 central estimate. The result is far more sensitive to the terminal multiple than to the discount rate: at r=10%, 9×→15× moves per-share value 34.3% ($1.24→$1.67), while at the 12× column, 8%→12% moves it only 10.9% ($1.53→$1.38) — a roughly 3× gap. (An earlier draft of this section stated "~35%" and "~14%" for these two figures; the "~14%" was a prose arithmetic error caught by the verifier, `pv/sotp/r1_review.md` objection 2 — the underlying table was always correct, and the corrected percentages make the qualitative point *more* pronounced, not less.) This is the arithmetic counterpart of §4's finding that the terminal value carries most of the weight.

**No independent view on the discount rate is asserted here.** 10% is used because the brief specifies it as the default, deliberately kept as a variable in the script. `TV` §4.3 separately derives an implied required return of roughly 11%–13% for a TSXV microcap with this concentration and unhedged FX profile, built up from NamSys's own sourced 2.25% GIC yield (`FSQ2` Note 15) plus an unsourced equity-risk/size/illiquidity premium (analyst judgement, flagged as such in `TV`). Using 12% instead of 10% would lower the base case to $1.38 (12× column above) — a modest, not a conclusion-changing, difference.

---

## 7. What I am confident about, and what I am not

**High confidence (arithmetic, given the inputs from `FC`/`TV`/`OE`):**

- The mechanical PV build itself: given the owners'-earnings path, the terminal value, the discount rate, and the standalone-asset figure, the $1.46 base-case answer is simple, transparent arithmetic with no hidden steps (`work_products/valuation_calcs.py`).
- NamSys has no debt and negligible off-balance-sheet obligations other than one contingent, non-certain item (§3.3) — this is a sourced fact (`OE` §2), not a judgement call, and it materially simplifies this valuation relative to a levered business.
- The standalone cash/short-term-investment figure ($7,366,047, ~$0.27/share) is directly disclosed and is correctly additive rather than something to be capitalised at a multiple, because owners' earnings already exclude the interest income it generates (`OE` §2.2(a), §4).
- Choice of diluted share count (Q2-only vs H1-average) does not move the answer (§3.4).
- The FY2026E flow and the standalone-asset balance do not overlap (§3.1, §3.3) — this took a verifier round to get right (§9), but the corrected treatment is now internally consistent: the balance is the actual current one, and the one dollar figure common to both (H1 FY2026's $1,497,265 of realized operating cash) is counted exactly once.

**Genuinely uncertain — inherited in full from `FC` and `TV`, not resolved here:**

- **The terminal multiple is the single largest driver of the per-share answer** (§4, §6) and is analyst judgement, not a market-observed fact for NamSys itself (`TV` §7 gives its own honest range: "I would not defend 12× against 11× or 13× on the evidence available").
- **Whether the FY2030E earnings base being capitalised is right at all** — it inherits `FC`'s flat-USD/CAD assumption (±10% currency moves FY2030E owners' earnings ±26%, `FC` §7) and the inference that the Mexico line in the geographic note is a single customer (`FC` §4.1). If that inference is wrong, both the earnings and the appropriate multiple would need revisiting together, not independently (`TV` §7).
- **Customer concentration risk is a five-year window's worth of scenario coverage capitalised into a perpetuity.** `FC` §7 sizes the effect of losing the Mexican account or the legacy US account only inside FY2026–FY2030; the terminal multiple is what is doing the work of pricing that risk *forever*, and `TV` §3.2 is explicit that this is exactly the tension the multiple has to resolve.
- **The discount rate itself is not independently derived here** — it is the brief's specified default of 10%, sensitized in §6 but not defended as "the" correct cost of capital for this security.
- **The contingent $1.1M termination commitment** (§3.3): reasonable analysts could treat this as debt-like; doing so costs $0.04/share and does not change any conclusion.

**One thing this valuation deliberately does not do.** It does not compare the resulting $1.18–$1.76 (or $0.78–$2.47 across scenarios) range to where CTZ.V trades. Per the brief, this exercise is stock-price-blind throughout — inputs, method, and output.

---

## 9. Revision history

**Round 1 (September 17, 2026).** The verifier (`pv/sotp/r1_review.md`) raised three objections; the full response is in `pv/sotp/r1_response.md`. Summary:

1. **Conceded, with a correction.** The original draft added the April 30, 2026 standalone-cash balance ($7,366,047) *and* the full, unadjusted FY2026E owners' earnings undiscounted at t=0, double-counting the $1,497,265 of H1 FY2026 operating cash already inside that balance (`FSQ2` cash-flow statement). Fixed by netting that amount out of each scenario's FY2026E t=0 flow (§3.1), which moved the base case from $1.51 to **$1.46**/share (all headline figures in this document reflect the correction). A rolling-the-balance-back-to-October-2025 alternative was considered and rejected because it would re-credit today's valuation with the $4,027,790 special dividend already paid out to March 2026 shareholders while still dividing by today's post-buyback share count — see §3.3.
2. **Conceded.** §6's discount-rate-sensitivity narrative stated "~14%" for the 8%→12% spread at the 12× multiple; the correct figure (matching the script's own table) is 10.9%. Does not change any conclusion — if anything it widens the gap versus the terminal-multiple sensitivity, reinforcing the point being made.
3. **Conceded.** "Buybacks under the NCIB are ongoing" (§3.4) was asserted without a source covering the valuation date; the only disclosed NCIB authorization had already expired (March 26, 2026) by the September 17, 2026 preparation date. The characterization is dropped. Immaterial to the numeric conclusion either way, since the share-count choice moves the answer by only 0.14%.

Net effect on the conclusion: the central estimate moved from **$1.51 to $1.46 per diluted share** (−3.3%), and the full scenario range moved from $0.83–$2.52 to $0.77–$2.47. Nothing else about the method, the sourcing, or the qualitative conclusions changed.

**Round 2 (September 18, 2026).** Not a review finding — an upstream correction in `FC`. The non-compensation selling line was hard-coded in `forecast_earnings_calcs.py` as a five-year level vector that matched the rule documented in `FC` §4 ("\$150,000 in FY2026 compounding at 10%/yr in the base case, 5%/yr in the bear and 14%/yr in the bull") in the **base case only**: the bull vector was in fact a flat +\$25,000/yr arithmetic step and the bear vector an irregular +20k/+15k/+10k/+10k ladder. `FC` now implements the documented rule, and this document, `TV`, `terminal_value_calcs.py`, `valuation_calcs.py` and `work_products/valuation.xlsx` are updated to match. The base case is **completely unaffected** (the 10% rule already reproduced its vector to the dollar); the bull case falls \$0.0007/share and both bear variants rise \$0.0049/share, moving one headline figure at two decimal places: bear, no cost response, from \$0.77 to **\$0.78**. FY2030E owners' earnings move from \$4,652,298 to \$4,649,840 (bull), \$2,078,323 to \$2,094,988 (bear right-sized) and \$1,488,999 to \$1,505,664 (bear no cost). The central estimate of **\$1.46** and every base-case figure in this document are unchanged.

---

## 10. Source index

| Reference                                                 | Used for                                                                                     |
|------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| `work_products/forecast_earnings.md`                       | FY2026E–FY2030E owners' earnings by scenario                                                  |
| `work_products/terminal_value.md`                           | Terminal multiple selection and terminal value at end of FY2030E, by scenario                 |
| `work_products/owners_earnings_and_roic.md`                 | Owners'-earnings definition; no-debt confirmation; standalone cash and short-term investments |
| `primary_sources/2Q2026/FS_Q2_NamSys_Apr_30_26_FINAL.md`    | Diluted share count (three months and six months ended April 30, 2026); cash, STI and H1 operating-cash-flow balances |
| `primary_sources/2Q2026/MDA_Q2_NamSys_Apr_30_26_FINAL.md`   | Diluted share count corroboration; NCIB authorization window                                  |
| `pv/sotp/r1_review.md`                                      | Verifier round 1 objections                                                                    |
| `pv/sotp/r1_response.md`                                    | Prover's response to verifier round 1                                                         |
| `work_products/valuation_calcs.py`                          | All calculations in this document                                                             |
