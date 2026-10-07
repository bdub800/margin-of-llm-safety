# Adobe Inc. (ADBE)

Share price: $284.88 (as provided)
Date: 2026-09-03

*All figures in USD millions except per-share and percentage data unless noted. All arithmetic is in `work_products/financials_summary_calcs.py` (run with `uv run python work_products/financials_summary_calcs.py`). Sources are `primary_sources/FY2025/` (Form 10-K, fiscal year ended November 28, 2025) and `primary_sources/2Q2026/` (Form 10-Q, quarter ended May 29, 2026). Q3 FY2026 had not been reported as of this writing — Adobe's Q3 FY2026 earnings release is scheduled for September 10, 2026 (Knowledge Store ID 27) — so the 2Q FY2026 10-Q is the most recent primary source available.*

---

## 1. Financial and Operating metrics

| Metric (USD millions)                | FY2023  | FY2024  | FY2025  | H1 2025 | H1 2026 | TTM to Q2 FY2026 |
| ------------------------------------- | ------- | ------- | ------- | ------- | ------- | ----------------- |
| Revenue                               | 19,409  | 21,505  | 23,769  | 11,587  | 13,016  | 25,198             |
| Gross profit                          | 17,055  | 19,147  | 21,218  | 10,327  | 11,637  | 22,528             |
| Gross margin                          | 87.9%   | 89.0%   | 89.3%   | 89.1%   | 89.4%   | 89.4%              |
| Operating income (EBIT)               | 6,650   | 6,741   | 8,706   | 4,272   | 4,656   | 9,090              |
| Operating margin                      | 34.3%   | 31.3%   | 36.6%   | 36.9%   | 35.8%   | 36.1%              |
| D&A (per cash flow statement)         | 872     | 857     | 818     | 426     | 367     | 759                |
| EBITDA (EBIT + D&A)                   | 7,522   | 7,598   | 9,524   | 4,698   | 5,023   | 9,849              |
| EBITDA margin                         | 38.8%   | 35.3%   | 40.1%   | 40.5%   | 38.6%   | 39.1%              |
| Interest expense                      | (113)   | (169)   | (263)   | (130)   | (128)   | (261)              |
| Net income                            | 5,428   | 5,560   | 7,130   | 3,502   | 3,601   | 7,229              |
| Net margin                            | 28.0%   | 25.9%   | 30.0%   | 30.2%   | 27.7%   | 28.7%              |
| Stock-based compensation              | 1,718   | 1,833   | 1,942   | 956     | 1,043   | 2,029              |
| Cash from operating activities (CFO)  | 7,302   | 8,056   | 10,031  | 4,673   | 5,123   | 10,481             |
| Capital expenditures (PP&E purchases) | 360     | 183     | 179     | 73      | 95      | 201                |
| Free cash flow (CFO − capex)          | 6,942   | 7,873   | 9,852   | 4,600   | 5,028   | 10,280             |
| Unlevered FCF (FCF + interest exp.)   | 7,055   | 8,042   | 10,115  | 4,730   | 5,156   | 10,541             |
| Basic EPS                             | $11.87  | $12.43  | $16.73  | n/a     | n/a     | n/a                |
| Diluted EPS                           | $11.82  | $12.36  | $16.70  | n/a     | n/a     | n/a                |

*(Computed, `financials_summary_calcs.py` §1–3. TTM = FY2025 + H1 2026 − H1 2025.)*

**Adjusted EBITDA:** Adobe does not report an Adjusted EBITDA or equivalent non-GAAP measure anywhere in the FY2025 10-K or 2Q FY2026 10-Q MD&A sections (checked both `md_and_a.md` files for "non-GAAP" and "EBITDA" — no matches). Per instructions, this line is omitted rather than approximated; the EBITDA line above is a simple GAAP construction (EBIT + reported D&A), not a company-defined metric.

**Owners' Earnings and ROIC** (already computed in `work_products/owners_earnings_and_roic.md`, not recomputed here):

