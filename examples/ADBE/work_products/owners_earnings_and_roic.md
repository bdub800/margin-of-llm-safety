# Adobe Inc. (ADBE) — Owners' Earnings and Return on Invested Capital

*Prepared 2026-08-28. All arithmetic is in `work_products/owners_earnings_calcs.py` (run with `uv run python work_products/owners_earnings_calcs.py`). Every input is traced to `primary_sources/FY2025/` (Form 10-K, FYE November 28 2025), `primary_sources/2Q2026/` (Form 10-Q, period ended May 29 2026), the Q4 FY2025 / Q1 FY2026 / Q2 FY2026 earnings call transcripts, `work_products/causal_model.md`, or the Knowledge Store. The most recent primary source is the Q2 FY2026 10-Q; Q3 FY2026 had not been reported as of this writing (Knowledge Store ID 9).*

---

## 1. Answer first

| Measure                                                              | FY2023  | FY2024   | FY2025    | TTM to Q2 FY2026 |
| -------------------------------------------------------------------- | ------- | -------- | --------- | ---------------- |
| Owners' earnings (Method A, normalised)                              | $5,545M | $6,441M  | $7,119M   | $7,490M          |
| Owners' earnings (Method B, cash cross-check)                        | $4,658M | $5,483M  | $7,049M   | $7,375M          |
| Owners' earnings margin (Method A)                                   | 28.6%   | 30.0%    | 30.0%     | 29.7%            |
| Owners' earnings per diluted share (Method A)                        | $12.08  | $14.32   | $16.67    | $18.71           |
| Growth in owners' earnings, YoY                                      | —       | +16.2%   | +10.5%    | +5.2%            |
| Invested capital (period end)                                        | n/a     | $10,767M | $9,653M   | $11,164M         |
| **ROIC (owners' earnings / average invested capital)**               | n/a     | n/a      | **69.7%** | **72.0%**        |
| ROIC, conservative floor (adds PV of hosting commitments to capital) | n/a     | n/a      | 43.2%     | 44.9%            |

*(Computed, `owners_earnings_calcs.py` §3, §4, §5, §6, §7. FY2023 ROIC is not shown because the FY2025 10-K balance sheet only goes back to November 29 2024, so no FY2023 opening capital is available in `primary_sources`.)*

**The two headline conclusions.**

1. **Owners' earnings are roughly $7.5 billion, or ~30% of revenue, and the level is far more stable than GAAP net income suggests.** GAAP net income grew 2.8% in 1H FY2026 (`primary_sources/2Q2026/financial_statements.md`), which reads as a stall. It is not one: about $220M of that gap is a GAAP tax-rate step-up (18% → 23%) that is largely a *timing and mix* effect rather than a change in cash burden (`work_products/causal_model.md` §4.2; `primary_sources/2Q2026/md_and_a.md`), and a further $162M is the one-off goodwill impairment and FTC loss contingency. Normalising those, owners' earnings still grew ~5%.
2. **ROIC is extraordinarily high — roughly 45% at the most conservative reading and ~70% on the base measure — and, critically, Adobe's invested capital excluding acquisition goodwill is *negative* (−$3.9B at Q2 FY2026).** The operating business consumes no net capital: at Q2 FY2026 the deferred-revenue float alone ($7,250M) very nearly covers all operating assets outside goodwill and intangibles ($7,461M — receivables $1,993M, prepaid $1,449M, PP&E $1,870M, other assets $1,645M, plus $504M of retained operating cash), and trade payables and accruals more than cover the remainder. The practical consequence is that **ROIC is not a binding constraint on Adobe's organic growth rate.** Adobe's growth ceiling is set by demand and competition, not by its ability to fund reinvestment. This is the single most important structural fact in this document.

---

## 2. Method, and why it is built this way

The brief defines owners' earnings as true economic earnings available to owners after all obligations *except* interest on debt, with interest income removed and interest expense added back so that financing is handled separately against balance-sheet assets and debt. That makes the measure **unlevered**, and it should therefore be compared against invested capital (not equity).

I have used two independent constructions and checked that they agree. Where they do not, I show the exact bridge rather than picking the flattering one.

### Method A — normalised operating earnings (primary)

```
  Operating income (EBIT)
+ non-recurring charges booked inside operating expenses
+ amortisation of PURCHASED intangibles
+ PP&E depreciation
− maintenance capex
= pre-tax owners' earnings
× (1 − normalised tax rate)
= OWNERS' EARNINGS
```

Starting at EBIT automatically satisfies the unlevered requirement: interest expense, interest income and investment gains all sit below the operating line in Adobe's income statement (`primary_sources/FY2025/financial_statements.md`, Note 18) and are therefore already excluded.

FY2025 worked example (computed, §3):

| Component                               | FY2025      | Source                                        |
| --------------------------------------- | ----------- | --------------------------------------------- |
| Operating income (EBIT)                 | $8,706M     | FY2025 10-K Consolidated Statements of Income |
| + non-recurring charges in EBIT         | $0M         | none in FY2025                                |
| + amortisation of purchased intangibles | $310M       | FY2025 10-K Note 8                            |
| + PP&E depreciation                     | $236M       | FY2025 10-K Note 6                            |
| − maintenance capex                     | ($241M)     | 3-year average actual capex, see §2.2         |
| = pre-tax owners' earnings              | $9,011M     | computed                                      |
| − normalised tax @ 21%                  | ($1,892M)   | see §2.3                                      |
| **= Owners' earnings**                  | **$7,119M** | computed                                      |

### 2.1 Adjustments I made, and the ones I deliberately did not

**Stock-based compensation is NOT added back.** It is a real cost to owners and is already deducted inside EBIT ($1,942M in FY2025, $2,031M TTM — FY2025 10-K Note 12, Q2 FY2026 10-Q Note 9). I tested whether the GAAP grant-date-fair-value charge is a fair proxy for the true economic cost, which is the value of shares actually handed to employees: Adobe delivered 3.6M restricted stock units, 0.1M performance shares and 1.1M ESPP shares in FY2025 (10-K Note 12), i.e. 4.8M shares, at a weighted-average RSU grant-date fair value of $407.67. At ~$400/share that is ~$1,920M against the $1,942M GAAP charge (computed, §7). **The GAAP number is a good proxy — within ~1%.** This is a real check, not an assumption: the two constructions are independent.

**Amortisation of purchased intangibles IS added back** ($310M FY2025, $234M TTM; 10-K Note 8, 10-Q Note 7). The economic argument is that the acquired customer relationships and technology are maintained and replaced by R&D and sales-and-marketing spend that is *already* fully expensed in the P&L, so charging amortisation as well double-counts. The consistency requirement is that the corresponding capital must stay in invested capital — and it does: goodwill and intangibles of $13,352M (FY2025) and $15,053M (Q2 FY2026) are the dominant component of invested capital in §4. If you disagree with this add-back, subtract $234M pre-tax / ~$185M after tax from TTM owners' earnings — a 2.5% effect. It does not change any conclusion.

**Non-recurring items added back:**

| Item                                           | Period    | Amount  | Source                                                             |
| ---------------------------------------------- | --------- | ------- | ------------------------------------------------------------------ |
| Figma acquisition termination fee              | FY2024    | $1,000M | FY2025 10-K income statement, separate line                        |
| Lease-related asset impairments                | FY2024    | $78M    | FY2025 10-K cash flow statement; Note 7 places it in G&A           |
| Goodwill impairment (Publishing & Advertising) | Q2 FY2026 | $70M    | Q2 FY2026 10-Q Note 7 and segment footnote                         |
| Loss contingency (FTC/DOJ ROSCA settlement)    | 1H FY2026 | $92M    | Q2 FY2026 10-Q segment footnote; settled March 12 2026 per Note 13 |

Two honest caveats on these. First, **the goodwill impairment is non-cash but not economically meaningless** — it is Adobe writing down a legacy unit whose earning power genuinely deteriorated (Publishing & Advertising revenue was $256M and shrinking 7% in FY2025 — `primary_sources/FY2025/md_and_a.md`; see `work_products/causal_model.md` §3.2). Adding it back to the earnings *flow* is right; ignoring what it signals about that unit would not be. Second, **litigation charges are only non-recurring one at a time.** Adobe has an ongoing securities class action and consolidated derivative actions (10-Q Note 13). A normalised annual legal provision of, say, $30–50M would be defensible and would reduce owners' earnings by ~$25–40M after tax (~0.5%). I have not made that adjustment because I cannot source a run-rate; flagged as a known small optimism in the number.

**Cyclicality: no adjustment made, and I think that is right.** Adobe is ~96–97% subscription revenue recognised ratably (`primary_sources/FY2025/md_and_a.md`; `primary_sources/2Q2026/md_and_a.md`), so reported revenue is a smoothed function of a contracted book rather than a cyclical order flow (`work_products/causal_model.md` §0). There is no cycle to normalise out. The relevant volatility for Adobe is competitive and strategic, not cyclical.

**Off-balance-sheet hosting commitments: no earnings adjustment.** Adobe's $6.82B of non-cancellable purchase obligations relate to third-party hosting and data-centre services (FY2025 10-K Note 16). These are contracted *operating* spend, and the spend is already flowing through cost of revenue as incurred. Adding a charge would double-count. I do address them on the capital side in §4.

### 2.2 Maintenance capex — the first judgment call

Adobe rents essentially all of its compute rather than owning it (`work_products/causal_model.md` §4.3), so capex is facilities and internal IT, and it is genuinely small: $360M (FY2023), $183M (FY2024), $179M (FY2025), $201M TTM (FY2025 10-K and Q2 FY2026 10-Q cash flow statements).

Recent capex is running *below* depreciation ($236M in FY2025, Note 6), and net PP&E has been shrinking ($1,936M → $1,873M → $1,870M). Using one year's depressed capex would flatter owners' earnings. **I use the three-year average actual capex of $241M as maintenance capex for every period** — which lands within $5M of FY2025 depreciation, a useful independent confirmation that it is the right order of magnitude.

This choice barely matters: swinging maintenance capex by ±$60M changes owners' earnings by ~$47M after tax, or 0.6%. I flag it and move on rather than building a machine around it.

*(One item I have excluded: "purchases of long-term investments, intangibles and other assets" of $134M in FY2025. Adobe does not disaggregate it, so I cannot tell how much is financial investment versus capitalised intangibles. If all of it were capital spending, TTM owners' earnings would fall by ~$106M after tax, or 1.4%. Flagged as a bounded, immaterial omission.)*

### 2.3 The normalised tax rate — the second and larger judgment call

This is where Adobe is genuinely messy, and it is worth being explicit rather than picking a number.

| Rate measure                           | FY2023 | FY2024 | FY2025 | 1H FY2026 | FY2026 guide |
| -------------------------------------- | ------ | ------ | ------ | --------- | ------------ |
| GAAP effective tax rate                | 20%    | 20%    | 18%    | 23%       | ~22.5%       |
| Current tax provision / pre-tax income | 26.4%  | 26.5%  | 24.3%  | n/a       | —            |
| Cash taxes paid / pre-tax income       | 27.3%  | 24.9%  | 25.4%  | n/a       | —            |
| Management's non-GAAP tax rate         | —      | —      | —      | —         | ~18%         |

*(GAAP ETR: `primary_sources/FY2025/md_and_a.md` line 327 and `primary_sources/2Q2026/md_and_a.md` line 288. Current tax: FY2025 10-K Note 10. Cash taxes paid: cash-flow supplemental disclosures. FY2026 guides: `primary_sources/2Q2026/earnings_call_transcript.md` line 324 — GUIDANCE, forward-looking. Ratios computed, §2.)*

The 6–7pp wedge between the GAAP rate and the cash rate is not a permanent feature: it is Section 174 forced capitalisation of domestic R&D, which shows up as a $2,065M "capitalized expenses" deferred tax asset at FY2025 year-end (10-K Note 10). The One Big Beautiful Bill Act "*restores immediate expensing of domestic research and development costs*" from fiscal 2026, and Adobe states it "*anticipate[s] a reduction to our effective rates for cash taxes paid for fiscal 2026 and beyond*" (`primary_sources/2Q2026/md_and_a.md`). The evidence that this is already happening is in the 1H FY2026 cash flow statement: the deferred-income-tax line swung from −$288M to **+$111M** year over year (Q2 FY2026 10-Q), i.e. the deferred tax asset has begun to unwind.

So the two rates should converge — the GAAP rate rising (18% → ~22.5%) and the cash rate falling. **I use 21% as the normalised rate**, which is approximately the U.S. federal statutory rate, sits within a point of the FY2023–FY2026E average GAAP ETR of 20.1% (computed, §2), and lies between the two converging measures. It is a round number chosen because the underlying reality does not support more precision.

Sensitivity (computed, §3 and §6):

| Normalised tax rate                       | TTM owners' earnings | TTM ROIC  |
| ----------------------------------------- | -------------------- | --------- |
| 18% (management's non-GAAP rate)          | $7,775M              | 74.7%     |
| **21% (base case)**                       | **$7,490M**          | **72.0%** |
| 25% (recent cash-tax experience persists) | $7,111M              | 68.3%     |

The whole plausible range is ±4% on owners' earnings. No conclusion in this document turns on it.

---

## 3. The cash cross-check, and where the two methods disagree

Method B starts from reported cash flow from operations and strips out the three things that make CFO *not* owners' earnings (computed, §4):

| Component                                                      | FY2025      | TTM to Q2 FY2026 |
| -------------------------------------------------------------- | ----------- | ---------------- |
| Cash flow from operations                                      | $10,031M    | $10,481M         |
| − maintenance capex                                            | ($241M)     | ($241M)          |
| − stock-based compensation (added back in CFO; a real cost)    | ($1,942M)   | ($2,031M)        |
| − increase in deferred revenue (growth float, not earnings)    | ($771M)     | ($813M)          |
| − net non-operating income (to keep the measure unlevered)     | ($28M)      | ($21M)           |
| **= Owners' earnings (cash method, at actual cash tax rates)** | **$7,049M** | **$7,375M**      |

**The two methods agree to 1.0% in FY2025 and 1.5% TTM.** That is the main reason I am comfortable with the ~$7.5B figure. The exact algebraic bridge is printed by the script (§4); for FY2025 it is: +$272M of amortisation in CFO that Method A does not add back (principally capitalised sales-commission amortisation), +$48M other non-cash, −$166M of working-capital movement excluding deferred revenue (which is where the *cash* commission spend sits, largely cancelling the +$272M), and −$224M net from Adobe's actual current tax rate of 24.3% running above the 21% normalised rate. Total −$70M. It ties exactly. The TTM bridge ties to within $2M, the residual being a definitional difference between the SBC figure in Note 9 ($1,045M) and the cash-flow statement ($1,043M).

FY2023 and FY2024 diverge much more (−16.0% and −14.9%) and the reasons are known and specific: FY2024's cash flow carries the $1.0B Figma termination fee that Method A normalises out (`primary_sources/FY2025/md_and_a.md` confirms "*Fiscal 2024 cash flows from operations were adversely impacted by payment of the $1 billion Figma termination fee*"), and FY2023's current tax rate was 26.4% against the 21% normalised rate. Neither divergence is a methodology failure.

### 3.1 Why owners' earnings are lower than the free cash flow you will see quoted

Conventional free cash flow (CFO less capex) was $9,852M in FY2025 and $10,280M TTM (computed, §4). My owners' earnings figure is ~$2.5–2.8B lower. The entire gap is two deliberate deductions:

- **Stock-based compensation (~$2.0B).** Non-cash, but owners pay for it in shares. Excluding it would be indefensible.
- **The deferred-revenue float build (~$0.8B).** Customers pay in advance; the growth in that float is customer cash, not earnings. It recurs only while the book keeps growing, and the causal model flags that the float is already decelerating — deferred revenue grew 12.3% in FY2025 but only 3.1% sequentially in 1H FY2026, and remaining performance obligations fell $0.25B sequentially (`work_products/causal_model.md` §4.1). Treating a growth-contingent source of cash as sustainable earnings is exactly the kind of error that makes a number precisely wrong.

This is a judgment, and it is the largest single one in the document. **If you disagree and want the float counted, add ~$640M after tax to owners' earnings** (TTM ~$8.1B) and ROIC rises to ~78%. It does not change the conclusion; it changes the level by ~9%.

---

## 4. Invested capital

Per the brief, invested capital is the capital actually deployed to operate the business. I build it on the asset side because it is more transparent (computed, §5):

```
  Total assets
− cash, equivalents and short-term investments IN EXCESS of operating needs
− net deferred income tax assets (a tax-timing asset, not operating capital)
− operating lease right-of-use assets (per the brief)
− non-interest-bearing operating liabilities (payables, accruals, DEFERRED REVENUE,
    income taxes payable, other liabilities), excluding lease liabilities
= INVESTED CAPITAL
```

| Component                                                     | FY2024 (Nov 29 2024) | FY2025 (Nov 28 2025) | Q2 FY2026 (May 29 2026) |
| ------------------------------------------------------------- | -------------------- | -------------------- | ----------------------- |
| Total assets                                                  | $30,230M             | $29,496M             | $29,933M                |
| − excess cash and short-term investments                      | ($7,456M)            | ($6,120M)            | ($5,122M)               |
| − net deferred income tax assets                              | ($1,657M)            | ($2,186M)            | ($1,998M)               |
| − operating lease right-of-use assets                         | ($281M)              | ($312M)              | ($299M)                 |
| − non-interest-bearing operating liabilities                  | ($10,069M)           | ($11,225M)           | ($11,350M)              |
| **= Invested capital**                                        | **$10,767M**         | **$9,653M**          | **$11,164M**            |
| memo: goodwill + other intangibles, net                       | $13,570M             | $13,352M             | $15,053M                |
| memo: **invested capital EXCLUDING goodwill and intangibles** | −$2,803M             | **−$3,699M**         | **−$3,889M**            |

*(Balance sheet figures from `primary_sources/FY2025/financial_statements.md` and `primary_sources/2Q2026/financial_statements.md`. Non-interest-bearing operating liabilities for FY2025 = trade payables $417M + accrued expenses $2,648M + deferred revenue $6,905M current and $125M long-term + income taxes payable $153M current and $469M long-term + other liabilities $508M.)*

**Assumption — operating cash need at 2% of revenue.** Adobe collects in advance and runs negative working capital, so its genuine operating cash requirement is small. 2% of revenue is $475M (FY2025) / $504M (TTM). This is an assumption, not a sourced figure. Sensitivity (computed, §6): 0% of revenue gives TTM ROIC of 75.5%; 2% gives 72.0%; 5% gives 67.2%. Immaterial to the conclusion.

**Judgment — net deferred tax assets excluded from invested capital.** These arose from Sec. 174 R&D capitalisation and are a prepaid-tax asset, not capital deployed to run the business. Including them would raise FY2025 invested capital to $11,839M and lower ROIC to 58.7% (FY2025) and 59.9% (TTM) (computed, §8). Still exceptional; conclusion unchanged.

### 4.1 Off-balance-sheet commitments — and why I do not simply add them

The brief says to add off-balance-sheet commitments to invested capital. Adobe's are large: **$6,821M of non-cancellable unconditional purchase obligations, "*primarily relating to contracts with vendors for third-party hosting and data center services*"** (FY2025 10-K Note 16; `primary_sources/FY2025/md_and_a.md`). Present-valued at 5% on the disclosed maturity schedule, that is $6,259M (computed, §5).

There is a real conceptual problem with just adding it. If Adobe *owned* its data centres, that capital would sit on the balance sheet and the associated cost would be depreciation. Because Adobe rents, the capital is off balance sheet **and** the cost is already fully deducted inside cost of revenue. Adding the commitment to capital without adding the rent back to earnings double-charges Adobe. Doing the full operating-lease-style capitalisation (impute an asset, back out the rent, impose a depreciation and interest split) requires assuming a hosting cost split that Adobe does not disclose — the MD&A says only "*primarily*" (`primary_sources/2Q2026/md_and_a.md`) — which is precisely the stacked-assumption trap the brief warns against.

So I present it as a **floor, explicitly labelled as double-counted**: FY2025 ROIC 43.2%, TTM 44.9% (computed, §6). The true figure is above this and below the base case. **The honest statement is: Adobe's ROIC is somewhere between roughly 45% and 75%, and the choice within that band does not matter for any decision.**

### 4.2 What the composition of invested capital actually tells you

This is the part worth dwelling on. Adobe's invested capital of $9.7–11.2B is *entirely* acquisition goodwill and intangibles ($13.4–15.1B), offset by a large negative operating capital position. Strip out the goodwill and intangibles and **invested capital is −$3.9B at Q2 FY2026**.

Three consequences:

1. **The organic business needs no capital.** Incremental organic ROIC is not merely high; it is undefined in the good direction. Growth funds itself out of customer prepayments. This is why Adobe can return more than 100% of owners' earnings to shareholders and still grow.
2. **The measured ROIC is a verdict on capital *allocation*, not on the operating business.** Nearly all invested capital is what Adobe paid for acquisitions over two decades. The reported ~70% ROIC says those acquisitions, in aggregate, have been well made. The $70M Publishing & Advertising goodwill impairment in Q2 FY2026 (10-Q Note 7) is the first crack in that record in the periods presented, and the $1.9B Semrush acquisition — which added $1,251M of goodwill and $582M of intangibles (10-Q Note 3) — is the next test. Semrush raised invested capital by ~$1.8B in a single quarter for ~$480M of acquired ARR (Knowledge Store ID 4) and ~$280M of expected FY2026 revenue (`primary_sources/2Q2026/earnings_call_transcript.md` line 322 — GUIDANCE). **That is a materially lower-return use of capital than the existing base**, and it is why TTM invested capital rose $1.5B while owners' earnings rose ~$370M.
3. **Because ROIC vastly exceeds any plausible growth rate, the reinvestment framing of ROIC does not bind here.** The standard heuristic — organic growth cannot exceed ROIC — is not the operative constraint at 45–75%. Adobe's growth is limited by demand, competition and its own strategic choices (the deliberate ~$480M FY2026 organic ARR give-up documented in `work_products/causal_model.md` §1.2), not by the cost of capital deployment.

---

## 5. Consistency checks against the causal model

I checked this work against `work_products/causal_model.md` for contradictions. Three places matter:

- **Owners' earnings level.** The causal model's §4 presents "SBC-adjusted owners' earnings" of $7,910M (FY2025) and $3,983M (1H FY2026), built as CFO − actual capex − SBC. My FY2025 figure is $7,119M. **The two are consistent and the gap is fully explained**: the causal model deliberately used the simplest possible construction and did not deduct the $771M deferred-revenue float build, did not normalise tax, and used actual rather than average capex. $7,910M − $771M float = $7,139M, within 0.3% of my $7,119M. I regard my figure as the better one for valuation purposes because it removes a growth-contingent cash source, but the causal model was not wrong; it was coarser and said so.
- **The tax story.** The causal model §4.2 argues the GAAP rate is rising while the cash rate should fall, so cash owners' earnings are much less impaired than GAAP net income. My data confirm the mechanism directly: the deferred-tax line in the cash flow statement swung from −$288M to +$111M year over year (Q2 FY2026 10-Q). Consistent.
- **The buyback sustainability point.** The causal model §4.4 flags buybacks running above what the business generates. On my (stricter) owners' earnings measure the ratio is worse than the causal model's 1.43x: **0.79x (FY2023), 1.47x (FY2024), 1.58x (FY2025), and 1.23x in 1H FY2026** (computed, §7). The corroborating balance-sheet evidence is unambiguous — cash and equivalents fell $7,613M → $5,431M → $4,919M, and Adobe drew $494M of commercial paper having had none outstanding at FY2025 year-end (Q2 FY2026 10-Q Note 14). Consistent, and I would state it more strongly: **the buyback is not funded out of owners' earnings and has not been since FY2024.**

---

## 6. What I am confident about, and what I am not

**High confidence:**

- Owners' earnings of ~$7.5B TTM, ~30% of revenue. Two independent constructions agree to 1.5%, and the bridge between them ties to $2M.
- The SBC charge is a fair proxy for the economic cost of dilution — checked independently against shares actually delivered (~1% difference).
- Invested capital excluding goodwill and intangibles is negative. This is arithmetic off the balance sheet, not a judgment.
- ROIC is in the 45–75% band on any defensible treatment of the hosting commitments, tax rate and operating cash. It is far above any plausible growth rate.
- Buybacks have exceeded owners' earnings every year since FY2024 and are being funded from the cash pile and, newly, commercial paper.

**Moderate confidence (sourced, but requiring judgment):**

- The 21% normalised tax rate. The full defensible range is 18–25%, worth ±4% on owners' earnings.
- Excluding the deferred-revenue float from owners' earnings. Defensible either way; worth ~9% on the level.
- Adding back purchased-intangible amortisation. Worth ~2.5%.
- Maintenance capex of $241M. Worth ~0.6%.

**Genuinely uncertain, and these are the ones that matter:**

1. **Whether ~30% owners'-earnings margin is the right forward run-rate.** It is a backward-looking measurement. Management guides non-GAAP operating margin down from 47.4% (Q1 FY2026 actual) to ~44% in Q3 FY2026, with the full year at ~45% (`primary_sources/1Q2026/`, `2Q2026/earnings_call_transcript.md` — GUIDANCE), driven by advertising to fill the freemium funnel. That spend is structural to the strategy and persists into FY2027 (`work_products/causal_model.md` §3.1). **Whether it is an expense or an investment is unresolvable from the filings.** As a bound: the FY2024→FY2025 advertising step-up alone was $330M ($1,040M → $1,370M, FY2025 10-K Note 1); if treated as growth investment rather than expense, that is ~$261M after tax, or 3.7% of FY2025 owners' earnings (computed, §7). I have *not* included it in the base case.
2. **Whether AI inference cost breaks the gross margin, and therefore the owners'-earnings margin.** It has not yet — the causal model's rate/mix bridge puts the Q2 FY2026 AI/hosting drag on total gross margin at only ~17bp — but ~150M new free monthly active users are being routed through generative features from Q3 FY2026, and the mix lever that has been offsetting it is nearly exhausted (`work_products/causal_model.md` §2.1a, §2.3). This is the main channel by which the ~30% margin could deteriorate, and it is unobserved.
3. **Whether the goodwill in invested capital is worth its carrying value.** ROIC of ~70% is computed against a capital base that is ~100% goodwill from past acquisitions. The Q2 FY2026 impairment says at least one reporting unit's goodwill was not. Semrush adds $1.25B more at a visibly lower incremental return.
4. **SBC is set to rise, and dilution with it.** Adobe granted 7.0M RSUs in 1H FY2026 against 5.2M in all of FY2025, at a weighted-average grant fair value of $293.34 versus $407.67 (10-Q Note 9; 10-K Note 12) — more shares to deliver the same dollar value as the stock fell. Unrecognised compensation cost rose from $3.24B to $4.21B, and anti-dilutive potential shares jumped from 5.1M to 12.1M. **The SBC charge deducted in owners' earnings will grow faster than revenue for at least the next two years**, which is a headwind to the margin that is already contracted and not visible in current-period numbers.

*Market cross-check, for orientation only (not a valuation): at the reported market capitalisation of $108.7–112.1bn (Knowledge Store ID 7), and Q2 FY2026 net debt of ~$1.0bn (debt at par $6,150M + $494M commercial paper, less $4,919M cash + $707M short-term investments), enterprise value is ~$110–113bn, or **14.6–15.1x TTM owners' earnings — an unlevered earnings yield of 6.6–6.8%** (computed, §7). Note that the Knowledge Store is internally inconsistent on price: ID 7 reports a $290.00 close on August 27 2026 while ID 8 quotes $258.42; I have used the market-capitalisation figures rather than the share prices, and flag the discrepancy rather than resolving it.*

---

*Calculations: `work_products/owners_earnings_calcs.py`.*
