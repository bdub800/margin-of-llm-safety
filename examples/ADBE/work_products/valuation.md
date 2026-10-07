# Adobe Inc. (ADBE) — Intrinsic Valuation, FY2026E–FY2030E + Terminal Value

*Prepared 2026-09-01; revised 2026-09-01 after prover/verifier review (`pv/sotp/r1_review.md`, response in `pv/sotp/r1_response.md`). All arithmetic is in `work_products/valuation_calcs.py` (run with `uv run python work_products/valuation_calcs.py`). This step combines, without altering, the owners' earnings forecast in `work_products/forecast_earnings.md` (and its calc script), the terminal value in `work_products/terminal_value.md` (and its calc script), and the balance-sheet work in `work_products/owners_earnings_and_roic.md` (and its calc script). This valuation is deliberately **trading-price blind** — Adobe's current share price and market capitalisation are not used as an input anywhere below.*

---

## 1. Answer first

| Basis                                                            | Discount rate | Intrinsic value / diluted share |
|-------------------------------------------------------------------|---------------|----------------------------------|
| **Probability-weighted** (headline)                              | 15%           | **~$278**                       |
| Base case only (40%-weighted scenario)                            | 15%           | ~$298                            |
| SEVERE case (15%-weighted scenario)                                | 15%           | ~$104                            |
| BEAR case (25%-weighted scenario)                                  | 15%           | ~$183                            |
| BULL case (20%-weighted scenario)                                  | 15%           | ~$487                            |

*(Computed, `valuation_calcs.py` §2.)*

**The headline number is ~$278 per diluted share, built from a probability-weighted owners' earnings stream discounted at 15%, plus a probability-weighted terminal value at the end of FY2030, plus today's standalone excess cash and short-term investments, less today's total debt-like items (including, per revision, the PV of off-balance-sheet hosting commitments), divided by today's diluted share count.** That is the single most defensible point estimate this model can produce, but the four-scenario spread ($104–$487) is the honest content of the answer: **it is a ~4.7× range from the least to most favourable weighted scenario**, driven almost entirely by whether generative AI substitutes or merely augments Adobe's creative workflows — the same open question that dominates both upstream work products (`work_products/forecast_earnings.md` §9, `work_products/terminal_value.md` §9).

**Three things to hold onto about how this number is built, because each one moves the answer by double digits of dollars per share:**

1. **The terminal value is 72% of enterprise value at the 15% discount rate** (computed, §2 below). This valuation is overwhelmingly a bet on what Adobe is worth as an ongoing concern in 2030, not on the five explicit forecast years. Everything said about the fragility of the terminal multiple in `work_products/terminal_value.md` (§8, §9) — especially that 38% of the weighted terminal value comes from the 20%-probability bull case — applies with full force here.
2. **The discount rate is a stated variable, not a fitted one.** At 15% the answer is $278; at 10% it is $327; at 20% it is $238 (computed, §4 below) — a ±16% swing on the headline number from a ±5pp change in the rate. The brief fixes 15%; I have not second-guessed it, but the reader should not treat $278 as more precise than a ±16%-per-5pp-of-rate number can be.
3. **The equity bridge is meaningfully negative** (−$8.2bn, computed §3) — Adobe's total debt-like items, including the PV of off-balance-sheet hosting commitments, exceed its excess cash by a margin worth about $20/share. §3 discloses that this line item is a genuine judgment call with a $16.74/share range depending on which internally-consistent convention is used (§5), not a settled fact.

---

## 2. Method

Per the brief: value = PV(forecast owners' earnings) + PV(terminal value) + standalone assets − all debt, then divided by the current diluted share count. Two conventions are fixed by the brief and carried through exactly:

- **Timing.** The current fiscal year is t=0 and is *not* discounted. As of the 2026-09-01 valuation date, Adobe is inside FY2026 (fiscal year-end late November 2026; Q3 FY2026 reports September 10 2026 and is not yet in hand). So **FY2026E = t=0, FY2027E = t=1, FY2028E = t=2, FY2029E = t=3, FY2030E = t=4.** The terminal value is constructed in `work_products/terminal_value.md` as the value of the business *at the end of FY2030* — i.e., realised at the same moment as the FY2030 cash flow — so it is discounted at the same t=4 factor, not t=5.
- **Discount rate.** Set as a variable, `DISCOUNT_RATE = 0.15` in the script, per the brief. Section 4 below shows the sensitivity.
- **Trading-price blind.** No step below reads Adobe's share price or market capitalisation. (`work_products/terminal_value.md` used today's trading multiple as one anchor among several for choosing the *terminal* multiple — that choice was made in the prior work product and is taken as a given input here, not re-derived from price.)

