# NamSys Inc. (TSXV: CTZ) — Causal Model of the Business

*Prepared September 15, 2026. All dollar figures Canadian unless stated. Fiscal year ends October 31. Every number in this document is an output of `work_products/causal_model_calcs.py`, which tags each input with the filing it came from. This document is stock-price-blind: no quote, market capitalisation, or price-derived multiple is used.*

Source tags used throughout:

| Tag     | File                                                       |
|---------|------------------------------------------------------------|
| `FS23`  | `primary_sources/FY2023/Namsys_-_Annual_FS_-_Feb262024.md` |
| `FS24`  | `primary_sources/FY2024/NamSys_AFS_021925.md`              |
| `FS25`  | `primary_sources/FY2025/NamSys_AFS_022426.md`              |
| `MDA25` | `primary_sources/FY2025/NamSys_MDA_022426.md`              |
| `FSQ2`  | `primary_sources/2Q2026/FS_Q2_NamSys_Apr_30_26_FINAL.md`   |
| `MDQ2`  | `primary_sources/2Q2026/MDA_Q2_NamSys_Apr_30_26_FINAL.md`  |
| `AM25`  | `fetched_docs/namsys_2025_annual_meeting_transcript.md`    |
| `AM26`  | `fetched_docs/namsys_2026_annual_meeting_transcript.md`    |
| `OE`    | `work_products/owners_earnings_and_roic.md`                |
| `OV`    | `work_products/overview.md`                                |

---

## 0. What this document is, and what it deliberately is not

A causal model is a claim about *which variables move which other variables, in what direction, with what lag, and how hard*. It is falsifiable. It is not a forecast, and it is not a list of "key issues" (that is `OV`).

I have built the model around four chains (§2–§5) and six feedback loops (§6). Where a link is measurable from the filings, I measure it. Where the sources only support a direction and not a magnitude, I say so and stop — rather than manufacturing a coefficient. The single most important thing this exercise surfaced is in §3.4, §3.5 and §7: **the business is in the middle of a driver handover that the headline revenue line hides**, and the model says what to watch to tell whether it completes. *Revised after verifier review (round 1): the aggregate deceleration is established, but its cause is ambiguous between broad-base US saturation and a single large account contracting — see §3.5 and §6. Response at `pv/causal_model/r1_response.md`.*

---

## 1. The model in one page

NamSys sells per-endpoint subscriptions to a customer list "measured in dozens, not thousands" (`AM25`) that runs physical cash-handling infrastructure: armoured vehicles, cash vaults, and retail smart safes. Demand is created by the *fixed per-touch cost* of handling cash — "it doesn't matter if you are handling \$500 or \$5,000, the cost to move and count those notes is the same" (`AM26`). Revenue therefore tracks the **count of cash-handling endpoints running NamSys software**, not the dollar volume of cash. Price is a small and rising second-order term, not zero — see §3.1.

Four chains produce the financials:

1. **Revenue chain.** Endpoints per account × accounts × rate per endpoint × USD/CAD. Churn ≈ 0 and price is small (but *not* zero in FY2024–FY2026 — see §3.1), so growth is *predominantly* endpoint growth, which arrives as discrete customer rollout projects. This makes revenue **lumpy on a 1–2 year cycle**, not smooth.
2. **Cost chain.** Cost is ~59% compensation (`FS25` Note 14 vs. `MDA25`) for a 17→21 person fully-remote team (`AM25`, `AM26`). Headcount is hired in steps, ahead of the revenue it serves. So margin is a *ratio of a step function to a growing-but-lumpy numerator* and oscillates.
3. **Currency chain.** ~96% of revenue is USD-billed against a mostly-CAD cost base, unhedged (`FSQ2` Note 11; `MDA25` Risk Factors). This gears operating income to USD/CAD at **~2.0–2.4×** the revenue effect (§3.6).
4. **Capital chain.** The business needs ~\$1M of invested capital to produce ~\$2.3M of owners' earnings (`OE`). There is no internal reinvestment sink, so cash accumulates and earns 2.0–2.45% pre-tax (`FSQ2` Note 15) — below any plausible inflation rate. Value therefore compounds only through (a) capital-free organic growth and (b) distributions.

The economically load-bearing consequence: **NamSys's earnings are geared, in both directions, to a revenue line it does not control the timing of.** Because costs are fixed in the short run, revenue surprises pass through to operating income at roughly 0.9–1.0:1 on the way down *in the first year* (falling to ~0.6–0.7 once headcount is right-sized, §4.4) against ~32–58% on the way up.

---

## 2. The root cause of demand: touch counts, not cash volume

This is the foundation, so it is worth separating the parts that are sourced from the parts that are management's thesis.

**Sourced mechanics.** Cash must be physically transported and counted; the cost of doing so is per-note and per-trip, not per-dollar (`AM26`). NamSys's three products each attack one stage: Cirreon Retail (in-store safes/recyclers), Cirreon CIT (armoured-vehicle route and parcel tracking on handhelds), and Currency Controller (bank/CIT vault processing, deposit and ATM-order fulfilment, reconciliation) (`AM26`; `MDA25` Overview).

**The key structural inference.** Management itself measures its opportunity in *units of physical infrastructure*, not dollars of cash: "on a truck basis, we know that our software runs on approximately 8% of all the... cash and transit vehicles in the US," and the worldwide TAM is "at least 10 times what it is in the US," which is "just trucks, which is a rough correlation towards... what we'd be able to deliver in terms of revenue" (`AM26`). **Inference:** revenue scales with endpoint count. It is an inference, not a disclosure — the filings never state the pricing unit — but management's own use of vehicle count as a revenue proxy is direct support for it.

**Why this matters, and why it is the opposite of the naive "cash is dying" read.** If revenue scales with endpoint *count* rather than cash *volume*, then a moderate secular decline in cash usage is a **tailwind, not a headwind**: volumes fall, the fixed per-touch cost is spread over fewer notes, unit cost rises, and the ROI on efficiency software rises with it. The endpoints still exist and still need running. `MDA25` Risk Factors describe exactly this substitution already happening — retailers won't buy hardware, so "the major currency providers and carriers have for the last few years been transitioning their business to the provision of a complete turnkey service," i.e. the work migrates toward CIT and vault operators, which is where NamSys's two strongest products sit.

