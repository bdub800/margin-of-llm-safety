# Boyd Group Services Inc. (BYD.TO / BGSI) — Owners' Earnings and ROIC

All figures in **US$ millions** unless stated. Boyd reports in U.S. dollars. Calculations: `work_products/owners_earnings_roic.py` (run with `uv run python work_products/owners_earnings_roic.py`). Excel model: `work_products/valuation.xlsx`, built by `work_products/build_valuation_xlsx.py` and formula-verified by `work_products/verify_valuation_xlsx.py` (all checks pass).

Sources are the audited/interim filings in `primary_sources/`: `FY2023/Boyd_AFS.md`, `FY2023/Boyd_MDA.md`, `FY2024/Boyd_AFS.md`, `FY2024/Boyd_MDA.md`, `FY2025/BoydGroup_AFS.md`, `FY2025/BoydGroup_MDA.md`, `Q2FY26/BoydGroup_Q2.md`, `Q2FY26/BoydGroup_MDA.md`.

---

## 1. Headline answer

| Metric                                         | FY2023  | FY2024  | FY2025  | TTM Jun-2026 |
|------------------------------------------------|---------|---------|---------|--------------|
| Sales                                          | 2,946.0 | 3,070.3 | 3,142.8 | 3,594.4      |
| Adjusted EBITDA (as reported)                  |   368.2 |   334.8 |   376.3 |   460.3      |
| **Owners' Earnings (after normalized tax)**    | **132.4** | **91.8** | **108.9** | **145.9**  |
| Owners' Earnings margin                        |    4.5% |    3.0% |    3.5% |     4.1%     |
| **ROIC (OE ÷ avg. invested capital, ex-leases)** | **10.2%** | **6.4%** | **7.1%** | **6.5%**  |
| ROIC on tangible capital (ex-goodwill/intangibles) |  38.6% |  20.3% |  20.8% |    24.5%     |

Two facts dominate: Owners' Earnings is only ~29% of reported Adjusted EBITDA, because rent and maintenance capex consume roughly $215M of the $376M FY2025 Adjusted EBITDA; and ROIC on total capital deployed (~6–7%) is well below ROIC on tangible operating capital (~20%), because Boyd has paid ~$2.3bn of goodwill and acquired intangibles to assemble the network.

---

## 2. Method

Owners' Earnings = the cash the operating business throws off to common shareholders after all costs required to maintain the current earning power, **before** interest on debt and before growth capital.

Bridge (each line is a formula in `valuation.xlsx`, sheet "1 Earnings", section 2):

```
    Adjusted EBITDA (company-reported)
  − Cash lease payments (principal + interest)      ← replaces IFRS 16 ROU depreciation + lease finance cost
  − Maintenance capex (1.7% of sales)               ← replaces depreciation of PP&E
  − Software & licensing capex (actual)             ← replaces software amortization
  − Normalized recurring acquisition costs ($5M)
  = Pre-tax Owners' Earnings
  − Normalized tax @ 26.5%
  = Owners' Earnings
```

### 2.1 Why start from Adjusted EBITDA

Boyd's Adjusted EBITDA excludes only two things beyond D&A and finance costs: non-cash fair value adjustments, and "acquisition and transformational cost initiatives" (FY2025 MD&A, ADJUSTED EBITDA reconciliation). Both exclusions are defensible in principle — but I re-deduct a normalized acquisition charge below. Importantly, Adjusted EBITDA is **already after** share-based compensation, which flows through employee expenses (FY2025 AFS Note 27: long-term incentive plan $6.5M + share options $0.9M in 2025; $0.5M + $0.9M in 2024). So no SBC add-back or deduction is required. SBC is ~0.2% of sales; the year-to-year swing is mark-to-market noise on the cash-settled 2023/2024 plans, not an economic change.

### 2.2 Leases are treated as an operating cost, not as debt

This is the single most consequential methodology choice. Boyd leases substantially its entire shop network (right-of-use assets of $689.2M vs. owned PP&E of $581.1M at Dec-31-2025, FY2025 AFS balance sheet) and **actively converts owned property into leases**: 19 sale-leasebacks for $53.3M of proceeds in 2025, 33 for $64.9M in 2024 (FY2025 AFS Note 8). Management states this "allowed the Company to replenish capital that can be redeployed to further grow the business" and that from Q1-2025 "the development of start-up facilities will primarily be outsourced and upon completion, ownership will transfer directly to a leasing company" (FY2025 MD&A, Liquidity section).

Rent is therefore an unavoidable operating cost of occupying the current store base, not a financing decision. I deduct the **full cash lease payment** — principal plus interest, from the financing section of the cash flow statement ($161.6M in FY2025, which ties exactly to "Repayments $(161,561)" in FY2025 AFS Note 17). In exchange, right-of-use assets and lease liabilities are excluded from invested capital, and **the $1,050.9M of lease liabilities at Jun-30-2026 must NOT be treated as debt in a later enterprise-value bridge** — doing so would double-count. An alternative treatment (capitalize leases) is shown in §5 as a cross-check.

