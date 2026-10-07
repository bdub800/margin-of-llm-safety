# NamSys Inc. (TSXV: CTZ) — Owners' Earnings and Return on Invested Capital

All figures in Canadian dollars. Fiscal year ends October 31. Calculations are performed in `work_products/owners_earnings_and_roic.py`; every number below is an output of that script, and every input to that script is tagged with its source filing.

---

## 1. Headline conclusions

| Measure                                                 | FY2025      | TTM to Apr 30, 2026 |
|---------------------------------------------------------|-------------|---------------------|
| Revenue (as reported)                                    | $7,891,605  | $8,207,148          |
| Owners' Earnings (this analysis)                         | ~$2.25M     | ~$2.31M             |
| Owners' Earnings per diluted share                        | ~$0.082     | ~$0.084             |
| Owners' Earnings margin                                  | 28.5%       | 28.1%               |
| Operating Invested Capital (period end)                   | ~$0.99M     | ~$0.91M             |
| ROIC (period-end IC)                                     | ~227%       | ~254%               |
| ROIC (2-point average IC)                                | ~272%       | ~243%               |
| Excess cash + short-term investments (excluded from IC)   | ~$9.78M     | ~$6.96M             |

**The load-bearing conclusion is not the precise ROIC number — it is that NamSys operates on essentially no invested capital.** Operating invested capital is ~$1M against ~$2.3M of annual owners' earnings, so ROIC is a three-digit number under any reasonable assumption set and is not a binding constraint on growth. The economically meaningful statements are: (a) owners' earnings are ~$2.3M and convert to cash at ~99% over four years; (b) growth to date has required almost no incremental capital; and (c) the ~$7.4M of net cash on the balance sheet (April 30, 2026) is genuinely surplus and earns a separate, sub-inflation return.

---

## 2. Owners' Earnings — method

Per the definition in use, Owners' Earnings is the economic cash return available to common shareholders **before** any return on or from the balance sheet's financial assets. The build therefore starts at **reported operating income** (which already sits above interest income and below all operating costs) rather than at net income.

Three structural features of NamSys make this unusually clean:

1. **No debt, no interest expense.** "Other than trade and other payables, the Company has no debt outstanding and incurred no interest expense in respect of outstanding debt in the current or comparative periods" (FY2025 MD&A, *Financing and Other Costs and Income*). So the usual "add back interest expense" step is nil.
2. **No capitalised development costs.** "Software development costs are charged to net income in the period they are incurred, unless they meet specific capitalization criteria" (FY2025 AFS, Note 2, *Research and software development costs*). The balance sheet carries no intangible assets at all (FY2025 AFS, *Statements of Financial Position*). Reported operating income is therefore already struck after 100% of R&D — there is no hidden capex sitting in investing activities.
3. **Essentially no physical capital.** Total property and equipment is $34,689 at October 31, 2025 (FY2025 AFS, Note 4); FY2025 depreciation was $7,465 and FY2025 capex $9,661. Management confirmed the company "continue[s] to operate fully remote" with "21 employees" (`fetched_docs/namsys_2026_annual_meeting_transcript.md`). Depreciation is a real, if trivial, economic cost, and maintenance capex ≈ depreciation.

### 2.1 The bridge