The regime only inverts if decline is severe enough to *remove endpoints* — routes cancelled, vaults closed, safes pulled. That is the real bear case on demand, and it is a different question from "is cash's payment share falling."

**What is management assertion, not verified fact.** That cash is "10 to 20 percent of in-person payments in pretty much all major economies including the U.S. and the G7" (`AM26`), and "used for approximately one in five payments" in the US, "not changed since 2020," citing the Federal Reserve's cash diary study (`AM25`). I have not independently verified either figure; no such study is in `primary_sources` or `fetched_docs`. Treat the *stability* claim as unverified and self-interested.

---

## 3. The revenue chain

### 3.1 The identity

```
Revenue_CAD  =  Σ over accounts ( endpoints_i × rate_i )  ×  USD/CAD
```

Growth decomposes into five terms. The filings and transcripts let me size four of them, and the sizes are lopsided:

| Term                              | Contribution to growth                        | Evidence                                                                                                                                                                                                                                                                                                                                                                                                       |
|-----------------------------------|-----------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Expansion (endpoints per account) | **~75% of five-year growth; ~100% of FY2024** | "approximately 75% of it came from purely organic growth amongst our customers" (`AM26`); NRR 112% in FY2024 (`AM25`)                                                                                                                                                                                                                                                                                          |
| New accounts                      | ~25% over five years; ~0.3 pts in FY2024      | `AM26`; arithmetic in §3.3                                                                                                                                                                                                                                                                                                                                                                                     |
| Price                             | **Small, rising, magnitude not disclosed**    | Over five years: "Almost none of it came from price increases." But in the recent window: "we have engaged in price increases... as contracts came up for renewal, we took advantage of our ability to increase prices and recoup some of the inflationary pressure"; these "really started rolling out over the past two, maybe two and a half years" (`AM26`) — i.e. FY2024–FY2026, the window analysed here |
| Churn                             | **~0**                                        | "we experienced no customer churn" (`AM25`); "Historically, we've had little or no churn of customer accounts" (`AM25`)                                                                                                                                                                                                                                                                                        |
| USD/CAD                           | Sign known, magnitude not determinable        | §3.5                                                                                                                                                                                                                                                                                                                                                                                                           |

**The first-order conclusion follows mechanically.** With churn ≈ 0, new accounts ≈ 0 in any given year, price small, and a customer list of a few dozen, revenue growth is *mostly* endpoint growth inside a nearly-static account base. Note the direction of the price caveat: renewal repricing was *ramping up* across FY2024–FY2026, so it is a growth tailwind that was being added during the window in which growth decelerated. Under that reading, underlying endpoint growth decelerated by *more* than the recurring-revenue figures in §3.3 show. The opposite reading — that the repricing wave has now passed through most of the contract base and is exhausted — would instead make price a *contributor* to the deceleration. `AM26` supports neither decisively ("we do have the ability to change pricing more frequently" cuts toward ongoing; a one-per-contract conversion cuts toward exhausted), so **I cannot sign the price effect on the deceleration, and do not build on it either way**. There is no smoothing mechanism. Each large account's expansion is a discrete deployment project, so growth arrives in steps and then plateaus until the next one.

### 3.2 The clearest observed instance of that lumpiness

`AM25` explains the FY2024 acceleration explicitly: "This was the result of one of our large customers rolling out our Cirreon CIT application during the calendar year, and that rollout is now complete and was very successful." Cirreon CIT revenue rose 52% year-on-year in FY2024 (`AM25`).

The quarterly path is exactly what the model predicts after a rollout completes — a step up, then a plateau (`MDA25` and `MDQ2` quarterly tables, \$000s):

| Quarter | Revenue | Sequential | Year-on-year |
|---------|---------|------------|--------------|
| Q1-24   | 1,584   | —          | —            |
| Q2-24   | 1,661   | +4.9%      | —            |
| Q3-24   | 1,741   | +4.8%      | —            |
| Q4-24   | 1,854   | +6.5%      | —            |
| Q1-25   | 1,942   | +4.7%      | +22.6%       |
| Q2-25   | 2,010   | +3.5%      | +21.0%       |
| Q3-25   | 1,917   | −4.6%      | +10.1%       |
| Q4-25   | 2,023   | +5.5%      | +9.1%        |
| Q1-26   | 2,134   | +5.5%      | +9.9%        |
| Q2-26   | 2,134   | **+0.0%**  | **+6.2%**    |

Year-on-year growth falls from +22.6% to +6.2%. The last two quarters are *flat to the dollar* at \$2,134k.

### 3.3 Reconciling management's two retention statements

`AM25` gives net revenue retention of 112% for FY2024 against reported growth of 12.3%. Those two numbers together imply the existing account base contributed ~12.0 points and net-new accounts ~+0.3 points — i.e. in FY2024, essentially *all* growth was expansion inside existing accounts, which is consistent with `AM25`'s own attribution to a single large customer's rollout. `AM26`'s five-year "~75% organic / ~25% net new" split is therefore a five-year average around a much more concentrated single-year reality, not a stable annual mix. **The model should treat the new-account contribution as near zero in any given year and lumpy across years.**

Because churn ≈ 0 and new accounts ≈ 0, **recurring revenue growth is itself the best available NRR proxy**. Important limitation: NRR bundles price and volume by construction, so this is a proxy for *net retention*, not for endpoint growth specifically. Given the price caveat above, the endpoint-only component is somewhat lower than the figures below:

| Period    | Recurring revenue growth | Implied NRR |
|-----------|--------------------------|-------------|
| FY2025    | **+16.3%**               | ~116%       |
| H1 FY2026 | **+6.1%**                | ~106%       |

Source: `MDA25` and `MDQ2` revenue tables. The expansion engine has roughly halved.