| Measure                                                | FY2023 | FY2024  | FY2025  | TTM to Q2 FY2026 |
| ------------------------------------------------------- | ------ | ------- | ------- | ------------------ |
| Owners' earnings (Method A, normalised)                 | $5,545M | $6,441M | $7,119M | $7,490M            |
| Owners' earnings margin                                 | 28.6%  | 30.0%   | 30.0%   | 29.7%              |
| ROIC (owners' earnings / average invested capital)      | n/a    | n/a     | 69.7%   | 72.0%              |

*(Source: `work_products/owners_earnings_and_roic.md` §1. See that document for full methodology, including the cash cross-check, sensitivity ranges, and the finding that ex-goodwill invested capital is negative.)*

### Revenue by segment

Through FY2025, Adobe reported three segments. **Starting Q1 FY2026, Adobe combined Digital Media, Digital Experience, and Publishing and Advertising into a single reportable segment** "due to changes in how management evaluates results and allocates resources, reflecting the Company's shift to unified selling motions and integrated product innovation" (`primary_sources/2Q2026/financial_statements.md`, Note 15). Consequently, no segment-level breakdown exists for H1 2026 or TTM — only consolidated results are shown for those periods in the table above.

| Segment (FY2025)           | Revenue | Cost of revenue | Gross profit | Gross margin |
| --------------------------- | ------- | ---------------- | ------------- | ------------- |
| Digital Media               | 17,649  | 841              | 16,808        | 95%           |
| Digital Experience          | 5,864   | 1,625            | 4,239         | 72%           |
| Publishing and Advertising  | 256     | 85               | 171           | 67%           |
| **Total**                    | **23,769** | **2,551**     | **21,218**    | **89%**       |

| Segment (FY2024)           | Revenue | Cost of revenue | Gross profit | Gross margin |
| --------------------------- | ------- | ---------------- | ------------- | ------------- |
| Digital Media               | 15,864  | 680              | 15,184        | 96%           |
| Digital Experience          | 5,366   | 1,589            | 3,777         | 70%           |
| Publishing and Advertising  | 275     | 89               | 186           | 68%           |
| **Total**                    | **21,505** | **2,358**     | **19,147**    | **89%**       |

| Segment (FY2023)           | Revenue | Cost of revenue | Gross profit | Gross margin |
| --------------------------- | ------- | ---------------- | ------------- | ------------- |
| Digital Media               | 14,216  | 665              | 13,551        | 95%           |
| Digital Experience          | 4,893   | 1,603            | 3,290         | 67%           |
| Publishing and Advertising  | 300     | 86               | 214           | 71%           |
| **Total**                    | **19,409** | **2,354**     | **17,055**    | **88%**       |

*(Source: `primary_sources/FY2025/financial_statements.md`, Note 2. Note: the CODM does not review segment operating expenses or segment assets, so operating income and EBITDA cannot be disaggregated below the gross-profit line for any period — Adobe discloses only segment revenue, cost of revenue and gross profit.)*

### Other operating metrics

| Metric                                             | FY2024   | FY2025   | H1 2025  | H1 2026  |
| --------------------------------------------------- | -------- | -------- | -------- | -------- |
| Deferred revenue (total, period-end)                | $6,259M  | $7,030M  | n/a      | $7,250M  |
| Remaining performance obligations (RPO)             | n/a      | $22.52B  | $19.69B  | $22.27B  |
| Effective tax rate (GAAP)                           | 20%      | 18%      | 18%      | 23%      |

*(Deferred revenue and RPO: `primary_sources/FY2025/financial_statements.md` Note 2; `primary_sources/2Q2026/financial_statements.md` Note 2 and MD&A line 109 ("Remaining performance obligations of $22.27 billion as of May 29, 2026 increased by 13% from $19.69 billion as of May 30, 2025"). Effective tax rate: `primary_sources/FY2025/md_and_a.md` line 327; `primary_sources/2Q2026/md_and_a.md` line 288.)*

**Notes:**

- Total cost of revenue, R&D, S&M and G&A detail (the components of gross profit and operating income above) are in `primary_sources/FY2025/financial_statements.md` (Consolidated Statements of Income) and `primary_sources/2Q2026/financial_statements.md` (Condensed Consolidated Statements of Income). FY2024 operating expenses include a one-off $1,000M Figma acquisition termination fee, which depresses FY2024 operating margin relative to FY2023 and FY2025 — this is a known one-time item, not a trend (`primary_sources/FY2025/financial_statements.md` line 95).
- H1 2026 gross profit and revenue include a partial quarter of Semrush (acquired April 28, 2026 for $1.87B cash; `primary_sources/2Q2026/financial_statements.md` Note 3), but Adobe states the impact "was not material" to the condensed consolidated financial statements, so no pro-forma adjustment is made.
- EBITDA here is a simple GAAP construction (EBIT + cash-flow-statement D&A) for comparability purposes; it differs from the owners'-earnings build in `owners_earnings_and_roic.md`, which separately identifies PP&E depreciation ($236M FY2025) and purchased-intangible amortization ($310M FY2025) and treats non-recurring items and maintenance capex differently. Do not mix the two measures.
- Basic and diluted EPS are shown only for full fiscal years as reported; Adobe does not report a standalone TTM EPS figure, and computing one would require reconciling quarterly share-count changes that are not the focus of this summary.
- Q2 FY2026 includes a $70M non-cash goodwill impairment (Publishing & Advertising reporting unit) and a $92M ROSCA/FTC loss contingency (settled March 12, 2026) inside G&A — both flow through operating income and EBIT above without adjustment, consistent with reported GAAP figures (`primary_sources/2Q2026/financial_statements.md` Note 7, Note 13).

---

## 2. Capitalization, Cash, Debt, and Enterprise Value

| Item                                | Value (USD millions except per share and share count) |
| ------------------------------------ | ------------------------------------------------------- |
| Stock price                          | $284.88                                                  |
| Basic shares                         | 397.5M                                                   |
| Fully diluted shares                 | 397.8M                                                   |
| Implied market cap (basic)           | $113,240M                                                |
| Implied market cap (fully diluted)   | $113,325M                                                |
| Cash and cash equivalents            | $4,919M                                                  |
| Short-term investments               | $707M                                                    |
| Cash + short-term investments        | $5,626M                                                  |
| Total debt (senior notes + CP)       | $6,645M                                                  |
| Total operating lease liabilities    | $420M                                                    |
| Net debt (debt + leases − cash/ST)   | $1,439M                                                  |
| **EV (basic)**                        | **$114,679M**                                            |
| **EV (fully diluted)**                | **$114,764M**                                            |

*(Computed, `financials_summary_calcs.py` §4.)*

**Notes:**

- **Shares outstanding** use the most recent primary-source count: **397.5 million shares as of June 11, 2026**, per the cover page of the Q2 FY2026 10-Q (`primary_sources/2Q2026/cover_page.md`, line 63). This supersedes the FY2025 10-K cover page's 410.5M count as of January 9, 2026 (`primary_sources/FY2025/cover_page.md`, line 75), which is older. No developments after quarter-end (e.g. additional buybacks disclosed in later filings) were available to adjust this further, since no primary source postdates June 11, 2026.
- **Diluted shares** add 0.3 million to the basic count — the "dilutive potential common shares from stock plans and programs" disclosed for the six months ended May 29, 2026 in the EPS reconciliation (`primary_sources/2Q2026/financial_statements.md`, Note 12). This is a weighted-average-period figure (the closest disclosed proxy for a point-in-time dilutive add-on), so the diluted count is an approximation. Note that Adobe separately discloses 9.2 million anti-dilutive potential shares for the same period — these are excluded, consistent with the treasury-stock method, because their assumed exercise proceeds exceed the current share price.
- **Debt** is per Q2 FY2026 10-Q Note 14: $6,150M of senior notes at par (of which $1,350M is classified current), plus $500M of commercial paper drawn in the quarter (carrying value $494M). Carrying values on the balance sheet: current debt $1,843M ($1,349M current senior notes + $494M CP), long-term debt $4,802M.
- **Operating lease liabilities** ($91M current + $329M long-term) are included as debt-like items per the valuation convention specified in the brief. Adobe discloses no finance leases (`primary_sources/FY2025/financial_statements.md`, Note 1: "We do not have any finance leases").
- **No pension shortfall** is included — Adobe's filings do not disclose a defined-benefit pension plan.
- Off-balance-sheet hosting/data-center purchase obligations ($6.82B undiscounted per the FY2025 10-K, Note 16) are **not** included in this EV build. As discussed at length in `work_products/owners_earnings_and_roic.md` §4.1, capitalizing these without also adding back the associated rent expense to earnings double-counts the cost, since the spend is already fully expensed in cost of revenue as incurred. This is a judgment call flagged for consistency with the owners'-earnings work; if a reader prefers to include the ~$6.3B present value of these commitments as debt, EV would rise to roughly $120.9B (basic) / $121.0B (diluted), a further ~5.5% (computed, `financials_summary_calcs.py`; PV of $6,259M for the hosting commitments is taken unchanged from `owners_earnings_and_roic.md` §4.1).
- Market-cap and EV figures use the user-supplied stock price of $284.88 (2026-09-03). Note the Knowledge Store shows other, dated price points that do not match: $290.00 close on August 27, 2026 (Knowledge Store ID 7) and $292.40/share as of August 31, 2026 (Knowledge Store ID 63) — both are ~2–3% higher than the $284.88 used here, consistent with normal day-to-day price movement in the intervening days rather than a data conflict.

---

## 3. Valuation (LTM to Q2 FY2026)

| Metric                    | Basic | Fully Diluted |
| -------------------------- | ----- | -------------- |
| EV/EBIT                    | 12.6x | 12.6x          |
| EV/EBITDA                  | 11.6x | 11.7x          |
| EV/unlevered FCF           | 10.9x | 10.9x          |
| EV/Owners' Earnings        | 15.3x | 15.3x          |
| P/E (on LTM net income)    | 15.7x | 15.7x          |

*(Computed, `financials_summary_calcs.py` §5. LTM EBIT $9,090M, LTM EBITDA $9,849M, LTM unlevered FCF $10,541M, LTM net income $7,229M — all computed as FY2025 + H1 2026 − H1 2025. LTM Owners' Earnings of $7,490M is taken unchanged from `work_products/owners_earnings_and_roic.md` §1, Method A.)*

**Notes:**

- Basic and diluted multiples are nearly identical (the diluted share count is only 0.3M, or 0.08%, above the basic count) because most of Adobe's outstanding stock awards are currently anti-dilutive under the treasury-stock method at the current share price — see the capitalization notes above. This is a real feature of the current setup, not a methodological choice; it can reverse if the share price rises.
- **EV/Owners' Earnings (15.3x) is meaningfully higher than EV/EBITDA (11.6x) or EV/unlevered FCF (10.9x)**, because owners' earnings strips out stock-based compensation (~$2.0B TTM) and the deferred-revenue float build (~$0.8B TTM) as real economic costs/non-recurring cash sources, per the methodology in `owners_earnings_and_roic.md` §2–3. EV/Owners' Earnings is the most conservative of the four multiples shown and is the one most consistent with the "true economic earnings available to owners" definition used elsewhere in this analysis.
- These are point-in-time multiples on trailing results; they say nothing directly about forward growth or margin trajectory. Management's own guidance points to non-GAAP operating margin **compression** in H2 FY2026 (from ~47.4% in Q1 FY2026 to guided ~44% in Q3 FY2026; `primary_sources/1Q2026/` and `primary_sources/2Q2026/earnings_call_transcript.md` — forward guidance, not yet reported results), so the LTM multiples above should not be mechanically extrapolated forward. See `work_products/owners_earnings_and_roic.md` §6 for the fuller discussion of margin-trajectory uncertainty and `work_products/valuation.md` for a forward-looking DCF-style valuation that already exists in this repository.
- All multiples use the EV that **excludes** off-balance-sheet hosting commitments (see §2 note above). Including them would raise EV by ~5% and every multiple in this table by the same proportion.

---

*Calculations: `work_products/financials_summary_calcs.py`.*