| Line                                                | FY2022      | FY2023      | FY2024      | FY2025      | TTM Apr-26  |
|-----------------------------------------------------|-------------|-------------|-------------|-------------|-------------|
| Revenue                                              | 5,394,781   | 6,093,020   | 6,840,146   | 7,891,605   | 8,207,148   |
| Operating income (as reported)                       | 1,753,157   | 2,107,434   | 2,572,018   | 3,146,476   | 3,299,241   |
| + reported bad debt expense                          | 2,546       | 23,004      | 0           | 51,330      | 584         |
| − normalised bad debt expense                        | (19,220)    | (19,220)    | (19,220)    | (19,220)    | (19,220)    |
| + reported share-based compensation                  | 0           | 191,468     | 114,174     | 47,030      | 24,904      |
| − normalised share-based compensation                | (117,557)   | (117,557)   | (117,557)   | (117,557)   | (117,557)   |
| + depreciation of property and equipment             | 12,028      | 7,191       | 7,023       | 7,465       | 7,639       |
| − maintenance capex (actual PP&E purchases)          | (9,311)     | (4,982)     | (8,259)     | (9,661)     | (9,258)     |
| **= Normalised pre-tax owners' earnings**            | **1,621,643** | **2,187,338** | **2,548,179** | **3,105,863** | **3,186,333** |
| − normalised tax @ 26.5% (SBC non-deductible)        | (460,888)   | (610,797)   | (706,420)   | (854,206)   | (875,531)   |
| − other permanent tax differences (Note 9 residual)  | (1,091)     | (22,509)    | (3,013)     | (1,385)     | (1,162)     |
| **= OWNERS' EARNINGS**                               | **1,159,664** | **1,554,032** | **1,838,746** | **2,250,271** | **2,309,639** |
| OE margin                                            | 21.5%       | 25.5%       | 26.9%       | 28.5%       | 28.1%       |
| *Memo:* reported net income                          | 1,394,440   | 1,614,875   | 2,090,475   | 2,486,109   | 2,538,827   |
| *Memo:* interest income excluded                     | 5,812       | 195,112     | 291,840     | 265,771     | 244,711     |
| *Memo:* FX gain/(loss) excluded                      | 139,768     | (5,780)     | 25,590      | (10,945)    | (79,206)    |

TTM figures are FY2025 + H1 FY2026 − H1 FY2025, from `primary_sources/2Q2026/FS_Q2_NamSys_Apr_30_26_FINAL.md`.

### 2.2 Justification of each adjustment

**(a) Interest income removed (all periods).** Interest income of $265,771 in FY2025 (FY2024: $291,840) is a return on the GIC portfolio (FY2025 AFS, *Statements of Operations*; Note 15), not on the operating business. Starting from operating income excludes it automatically. It is accounted for separately as a balance-sheet asset (Section 4).

**(b) Foreign exchange gain/loss removed (all periods).** The FX line is the remeasurement of USD-denominated receivables: "The Company invoices its foreign customers in US dollars and recognizes a foreign exchange gain (loss) when the Canadian dollar amount of the receivable at period end, or the amount received in the period, is greater (less) than at the time of invoicing" (FY2025 MD&A, *Gain (loss) on foreign exchange*). It is a timing effect on a balance, not a change in earning power, and it is volatile: +$139,768 (FY2022), −$5,780, +$25,590, −$10,945, and −$79,206 on a TTM basis. Normalising it to nil is a judgment call. *This is the single largest discretionary exclusion in the TTM figure — including the TTM FX loss would cut TTM owners' earnings by ~$58k after tax, to ~$2.25M.* Note that this is **not** the same as the company's underlying CAD/USD exposure, which is far larger: ~96% of revenue is invoiced in USD (FY2025 AFS, Note 11) against a largely Canadian cost base, and that exposure is embedded in translated revenue, not in this line.

**(c) Bad debt normalised to $19,220 (four-year average of reported expense).** Reported bad debt has been $2,546 / $23,004 / $nil / $51,330 across FY2022–FY2025 and effectively $584 on a TTM basis. FY2025 was the worst year ("the Company determined that trade receivables from two customers were not collectible," FY2025 AFS, Note 3) and the TTM period is flattered by the FY2025 comparative dropping out. Given customer concentration — three customers were 15.9%, 12.3% and 10.7% of FY2025 revenue and 49% of the receivable balance (FY2025 AFS, Notes 3 and 7) — write-offs are a recurring cost of doing business, not an anomaly. The adjustment *raises* FY2025 pre-tax earnings power by $32,110 (replacing the reported $51,330 with the $19,220 normal level) and *reduces* TTM by $18,636 (replacing the near-nil reported $584 with $19,220), i.e. it cuts both ways. Magnitude is ~1% of owners' earnings either way.