### 3.4 The quality-of-growth wedge that the headline hides

H1 FY2026 total revenue grew 8.0%, but *recurring* revenue grew only 6.1% and Q2 recurring only 5.3% (`MDQ2`). Professional services — explicitly non-recurring "special projects that we take on from time to time" (`AM25`) — went from \$21,936 to \$96,457, contributing **23.6% of the entire dollar increase in revenue** off a 0.5% revenue base. In FY2025 the effect ran the other way: professional services *shrank*, so recurring growth (16.3%) exceeded total growth (15.4%).

So the true deceleration in the durable revenue line is **16.3% → 6.1%**, which is worse than the headline 15.4% → 8.0%. This is the most important single number in the model and it is not visible on the face of the income statement.

### 3.5 The geographic driver handover — and why it is FX-immune

Almost everything is billed in USD (`FSQ2` Note 11: ~96%, both years), and Canada is ~3.7% of revenue. So comparing the US region against the international regions **cancels the currency effect**: both legs are translated at the same rate. This is the one clean cut available in the data.

| Period          | US revenue growth | Intl ex-Canada growth | US share of revenue | Intl ex-Canada share |
|-----------------|-------------------|-----------------------|---------------------|----------------------|
| FY2023 → FY2025 | +24.2% (2 yrs)    | +53.1% (2 yrs)        | 75.8% (FY2025)      | 20.6% (FY2025)       |
| FY2024 → FY2025 | +13.2%            | +23.6%                | 75.8%               | 20.6%                |
| H1FY25 → H1FY26 | **+3.5%**         | **+26.2%**            | 73.5% (H1FY26)      | 22.8% (H1FY26)       |

Source: `FS23`/`FS25`/`FSQ2` Note 7 geographic tables. Growth contributions to the H1 FY2026 total of +8.0%: US **+2.69 pts**, international ex-Canada **+5.11 pts**, Canada +0.19 pts (sums to 7.98 pts — ties to reported).

**This is the central finding of the causal model — but it has a live alternative explanation that the data cannot currently rule out.** The US — three-quarters of the business, the market management says it "understands... very well" (`AM25`) — has decelerated to ~3.5% *in aggregate*.

**The alternative: one account, not broad saturation.** §3.7 shows the rank-#1 customer's revenue fell \$132,546 in the same half-year window (\$691,576 → \$559,030, −19.2%). Total US dollar growth was only +\$106,362. If that account sits in the US bucket — a priori likely, since the US is 73.5% of revenue — then stripping it from *both* the numerator and the base gives **US ex-#1 growth of +10.2%** (\$2,339,322 → \$2,578,230), not 3.5%. On that reading the US installed base is not saturating at all; a single large account fell off a cliff while the rest of the US grew double digits. Sizing it another way: had US revenue grown at its FY2025 rate of 13.2%, H1 FY2026 would have added \$400,169 instead of \$106,362; the rank-#1 decline alone covers **45.1%** of that \$293,807 shortfall. (Calculations in `causal_model_calcs.py` §12.)

**Why this cannot be settled from the filings.** Rank-slot identity is not disclosed (§3.7), and the geographic note does not break out customers. What *is* corroborating for the single-account reading: over-90-day trade receivables tripled to \$237,066 (`FSQ2` Note 3) and the company wrote off two customers in FY2025 and one in H1 FY2025 (`FS25` Note 3; `MDQ2`) — the pattern of a large account in distress rather than a base growing slowly. **I should have connected §3.5 and §3.7 before asserting the conclusion, and did not.** The honest statement is: *the aggregate deceleration is real and is not an artefact of attribution — recurring revenue growth of 6.1% and two flat sequential quarters are facts independent of which customer caused them — but the mechanism behind it is genuinely ambiguous between broad-base saturation (Loop C) and a single-account event (Loop E), and the latter now has the better circumstantial case.*

Note which way this cuts: Loop E is **not** the more benign reading. It is the realisation of the concentration risk sized at ~31–36% of year-one operating income in §4.4, via the exact mechanism `MDA25` Risk Factors describe.

Setting that aside, the international leg stands on its own: All of the momentum is a still-small international base compounding at ~26% (Mexico alone: \$381,617 → \$558,412, +46.3%). International is a *real* driver, not a story: the ISO/IEC 27001:2022 certification obtained February 2026 was explicitly framed as unlocking non-North-American customers (Knowledge Store ID 4), and `AM26` reports direct hires in the UK and Australia after the reseller channel had failed (`AM25`: "we've tried many times to work with resellers and integrators and had little to no success").

The arithmetic of the handover cuts in NamSys's favour *if the two rates hold*, because the fast-growing leg's weight rises each year (calculation in `causal_model_calcs.py`):

| Horizon | Implied total growth | Intl ex-Canada weight |
|---------|----------------------|-----------------------|
| +1 yr   | 8.6%                 | 26.5%                 |
| +2 yrs  | 9.4%                 | 30.5%                 |
| +3 yrs  | 10.3%                | 34.9%                 |

That is a mechanical projection of a two-point extrapolation, not a forecast. Its value is diagnostic: it shows that **~10% total growth requires international to stay above ~25% for years, and it shows that the model is now a bet on international execution rather than on the US installed base.**

### 3.6 On the currency term: what I can and cannot say

- **Sensitivity (computed; range, not a point estimate).** A 5% USD/CAD move changes FY2025 revenue by \$378,797 (4.8% of revenue). How much reaches operating income depends on the USD share of the cost base, which is **not disclosed**: `MDA25` says only that "the *majority* of our expenses, including employee wages, have been denominated in Canadian dollars" — "majority," not the "approximately 96%" precision used on the revenue side. Elasticity = (0.96 × Revenue − USD cost share × Operating cost) ÷ Operating income:

| USD share of cost base | Elasticity | 5% move → operating income |
|------------------------|------------|----------------------------|
| 0% (upper bound)       | 2.41×      | 12.0%                      |
| 10%                    | 2.26×      | 11.3%                      |
| 15%                    | 2.18×      | 10.9%                      |
| 25%                    | 2.03×      | 10.2%                      |
| 30%                    | 1.96×      | 9.8%                       |

  Bounding the USD cost share from what *is* disclosed: USD trade payables were US\$61,310 against total trade and other payables of \$360,682 (`FSQ2` Note 11 and statements of financial position) — 17–24% of payables depending on the rate. Against that, compensation is 58.6% of operating cost, the team is Canada-based, and the international hires are in the UK and Australia (`AM26`) — i.e. GBP/AUD, not USD — so the USD tail is mainly cloud hosting. **Plausible range 10–25%, giving an elasticity of ~2.0–2.3×; 2.41× is a ceiling.** I use **~2.0–2.4×** throughout. Each 1% of CAD appreciation costs roughly 2.0–2.4% of operating income. The conclusion is unchanged: NamSys is materially FX-geared and unhedged by policy.
- **Direction in H1 FY2026 (inference).** The reported FX loss of \$102,941 (`MDQ2`) arises, per the company's own description of the mechanic, "when the Canadian dollar amount of the receivable at period end, or the amount received in the period, is [less] than at the time of invoicing" (`MDA25`). A loss therefore means the CAD strengthened inside the invoice-to-collection window, so the year-on-year translation effect on reported CAD revenue was also adverse. Management confirms the same channel for FY2025: the Q3-25 sequential dip was "primarily due to exchange rates" and "on a U.S. dollar basis, the revenue actually increased sequentially between Q2 and Q4" (`AM26`).
- **Magnitude (not determinable).** The FX loss measures a ~2-month rate change (30-day terms, 59-day DSO); the revenue translation effect measures a ~12-month average-rate change. They are not convertible. I bound the y/y drag loosely at 0–5 points and **build no conclusion on the point estimate**. No FX rate series exists in `primary_sources`, `work_products`, `fetched_docs`, or the Knowledge Store; quoting one would be from internal AI model knowledge and I decline to make the model depend on it.

This is why §3.5 matters so much: the US-versus-international gap of ~23 points is *immune* to the FX uncertainty, because both legs carry the same rate. Whatever FX did, it did it to both.

### 3.7 The account-level texture inside the aggregate

`FS25` Note 7 and `FSQ2` Note 7 disclose the top three customers' revenue shares each period. Converting to dollars (annualised for half-years):

| Period | Rank #1    | Rank #2    | Rank #3  | Top 3 share |
|--------|------------|------------|----------|-------------|
| FY2024 | $1,368,029 | $608,773   | $608,773 | 37.8%       |
| FY2025 | $1,254,765 | $970,667   | $844,402 | 38.9%       |
| H1FY25 | $1,383,152 | $987,966   | $766,661 | 39.7%       |
| H1FY26 | $1,118,060 | $1,092,456 | $972,969 | 37.3%       |

**Caveat, and it is a real one:** the filings never identify these customers, so rank slot #1 in one period may not be the same company as rank slot #1 in another. Subject to that, the pattern is: **the largest account shrank in absolute dollars** (−8.3% FY2024→FY2025; −19.2% H1FY25→H1FY26) while #2 and #3 grew +17.7% in H1 FY2026. Two readings are consistent with the data — either the top account genuinely contracted, or reshuffling produced the appearance. Both are informative: the first says "zero churn" can coexist with meaningful account *contraction*, which is a gap in the retention narrative; the second says the top of the account base is converging in size, which slightly reduces single-name risk (top-3 concentration did fall from 39.7% to 37.3%).

---

## 4. The cost chain: a step function under a lumpy numerator

### 4.1 Cost is compensation, and compensation is headcount

FY2025 total operating cost (revenue less operating income) was \$4,745,129, of which the Note 14 compensation figure of \$2,781,506 is **58.6%** (`FS25` Note 14; `MDA25`). There is no capitalised software, no meaningful PP&E (\$34,689), no debt, and a fully-remote workforce with immaterial occupancy cost (`OE` §2; `FS25` Note 4). So the cost line is, to first order, *people*.

Headcount: 17 at the April 2025 meeting and through FY2024–FY2025 ("stable at 17 employees"; `MDA25` attributes the FY2025 gross-margin gain to "the level of staffing resources remaining relatively flat year-over-year"), rising to 21 by April 2026, "half development and half support" (`AM25`, `AM26`). That is **+23.5% headcount**.

A cross-check that validates the headcount inputs: `AM25` claims revenue per employee of "400,000 per employee" for FY2024. \$6,840,146 ÷ 17 = **\$402,362**. It ties, which confirms 17 as the FY2024 base rather than an interview approximation.

### 4.2 The margin mechanism, stated as a cycle

Because revenue is lumpy and headcount is a step function, gross margin is a ratio of a step to a staircase and therefore *oscillates rather than trends*. The last two periods are the two phases of one cycle:

| Period          | Revenue growth | Cost-of-sales compensation growth | Gross margin change |
|-----------------|----------------|-----------------------------------|---------------------|
| FY2024 → FY2025 | +15.4%         | **+2.9%**                         | **+2.0 pts**        |
| H1FY25 → H1FY26 | +8.0%          | **+20.4%**                        | **−2.9 pts**        |

Source: `MDA25`, `MDQ2`, and Note 14 in `FS25`/`FSQ2`. `MDQ2` states the cause in its own words: the decline is "mostly due to a higher staffing level, as a result of recent team additions, and an increase in staff compensation."

An operating-margin bridge confirms that compensation-versus-revenue is essentially the *whole* story of NamSys's margin history (bad debt removed from both halves so they compare; half-years compared only against half-years, since selling expense is seasonal):