Note this deduction does not double-count the $12.5M of short-term and low-value lease expense already inside operating expenses (FY2025 AFS Note 17), which relates to leases outside the lease-liability balance.

### 2.3 Maintenance capex: 1.7% of sales

Boyd does not publish a maintenance-capex figure, but it publishes the equivalent guidance: *"During 2026, the Company plans to make cash capital expenditures, excluding those related to network technology upgrades and acquisition and development of new locations, within the range of 1.6% and 1.8% of sales"* (FY2025 MD&A, Capital Expenditures; repeated in Q2FY26 MD&A). I use the 1.7% midpoint.

Cross-check against actuals. The cash flow line "Equipment purchases and facility improvements" is the non-growth capex bucket — growth capex sits inside "Acquisition and development of businesses". Actual vs. the 1.7% assumption:

| Year         | Actual equipment capex | % of sales | 1.7% assumption |
|--------------|------------------------|------------|-----------------|
| FY2023       |                  $57.5M |      1.95% |          $50.1M |
| FY2024       |                  $77.3M |      2.52% |          $52.2M |
| FY2025       |                  $54.3M |      1.73% |          $53.4M |
| TTM Jun-2026 |                  $53.3M |      1.48% |          $61.1M |

The assumption sits close to FY2025 actual and is *more* conservative than TTM actual, which is the right posture — H1-2026 equipment capex of $24.8M on $2,010M of sales (1.23%) is implausibly low for a network that just grew 25% via Joe Hudson's, and likely reflects integration-period timing rather than a lower steady-state need. **This is the largest single judgment in the model**; §6 shows the sensitivity.

I add actual software and licensing capex as a separate line rather than embedding it, because it is disclosed separately and is genuinely lumpy ($1.7M → $8.1M over three years).

Two items I deliberately do **not** net against capex:

- **Sale-leaseback proceeds** ($53.3M FY2025, $64.9M FY2024). These are one-off cash inflows exchanged for permanent rent obligations that are already charged in full above. Netting them would count the same benefit twice and make OE look structurally higher than it is.
- **Growth capex.** Boyd invested ~$54.0M in leaseholds and equipment for 27 start-up facilities in 2025 and ~$23.0M for 12 in 2024 (FY2025 MD&A, Start-ups), plus $218.5M in "Acquisition and development of businesses" (FY2025 AFS cash flows). This is discretionary growth spending and is correctly excluded from Owners' Earnings — but it is what management actually does with the money, and it is why OE will not simply be paid out.

### 2.4 Amortization of intangibles is excluded

FY2025 amortization of $28.0M is overwhelmingly acquired customer relationships ($22.8M, FY2025 AFS Note 11). Boyd's own reasoning is correct here: *"There are no future capital expenditures associated with maintaining or replacing these intangible assets"* (FY2025 MD&A, Adjusted Net Earnings). The economic cost was the purchase price, which is captured in invested capital, not a recurring charge. Excluding it from OE while keeping the intangible in invested capital is the internally consistent pairing.

### 2.5 Normalized acquisition costs of $5M/yr

Boyd expensed $30.5M of "acquisition and transformational cost initiatives" in FY2025 and $48.0M TTM. These split into (i) Joe Hudson's transaction costs — $9.1M net of tax in 2025 (FY2025 MD&A, five-year summary) and $13.5M pre-tax in H1-2026 (Q2FY26 AFS Note 4) — and (ii) Project 360 costs-to-achieve, $13.4M in 2025 (FY2025 MD&A). Neither recurs at that level. But Boyd completed 21 acquisitions in 2025 and 33 in 2024 (FY2025 AFS Note 5), so *some* deal cost recurs every year. The pre-mega-deal, pre-Project-360 run rate was $4.3M (FY2023) and $1.7M (FY2022). I deduct a flat $5.0M.

**This is a judgment, not a sourced figure.** A purist would deduct nothing (deal costs are part of the price of growth, which OE excludes); doing so would raise OE by ~$3.7M after tax in every period, or ~3%. It does not change any conclusion.

### 2.6 Taxes at 26.5% statutory, not at cash rates

FY2025 AFS Note 10a gives the combined basic Canadian and U.S. federal, provincial and state statutory rate as 26.66% (2025) and 26.53% (2024). Cash taxes paid were far lower — $3.7M in FY2025, $12.3M in FY2024, $27.9M in FY2023 — because of tax-deductible goodwill amortization on acquisitions ("Goodwill recognized during 2025 is expected to be deductible for tax purposes", FY2025 AFS Note 5) and U.S. bonus depreciation. Those shields are a function of *continued acquisition activity*, which is growth spending that OE excludes. Using the cash rate would be internally inconsistent — it would credit OE with a benefit generated by the growth capital OE ignores. I therefore use the statutory rate, which is the conservative and consistent choice. The size of the gap to actual cash tax, by period, is shown in the memo at the end of §3. Flagging the implication: reported cash generation will exceed OE for as long as Boyd keeps acquiring.