### 2.1 The owners' earnings and terminal-value inputs, unchanged from the prior work products

| ($M)                     | FY2026E (t=0) | FY2027E (t=1) | FY2028E (t=2) | FY2029E (t=3) | FY2030E (t=4) | Terminal value @ FY2030 |
|---------------------------|---------------|---------------|---------------|---------------|---------------|--------------------------|
| SEVERE (15% probability)  | 6,886         | 6,903         | 6,639         | 6,330         | 6,022         | 42,154 (7×)              |
| BEAR (25% probability)    | 7,426         | 7,739         | 7,941         | 8,064         | 8,105         | 89,155 (11×)             |
| BASE (40% probability)    | 7,729         | 8,475         | 9,278         | 10,055        | 10,745        | 161,175 (15×)            |
| BULL (20% probability)    | 7,891         | 9,062         | 10,394        | 11,722        | 13,035        | 286,770 (22×)            |
| **Probability-weighted**  | **7,559**     | **8,173**     | **8,771**     | **9,332**     | **9,835**     | **150,436**              |

*(Owners' earnings by scenario: `work_products/forecast_earnings_calcs.py` §9 printed output, reproducing `work_products/forecast_earnings.md` §1 and §9 exactly. Terminal values and multiples: `work_products/terminal_value.md` §1 and `terminal_value_calcs.py` §4. The probability-weighted OE row is the same weights — SEVERE 15% / BEAR 25% / BASE 40% / BULL 20%, `work_products/forecast_earnings.md` §1 — applied year by year; this exact path is not printed in the forecast_earnings.md prose but is produced by its own calc script and is reproduced in `valuation_calcs.py`.)*

**A structural note worth stating plainly:** discounting is linear, so probability-weighting the annual owners' earnings and the terminal value *before* discounting (as done above) gives the identical answer as computing each scenario's fully-discounted equity value independently and *then* probability-weighting the four results. `valuation_calcs.py` §2 checks this explicitly — both paths give $110,867M / $277.79 per share to the cent. This is a real internal-consistency check, not a tautology, and it also means the weighted answer is not sensitive to which of the two equivalent computation orders is used. It also confirms `work_products/terminal_value.md` §10's handoff instruction was followed correctly: the interim cash-flow stream and the terminal value are weighted on the same probabilities and combined once, not re-weighted.

### 2.2 Discounting (r = 15%)

| Year                     | t   | Discount factor | PV, weighted OE ($M) |
|--------------------------|-----|------------------|------------------------|
| FY2026E                  | 0   | 1.0000           | 7,559                  |
| FY2027E                  | 1   | 0.8696           | 7,107                  |
| FY2028E                  | 2   | 0.7561           | 6,634                  |
| FY2029E                  | 3   | 0.6575           | 6,136                  |
| FY2030E                  | 4   | 0.5718           | 5,621                  |
| **Sum, PV(owners' earnings)** |     |                  | **33,057**             |
| Terminal value, discounted at t=4 (0.5718 × $150,436M) |  |  | **86,012**              |
| **Enterprise value**    |     |                  | **119,069**             |

*(Computed, `valuation_calcs.py` §2. Figures are the probability-weighted case; the base-case-only and per-scenario figures are in §3 of this document.)*

**Terminal value is 72% of enterprise value** ($86,012M / $119,069M). This is the single most important structural fact about this valuation: it is a claim about Adobe's earning power and multiple in 2030, discounted back four years, far more than it is a claim about the next five years of cash flow.

---

## 3. The equity bridge — standalone assets and all debt

*Revised after `pv/sotp/r1_review.md`; see `pv/sotp/r1_response.md` for the full argument on both changes below.*

Per the brief, standalone assets are excess cash and investments not needed to operate the business, and debt includes all debt-like items — funded debt, pension shortfalls, off-balance-sheet commitments, and anything else company-specific. Both are taken as of the most current balance sheet available: the Q2 FY2026 10-Q, period ended May 29 2026 (`primary_sources/2Q2026/financial_statements.md`). Q3 FY2026 reports September 10 2026 and is not yet available.

| Item                                                                  | $M     | Source                                                                 |
|------------------------------------------------------------------------|--------|-------------------------------------------------------------------------|
| **Standalone assets**: excess cash + short-term investments            | 5,122  | `work_products/owners_earnings_and_roic.md` §4 (total cash+STI $5,626M less an assumed 2% of TTM revenue operating cash need of $504M) |
| Debt, current (incl. $494M commercial paper), carrying value            | 1,843  | `primary_sources/2Q2026/financial_statements.md`, balance sheet         |
| Debt, long-term, carrying value                                        | 4,802  | `primary_sources/2Q2026/financial_statements.md`, balance sheet         |
| Operating lease liabilities, current                                    | 91     | `primary_sources/2Q2026/financial_statements.md`, balance sheet         |
| Operating lease liabilities, long-term                                  | 329    | `primary_sources/2Q2026/financial_statements.md`, balance sheet         |
| Off-balance-sheet hosting purchase obligations, PV @ 5%                | 6,259  | `work_products/owners_earnings_and_roic.md` §4.1                        |
| **= Total debt-like items**                                            | **13,324** | computed                                                              |
| **Net standalone assets less debt**                                    | **−8,202** | computed                                                              |

*(Computed, `valuation_calcs.py` §3.)*

**Why operating lease liabilities and the off-balance-sheet hosting commitments are now treated identically, both as debt-like.** The prior draft included the $420M of lease liabilities as debt but excluded the $6,259M PV of hosting commitments, on the argument that the hosting cost is already embedded in the owners' earnings forecast being discounted, so subtracting it again would double-count. A verifier review (`pv/sotp/r1_review.md`, Objection 1) correctly identified that the same argument applies with equal force to lease payments — which are also fully embedded in EBIT every year, and are never excluded from owners' earnings the way debt interest is — so the draft was applying opposite rules to two economically similar items without reconciling why. That inconsistency is conceded in full; see `pv/sotp/r1_response.md`. It is resolved here by applying one rule symmetrically, and choosing the brief's own explicit, literal instruction as the tie-breaker: the brief lists "off-balance sheets commitments/obligations" as debt to include, without carving out an exception for commitments whose cost happens to also appear in the earnings forecast, so both leases and hosting commitments are now included. **This is a genuine, disclosed judgment call, not a settled fact** — §5 of the script and the table below show the other internally-consistent choices and their effect on the per-share answer.

| Bridge convention                                                             | Total debt-like | Weighted value / share |
|--------------------------------------------------------------------------------|------------------|--------------------------|
| **Headline: funded debt + leases + hosting, all included (follows the brief literally)** | **$13,324M** | **$277.79**              |
| Funded debt + leases only, hosting excluded (the prior draft's rule)          | $7,065M          | $293.48                  |
| Funded debt only, leases and hosting both excluded (the double-counting argument applied evenly) | $6,645M | $294.53                  |

*(Computed, `valuation_calcs.py` §5. The defensible range from this one input alone is $277.79–$294.53, a $16.74/share, 6.0% spread.)*

**Legal contingencies not included.** Adobe has an ongoing securities class action and consolidated derivative actions and states plainly that it is "unable to estimate a reasonably possible financial loss or range of financial loss, if any" (`primary_sources/2Q2026/financial_statements.md`, Note 13). There is no sourced number to include. This is flagged as an unquantified risk to the equity bridge, not a zero.

**No pension shortfall found.** No defined-benefit pension plan is disclosed in the FY2025 10-K or Q2 FY2026 10-Q; nothing was found to add.

**Current diluted share count: 399.1M.** A verifier review (`pv/sotp/r1_review.md`, Objection 2) correctly caught that the prior draft's 402.5M figure — the weighted-average diluted share count for the three months ended May 29 2026 — was mislabeled as "the most current actual figure available." It is not: the same 10-Q balance sheet reports 399.0M shares actually outstanding as of that same date (a point-in-time spot count), which is lower and more current than a three-month backward-looking average taken while Adobe was continuously repurchasing stock. That objection is conceded. The figure used here starts from that 399.0M spot count and adds the current dilutive effect from stock plans — 0.1M, per Note 12's three-months-ended-May-29-2026 gap between basic (402.4M) and diluted (402.5M) weighted averages, which is small because 12.1M of potential shares are currently anti-dilutive (`primary_sources/2Q2026/financial_statements.md`, Note 12) — giving **399.0 + 0.1 = 399.1M**. This keeps the brief's "diluted" requirement while using the most current spot count available, rather than a backward-looking quarterly average. Per the brief, no forecast future share count (e.g., the buyback-adjusted FY2030E figure of 341M in `work_products/forecast_earnings.md` §8) is used here.

**A dating note the verifier also raised (`pv/sotp/r1_review.md`, Objection 3) and that this document had not previously addressed:** the equity bridge above is anchored to the May 29 2026 balance sheet, while §2's discounting convention treats the entire FY2026 fiscal year as a forward, undiscounted (t=0) flow from the 2026-09-01 valuation date — a ~3-month gap between the two reference dates. Neither this document nor its predecessor reconciles that gap, and it is not obviously a double-count: the "current year is t=0, undiscounted" convention is itself a stated brief simplification that does not adjust for how far into the fiscal year the valuation date falls, so pairing it with the most recent *actual* balance sheet (rather than an unsourced, extrapolated September 1 balance sheet) keeps both sides of the calculation at the same, brief-specified level of approximation. No defensible quantified correction for this gap could be constructed from available sources — full reasoning in `pv/sotp/r1_response.md`, Objection 3.

---

## 4. Sensitivity to the discount rate

| Discount rate | PV(owners' earnings) | PV(terminal value) | Enterprise value | Value / diluted share | TV share of EV |
|----------------|-----------------------|----------------------|--------------------|--------------------------|-----------------|
| 10.0%          | 35,966                | 102,750              | 138,716            | $327.02                  | 74%             |
| 12.5%          | 34,448                | 93,916               | 128,364            | $301.08                  | 73%             |
| **15.0% (brief's rate)** | **33,057**  | **86,012**           | **119,069**         | **$277.79**               | **72%**         |
| 17.5%          | 31,780                | 78,922               | 110,702            | $256.83                  | 71%             |
| 20.0%          | 30,604                | 72,548               | 103,152            | $237.91                  | 70%             |

*(Computed, `valuation_calcs.py` §4, probability-weighted path throughout.)*

The terminal value's share of enterprise value is stable across this range (70–74%) — the discount rate does not change *what the valuation is really about*, only its level. A 5-point change in the discount rate moves the per-share answer by roughly 14–16%.

---

## 5. What I am confident about, and what I am not

**High confidence (arithmetic, given the upstream inputs):**

- The discounting mechanics themselves: the linearity check in §2.1 that weighting-then-discounting equals discounting-then-weighting ties to the cent.
- Terminal value dominates this valuation (72% of enterprise value at 15%) — this is a direct, unavoidable consequence of a 15% discount rate applied to a five-year explicit horizon plus a large terminal claim, not a modelling choice made here.
- The individual figures making up the equity bridge (excess cash, funded debt, lease liabilities, the PV of hosting commitments, and the diluted share count) each tie exactly to their primary-source line items (computed, §3).

**A genuine judgment call, disclosed and bounded, not a hidden one:**

- **Which items belong in the debt bridge.** §3 shows the answer ranges $277.79–$294.53/share (a 6.0% spread) depending on whether off-balance-sheet hosting commitments and/or lease liabilities are treated as debt-like. This document's headline follows the brief's literal instruction to include off-balance-sheet commitments, applied symmetrically to leases; a reader who prefers the double-counting argument in the prior draft can read $294.53/share instead, and the reasoning for both is laid out in `pv/sotp/r1_response.md`.

**Genuinely uncertain — these decide the answer, and are inherited in full from the upstream work products:**

1. **Everything flagged as uncertain in `work_products/forecast_earnings.md` §9 and `work_products/terminal_value.md` §9** — free-to-paid conversion, whether generative AI substitutes or augments Adobe's creative workflows, inference unit-cost trajectory, and the CEO/CFO leadership vacuum — flows directly into this valuation because the owners' earnings paths and terminal multiples used here are exactly those work products' outputs, unaltered.
2. **The discount rate itself.** The brief fixes it at 15% as a variable to be set, not derived; §4 shows this single input is worth roughly $40–90 per share across a 10–20% band. This valuation does not take a view on whether 15% is the "correct" hurdle rate for Adobe — it applies the brief's stated rate and shows the sensitivity.
3. **The probability weights (SEVERE 15% / BEAR 25% / BASE 40% / BULL 20%) are analyst judgment, carried over unchanged from `work_products/forecast_earnings.md` §1, not independently re-derived here.** A reader who holds different weights can recompute the weighted answer directly from the per-scenario figures in §2.1, since the four scenario equity values ($104, $183, $298, $487 per share) are the actual load-bearing output of this document.
4. **The ~3-month gap between the equity bridge's balance-sheet date (May 29 2026) and the valuation date (September 1 2026)**, flagged in §3. Neither this document nor its predecessor can quantify a correction for it from available sources; it is disclosed as an open question rather than resolved.

---

*Calculations: `work_products/valuation_calcs.py`. Inputs traced to `work_products/forecast_earnings.md`, `work_products/terminal_value.md`, `work_products/owners_earnings_and_roic.md`, and their respective calc scripts, plus `primary_sources/2Q2026/financial_statements.md` for the current balance sheet and diluted share count.*