| Period               | Revenue    | Operating margin | Compensation / revenue | Non-comp cost / revenue |
|----------------------|------------|------------------|------------------------|-------------------------|
| FY2023               | $6,093,020 | 34.6%            | 39.7%                  | 25.7%                   |
| FY2024               | $6,840,146 | 37.6%            | 36.6%                  | 25.7%                   |
| FY2025               | $7,891,605 | 39.9%            | 35.2%                  | 24.9%                   |
| H1FY25 (ex-bad-debt) | $3,951,863 | 42.4%            | 34.4%                  | 23.2%                   |
| H1FY26 (ex-bad-debt) | $4,267,406 | 41.6%            | 36.1%                  | 22.3%                   |

- FY2023 → FY2025: operating margin +5.3 pts, of which the falling compensation ratio explains +4.4 pts — **84% of the entire margin expansion**. There is no second mechanism worth modelling.
- H1FY25 → H1FY26: operating margin −0.7 pts, from compensation ratio **+1.6 pts** (drag) partly offset by non-compensation **−0.9 pts**. The offset is discretionary: `MDQ2` reports travel and trade-show costs down \$26,751. **So the reported margin resilience in H1 FY2026 is partly the result of cutting the international-expansion spend that is supposed to drive the very growth the hiring was for.** That is an internal tension in the current plan, not a criticism of the arithmetic.

### 4.3 The hiring bet, priced

Two ways of asking "how much revenue does the current cost base need?":

| Test                                                                                               | Revenue required | vs. FY2025 actual | vs. H1FY26 annualised (\$8,534,812) |
|----------------------------------------------------------------------------------------------------|------------------|-------------------|-------------------------------------|
| Restore FY2025 gross margin (64.4%) at the annualised H1FY26 cost-of-sales run-rate of \$3,192,274 | **\$8,955,000**  | +13.5%            | +4.9%                               |
| Restore FY2025 revenue per employee (\$464,212) at 21 staff                                        | **\$9,748,000**  | +23.5%            | +14.2%                              |

The first test is the near-term one and it is **not far away** — roughly five points of revenue above the current run-rate restores the FY2025 gross margin, provided headcount holds at 21. The second is the multi-year test of whether the international hires were worth making.

One caveat that makes the drag *worse*, not better: annualised compensation per head appears to fall from \$160,165 (H1FY25 at 17 staff) to \$146,610 (H1FY26 at 21 staff), which cannot be right given `MDQ2` explicitly cites "an increase in staff compensation." The resolution is that 21 is the headcount *as at* April 2026 (`AM26`) while the H1 compensation figure reflects a lower average headcount over the half. **Inference:** the full run-rate cost of the hiring is not yet in the reported numbers, so the H2 FY2026 margin drag should be somewhat larger than H1's at constant revenue.

**This is the crisp statement of the bet:** management spent 2.9 points of gross margin in the half (4.7 points in Q2 alone, `MDQ2`) — \$356,014 of annualised incremental compensation — on +4 employees aimed at international time-zone and language coverage (`AM25`, `AM26`). The international leg is growing 26%. If that holds for ~2 years with headcount flat, the margin comes back and then some. If international decelerates toward the US's 3.5% while 21 people stay on the payroll, margin stays down and earnings stall.

### 4.4 Downside asymmetry — the part that is easy to miss

Fixed costs cut both ways. Incremental operating margin:

| Window                       | Δ operating income | Δ revenue  | Incremental margin |
|------------------------------|--------------------|------------|--------------------|
| FY2023 → FY2025              | $1,039,042         | $1,798,585 | **57.8%**          |
| H1FY25 → H1FY26, as reported | $152,591           | $315,543   | 48.4%              |
| H1FY25 → H1FY26, ex-bad-debt | $101,845           | $315,543   | **32.3%**          |

(Both half-year operating-income figures were rebuilt from the `MDQ2` expense lines and tie to the quarterly table: \$1,623,346 vs. 822+805 = \$1,627k; \$1,775,937 vs. 941+838 = \$1,779k.)

On the way *down*, there is no 58% or 32% — a lost customer removes revenue while 21 salaries continue, so the pass-through is ~100% in the first year. Sizing it with the disclosed concentration: the largest account was 13.1% of H1 FY2026 revenue (`FSQ2` Note 7) = \$559,030 in the half, i.e. **\$1,118,060 annualised** — the same figure §3.7 reports. **How much of that is really lost? Less than 100%, and the time horizon matters.** Some cost does go with the customer. FY2025 cost of sales was \$2,813,196, of which compensation was \$1,739,266 (61.8%), leaving a \$1,073,930 non-compensation residual — presumably mostly cloud hosting, though *the filings never disaggregate it* (Note 14 discloses only compensation), so that attribution is an **inference**. Annualised compensation per employee is \$146,610 (H1FY26, 21 staff). Scenarios (`causal_model_calcs.py` §13):

| Scenario                                                | Δ operating income | % of FY2025 op. income | Pass-through |
|---------------------------------------------------------|--------------------|------------------------|--------------|
| A. Year 1, nothing cut (contractual salaries continue)  | −\$1,118,060       | −35.5%                 | 100%         |
| B. + non-comp cost of sales falls pro-rata with revenue | −\$971,759         | −30.9%                 | 86.9%        |
| C. B + one support FTE not replaced                     | −\$825,149         | −26.2%                 | 73.8%        |
| D. B + two support FTEs not replaced                    | −\$678,539         | −21.6%                 | 60.7%        |
| E. B + three support FTEs not replaced                  | −\$531,929         | −16.9%                 | 47.6%        |

Even scenario B is generous in year one: on a multi-tenant SaaS platform the *marginal* hosting cost of one tenant is below the average, since base environments, monitoring and the ISO 27001 control set are fixed. Three specific frictions hold the near term close to A–B: (i) the **\$1,100,000 employee termination commitment to three employees** (`FS25` Note 13) means cutting senior staff carries a cash cost roughly equal to a year of the lost revenue; (ii) revealed preference — headcount went 17 → 21 *while* growth decelerated from 15.4% to 8.0% (`AM25`, `AM26`), so this management does not cut into weakness; (iii) 21 people covering three products and multiple time zones is thin to begin with. Over two to three years, attrition (no payout) rather than termination can get to C–D.