Simplification: the tax rate is applied to (Adjusted EBITDA − rent − maintenance capex), i.e. maintenance capex is implicitly assumed to equal tax depreciation. In a steady state that holds by construction; in Boyd's current growth phase, actual depreciation exceeds maintenance capex, so this is mildly conservative.

---

## 3. Owners' Earnings — full bridge

| (US$ millions)                             | FY2023  | FY2024  | FY2025  | TTM Jun-2026 |
|--------------------------------------------|---------|---------|---------|--------------|
| Sales                                      | 2,946.0 | 3,070.3 | 3,142.8 | 3,594.4      |
| Adjusted EBITDA                            |   368.2 |   334.8 |   376.3 |   460.3      |
| Adjusted EBITDA margin                     |   12.5% |   10.9% |   12.0% |   12.8%      |
| (−) Cash lease payments                    |  (131.4)|  (149.7)|  (161.6)|  (189.8)     |
| (−) Maintenance capex @ 1.7% of sales      |   (50.1)|   (52.2)|   (53.4)|   (61.1)     |
| (−) Software & licensing capex             |    (1.7)|    (3.1)|    (8.1)|    (5.9)     |
| (−) Normalized acquisition costs           |    (5.0)|    (5.0)|    (5.0)|    (5.0)     |
| **= Pre-tax Owners' Earnings**             | **180.1** | **124.8** | **148.2** | **198.5** |
| (−) Normalized tax @ 26.5%                 |   (47.7)|   (33.1)|   (39.3)|   (52.6)     |
| **= Owners' Earnings**                     | **132.4** | **91.8** | **108.9** | **145.9**  |
| Owners' Earnings margin                    |    4.5% |    3.0% |    3.5% |    4.1%      |

Period definitions: FY figures are as reported. TTM Jun-2026 = Q3-2025 + Q4-2025 + Q1-2026 + Q2-2026, built from the Q2FY26 MD&A quarterly Adjusted EBITDA table (98.4 + 103.6 + 122.4 + 135.9 = 460.3) and from FY2025-minus-H1-2025-plus-H1-2026 for every cash-flow line.

### Cross-check: reported cash flow from operations to Owners' Earnings

Boyd reports all interest and all lease principal in *financing* activities (FY2025 AFS Note 2u), so reported cash flow from operations is before rent and before interest. Running from there to normalized Owners' Earnings — using **actual** cash rent, **actual** capex and **actual** taxes — shows exactly what each normalization is worth:

| (US$ millions)                                            | FY2023  | FY2024  | FY2025  | TTM Jun-2026 |
|-----------------------------------------------------------|---------|---------|---------|--------------|
| Cash flow from operations (reported)                      |   357.5 |   313.3 |   353.0 |   407.0      |
| (−) Cash lease payments — actual                          |  (131.4)|  (149.7)|  (161.6)|  (189.8)     |
| (−) Equipment purchases & facility improvements — actual  |   (57.5)|   (77.3)|   (54.3)|   (53.3)     |
| (−) Software purchases and licensing — actual             |    (1.7)|    (3.1)|    (8.1)|    (5.9)     |
| **Cash flow after rent and actual capex**                 | **167.0** | **83.2** | **129.0** | **158.0** |
| (−) Working capital swing (OE normalizes to nil)          |   (19.1)|     5.9 |    (5.8)|    19.4      |
| (−) Equity-settled SBC added back in CFO                  |     0.0 |    (0.9)|    (4.3)|    (7.1)     |
| (−) Other non-cash items added back in CFO                |    (0.4)|    (1.0)|    (2.9)|    (6.4)     |
| (+) Actual acquisition & transformational costs           |     4.3 |     9.9 |    30.5 |    48.0      |
| (−) Normalized recurring acquisition cost                 |    (5.0)|    (5.0)|    (5.0)|    (5.0)     |
| (+) Capex: actual less assumed maintenance capex          |     7.4 |    25.1 |     0.9 |    (7.8)     |
| (+) Current income tax expense (added back)               |    25.9 |     7.7 |     5.8 |    (0.6)     |
| (−) Normalized income tax @ 26.5%                         |   (47.7)|   (33.1)|   (39.3)|   (52.6)     |
| **= Owners' Earnings (normalized)**                       | **132.4** | **91.8** | **108.9** | **145.9** |
| Check: less primary method                                |     0.0 |     0.0 |     0.0 |     0.0      |