**(d) Share-based compensation normalised to $117,557/yr.** SBC is a genuine economic cost to owners and is already expensed under IFRS, so no add-back is warranted. The issue is the *level*: reported SBC is collapsing ($191,468 → $114,174 → $47,030 → $24,904 TTM) because the only live grant — made "during the year ended October 31, 2023", fair value $357,566, vesting evenly over three years (FY2025 AFS, Note 6) — has almost fully amortised, and "No options were granted in the years ended October 31, 2025 and 2024" (FY2025 AFS, Note 6). Taking the run-rate $25k as the ongoing cost of equity compensation would assume NamSys never grants options again, which the existence and 2022 renewal of the option plan contradicts. I normalise to the FY2023–FY2025 average of $117,557, which is corroborated independently by the grant-level arithmetic: $357,566 ÷ 3 years = $119,189/yr. (The filings date the grant only to fiscal 2023; the option table's December 15, 2027 expiry combined with the Black-Scholes "Expected life in year: 5 years" implies a December 2022 grant date, but that is my *inference* and nothing in the calculation depends on it.) The two methods agree to within 1.4%. *This is an assumption, not a fact*; it reduces TTM owners' earnings by ~$93k pre-tax (~3%) versus using reported SBC.

**(e) Tax normalised at 26.5%, with SBC treated as non-deductible, plus each year's unexplained permanent difference.** "The basic rate of 26.50% was applied to the pre-tax income" (FY2025 MD&A, *Provision for Income Taxes*). Each year's Note 9 reconciliation discloses an "Adjustments to determine taxable income" line — the gap between 26.5% × reported pre-tax income and reported tax expense. Stock-option SBC is non-deductible to the issuer in Canada, and that explains most but not all of the gap:

| Period      | Note 9 "Adjustments to determine taxable income" | SBC × 26.5% | Unexplained residual | % explained by SBC |
|-------------|--------------------------------------------------|-------------|----------------------|--------------------|
| FY2022      | 1,091                                            | 0           | 1,091                | n/a (no SBC)       |
| FY2023      | 73,248                                           | 50,739      | 22,509               | 69%                |
| FY2024      | 33,269                                           | 30,256      | 3,013                | 91%                |
| FY2025      | 13,848                                           | 12,463      | 1,385                | 90%                |
| TTM Apr-26  | 7,762                                            | 6,600       | 1,162                | 85%                |

Sources: FY2023 AFS Note 9 (FY2022, FY2023), FY2024 AFS Note 9, FY2025 AFS Note 9, Q2 FY2026 FS Note 9 (H1-26 $1,846 / H1-25 $7,932). The tax charge is therefore 26.5% × (normalised base + normalised SBC) **plus the year's unexplained residual**, rather than assuming SBC is the sole permanent difference. FY2023 is the outlier: $22,509 — roughly a third of that year's adjustment — is driven by some other non-deductible item the filings do not identify. Carrying it explicitly costs FY2023 owners' earnings 1.4%; the effect on FY2025 and TTM is under 0.1%. *The 26.5% base rate is a sourced fact; the SBC-non-deductibility attribution is an inference supported by the FY2024/FY2025/TTM columns above and contradicted in part by FY2023, which is why the residual is carried rather than assumed away.*

**(f) Depreciation added back, maintenance capex deducted.** Both are trivial (~0.1% of revenue) and roughly equal; the net effect is a $2,196 drag in FY2025. FY2022 right-of-use asset depreciation of $10,768 is deliberately **not** added back — it represented the real cost of renting premises (with the $11,250 cash lease payment sitting in financing activities), i.e. a genuine recurring operating cost.

**(g) What I deliberately did NOT adjust.**

- *Growth R&D and growth sales spend are left as a full charge.* FY2025 selling expense rose 61.6% to $714,618, driven by "the addition of a new business development position covering the European market and expanded travel as well as trade show attendance costs ($255,466)" (FY2025 MD&A, *Selling Expenses*). Management describes adding people "half development and half support" and hiring a UK salesperson and an Australian support person (`fetched_docs/namsys_2026_annual_meeting_transcript.md`). Some of this is discretionary growth investment whose removal would raise "maintenance" earnings power. I have not tried to split it: the disclosure does not permit a defensible allocation, and stacking such an estimate would be precisely the kind of false precision to avoid. **The practical effect is that the owners' earnings figures above are conservative** — true maintenance-only earnings power is higher, plausibly by $200–400k pre-tax, but I cannot source that split.
- *The FY2024 related-party costs that disappeared.* FY2024 G&A carried $45,600 of head-office rent and corporate-secretarial fees plus $110,000 of management fees paid to a company partially owned by the then-Chairman, who retired October 31, 2024; both were $nil in FY2025 (FY2025 AFS, Note 8(b)). The MD&A flags $50,000 of this as "a one-time-only management fee paid in the third quarter of 2024." I have **not** added these back to FY2024 or deducted a replacement cost in FY2025, because key management remuneration genuinely fell from $707,000 to $591,000 (FY2025 AFS, Note 8(a)) — the role was not re-priced. Net effect: FY2024 owners' earnings are understated by roughly $50k pre-tax relative to a "clean" year.
- *Office rent.* The FY2025 AFS Note 13 wording — "Monthly lease payments total $9,195 over the 12 month term" — reads as $9,195/month (≈$110k/yr). It is not. The Q2 FY2026 MD&A contractual-obligations table shows a total premises-lease obligation of **$6,896** at April 30, 2026, with nine months remaining: $9,195 × 9/12 = $6,896. So $9,195 is the **annual** total. Consistent with a fully-remote 21-person company, occupancy cost is immaterial and no normalisation is required.

### 2.3 Cash-flow sanity check

An owners' earnings figure that never shows up as cash is a fiction. Comparing to reported operating cash flow less capex less after-tax interest income:

| Period      | Operating cash flow | − capex | − after-tax interest income | = operating FCF | vs Owners' Earnings | Conversion |
|-------------|---------------------|---------|-----------------------------|-----------------|---------------------|------------|
| FY2022      | 962,018             | 9,311   | 4,272                       | 948,435         | 1,159,664           | 82%        |
| FY2023      | 1,659,749           | 4,982   | 143,407                     | 1,511,360       | 1,554,032           | 97%        |
| FY2024      | 2,508,076           | 8,259   | 214,502                     | 2,285,315       | 1,838,746           | 124%       |
| FY2025      | 2,196,505           | 9,661   | 195,342                     | 1,991,502       | 2,250,271           | 89%        |
| TTM Apr-26  | 2,470,641           | 9,258   | 179,863                     | 2,281,520       | 2,309,639           | 99%        |
| **FY22–FY25 cumulative** | —      | —       | —                           | **6,736,612**   | **6,802,712**       | **99%**    |

Four-year cumulative conversion of 99% is strong corroboration that the accrual earnings are real cash. Single-year conversion swings ±15% on working-capital timing — chiefly deferred revenue (+$153,202 in FY2024, −$139,010 in FY2025; FY2025 AFS, *Statements of Cash Flows*) and receivables. FY2025's 89% reflects a real deterioration in collections: on trade receivables only, days sales outstanding rose from 45.7 days at October 31, 2024 ($857,096 ÷ $6,840,146 × 365) to 53.9 days at October 31, 2025 ($1,164,580 ÷ $7,891,605 × 365), with over-90-day balances up from $16,861 to $126,998 (FY2025 AFS, Note 3). I treat this as a working-capital investment/collections issue rather than an earnings overstatement, but it is worth monitoring.

---

## 3. Return on Invested Capital

### 3.1 What counts as invested capital

Invested capital here is **operating** capital only. Excluded: short-term investments and surplus cash (non-operating financial assets — $9,329,249 of cashable GICs at October 31, 2025, FY2025 AFS Note 15); income taxes receivable/payable and deferred income tax assets (tax accounts, not operating capital). Included: an estimate of the cash genuinely needed to run the business, working capital, PP&E, and the capitalised off-balance-sheet office lease. There are no operating lease right-of-use assets on the balance sheet to remove.

| Component (period end)                        | FY2022    | FY2023    | FY2024    | FY2025    | Apr-30-26 |
|-----------------------------------------------|-----------|-----------|-----------|-----------|-----------|
| Operating cash (1 month of cash opex)         | 302,466   | 315,577   | 345,578   | 390,886   | 406,280   |
| + Trade and other receivables                 | 1,038,800 | 1,181,189 | 975,812   | 1,241,499 | 1,381,988 |
| + Prepaid expenses                            | 114,670   | 139,050   | 171,893   | 162,679   | 146,330   |
| + Property and equipment                      | 33,466    | 31,257    | 32,493    | 34,689    | 34,661    |
| − Trade and other payables                    | (433,360) | (423,386) | (428,543) | (544,985) | (360,682) |
| − Deferred revenue                            | (222,349) | (287,783) | (440,985) | (301,975) | (707,554) |
| + Capitalised office lease (as disclosed)     | 0         | 7,474     | 8,927     | 9,195     | 6,896     |
| **= Operating invested capital**              | **833,693** | **963,378** | **665,175** | **991,988** | **907,919** |
| *Memo:* excess cash + short-term investments  | 5,205,656 | 6,902,735 | 7,701,773 | 9,784,786 | 6,959,767 |
| Invested capital as % of revenue              | 15.5%     | 15.8%     | 9.7%      | 12.6%     | 11.1%     |

**Operating cash assumption.** I use one month of cash operating costs (cost of sales + opex, less SBC and depreciation): ~$391k for FY2025. Justification: 99% of revenue is recurring and billed monthly (FY2025 MD&A), there is no debt to service, and the largest single payables item is accrued remuneration. This is the one genuinely arbitrary input, and Section 3.3 sensitises it. Note the company's own stated capital policy is a liquidity floor of "the greater of (i) $50,000 and (ii) an amount required in order to maintain operations and cover general and administrative expenses for a period of 6 months" (FY2025 AFS, Note 12) — that is a TSXV listing-maintenance policy, not an operating requirement, but I run it as the extreme upper bound.

**Off-balance-sheet items.** The premises lease is capitalised at one year of payments, using the commitment disclosed at each balance sheet date rather than a single flat figure: nil at October 31, 2022 (the earlier IFRS-16 right-of-use lease had run off — $11,250 of cash lease payments and $10,768 of ROU depreciation during FY2022 — and the FY2022 AFS is not in `primary_sources`, so no forward commitment is available); $7,474 at October 31, 2023 (FY2023 AFS Note 13, Jan–Dec 2024 lease); $8,927 at October 31, 2024 (FY2024 AFS Note 13, Feb 2025–Jan 2026); $9,195 at October 31, 2025 (FY2025 AFS Note 13, Feb 2026–Jan 2027); and the $6,896 residual obligation at April 30, 2026 (Q2 FY2026 MD&A). The spread is immaterial — under 1.1% of invested capital in any period. The **employee termination commitment of $1,100,000** to three employees (FY2025 AFS, Note 13; unchanged at April 30, 2026) is *not* included in base-case invested capital: it is a contingent liability payable only on termination without cause, not capital deployed in the business. It is sensitised below because it is the largest off-balance-sheet number in the filings and a reasonable analyst could disagree.

### 3.2 ROIC

| Basis                                     | FY2022 | FY2023 | FY2024 | FY2025 | TTM Apr-26 |
|-------------------------------------------|--------|--------|--------|--------|------------|
| ROIC on period-end invested capital        | 139%   | 161%   | 276%   | 227%   | 254%       |
| ROIC on 2-point average invested capital   | n/a    | 173%   | 226%   | 272%   | 243%       |

The TTM period-end figure is flattered by seasonality: deferred revenue at April 30, 2026 was $707,554 versus $301,975 at October 31, 2025 (annual maintenance billings), which artificially depresses invested capital. The 2-point average is the fairer read.

**Incremental ROIC, FY2022 → FY2025:** owners' earnings rose $1,090,608 while operating invested capital rose $158,295. The ratio (~690%) is arithmetically correct but meaningless as a precise figure. The correct statement is: **NamSys added ~$2.5M of revenue and ~$1.1M of owners' earnings over three years while consuming roughly $150k of additional operating capital.** Growth is not capital-constrained.

### 3.3 Sensitivity — FY2025 owners' earnings of $2,250,271 against alternative invested-capital definitions

| Scenario                                                                       | Invested capital | ROIC |
|--------------------------------------------------------------------------------|------------------|------|
| Zero operating cash                                                             | 601,102          | 374% |
| **Base case: 1 month of cash operating costs**                                   | **991,988**      | **227%** |
| Note 12 liquidity policy, literal reading: 6 months of the G&A line only          | 1,184,094        | 190% |
| 3 months of cash operating costs                                                 | 1,773,760        | 127% |
| Base + $1.1M employee termination commitment                                     | 2,091,988        | 108% |
| Note 12 liquidity policy, broad reading: 6 months of *total* cash opex            | 2,946,419        | 76%  |
| Base + 3 years of *all* cost-of-sales compensation capitalised                   | 6,111,512        | 37%  |

Note 12's wording — a floor of the greater of $50,000 and "an amount required in order to maintain operations and cover general and administrative expenses for a period of 6 months" — supports either the narrow reading (6 months of the $1,165,985 G&A line = ~$583,000) or the broad one ("maintain operations" as total cash opex = ~$2,345,000). Both are shown; neither feeds the base case.

The last row is a deliberately punitive upper bound on invested capital, addressing the objection that NamSys's real asset is expensed software. It capitalises three years of the *entire* compensation charge in cost of sales — $1,739,266 (FY2025) plus $1,690,129 (FY2024) taken twice as a proxy for FY2023 (FY2025 AFS, Note 14; FY2023 is not separately disclosed at this granularity, so this is an estimate). It overstates the case badly, because most of that headcount is hosting, delivery and customer support rather than capitalisable development. Even so, ROIC is ~37%.

**The honest conclusion from this table: ROIC is between roughly 37% and 374% depending on definition, and I cannot narrow it much further — nor does it matter.** Every scenario clears any plausible cost of capital by a wide margin. The economically robust statement is the one in Section 3.2: incremental growth has required negligible incremental capital.

---

## 4. The balance-sheet asset, held separately

Owners' earnings above deliberately exclude the financial portfolio. At April 30, 2026 the company held $940,082 of cash and $6,425,965 of short-term investments — $7,366,047, or ~$0.27 per diluted share, against no debt (Q2 FY2026 FS, *Statements of Financial Position*). At October 31, 2025 the figure was $10,175,672 / ~$0.37 per diluted share, consistent with the company's own press release (Knowledge Store ID 8). The decline is entirely capital return: a $0.15/share special dividend of $4,027,790 paid March 2026 plus $240,996 of buybacks in H1 FY2026 (Q2 FY2026 FS, Note 6; Knowledge Store ID 1).

Two observations on the quality of this asset:

- It earns poorly. The GICs bear 2.0%–2.45% (FY2025 AFS, Note 15; Q2 FY2026 FS, Note 15) — at or below likely inflation, so on an after-tax real basis the portfolio destroys a small amount of value each year. Interest income is already falling ($291,840 → $265,771 → $244,711 TTM) despite a larger average balance, reflecting lower rates.
- Management has been unable to deploy it. "We have been focused for several years on an acquisition strategy. That has not been successful, but it is not for lack of trying" (`fetched_docs/namsys_2026_annual_meeting_transcript.md`). The March 2026 special dividend is the corrective action.

For valuation, the sensible treatment is owners' earnings plus surplus cash valued at roughly par, not owners' earnings capitalised at a multiple that implicitly re-values the cash.

---

## 5. What I am confident about vs. what is genuinely uncertain

**High confidence (directly sourced, low estimation content):**

- Owners' earnings of **$2.2–2.3M** in FY2025/TTM. The largest single normalising adjustment (SBC) moves the answer by ~3%; all adjustments combined move FY2025 by only $62,389, or 2.7%, from reported operating income taxed at 26.5% ($2,312,660).
- Four-year cash conversion of ~99% — the earnings are real cash.
- Operating invested capital is under $1.5M on any reasonable definition, versus $7.4M of surplus net cash.
- The business is structurally capital-light: no debt, no capitalised software, $34,689 of PP&E, fully remote.
- Owners' earnings have compounded from $1.16M (FY2022) to $2.25M (FY2025), i.e. 24.7%/yr, ahead of 13.5%/yr revenue growth — genuine operating leverage.

**Genuinely uncertain:**

- **The precise ROIC number.** Range of 37%–374% across defensible definitions (Section 3.3). Treat "ROIC is very high and not a constraint" as the finding; treat any point estimate as decoration.
- **Normalised SBC.** No grants since December 2022. If the company never grants again, TTM owners' earnings are ~$93k pre-tax higher than shown. If it grants on a larger base at today's ~$1.20 share price (Knowledge Store ID 1), the true run-rate cost is higher than $117,557. My figure sits near the middle of that range but is an assumption.
- **Maintenance vs. growth split within opex.** Unsourceable from the filings. My figures charge 100% of growth spending against owners' earnings, which understates maintenance earnings power — an asymmetry that favours the buyer.
- **Whether the FY2025 gross-margin and expense structure holds.** H1 FY2026 shows cost-of-sales compensation up 20.4% year-on-year ($844,523 → $1,016,795; Q2 FY2026 FS, Note 14) against revenue up only 8.0%, and gross margin compressing. Management states margins "will remain stable going forward" (`fetched_docs/namsys_2026_annual_meeting_transcript.md`), but TTM owners' earnings growth of 2.6% versus FY2025's 22.4% shows the near-term deceleration is real, not an artefact of my adjustments.
- **The forward growth rate.** ROIC does not bind it — the constraint is sales and market penetration, not capital. Management cites ~8% of US cash-in-transit vehicles running its software and an international market "at least 10 times" the US (`fetched_docs/namsys_2026_annual_meeting_transcript.md`); those are unaudited management estimates and should be treated as such.

**Practical implication:** because invested capital is negligible and there is no debt, essentially **100% of owners' earnings is distributable each year without impairing the business** — which is exactly the pattern observed (special dividends of $1,350,477 in FY2024 and $4,027,790 in FY2026, plus continuous NCIB buybacks; FY2025 AFS Note 6, Q2 FY2026 FS Note 6).

---

## 6. Source index

| Reference                                                     | Used for                                                                          |
|---------------------------------------------------------------|-----------------------------------------------------------------------------------|
| `primary_sources/FY2023/Namsys_-_Annual_FS_-_Feb262024.md`     | FY2022/FY2023 statements; Note 9 tax reconciliation; Note 13 office lease          |
| `primary_sources/FY2024/NamSys_AFS_021925.md`                  | FY2024 statements; Note 9 tax reconciliation; Note 13 office lease                 |
| `primary_sources/FY2025/NamSys_AFS_022426.md`                  | FY2025 statements; Notes 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 15                      |
| `primary_sources/FY2025/NamSys_MDA_022426.md`                  | Tax rate, segment expense commentary, interest income, FX commentary                |
| `primary_sources/2Q2026/FS_Q2_NamSys_Apr_30_26_FINAL.md`       | H1 FY2026/H1 FY2025 statements; Notes 6, 8, 9, 13, 14, 15                           |
| `primary_sources/2Q2026/MDA_Q2_NamSys_Apr_30_26_FINAL.md`      | Contractual obligations table (resolves the office-lease ambiguity); capex          |
| `fetched_docs/namsys_2026_annual_meeting_transcript.md`        | Headcount, remote operation, acquisition strategy, margin guidance, market context  |
| Knowledge Store ID 1                                           | Share price ~$1.20 (July 2026); $0.15 special dividend / $4,027,790                 |
| Knowledge Store ID 8                                           | FY2025 press release; net cash $10,175,672 = $0.37 per diluted share                |
| `work_products/owners_earnings_and_roic.py`                    | All calculations                                                                    |