**Sanity check against the observed incremental margin.** Upside incremental margin was 57.8% (FY2023→FY2025) and 32.3% (H1FY26 ex-bad-debt), which under perfect symmetry would imply 32–58% downside pass-through — scenarios D–E. But the upside figure embeds *growth* spending (international sales and support hires) that would not reverse on losing a customer, so true steady-state pass-through should sit **above** that range, i.e. toward C–D.

**Revised statement, replacing the ~100% shorthand:** losing the largest account costs roughly **31–36% of operating income in year one** (pass-through 87–100%) and roughly **22–26% in steady state after right-sizing** (pass-through 61–74%). The qualitative point stands and is what matters for the causal model — the cost base does not flex with revenue on anything like a quarterly timescale, so revenue shocks land almost entirely on earnings before management can respond — but the permanent impairment is meaningfully smaller than the first-year hit.

And this is not a hypothetical risk category — `MDA25` Risk Factors describe the specific mechanism by which it happens without NamSys doing anything wrong: "When two banks merge, the continuing entity usually selects one technology provider for a given function. Our experience in the past would suggest that the provider with the largest installed base in the combined entity will replace the provider with the smaller installed base." That is a winner-take-most rule applied to an end-market management describes as already highly consolidated — "approximately 75% of that market on the CIT side is controlled by Brinks and Loomis and Garda" (`AM26`).

---

## 5. The capital chain: an engine with no gearbox

Established in `OE` and not re-derived here: operating invested capital is ~\$1M against ~\$2.3M of owners' earnings, four-year cash conversion is ~99%, and there is no debt and no capitalised software. The causal consequence is that **growth consumes no capital** — FY2022→FY2025 added ~\$2.5M of revenue and ~\$1.1M of owners' earnings on ~\$150k of incremental operating capital (`OE` §3.2).

The corollary is the part that matters causally: **there is no internal reinvestment sink, so retained cash is a negative-carry asset.** At April 30, 2026 the company held \$7,366,047 of cash and short-term investments (`FSQ2` statements of financial position) in GICs yielding 2.0–2.45% pre-tax (`FSQ2` Note 15) — \$147,321–\$180,468 pre-tax, or \$108,281–\$132,644 after tax at the 26.5% rate (`MDA25`), i.e. **1.5–1.8% nominal**. Interest income on short-term investments has been *falling* even as the average balance rose: \$273,084 (FY2024) → \$235,681 (FY2025), and \$115,058 → \$95,212 across the half-years (`MDA25`, `MDQ2`).

The intended gearbox is acquisition, and it has not engaged: "We have been focused for several years on an acquisition strategy. That has not been successful, but it is not for lack of trying" (`AM26`), against criteria that are genuinely restrictive — right size, product-synergistic, technologically compatible, already profitable, "not a turnaround story" (`AM26`). Management has now added a new reason the gearbox may never engage: with AI having changed software-development economics "so dramatically in the past... six plus months," the question becomes "is it cheaper for us to build that rather than buy it?" (`AM26`).

So the capital chain terminates in distribution by default, which is what the record shows: a \$1,350,477 special dividend paid June 2024 (`MDA25`, "Special Dividend"), a \$4,027,790 special dividend paid March 12, 2026 (`FSQ2` Note 6), plus continuous NCIB buybacks — \$240,996 for 187,100 shares in H1 FY2026 alone (`MDQ2`, "Outstanding Securities Data"). **Causally: compounding at NamSys happens at the shareholder level, not inside the company.** The intrinsic growth rate is set by sales capacity and market penetration, and ROIC — however computed — is not the binding constraint (`OE` §5).

---

## 6. The feedback loops

| # | Loop                           | Sign           | Mechanism                                                                                                                                                                          | Strength of evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|---|--------------------------------|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| A | Capital-free growth            | + but **open** | Endpoints ↑ → revenue ↑ with ~no incremental capital → cash ↑ → *no reinvestment sink* → distribution                                                                              | Strong. `OE` §3.2; dividend/NCIB record. The loop does not close internally — this is why it does not compound.                                                                                                                                                                                                                                                                                                                                                                                                              |
| B | Platform entrenchment          | +              | Multi-product attach across the cash supply chain → NamSys sits between banks, CIT firms and retailers → switching cost rises → churn stays ~0 → expansion continues               | Moderate. Mechanism is real and observable (Currency Controller "often deployed in combination with the CIT application and is mission critical as it handles most of the cash and transit to bank integration," `AM25`; zero churn, `AM25`; stable ~40/40/23 product mix with "all these products growing at approximately the same rate," `AM26`). The MCP/agent-interoperability extension of it (`AM26`) is forward-looking assertion with no results yet.                                                               |
| C | Expansion exhaustion           | **−**          | Dozens of accounts + ~0 churn + ~0 price + ~0 new accounts → growth must decay as each account's endpoint penetration saturates, unless new accounts or new geographies replace it | **Strong and currently firing.** Recurring growth 16.3% → 6.1%; US growth → 3.5%; two flat sequential quarters; the FY2024 rollout that drove the prior step-up is "now complete" (`AM25`). This is the dominant loop right now.                                                                                                                                                                                                                                                                                             |
| D | AI symmetry                    | − (long)       | AI cuts build cost for NamSys *and* for competitors *and* for customers → integration moat erodes → pricing power capped                                                           | Moderate; management's own framing. "The pressure to keep prices static is going to increase just because customers are going to ask themselves, can I build something like this myself"; "pricing power is something that has been impacted by AI" (`AM26`). **Near-term P&L impact is small precisely because price already contributes ~0 to growth** — there is no pricing tailwind to lose. The real exposure is long-term and concentrated in the largest accounts, which are the ones with the resources to insource. |
| E | Consolidation winner-take-most | − (event)      | End-market M&A → surviving entity standardises on the larger installed base → an account is won or lost wholesale, independent of product quality                                  | Strong mechanism, unknowable timing. `MDA25` Risk Factors; three-player 75% CIT concentration (`AM26`). Fixed costs make each event ~1:1 to operating income (§4.4).                                                                                                                                                                                                                                                                                                                                                         |
| F | FX                             | ± (exogenous)  | USD/CAD → 96% of revenue, ~10–25% of cost → ~2.0–2.4× gearing on operating income                                                                                                  | Strong and computed. Purely exogenous; unhedged by policy (`MDA25`). Adds ±10%-order noise to operating income on ordinary currency moves and can mask or mimic 2–4 points of underlying growth.                                                                                                                                                                                                                                                                                                                             |