Every reconciling item is a disclosed figure and the reconciliation **foots to zero in all four periods** — there is no plug. Two construction notes: the add-back is *current income tax expense* from the statement of earnings rather than cash tax paid, because the working-capital line already carries the income-taxes-payable movement and using the cash figure would double-count it; and the "Other" non-cash add-back in CFO is removed because it is mostly losses on disposal, which sit in operating expenses and are therefore already inside Adjusted EBITDA.

**What this does and does not establish.** It confirms the Owners' Earnings build reconciles cleanly to reported cash flow with no unexplained residual, which rules out an error in the EBITDA build-up or in transcribing cash-flow lines. It does not prove the assumptions are *right* — it shows what they are worth, so a reader can disagree and re-price them. The three normalizations are individually large and partly offsetting: in FY2025 the acquisition-cost normalization adds $25.5M net while the tax normalization subtracts $33.5M net; in TTM they are +$43.0M and −$53.2M. Normalized OE landing near actual post-capex cash flow in FY2025 ($108.9M vs. $129.0M) reflects that offset, not independent confirmation.

### Memo: actual cash tax paid vs. Adjusted EBITDA after rent

Computed in `owners_earnings_roic.py`, section 12. "Adjusted EBITDA after rent" = Adjusted EBITDA less cash lease payments (principal + interest), i.e. the same starting point the Owners' Earnings bridge uses before capex. FY2022 is shown for a longer history only; it is not used elsewhere in the model.

| (US$ millions)                     | FY2022  | FY2023  | FY2024  | FY2025  | TTM Jun-26 |
|------------------------------------|---------|---------|---------|---------|------------|
| Adjusted EBITDA                    |   273.5 |   368.2 |   334.8 |   376.3 |      460.3 |
| (−) Cash lease payments            |  (117.0)|  (131.4)|  (149.7)|  (161.6)|    (189.8) |
| **Adjusted EBITDA after rent**     | **156.5** | **236.9** | **185.2** | **214.7** | **270.5** |
| Cash income taxes paid (actual)    |     3.9 |    27.9 |    12.3 |     3.7 |        4.4 |
| **Cash tax % of EBITDA after rent** | **2.5%** | **11.8%** | **6.6%** | **1.7%** | **1.6%** |
| Normalized OE tax, % of same base  |     n/a |   20.1% |   17.9% |   18.3% |      19.4% |

Sources: cash taxes paid — FY2023 AFS line 297 (FY2023 and FY2022), FY2024 AFS line 300, FY2025 AFS line 318, and Q2FY26 interim line 190 for the H1 figures used in TTM ($3,669k − $2,555k + $3,260k = $4,374k). FY2022 Adjusted EBITDA from FY2023 MD&A line 282; FY2022 lease payments from FY2023 AFS lines 277–281 ($92,203k + $3,047k + $21,363k + $432k). Other periods as in the §3 bridge.

**What it shows.** Boyd has paid cash tax of only 1.6–11.8% of Adjusted EBITDA after rent, and under 2% in FY2025 and TTM, against the 17.9–20.1% implied by the normalized 26.5% charge on the same base. (The normalized charge is below 26.5% of this base because it is applied after maintenance capex and normalized acquisition costs.) FY2023 is the outlier high: it was the peak earnings year, with earnings before income taxes of $119.5M (FY2023 AFS line 221) against $28.7M in FY2025 (FY2025 AFS line 239).

**Why cash tax is this low.** Three disclosed reasons, and a fourth that matters for consistency:

- **Tax-deductible acquisition goodwill and intangibles.** "Goodwill recognized during 2025 is expected to be deductible for tax purposes" (FY2025 AFS Note 5, line 703). For 2026, ~$374.0M of acquisition goodwill and ~$602.6M of Joe Hudson's intangibles are expected to be deductible (Q2FY26 interim Note 4, lines 316-318). This shield is large and will persist for years, but only because Boyd keeps buying businesses.
- **Accelerated / bonus depreciation.** FY2025 AFS Note 10 (line 848) refers to "states that do not conform to federal bonus depreciation provisions". Inference: this implies Boyd is claiming federal bonus depreciation, which front-loads tax deductions on capex; the filings do not quantify it.
- **Loss carryforwards.** US net operating losses of $37.4M and Canadian non-capital losses of $24.4M at Dec-2025 (FY2025 AFS Note 10d, line 903).
- **Interest deductions.** Cash tax is a *levered* figure — it is after the deduction for interest on debt — while Owners' Earnings is measured *before* interest and so needs an *unlevered* tax. FY2025 interest on long-term debt of $32.7M (FY2025 AFS line 300) shields about $8.7M of tax at 26.5%. That part of the gap belongs to the debt holders' side of the capital structure, not to the operating business.