**Which loop dominates — revised after review.** Something is clearly slowing the top line: recurring growth of 6.1% and two flat sequential quarters are facts. But **Loop C and Loop E are not distinguishable from the available data, and Loop E has the better circumstantial case** (§3.5): US growth ex the rank-#1 account is ~10.2%, the rank-#1 account fell 19.2%, over-90-day receivables tripled, and three customers have been written off in two years. So Loop E is *not* an option-like tail risk — it may already be the operative mechanism. This matters for forecasting: Loop C predicts a durable ~3–6% US grind; Loop E predicts a one-off step down that could stabilise, reverse, or repeat unpredictably, with fat tails in both directions. Loop B has not yet produced an offset. Loop A guarantees that whatever earnings exist convert to cash and get distributed. Loop D is a long-dated cap on the price lever. Loop F is large-amplitude exogenous noise. **A model of NamSys that treats the deceleration as settled broad-base saturation is over-confident; the correct posture is that the aggregate slowdown is established and its cause is not.**

---

## 7. What the model says the business is doing right now

Assembling the chains: NamSys is mid-way through a **driver handover from a saturating US installed base to a small, fast-growing international one**, and it has pre-paid the cost of that handover in headcount.

**Caveat added after review:** the US half of that statement may be wrong. If the rank-#1 account's \$132,546 decline sits in the US bucket, US revenue ex that account grew ~10.2%, and there is no saturation to hand over from — only a concentration event to absorb (§3.5). The international half of the statement is unaffected.

The evidence that the handover is real and on track:

- International ex-Canada growing 26.2% versus US 3.5% — an FX-immune comparison (§3.5).
- Mexico +46.3% in H1 FY2026; ISO 27001 certification obtained specifically to clear non-North-American customer security requirements (Knowledge Store ID 4).
- Direct-hire international model replacing the reseller model that management says failed for structural, well-articulated reasons (`AM25`).
- Headcount and support/time-zone investment already in the cost base (`AM26`), so the spend is sunk, not pending.

The evidence that it may not complete on the current schedule:

- Recurring revenue growth of 6.1% is the weakest in the available record, and two sequential quarters are flat.
- Headline growth of 8.0% is flattered by \$74,521 of non-recurring professional services — 23.6% of the dollar increase (§3.4).
- Trade-receivable quality is deteriorating on a clear trend: DSO 45.7 → 53.9 → 59.2 days, and over-90-day balances \$16,861 → \$126,998 → \$237,066, now **17.8% of trade receivables**, against "generally 30 day terms" (`FS25` Note 3; `FSQ2` Note 3). FY2025 already produced \$51,330 of write-offs from two customers (`FS25` Note 3). *Causal reading:* if the international push is bringing on customers in jurisdictions with slower payment behaviour, receivable ageing is the leading indicator of a growth-quality problem and eventually of bad debt. This is an inference — the filings do not attribute the ageing to any region — but it is the most testable early-warning signal in the model.
- The non-compensation cost cuts that cushioned reported margin were travel and trade-show spend (`MDQ2`) — the input to international selling.

Management's own statements are, notably, consistent with the model rather than in conflict with it: margins "will remain stable going forward" (not expanding), and AI-driven feature velocity will be "offset by the need for more support" so margin expansion is a long-term possibility only, "as soon as features stabilize" (`AM26`). Management is describing a period of *reinvestment with flat margins*, which is exactly what §4.2 measures.

---

## 8. Sensitivity summary — where the earnings actually come from

Each row is a computed elasticity or pass-through, not an assumption. Base is FY2025 (operating income \$3,146,476; revenue \$7,891,605).

| Driver moved by...                                            | Effect on operating income                                                                                              | Confidence                                                                                                                                                                                                                      |
|---------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| USD/CAD ±5%                                                   | ∓\$343,000 to ∓\$379,000 = ∓10.2% to ∓12.0% (elasticity ~2.0–2.4×)                                                      | High on the range; the USD share of the cost base is undisclosed (`MDA25` says "majority" CAD), so no point estimate is defensible (§3.6)                                                                                       |
| Revenue +\$1 of organic growth (observed range)               | +\$0.32 to +\$0.58                                                                                                      | Medium — range is the observed FY23→FY25 (57.8%) vs. H1FY26 ex-bad-debt (32.3%) incremental margin; the low end already carries the recent hiring                                                                               |
| Revenue −\$1 (lost account)                                   | ≈ −\$0.87 to −\$1.00 in year 1; ≈ −\$0.61 to −\$0.74 in steady state                                                    | Medium-high — year-1 stickiness is well grounded (contractual salaries; \$1.1M termination commitment, `FS25` Note 13); the steady-state figure depends on a variable/fixed split of cost of sales that is not disclosed (§4.4) |
| Loss of the single largest customer (13.1% of H1FY26 revenue) | −31% to −36% of operating income in year 1; −22% to −26% in steady state                                                | High on arithmetic; rank-slot identity unverified (§3.7) and timing unknowable                                                                                                                                                  |
| Headcount 17 → 21, revenue flat                               | −\$356,014 (annualised H1FY26 total compensation increase: \$1,539,406 vs. \$1,361,399 per half, `FS25`/`FSQ2` Note 14) | High                                                                                                                                                                                                                            |
| Revenue to \$8.96M with headcount at 21                       | Restores the FY2025 64.4% gross margin                                                                                  | High — arithmetic on the H1FY26 run-rate                                                                                                                                                                                        |
| Surplus cash \$7.37M                                          | +\$108k–\$133k after tax, i.e. ~4–6% of owners' earnings, earning below inflation                                       | High                                                                                                                                                                                                                            |

**Read the table as a whole and the conclusion is uncomfortable but clear:** the two largest swing factors on reported earnings — currency and single-account retention — are both things NamSys does not control and does not hedge. The factor it does control (organic endpoint growth) is the smallest per-unit mover and the slowest.

---

## 9. Falsifiers and monitorables

The model makes specific, checkable predictions. In rough order of diagnostic value per unit of effort:

1. **Recurring revenue growth, not total revenue.** The model says the durable driver decelerated to 6.1%. *Falsified if* recurring growth re-accelerates above ~10% without a professional-services contribution. *Confirmed if* it stays at 5–7%.
2. **The US line in Note 7, read *jointly* with the top-customer shares in the same note.** This is now the decisive test, and it must be done as one test, not two. If US growth recovers toward double digits while the rank-#1 share keeps falling, the cause was a single account (Loop E) and the rest of the US base is healthy. If US growth stays ~3–5% while the rank-#1 share stabilises, the cause is broad saturation (Loop C). If both deteriorate, it is both. Also watch for a new large-account rollout announcement — the specific event that resets Loop C.
3. **International ex-Canada growth rate.** Must stay above ~25% for the handover arithmetic in §3.5 to work. *Falsified if* it drops toward 10%, at which point total growth converges to ~6% and the 21-person cost base is stranded.
4. **Cost-of-sales compensation (Note 14) versus revenue.** The model says margin recovers only if compensation growth falls below revenue growth. Note 14 is disclosed every quarter and is the cleanest early read on the margin cycle. Headcount disclosure at the annual meeting is the corroborating datapoint.
5. **Over-90-day trade receivables (Note 3).** \$16,861 → \$126,998 → \$237,066. *Confirms* a growth-quality problem if it keeps rising as a share of receivables; *falsifies* my inference if it reverses while international growth continues.
6. **Top-3 customer shares (Note 7).** The one place account-level dynamics surface. A rank-slot share falling while total revenue grows is account contraction, which would contradict the "zero churn ⇒ healthy retention" framing.
7. **Any acquisition closing.** Would invalidate §5's conclusion that compounding happens only at the shareholder level, and would introduce integration risk and a capital base the model currently says does not exist.
8. **Professional services revenue.** If it stays elevated, the revenue mix is becoming less recurring — note recurring fell from 99.0% of revenue in FY2025 to 97.7% in H1 FY2026 (`MDA25`, `MDQ2`).

---

## 10. Confidence ledger

**High confidence — arithmetic on disclosed figures, minimal estimation:**

- Cost is ~59% compensation and headcount-driven; the compensation ratio explains ~84% of the FY2023→FY2025 operating-margin expansion and the entirety of the H1 FY2026 compression.
- Operating income is geared ~2.0–2.4× to USD/CAD, unhedged. (The 2.41× ceiling assumes a 100%-CAD cost base; `MDA25` says only "majority," so the range, not the point, is the finding.)
- US revenue grew 3.5% versus international ex-Canada 26.2% in H1 FY2026, and this comparison is currency-neutral.
- Recurring revenue growth decelerated from 16.3% to 6.1%; 23.6% of H1 FY2026's dollar growth was non-recurring professional services.
- Growth consumes essentially no capital; ~100% of owners' earnings is distributable; surplus cash earns 1.5–1.8% after tax.
- Fixed costs make revenue loss roughly 0.87:1 to 1:1 to operating income **in year one**; losing the largest customer costs ~31–36% of operating income then, falling to ~22–26% once support headcount is right-sized (§4.4). The variable/fixed split within cost of sales is not disclosed, so the steady-state figure is the softer of the two.
- Receivable ageing is deteriorating on a three-period trend.

**Genuine uncertainty — directionally supported, magnitude unresolved:**

- **How much of the H1 FY2026 slowdown is FX versus volume.** Sign is established; magnitude is not determinable from available sources (§3.6). This is the largest single gap in the model. It matters because it determines whether US volume growth is ~3.5% (bad) or ~6.5% (merely slow).
- **Whether the US deceleration is broad-base saturation, a gap between rollouts, or one large account contracting.** All three are consistent with the data; the third has the strongest circumstantial support (§3.5: US ex-rank-#1 grew ~10.2%). Distinguishing them requires the next 2–3 quarters of the Note 7 geographic and top-customer disclosures read together. **This is now the largest open question in the model, ahead of the FX magnitude.**
- **How much of FY2024–FY2026 growth was renewal repricing rather than endpoint expansion.** Management confirms repricing began in that window but never sizes it (§3.1). It is not even signed as to its effect on the *deceleration*.
- **Whether rank-slot #1's dollar decline is a real account contraction.** Customer identity is not disclosed (§3.7).
- **Endpoint-based pricing.** The load-bearing structural inference of §2. Supported by management's use of vehicle count as a revenue proxy, never disclosed directly.

**Management assertion, not independently verified:**

- Cash's share of payments and its stability (`AM25`, `AM26`).
- Zero churn (a company statement; no cohort data is published).
- The "at least 10×" international TAM — explicitly a truck-count proxy, and `AM26` itself concedes the market "is not covered by a lot of researchers, a lot of it is kind of almost anecdotal."
- The MCP/agent interoperability moat (`AM26`) — a strategy with no results yet, and symmetric by construction, since competitors can build the same interfaces.

---

## 11. Calculation reference

All figures in this document are produced by `work_products/causal_model_calcs.py`. Run with `uv run python work_products/causal_model_calcs.py`. The script's sections map to this document as follows: §1 → doc §3.1/3.4; §2 → doc §3.5; §3 → doc §3.6; §3b → doc §3.2; §4 → doc §4.1/4.3; §4b → doc §4.2; §5 → doc §4.4; §6 → doc §3.7; §7 → doc §3.3; §8 → doc §7; §9 → doc §5; §10 → doc §2. Every input in the script carries a source tag in a comment.