**What it is worth.** Had actual cash tax been used instead of the normalized charge, Owners' Earnings would be $152.2M (FY2023), $112.5M (FY2024), $144.6M (FY2025) and $194.1M (TTM), against $132.4M / $91.8M / $108.9M / $145.9M as reported — $20–48M a year higher. I keep the normalized rate for the reasons in §2.6: most of the shield is generated by acquisition spending, which Owners' Earnings excludes, and part of it is an interest shield that Owners' Earnings, being pre-interest, should not claim. But this is a real and persistent cash benefit to shareholders so long as Boyd keeps acquiring, and a valuation should account for it separately — for example as a present value of the tax amortization shield on the existing goodwill and intangibles base (an inference about method, not computed here).

---

## 4. Invested capital

Invested capital = operating capital Boyd itself funded. It **excludes** right-of-use assets (paired with charging full rent), cash above an operating requirement, deferred tax balances, derivative instruments, and all interest-bearing debt.

**What is added and what is subtracted**, line by line, straight off the face of the statements of financial position (FY2023 AFS for Dec-2022/Dec-2023; FY2025 AFS for Dec-2024/Dec-2025; Q2FY26 interim for Jun-2026):

| (US$ millions)                               | Dec-2022 | Dec-2023 | Dec-2024 | Dec-2025 | Jun-2026 |
|----------------------------------------------|----------|----------|----------|----------|----------|
| (+) Cash, capped at operating requirement    |     15.1 |     22.5 |     20.0 |     25.0 |     23.0 |
| (+) Accounts receivable                      |    139.3 |    145.8 |    120.6 |    137.5 |    175.2 |
| (+) Income taxes recoverable                 |      5.7 |      7.7 |     12.3 |     10.2 |      9.3 |
| (+) Inventory                                |     78.8 |     78.5 |     73.1 |     68.3 |     78.0 |
| (+) Prepaid expenses                         |     36.5 |     41.7 |     44.7 |     53.8 |     61.4 |
| (+) Property, plant and equipment            |    314.6 |    439.0 |    529.7 |    581.1 |    714.2 |
| (+) Intangible assets                        |    332.9 |    342.8 |    336.9 |    356.3 |  1,029.8 |
| (+) Goodwill                                 |    601.7 |    634.0 |    643.9 |    702.5 |  1,227.8 |
| (+) Other long-term assets                   |      6.1 |     11.7 |     12.1 |     12.6 |     14.0 |
| (−) Accounts payable and accrued liabilities |   (307.7)|   (339.8)|   (306.9)|   (339.3)|   (427.1)|
| (−) Unearned rebates                         |     (5.2)|     (4.6)|     (4.0)|     (3.3)|     (3.0)|
| **= Invested capital (ex-leases)**           | **1,217.7** | **1,379.4** | **1,482.3** | **1,604.7** | **2,902.5** |
| Memo: right-of-use assets (excluded)         |    568.4 |    654.3 |    668.1 |    689.2 |    951.1 |
| Memo: IC excluding goodwill & intangibles    |    283.0 |    402.6 |    501.5 |    545.9 |    644.9 |

Every row above is a balance-sheet caption reproduced verbatim; nothing is derived or estimated. The same figure can be reached top-down from reported total assets, which is how I check that nothing has been silently dropped:

| (US$ millions)                               | Dec-2022 | Dec-2023 | Dec-2024 | Dec-2025 | Jun-2026 |
|----------------------------------------------|----------|----------|----------|----------|----------|
| Total assets (reported)                      |  2,102.8 |  2,382.4 |  2,464.2 |  3,860.0 |  4,298.1 |
| (−) Cash above operating requirement         |      0.0 |      0.0 |      0.0 | (1,203.6)|      0.0 |
| (−) Right of use assets                      |   (568.4)|   (654.3)|   (668.1)|   (689.2)|   (951.1)|
| (−) Deferred income tax asset                |     (3.8)|     (4.3)|     (2.8)|    (12.6)|    (10.1)|
| (−) Derivative financial instruments         |      0.0 |      0.0 |      0.0 |     (7.2)|     (4.3)|
| = Operating assets included                  |  1,530.6 |  1,723.8 |  1,793.2 |  1,947.3 |  3,332.7 |
| (−) Accounts payable and accrued liabilities |   (307.7)|   (339.8)|   (306.9)|   (339.3)|   (427.1)|
| (−) Unearned rebates                         |     (5.2)|     (4.6)|     (4.0)|     (3.3)|     (3.0)|
| **= Invested capital (ex-leases)**           | **1,217.7** | **1,379.4** | **1,482.3** | **1,604.7** | **2,902.5** |

The two builds agree to nil at every date (`owners_earnings_roic.py`, section 11).

**Balance-sheet items deliberately left out, and why:**

- **Right-of-use assets** — paired with charging full cash rent in Owners' Earnings. Including both would double-count the leased shops.
- **Cash above the operating requirement** — $1,203.6M at Dec-2025 (IPO and senior-note proceeds warehoused for the Joe Hudson's closing, FY2025 AFS Note 6). Non-operating.
- **Deferred income tax assets and liabilities** — accounting basis differences, not capital deployed by management.
- **Derivative financial instruments** — cross-currency swaps hedging the senior notes; a financing item.
- **All interest-bearing liabilities** — long-term debt, senior unsecured notes and lease liabilities. ROIC is a return on *capital deployed*, measured before how it was funded; these belong in the enterprise-value bridge (§7), not here.
- **Dividends payable** — a distribution already declared, not operating capital.

Two notes on construction:

- **Cash.** Boyd's cash balance was $15.1M (Dec-22), $22.5M (Dec-23), $20.0M (Dec-24) and $23.0M (Jun-26). The $1,228.6M at Dec-31-2025 was IPO and senior-note proceeds warehoused for the Joe Hudson's closing on Jan-9-2026 (FY2025 AFS Note 6), so it is plainly non-operating. I cap operating cash at $25M. Assumption, but the historical balances support it and the choice moves ROIC by under 0.1pp.
- **Unearned rebates.** These are presented in the **non-current** liabilities block of the balance sheet, below the current-liabilities subtotal, so they are shown on their own row rather than inside working capital. I still net them out of invested capital: FY2025 AFS Note 18 describes prepaid rebates received from a trading partner amortized over 12 years as a reduction of cost of sales — supplier-funded, non-interest-bearing operating capital. Worth $3.0–5.2M, ~0.2% of invested capital.
- **Negative working capital.** Boyd runs structurally negative operating working capital excluding cash (−$69.5M at Dec-25, −$103.2M at Jun-26). Customers are insurers who pay reliably, and parts suppliers fund the float. This is a genuine, durable feature of the model and it reduces invested capital.
- Intangibles are carried at **net** book value. Using gross cost (FY2025 AFS Note 11: $580.2M gross vs. $356.3M net) would lower FY2025 ROIC by roughly 0.6pp. This is arguably more consistent with excluding amortization from OE; I use net because it ties directly to the balance sheet, and flag the bias.

---

## 5. ROIC

| (US$ millions)                                | FY2023  | FY2024  | FY2025  | TTM Jun-2026 |
|-----------------------------------------------|---------|---------|---------|--------------|
| Owners' Earnings                              |   132.4 |    91.8 |   108.9 |   145.9      |
| Average invested capital (ex-leases)          | 1,298.5 | 1,430.8 | 1,543.5 | 2,253.6      |
| **ROIC**                                      |**10.2%**| **6.4%**| **7.1%**| **6.5%**     |
| Average IC ex-goodwill & intangibles          |   342.8 |   452.1 |   523.7 |   595.4      |
| **ROIC on tangible operating capital**        |**38.6%**|**20.3%**|**20.8%**|**24.5%**     |
| *Alt. treatment: OE with leases capitalized*  |   148.2 |   111.0 |   133.5 |   174.8      |
| *Alt.: average IC including ROU assets*       | 1,909.9 | 2,092.1 | 2,222.2 | 3,073.8      |
| *Alt.: ROIC with leases capitalized*          |    7.8% |    5.3% |    6.0% |    5.7%      |

### How average invested capital is derived

**Convention.** Simple two-point average of the opening and closing balance sheet for each period, i.e. average IC = (opening + closing) / 2. Boyd publishes a balance sheet only at Dec-31 (annual) and Jun-30 (interim), so a two-point average is the finest granularity the filings support — a monthly- or quarterly-weighted average is not computable from these sources. The per-date balances are the "Invested capital" rows of the §4 table.

| Period       | Opening   | Closing   | Average   | Formula                    |
|--------------|-----------|-----------|-----------|----------------------------|
| FY2023       |   1,217.7 |   1,379.4 |   1,298.5 | (Dec-2022 + Dec-2023) / 2  |
| FY2024       |   1,379.4 |   1,482.3 |   1,430.8 | (Dec-2023 + Dec-2024) / 2  |
| FY2025       |   1,482.3 |   1,604.7 |   1,543.5 | (Dec-2024 + Dec-2025) / 2  |
| TTM Jun-2026 |   1,604.7 |   2,902.5 |   2,253.6 | (Dec-2025 + Jun-2026) / 2  |

**The ex-goodwill/intangibles base** is the same invested capital at each date less the two acquisition accounts, taken straight off the balance sheet:

| Date     | IC ex-leases | (−) Goodwill | (−) Intangibles | = Tangible IC |
|----------|--------------|--------------|-----------------|---------------|
| Dec-2022 |      1,217.7 |       (601.7)|          (332.9)|         283.0 |
| Dec-2023 |      1,379.4 |       (634.0)|          (342.8)|         402.6 |
| Dec-2024 |      1,482.3 |       (643.9)|          (336.9)|         501.5 |
| Dec-2025 |      1,604.7 |       (702.5)|          (356.3)|         545.9 |
| Jun-2026 |      2,902.5 |     (1,227.8)|        (1,029.8)|         644.9 |

Averaging those the same way gives $342.8M (FY2023), $452.1M (FY2024), $523.7M (FY2025) and $595.4M (TTM). The leases-capitalized base adds right-of-use assets at each date and averages identically, giving $1,909.9M / $2,092.1M / $2,222.2M / $3,073.8M. All three derivations are printed by `owners_earnings_roic.py` (section 10).

**One caveat on the TTM average.** The two-point average assigns ~50% weight to the post-Joe Hudson's balance sheet. That happens to be roughly the right weighting — Joe Hudson's closed 9 January 2026 (FY2025 AFS Note 32), so its capital was deployed for about 5.7 of the 12 TTM months, and TTM Owners' Earnings likewise contains about that much of its earnings. The averaging convention is therefore not the source of the TTM distortion; the unrealized synergies discussed below are.

**Reading these three numbers.**

- **ROIC on tangible operating capital (20–25%)** is the underlying unit economics: what a Boyd collision shop earns on the working capital and equipment actually required to run it. It is high, and it is the number that governs how attractive *incremental* organic growth (start-ups) is. The FY2023 figure of 38.6% is flattered by a small denominator and by an unusually strong revenue year.
- **ROIC on total invested capital (6.4–7.1% recently)** is the honest measure of management's capital allocation record, because it charges the ~$2.3bn of goodwill and acquired intangibles Boyd has paid to assemble the network. Boyd does not disclose a corporate hurdle rate. The only WACC-like figure in the filings is an *impairment-test input*: FY2025 AFS Note 12 lists "a terminal growth rate of 3% and a weighted average cost of capital of 7% to 9%" among the assumptions in the fair-value-less-costs-to-sell model for the US and Canadian CGUs. That is a narrower-purpose number than a capital-allocation hurdle rate, and impairment discount rates can be set conservatively low. Note the direction of that bias: if true WACC is higher than 7–9%, the shortfall is *wider*, not narrower. Total-capital ROIC of 6.4–7.1% sits below the bottom of even the disclosed range, and a more typical mid-cap-acquirer WACC of 9–11% would put the gap at 2–4pp. I have not substituted a WACC estimate of my own, having no sourced basis for one. **That is the central tension in this business: excellent operating economics, mediocre returns on the price paid to acquire them.**
- The **leases-capitalized alternative** (5.3–7.8%) confirms the direction. Whichever lease convention you use, total ROIC sits in the mid-to-high single digits and tangible ROIC is ~20%+. The conclusion is robust to the methodology choice, which is the point of running both.

**The TTM ROIC of 6.5% understates the post-Joe Hudson's business and should not be annualized.** Invested capital at Jun-30-2026 includes the full $1,321.4M paid for Joe Hudson's (Q2FY26 AFS Note 4), while TTM Owners' Earnings includes under six months of its contribution and only partial synergies. Management reports $35M of Project 360 + Joe Hudson's synergies realized in H1-2026, with $30M more expected in 2026 and $35M between 2027 and 2029 (Q2FY26 MD&A). Roughly $65M of annualized pre-tax synergy is still to come, which on unchanged capital is worth about 2.1pp of ROIC (=$65M × 0.735 ÷ $2,253.6M — inference, my arithmetic, assuming synergies drop straight to OE). That would put pro-forma ROIC at ~8.6%.

**On cyclicality.** FY2023 was not a normal year. FY2023 Adjusted EBITDA of $368.2M on $2,946.0M of sales came during the post-COVID claims-cost inflation surge; FY2024 same-store sales then fell and FY2025 same-store sales were −0.2% (FY2025 MD&A, Same-store sales) as repairable claims volumes declined. Management estimates repairable claims volume down 0–2% in H1-2026 and notes "the average total cost of repair remained below historical levels" (Q2FY26 MD&A). So FY2023 is a cyclical high and FY2024 a cyclical low for this metric. **I would centre normalized ROIC on total capital at 7–8%, not on either endpoint.**

---

## 6. Sensitivity — the maintenance-capex assumption

| Maintenance capex, % of sales | FY2023 OE (ROIC) | FY2024 OE (ROIC) | FY2025 OE (ROIC) | TTM OE (ROIC) |
|-------------------------------|------------------|------------------|------------------|---------------|
| 1.4%                          |   138.9 (10.7%)  |    98.5 (6.9%)   |   115.9 (7.5%)   |  153.8 (6.8%) |
| **1.7% (base)**               | **132.4 (10.2%)**| **91.8 (6.4%)**  | **108.9 (7.1%)** |**145.9 (6.5%)**|
| 2.0%                          |   125.9 ( 9.7%)  |    85.0 (5.9%)   |   102.0 (6.6%)   |  138.0 (6.1%) |
| 2.5%                          |   115.1 ( 8.9%)  |    73.7 (5.2%)   |    90.5 (5.9%)   |  124.8 (5.5%) |

A 0.3pp change in the maintenance-capex assumption moves Owners' Earnings by ~$7M (6–7%) and ROIC by ~0.4pp. Even at a punitive 2.5% of sales, tangible ROIC stays at 16.3% (FY2024) / 17.3% (FY2025) / 21.0% (TTM) and total ROIC near 6%. The qualitative conclusion does not turn on this assumption.

---

## 7. Non-operating items excluded from Owners' Earnings

Carry these into the enterprise-value bridge later (all at Jun-30-2026, from the Q2FY26 balance sheet):

| Item                                                   | US$ millions |
|--------------------------------------------------------|--------------|
| Cash                                                   |        +23.0 |
| Long-term debt (current $7.2M + non-current $411.6M)   |       −418.8 |
| Senior unsecured notes                                 |       −557.2 |
| Derivative financial instruments, net ($4.3M − $3.0M)  |         +1.3 |
| Net deferred income tax liability ($104.3M − $10.1M)   |        −94.3 |
| Dividends payable                                      |        −3.1  |
| **Net non-operating position**                         |   **−1,049.1** |
| *Lease liabilities ($159.6M + $891.3M) — MEMO ONLY*    | *(−1,050.9)* |

**Do not deduct the lease liabilities as debt.** Rent is charged in full inside Owners' Earnings, so the obligation is already capitalized in the earnings stream. Deducting both would double-count roughly $1.05bn.

Other excluded non-operating flows: interest expense on debt and senior notes (below the Adjusted EBITDA line by construction) and interest income, including the $5.6M "interest received on proceeds of senior unsecured notes and equity offering" in FY2025 (FY2025 AFS cash flows). Boyd's $8.4M investment supporting the glass business (FY2025 AFS Note 13) is left inside "other long-term assets" as immaterial rather than carved out.

---

## 8. Confidence

**Confident:**

- Owners' Earnings is far below Adjusted EBITDA — roughly 29% of it. Cash rent alone absorbs 43% of FY2025 Adjusted EBITDA. This is arithmetic off reported cash flow lines, and the two independent builds agree to 0.5%.
- Tangible operating capital earns ~20%+. The underlying shop economics are genuinely good.
- ROIC on total capital deployed is in the mid-to-high single digits and has been below 8% since FY2024 on any lease convention. Boyd's own impairment model uses a 7–9% WACC, so the business has been earning around or below its cost of capital on acquired capital.
- Working capital is structurally negative and the excess-cash and debt positions at Jun-30-2026 are directly readable off the balance sheet.

**Genuinely uncertain:**

- **Maintenance capex.** The 1.7% guidance is management's, and it excludes network technology upgrades ($10.7M spent in 2025, guided to only $2–4M in 2026 — FY2025 MD&A). A network of ~1,300 shops with $87.9M of annual PP&E depreciation may need more than $53M/yr once the store base matures. Sensitivity in §6; this is the biggest swing factor.
- **Normalized earnings power post-Joe Hudson's.** TTM OE of $145.9M reflects a half-integrated business. Management targets a 14% Adjusted EBITDA margin (Q2FY26 MD&A) vs. 12.8% TTM, with ~$65M of annualized synergy still to land. Whether the 14% target is achieved is the main determinant of forward OE, and I have no independent basis to verify it.
- **Where in the cycle we are.** Repairable claims volumes have been down two-plus years and average repair cost is "below historical levels" (Q2FY26 MD&A). If that normalizes, same-store sales and margin both improve; if the decline is structural (safer vehicles, higher insurance deductibles pushing claims out of the system), FY2024–25 is the new baseline, not a trough.
- **The $5M normalized acquisition cost** is a judgment with no direct source. Worth ±$4M of OE against the base case — but note from §3 that the *gross* normalization is $25.5M in FY2025 and $43.0M in TTM, so a reader who treats all deal costs as recurring gets a materially lower OE.
- **Confidence calibration.** The §3 reconciliation foots to zero, which validates the arithmetic, not the judgment calls. Read the individual normalization lines there to see what each one is worth before relying on the $108.9M.

**Deliberately not quantified:** start-up locations drag on current earnings — 27 opened in 2025, with new locations running a 36.1% operating-expense ratio vs. 34.4% company-wide, and pre-opening costs incurred before any revenue (FY2025 MD&A). A rough read on the disclosed excess opex is only ~$2–3M, but pre-opening losses on not-yet-open sites are not disclosed. Owners' Earnings as computed is therefore modestly understated relative to a true steady-state, no-growth business. I have not adjusted for it because the disclosure does not support a defensible number.
