# NamSys Inc. (TSXV: CTZ) — Five-Year Owners' Earnings Forecast, FY2026E–FY2030E

*Prepared September 16, 2026. All figures in Canadian dollars unless stated. Fiscal year ends October 31. Every number in this document is an output of `work_products/forecast_earnings_calcs.py`; run it with `uv run python work_products/forecast_earnings_calcs.py`. Each input in that script carries a source tag in a comment. This document is stock-price-blind: no quote, market capitalisation or price-derived multiple is used anywhere.*

Source tags used throughout:

| Tag     | Source                                                     |
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
| `CM`    | `work_products/causal_model.md`                            |

---

## 1. Headline

| Owners' Earnings (CAD)        | FY2025A   | FY2026E   | FY2027E   | FY2028E   | FY2029E   | FY2030E   | 5-yr CAGR | Cumulative FY26–30 |
|-------------------------------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|--------------------|
| **Base**                      | 2,250,271 | 2,375,755 | 2,413,913 | 2,548,061 | 2,716,487 | 2,859,320 | **+4.9%** | **12,913,536**     |
| Bull                          | 2,250,271 | 2,497,370 | 2,875,019 | 3,456,739 | 4,050,655 | 4,649,840 | +15.6%    | 17,529,623         |
| Bear (no cost response)       | 2,250,271 | 2,186,559 | 1,910,394 | 1,467,614 | 1,469,920 | 1,505,664 | −7.7%     | 8,540,150          |
| Bear (management right-sizes) | 2,250,271 | 2,186,559 | 2,104,052 | 1,804,902 | 2,033,866 | 2,094,988 | −1.4%     | 10,224,367         |

The FY2025 actual is from `OE` §2.1. Underlying revenue and margin:

| Base case               | FY2025A   | FY2026E   | FY2027E   | FY2028E    | FY2029E    | FY2030E    |
|-------------------------|-----------|-----------|-----------|------------|------------|------------|
| Revenue                 | 7,891,605 | 8,655,668 | 9,411,573 | 10,116,115 | 10,797,518 | 11,462,356 |
| Revenue growth          | +15.4%    | +9.7%     | +8.7%     | +7.5%      | +6.7%      | +6.2%      |
| Operating income        | 3,146,476 | 3,278,669 | 3,330,585 | 3,513,099  | 3,742,250  | 3,936,580  |
| Operating margin        | 39.9%     | 37.9%     | 35.4%     | 34.7%      | 34.7%      | 34.3%      |
| Owners' earnings        | 2,250,271 | 2,375,755 | 2,413,913 | 2,548,061  | 2,716,487  | 2,859,320  |
| Owners' earnings margin | 28.5%     | 27.4%     | 25.6%     | 25.2%      | 25.2%      | 24.9%      |
| Average headcount       | 17        | 19.8      | 22.5      | 24.0       | 25.0       | 26.0       |

**The one-sentence version.** Revenue keeps compounding at a mid-to-high single-digit rate driven by cross-sell and endpoint expansion inside a small, near-zero-churn account base, but owners' earnings grow far more slowly than they did in FY2022–FY2025 for two specific reasons that have nothing to do with demand deteriorating: roughly 9 points of the 24.7%/yr historical owners'-earnings growth (`OE` §5) was a weakening Canadian dollar, which I set to zero by holding USD/CAD flat; and the 17→21 headcount step already taken in FY2026 (`AM26`) resets the cost base upward before the revenue it was hired to generate arrives.

**Three things this analysis changes versus the existing work products.** All three are documented below and all three are consequences of adding two data sources that `CM` explicitly said it lacked — a Bank of Canada USD/CAD series, and a numerical test linking the geographic note to the customer-concentration note:

1. There has been **almost no constant-currency deceleration at the aggregate level**. `CM` §3.4 called the 16.3% → 6.1% recurring-revenue deceleration "the most important single number in the model." Roughly 3 points of the reported slowdown on each side of the comparison is currency. On a constant-currency basis, total revenue growth went from +12.0% (FY2025) to +11.4% (H1 FY2026), and recurring-only from ~13.0% to ~9.3%. Real, but far less dramatic (§3).
2. The US is **not** growing at 3.5%. It grew **+6.6% constant currency**, and +14.1% excluding one shrinking legacy account (§4).
3. `CM` §3.5/§3.7 assumed the "rank-#1 customer" was a single continuing account that fell 19.2%. It almost certainly is not: **the Mexico country total matches a disclosed top-3 customer share to within 0.06 percentage points in four consecutive periods**, so slot #1 in H1 FY2026 is a Mexican account that *grew 46%*, while the shrinking legacy account has slipped to slot #2 or lower (§4.1).

---

## 2. Method, and why it is built this way

### 2.1 The forecast object

Owners' earnings, per the definition in use and as built in `OE` §2: reported operating income, normalised for bad debt and share-based compensation, plus depreciation less maintenance capex, taxed at the statutory rate with share-based compensation treated as non-deductible. Interest income on the GIC portfolio is deliberately excluded (it is a return on a financial asset, not on the operating business — `OE` §4). Per-share figures are not forecast.

**The forward engine is the identical arithmetic, driven forward — not a new method.** The script back-tests it on FY2025 (§4b of the script):

| Check                                      | Rebuilt   | Reported / `OE`    | Difference   |
|--------------------------------------------|-----------|--------------------|--------------|
| FY2025 operating income                    | 3,146,476 | 3,146,476 (`FS25`) | 0            |
| FY2025 normalised pre-tax owners' earnings | 3,105,863 | 3,105,863 (`OE`)   | 0            |
| FY2025 owners' earnings                    | 2,250,272 | 2,250,271 (`OE`)   | 1 (rounding) |

### 2.2 Forecast in USD, not CAD

~96% of revenue is invoiced in US dollars (`FSQ2` Note 11; `MDQ2`: "U.S. dollar sales represent 95% or more of total sales"), against a cost base that is a "majority" Canadian (`MDA25` Risk Factors). Reported CAD revenue is therefore the product of two independent things: commercial volume, denominated in USD, and an exogenous exchange rate. Forecasting the CAD line directly conflates them.

`CM` §3.6 declined to size the currency term because "No FX rate series exists in `primary_sources`, `work_products`, `fetched_docs`, or the Knowledge Store." That gap is now closed with the Bank of Canada's published monthly average USD/CAD (series `FXMUSDCAD`), aggregated to NamSys fiscal years (Knowledge Store ID 11):

| Period                           | Average USD/CAD | Change vs prior |
|----------------------------------|-----------------|-----------------|
| FY2022 (Nov 21 – Oct 22)         | 1.2878          | —               |
| FY2023 (Nov 22 – Oct 23)         | 1.3487          | +4.7%           |
| FY2024 (Nov 23 – Oct 24)         | 1.3610          | +0.9%           |
| FY2025 (Nov 24 – Oct 25)         | 1.4009          | **+2.9%**       |
| H1 FY2025 (Nov 24 – Apr 25)      | 1.4209          | —               |
| H1 FY2026 (Nov 25 – Apr 26)      | 1.3792          | **−2.9%**       |
| Q3 FY2026 (May – Jul 26)         | 1.3957          | +1.2% vs H1FY26 |
| FY2026 to date (Nov 25 – Aug 26) | 1.3852          | −1.1% vs FY2025 |

*Caveat: the monthly average is an approximation of the actual translation rate. Revenue is recognised monthly and translated at transaction-date rates, so the fiscal-year average of monthly averages is close but not exact. The errors are well under a percentage point and do not carry any of the conclusions.*

**FX assumption.** USD/CAD is held **flat** at 1.3860 in FY2026 (the ten realised months averaged 1.3852; September and October are assumed at the August level of 1.3898) and 1.39 thereafter, which is the latest observable monthly average. This is an explicit no-view assumption, not a forecast. Because currency is exogenous and uncorrelated with operating execution, it is held flat in **all three** operating scenarios and varied only in the sensitivity table (§7). Mixing a currency view into a bull/bear case would double-count risk and make the scenarios uninterpretable.

### 2.3 Root-cause drivers, not downstream effects

The chain is: **endpoints × rate per endpoint → USD revenue → CAD revenue; headcount × compensation per head → cost; the difference → operating income → owners' earnings.** Revenue is not forecast as a growth rate off a headline number.

Two structural facts license this framing. First, "it doesn't matter if you are handling \$500 or \$5,000, the cost to move and count those notes is the same" (`AM26`), so demand is created by the count of cash-handling endpoints, not the dollar value of cash. Second, management measures its own opportunity in units of physical infrastructure — "on a truck basis, we know that our software runs on approximately 8% of all the... cash and transit vehicles in the US," and the worldwide market is "at least 10 times" the US, which is "just trucks, which is a rough correlation towards... what we'd be able to deliver in terms of revenue" (`AM26`). Management's use of vehicle count as a revenue proxy is direct support for endpoint-based pricing; the filings never disclose the pricing unit, so this remains an **inference** (also `CM` §2).

Endpoints are not separately disclosed, so the observable proxy is **revenue per geographic bucket in constant currency**, decomposed so that each bucket has a single dominant causal driver. That decomposition is §4. Cost is forecast from headcount and compensation per head because "Total employee compensation expense" is disclosed quarterly (Note 14) and is 58.6% of total operating cost (`CM` §4.1) — i.e. the cost line genuinely *is* people.

### 2.4 Segments

NamSys reports one segment. Two cuts are available: by product (Cirreon Retail ~40%, Currency Controller ~40%, Cirreon CIT ~23%; `AM26`) and by geography (`FS25`/`FSQ2` Note 7). **I use geography.** Reasons: the geographic note gives an audited dollar series back to FY2022, whereas the product split is given only as approximate percentages in transcripts; and management states the products are "all growing at approximately the same rate right now" so "their overall proportions will not change over the next 12 months" (`AM26`), which means the product cut carries almost no forecasting information. The geographic cut, by contrast, contains the entire story — see §4.

### 2.5 The current partial year

FY2026 ends October 31, 2026 and Q3 has not yet been filed (NamSys released Q3 results on September 25, 2024 and September 26, 2023, so the Q3 FY2026 release is due after this document's date; `fetched_docs/namsys_newswire_list_sep2026.md`). Per the brief, **FY2026 is forecast as a whole year using the same driver methodology as every other year** — i.e. a full-year growth rate applied to the FY2025 base for each bucket, not reported-half actuals plus an assumed H2 stub.

**Be clear about what that does and does not buy, though.** The FY2026 growth-rate assumptions for the three largest buckets are explicitly *calibrated to* the H1 FY2026 constant-currency readings (§4.2, §4.3, §4.4 each say so). The most recent observation is the best available signal for the current year, so this is the right way to set them — but it means §6's revenue reconciliation is a **consistency check on that calibration, not an out-of-sample test of it**. It confirms the FY2026 growth rates are internally coherent with the H1 dollars and the FX path; it does not independently corroborate them. The one genuinely independent part of §6 is the compensation check: average headcount of 19.8 comes from the disclosed 17→21 trajectory (`AM26`), not from H1 dollars, and it lands within 1.3% of H1 actual compensation. That check is informative; the revenue one is weaker, and the "FY2026E is conservative" claim in §6 rests on the *sequential* arithmetic (the implied H2 asks for less sequential growth than either realised quarter delivered), which is the part that does not depend on the calibration.

---

## 3. What actually happened: constant-currency decomposition

Converting each geographic line at that period's average rate (Canada left in CAD):

| Period    | US (USD)  | Mexico (USD) | Other intl (USD) | USD total | Canada (CAD) |
|-----------|-----------|--------------|------------------|-----------|--------------|
| FY2023    | 3,570,472 | 357,184      | 430,151          | 4,357,807 | 215,646      |
| FY2024    | 3,880,935 | 447,688      | 518,500          | 4,847,123 | 243,212      |
| FY2025    | 4,268,205 | 604,008      | 556,385          | 5,428,598 | 286,682      |
| H1 FY2025 | 2,133,083 | 268,574      | 273,033          | 2,674,691 | 151,395      |
| H1 FY2026 | 2,274,695 | 404,881      | 299,449          | 2,979,026 | 158,734      |

Source: `FS23`/`FS24`/`FS25`/`FSQ2` Note 7 geographic tables, divided by Knowledge Store ID 11 rates. "Other intl" = Dominican Republic + Puerto Rico + Other.

| Bucket                | FY24→FY25 reported CAD | FY24→FY25 constant USD | H1 y/y reported CAD | H1 y/y constant USD |
|-----------------------|------------------------|------------------------|---------------------|---------------------|
| US                    | +13.2%                 | **+10.0%**             | +3.5%               | **+6.6%**           |
| Mexico                | +38.9%                 | +34.9%                 | +46.3%              | **+50.8%**          |
| Other international   | +10.5%                 | +7.3%                  | +6.5%               | +9.7%               |
| **Total (ex-Canada)** | **+15.4%**             | **+12.0%**             | **+8.0%**           | **+11.4%**          |

**This is the single most important correction in this document.** `CM` §3.5 built its central finding on "US +3.5% versus international ex-Canada +26.2%," describing a US installed base that had stopped growing, and `CM` §10 listed "how much of the H1 FY2026 slowdown is FX versus volume" as "the largest single gap in the model." The answer is: most of it. FY2025 enjoyed a +2.9% translation tailwind and H1 FY2026 suffered a −2.9% headwind — a round trip of roughly 5.8 points in the *reported* growth rate between the two comparison periods, which is most of the 7.4-point reported deceleration (15.4% → 8.0%). Constant currency, the total deceleration is 12.0% → 11.4%, i.e. within noise.

Recurring revenue tells a softer but still real story. Recurring revenue grew +16.3% in FY2025 and +6.1% in H1 FY2026 as reported (`MDA25`, `MDQ2`). Applying the same translation adjustment gives approximately **+13.0% → +9.3% constant currency** — a genuine ~4-point deceleration in the durable line, driven by professional services making up the difference in H1 FY2026 (`MDQ2`: professional services $21,936 → $96,457, which is 23.6% of the entire dollar increase in revenue). So `CM` §3.4 was directionally right that the headline flattered the durable line; it was wrong about the magnitude of the total-revenue deceleration.

The sequential "two flat quarters" observation in `CM` §3.2 is also substantially an FX artefact. Q1 FY2026 (Nov–Jan) averaged 1.3878 and Q2 FY2026 (Feb–Apr) averaged 1.3706, a −1.24% move; revenue was flat to the dollar at \$2,134k in CAD (`MDQ2`), which means it grew **+1.25% sequentially in USD**. Still slow, but not a stall.

---

## 4. The revenue drivers

### 4.1 First: the Mexico country total is almost certainly one customer

The filings disclose the top-3 customer shares each period but never identify them (`FS24`/`FS25`/`FSQ2` Note 7). They separately disclose revenue by country. Testing whether any country total *equals* a disclosed customer share:

| Period    | Mexico as % of revenue | Disclosed top-3 shares | Closest | Gap (pp)  |
|-----------|------------------------|------------------------|---------|-----------|
| FY2023    | 7.91%                  | 24.9%                  | 24.9%   | −16.99    |
| FY2024    | 8.91%                  | 20.0%, 8.9%, 8.9%      | 8.9%    | **+0.01** |
| FY2025    | 10.72%                 | 15.9%, 12.3%, 10.7%    | 10.7%   | **+0.02** |
| H1 FY2025 | 9.66%                  | 17.5%, 12.5%, 9.7%     | 9.7%    | **−0.04** |
| H1 FY2026 | 13.09%                 | 13.1%, 12.8%, 11.4%    | 13.1%   | **−0.01** |

Four consecutive matches to within 0.06 percentage points. FY2023 is the only miss, and in that year only one customer share was disclosed (24.9%), so Mexico at 7.9% could not have appeared in the list regardless.

**This is an inference, not a disclosure.** The filings never state that Mexico is one customer, and it is possible — though in my judgement unlikely, given four independent near-exact matches — that Mexico is several customers whose total coincidentally tracks a top-3 share. I flag it as inference and carry the consequence explicitly rather than burying it.

The consequence matters a great deal. `CM` §3.5 and §3.7 read the top-3 disclosure as slot-stable and concluded that "the largest account shrank in absolute dollars... −19.2% H1FY25→H1FY26," making that decline the leading explanation for the US slowdown. Under the Mexico reading, **slot #1 in H1 FY2026 is the Mexican account, which grew 46%**. The historically largest account — 24.9% (FY2023), 20.0% (FY2024), 15.9% (FY2025), 17.5% (H1 FY2025) — has been pushed down to slot #2 or lower.

### 4.2 Driver bucket 1 — the shrinking legacy US account

**First, that it is a US account is demonstrable, not assumed.** `CM` §3.5 called it only "a priori likely" that this account sits in the US bucket "since the US is 73.5% of revenue." That is a probabilistic claim, and the "US ex-legacy" framework in §4.3 — and the corrected +6.6% US figure in §3 — depend on it, so it deserves the same standard as the Mexico test in §4.1. The Note 7 geographic table is by country, so a single customer's revenue cannot exceed its own country bucket. Eliminating on that basis (script §1b):

| Period    | Legacy account (CAD) | Country buckets large enough to contain it                            |
|-----------|----------------------|-----------------------------------------------------------------------|
| FY2023    | 1,517,162            | US only                                                               |
| FY2024    | 1,368,029            | US only                                                               |
| FY2025    | 1,254,765            | US only                                                               |
| H1 FY2025 | 691,576              | US only                                                               |
| H1 FY2026 | 546,228              | US; Mexico (excluded — Mexico is already its own separate top-3 slot) |

Mexico is excluded in the last row because Mexico's \$558,412 already matches slot #1 at 13.1% (§4.1); hosting a second top-3 account at 12.8% would require Mexico to be ≥25.9% of revenue, or \$1,105,258, which it is not. So in every period the US is the only possible home. *Caveat: this establishes the account is predominantly US-domiciled, not that literally 100% of its revenue is booked to the US line.*

| Period    | Share           | CAD       | USD       | y/y USD    |
|-----------|-----------------|-----------|-----------|------------|
| FY2023    | 24.9%           | 1,517,162 | 1,124,907 | —          |
| FY2024    | 20.0%           | 1,368,029 | 1,005,165 | −10.6%     |
| FY2025    | 15.9%           | 1,254,765 | 895,685   | −10.9%     |
| H1 FY2025 | 17.5%           | 691,576   | 486,717   | —          |
| H1 FY2026 | 12.8% (slot #2) | 546,228   | 396,047   | **−18.6%** |
| H1 FY2026 | 11.4% (slot #3) | 486,484   | 352,729   | −27.5%     |

Constant-currency declines in each of FY2024, FY2025 and H1 FY2026, the last at an accelerated rate, and beginning well before the current slowdown. Which H1 FY2026 slot this account occupies is not determinable; the base case uses the less-bad of the two.

**Root cause (partly inference).** The filings do not say. Two sourced mechanisms fit. The first is competitive displacement in the retail product: "we are seeing more competition from the hardware manufacturers themselves, so the people that make these SmartSafe and Recycler devices. They essentially learn that there's a benefit of recurring revenue, and many are developing their own proprietary software" (`AM25`) — and Cirreon Retail is the product management repackaged specifically "to try to reinvigorate growth for future years" (`AM25`), i.e. the one product it concedes is not growing. The second is the customer losing its own volume. What the record rules *out* is churn: management states "we experienced no customer churn" (`AM25`), so this is contraction inside a retained account — which is itself a gap in the zero-churn narrative that `CM` §3.7 correctly identified.

**Forecast: −20%/yr in constant currency.** That is between the FY2024/FY2025 rate (−11%) and the H1 FY2026 rate (−18.6% to −27.5%), and continues an established three-year trend rather than assuming a turn. The account shrinks from 15.9% of FY2025 revenue to 3.6% by FY2030E, so **the drag mechanically fades**: it costs the US bucket ~4 points of growth in FY2026 and under 1 point by FY2030. The sensitivity of losing it outright in FY2027 is small in the terminal year (−9% on FY2030E owners' earnings) and moderate cumulatively (−12%), precisely because the base case has already written most of it off.

### 4.3 Driver bucket 2 — the rest of the US

| Period                                    | US ex-legacy (USD) | Growth |
|-------------------------------------------|--------------------|--------|
| FY2024                                    | 2,875,770          | —      |
| FY2025                                    | 3,372,520          | +17.3% |
| H1 FY2025                                 | 1,646,366          | —      |
| H1 FY2026                                 | 1,878,649          | +14.1% |
| H1 FY2026, ex professional-services spike | —                  | +10.8% |

The last row strips the entire H1 FY2026 professional-services increase (USD 54,499) out of this bucket — a deliberately punitive treatment, since some of that implementation work plausibly belongs to the Mexican rollout instead.

**Root causes, in the order they matter:**

- **Expansion inside existing accounts.** "Approximately 75% of it came from purely organic growth amongst our customers" over five years, and net revenue retention was 112% in FY2024 (`AM26`, `AM25`). The mechanism is more endpoints per account plus attach of the other two products ("Currency Controller... is often deployed in combination with the CIT application"; `AM25`) plus "optional modules and extensions that we sell to customers to further enhance their productivity" (`AM26`).
- **A hard ceiling on new US logos.** "Approximately 75% of that market on the CIT side is controlled by Brinks and Loomis and Garda, of the remaining 25%, we feel we've got a small majority of those clients" (`AM26`). NamSys runs on ~8% of all US CIT vehicles, i.e. roughly a third of the addressable non-big-three truck base while already holding a majority of the addressable *clients*. The easy logos are won; what remains is a smaller tail. This is the root cause of decay, and it is a statement about market structure, not about demand.
- **The endpoint universe itself is stable, not shrinking.** The Federal Reserve's 2026 Diary of Consumer Payment Choice (survey conducted October 2025) found cash used for about 1 in 7 US payments and that "U.S. consumer payment use remained largely consistent over the past three years" (Knowledge Store ID 12). Note this *corrects* management, which claimed "approximately one in five payments... not changed since 2020" (`AM25`) — the level is overstated, but the stability claim, which is the load-bearing one, is independently corroborated.
- **Price, small.** Renewal repricing "really started rolling out over the past two, maybe two and a half years" but "routinely increasing prices is not something that we're planning to do" (`AM26`), and management concedes "pricing power is something that has been impacted by AI" (`AM26`). I carry price inside the bucket rate rather than modelling it separately; it is worth perhaps 1–2 points and is not separable from volume in any disclosure.

**Forecast: 13% → 11% → 9.5% → 8% → 7%.** The starting point sits between the two observed H1 FY2026 readings (14.1% with the professional-services spike, 10.8% without). The decay is the market-structure ceiling asserting itself, and it is the same shape the data already shows (17.3% → 14.1%).

### 4.4 Driver bucket 3 — the Mexican account

FY2025 USD 604,008, growing +34.9% (FY2025) and +50.8% (H1 FY2026) in constant currency.

**Root cause: a single large customer mid-rollout.** This is the same pattern the record already documents once: "This was the result of one of our large customers rolling out our Cirreon CIT application during the calendar year, and that rollout is now complete and was very successful," with that product up 52% year-on-year in FY2024 (`AM25`). Rollouts ramp over roughly one to two years and then plateau at the new level. Management's framing of Mexico is consistent — the Sankey chart shows "the United States and Mexico constitute our top sources" (`AM26`).

**Forecast: +48%, +18%, +10%, +7%, +5%.** Ramp completes in FY2027, then the account behaves like a mature one. **This is the single largest risk in the forecast, and it runs in both directions.** By FY2030E Mexico is 15.8% of revenue in the base case versus 10.7% in FY2025 — i.e. the base case has customer concentration *increasing*, not decreasing, and the concentration simply migrating from the shrinking legacy account to this one. Losing it in FY2028 costs 41% of FY2030E owners' earnings and 26% of the five-year cumulative (§7). `MDA25` Risk Factors describe exactly the mechanism by which such an account disappears without NamSys doing anything wrong: "When two banks merge, the continuing entity usually selects one technology provider for a given function... the provider with the largest installed base in the combined entity will replace the provider with the smaller installed base."

### 4.5 Driver bucket 4 — the rest of international

FY2025 USD 556,385 (Dominican Republic, Puerto Rico, Other), growing +7.3% (FY2025) and +9.7% (H1 FY2026) constant currency.

**This corrects a second `CM` claim.** `CM` §3.5 and §7 treated "international ex-Canada growing 26.2%" as the evidence that a driver handover to international was "real and on track." It is not a broad international trend: strip Mexico out and the rest of the international base grows at high single digits. The international momentum is one Mexican account.

**Root causes of the forward rate.** The inputs to new international logos are (a) local presence, since the reseller model failed for structural reasons — "we've tried many times to work with resellers and integrators and had little to no success... the sales cycle for our applications can be quite long. Any sales agreement that we sign typically gathers dust for 12 to 24 months" (`AM25`); (b) time-zone and language coverage, which is why the FY2026 hires are "a support person in Australia" and "a salesperson in the UK," with "either software or support engineer in both of those regions in 2026" to follow (`AM26`); and (c) the ISO/IEC 27001:2022 certification obtained February 2026, framed as unlocking non-North-American customers (Knowledge Store ID 4). With 12–24 month sales cycles, the FY2024–FY2026 hires and the February 2026 certification should convert in FY2027–FY2029.

**Forecast: +9%, +13%, +15%, +15%, +14%.** Acceleration from the current high-single-digit rate as those inputs convert. Even so, this bucket only reaches USD 1.03M by FY2030E — **on a \$556k base, the international strategy cannot move the answer within five years unless it lands a second Mexico-sized account.** That is the honest arithmetic of a small base, and it is why the bull case is defined by exactly that event.

### 4.6 Canada

\$286,682 in FY2025, +4.8% in H1 FY2026. Forecast +5%/yr. Immaterial (2.5% of revenue) and left in CAD since it carries no translation exposure.

---

## 5. The cost drivers

### 5.1 Headcount is the forecast

FY2025 cost structure, from `FS25` Note 14 and the statements of operations:

| Component                                     | FY2025        | % of operating cost |
|-----------------------------------------------|---------------|---------------------|
| Cash compensation (Note 14 less reported SBC) | 2,734,476     | 57.6%               |
| Reported share-based compensation             | 47,030        | 1.0%                |
| Non-compensation cost of sales (hosting etc.) | 1,073,930     | 22.6%               |
| Non-compensation G&A                          | 610,223       | 12.9%               |
| Non-compensation selling                      | 228,140       | 4.8%                |
| Bad debt                                      | 51,330        | 1.1%                |
| **Total operating cost**                      | **4,745,129** | **100%**            |

**Headcount path: 19.8 average in FY2026, then 22.5, 24.0, 25.0, 26.0.** Sourced anchors: 17 through FY2024–FY2025 (`AM25` "stable at 17 employees"; `MDA25` attributes the FY2025 gross-margin gain to "the level of staffing resources remaining relatively flat year-over-year") and 21 as at April 23, 2026 (`AM26`). Forward additions are driven by the causal requirement, not by a revenue ratio: international expansion needs one to two heads per region for time-zone and language coverage, management has named UK and Australia engineers as the next hires (`AM26`), and development headcount should grow slowly because "without adding headcount in engineering, we're able to pursue product initiatives in parallel" (`AM26`). Net ~+1.2 heads/yr after the FY2027 step to 23.

A cross-check on the longer history: FY2022 compensation of \$2,075,797 (`FS23` Note 14; no share-based compensation in FY2022, so it is all cash) divided by the FY2023 per-head rate of \$130,897 implies **15.9 staff in FY2022**, or 16.3 if FY2022 wages were 3% lower. So headcount went ~16 → 21 over four years, i.e. **~+1.25/yr — exactly the rate the forecast assumes after FY2027**. The FY2023–FY2025 flat-at-17 stretch is the anomaly, not the norm, and it was followed immediately by four hires.

**Cash compensation per head: \$160,852 in FY2025 (FY2025 cash compensation ÷ 17), inflated 3.5%/yr.**

*I want to be explicit about a weakness here.* The implied per-head figure rises \$130,897 → \$140,747 → \$160,852 across FY2023–FY2025, i.e. +14.3% in FY2025 alone at nominally flat headcount. That cannot be pure wage inflation. The most likely explanation is average-versus-point-in-time headcount: 17 is what management said at an April meeting, and FY2025 carried the first full year of the international business-development hire added during FY2024 (`AM25`, `MDA25`: FY2025 selling expense rose 61.6% on "the addition of a new business development position covering the European market"). The forward 3.5% assumption is therefore **not** validated by the historical per-head series; it is validated by the forward reconciliation in §6, which predicts H2 FY2026 compensation within 1.3% of 21 staff at the run rate. A 5.0% wage assumption costs 10% of FY2030E owners' earnings (§7).

### 5.2 Non-compensation costs

- **Non-compensation cost of sales** (\$1,073,930 in FY2025): grown at **0.85 × revenue growth**. Root cause is cloud hosting and third-party software, which scale with endpoints served but at declining unit prices. The filings never disaggregate this line (Note 14 discloses only compensation), so the hosting attribution is an **inference** (also `CM` §4.4). It matters little: forcing the elasticity to 1.0 changes FY2030E owners' earnings by −2%.
- **Non-compensation G&A** (\$610,223): +3.5%/yr. Root cause is public-company and IT-security costs, which are essentially fixed. Corroboration: H1 FY2026 non-compensation G&A annualises to \$607,404, i.e. flat year-on-year (`MDQ2`: G&A "increase of \$8,154 or 1.4%"), and `MDQ2` cites "software, related support and IT security costs... higher by \$10,309" as the growth item.
- **Non-compensation selling** (\$228,140 in FY2025): \$150,000 in FY2026 compounding at **10%/yr in the base case, 5%/yr in the bear and 14%/yr in the bull**. H1 FY2026 was cut to \$65,396 — `MDQ2` attributes it to "lower travel and trade show attendance costs (\$26,751)" — but that is the input to the international strategy the forecast relies on, so it is modelled as re-expanding. `CM` §4.2 correctly flagged this as an internal tension in the current plan; the forecast resolves it by assuming management re-spends rather than by assuming the cut is free. **This is the only cost line whose growth rate differs by scenario, and deliberately so:** it is pure discretionary growth investment, and the revealed behaviour runs both ways — `MDA25` attributes FY2025's 61.6% selling-expense jump to "the addition of a new business development position covering the European market and expanded travel as well as trade show attendance costs (\$255,466)," while `MDQ2` shows the line being cut when growth slowed. A bull case that lands a second large international account on bear-case selling dollars would be internally inconsistent. The line is small — 4.8% of FY2025 operating cost — so the scenario spread moves FY2030E owners' earnings by ~1% in the bear and ~0.05% in the bull, and not at all in the base case.
- **Bad debt**: \$19,220/yr, the normalisation carried over from `OE` §2.2(c).
- **Share-based compensation**: \$117,557/yr, normalised per `OE` §2.2(d) and treated as non-deductible for tax. Reported SBC has collapsed to \$4,894 in H1 FY2026 because the only live grant has nearly fully amortised (`FSQ2` Note 6), but shareholders approved an "amended and restated stock option plan" in April 2026 with 98.6% support (`AM26`), so assuming zero future grants is not credible.
- **Depreciation less maintenance capex**: −\$2,196/yr flat, per `OE` §2.1. Property and equipment is \$34,689 in total (`FS25` Note 4); this line is noise.

### 5.3 Tax

26.5% ("The basic rate of 26.50% was applied to the pre-tax income" — `MDA25`; the same rate is applied in `MDQ2`), levied on normalised pre-tax owners' earnings plus the non-deductible share-based compensation, plus \$1,300/yr of the unexplained Note 9 permanent difference (FY2025: \$1,385; TTM: \$1,162 — `OE` §2.2(e)).

---

## 6. FY2026E reconciled against reported H1 FY2026

The FY2026 forecast was produced by the driver method without reference to reported halves. Checking it afterwards:

| Check                                               | Value         |
|-----------------------------------------------------|---------------|
| FY2026E revenue (driver model)                      | 8,655,668     |
| H1 FY2026 actual (`FSQ2`)                           | 4,267,406     |
| **Implied H2 FY2026**                               | **4,388,262** |
| Implied H2 vs H1                                    | +2.8%         |
| Q3 FY2026 FX tailwind vs H1 (Knowledge Store ID 11) | +1.2%         |
| Implied constant-currency sequential growth         | ~+1.6%        |

H1 quarters grew +5.5% and 0.0% sequentially in reported CAD (`MDQ2`), which is +5.5% and +1.25% in USD once the Q1→Q2 rate move of −1.24% is removed. So the model's implied H2 asks for materially *less* sequential growth than either realised quarter delivered. **FY2026E is, if anything, conservative** — and note that this particular argument is *sequential*, so it does not depend on the bucket-rate calibration described in §2.5; it would hold whatever year-on-year rates had been chosen, as long as they produced this revenue level.

**One offsetting optimism, sized.** The geographic note does not separate recurring revenue from professional services, so the bucket growth rates carry H1 FY2026's elevated professional-services level (2.3% of revenue) forward. If professional services instead revert to the FY2025 level of 1.0% of revenue, FY2026E revenue is overstated by roughly \$100,000, or 1.2% — smaller than the conservatism in the H2 sequential assumption above, so the two roughly cancel. Expressed in constant currency, FY2026E total growth of +9.7% CAD is ~+10.9%, against H1 FY2026 actuals of +11.4% total and +9.3% recurring. The forecast sits between the two, which is the right place for it.

On the cost side, the model's FY2026 average headcount of 19.8 implies H2 FY2026 compensation of \$1,761,818 against 21 staff at the assumed run rate of \$1,739,609 — a 1.3% gap. That is the real validation of the compensation-per-head assumption.

---

## 7. Sensitivities (base case)

| Variant                                         | FY2030E OE    | vs base  | Cumulative FY26–30 | vs base |
|-------------------------------------------------|---------------|----------|--------------------|---------|
| **Base case**                                   | **2,859,320** | —        | **12,913,536**     | —       |
| USD/CAD 1.25 from FY2027 (CAD +10%)             | 2,128,968     | −26%     | 10,257,218         | −21%    |
| USD/CAD 1.32 from FY2027 (CAD +5%)              | 2,494,143     | −13%     | 11,585,376         | −10%    |
| USD/CAD 1.46 from FY2027 (CAD −5%)              | 3,224,497     | +13%     | 14,241,699         | +10%    |
| USD/CAD 1.53 from FY2027 (CAD −10%)             | 3,589,676     | +26%     | 15,569,864         | +21%    |
| Mexican account lost in FY2028                  | 1,674,912     | **−41%** | 9,550,625          | −26%    |
| Mexican account flat from FY2027                | 2,487,235     | −13%     | 11,839,056         | −8%     |
| Legacy US account lost outright in FY2027       | 2,592,350     | −9%      | 11,378,762         | −12%    |
| Legacy US account stops shrinking (0%/yr)       | 3,406,578     | +19%     | 14,790,281         | +15%    |
| US ex-legacy growth 3 pts lower every year      | 2,229,922     | −22%     | 11,186,256         | −13%    |
| US ex-legacy growth 3 pts higher every year     | 3,562,364     | +25%     | 14,779,300         | +14%    |
| Headcount +1/yr only (23 by FY2030)             | 3,280,566     | +15%     | 14,062,754         | +9%     |
| Headcount +2.5/yr (31 by FY2030)                | 2,157,244     | −25%     | 11,347,821         | −12%    |
| Wage inflation 5.0% not 3.5%                    | 2,586,989     | −10%     | 12,183,194         | −6%     |
| Non-comp cost of sales scales 1.0× with revenue | 2,798,832     | −2%      | 12,734,198         | −1%     |

The FX rows imply an elasticity of roughly **2.6× on owners' earnings** (a 5% currency move shifts FY2030E owners' earnings 13%), slightly above the 2.0–2.4× operating-income elasticity in `CM` §3.6 — as expected, since owners' earnings are a smaller base than operating income and the same absolute swing is a larger proportion of it. **Currency and single-account retention remain the two largest swing factors, and NamSys controls neither and hedges neither** (`MDA25` Risk Factors) — that conclusion from `CM` §8 survives intact.

---

## 8. Scenarios: what has to be true

**Base (owners' earnings \$2.38M → \$2.86M, +4.9%/yr).** The legacy US account keeps shrinking at −20%/yr; the rest of the US grows 13% decaying to 7% as the accessible market saturates; the Mexican rollout completes in FY2027 and then behaves like a mature account; the rest of international accelerates modestly as the UK/Australia hires and ISO 27001 convert; headcount rises to 26 with 3.5% wage inflation; USD/CAD flat.

**Bull (\$2.50M → \$4.65M, +15.6%/yr).** The legacy account stabilises rather than continuing to shrink; the US ex-legacy base holds 10–14%; a **second Mexico-sized international rollout** lands from FY2028, taking the rest-of-international bucket to 20–30% growth; AI productivity holds headcount growth to ~1/yr, so the cost base does not chase revenue. The load-bearing item is the second large international account — this is the scenario in which management's "at least 10 times" international opportunity (`AM26`) starts to show up in the accounts.

**Bear (\$2.19M → \$1.51M, −7.7%/yr).** The legacy account is lost outright in FY2028 via the bank-merger mechanism in `MDA25` Risk Factors; the Mexican rollout completes and then goes flat; the rest of the US saturates to 4–6%; international never lands a second large account; **and management does not cut costs**, continuing to hire to 24 with 4.5% wage inflation. That last assumption is deliberate — `CM` §4.4 documents the revealed preference (headcount went 17 → 21 *while* growth decelerated) and the \$1,100,000 employee termination commitment to three employees (`FS25` Note 13) that makes cutting senior staff expensive. It is also the least realistic part of the bear case over a five-year horizon, which is why the fourth row of the headline table shows the same revenue path with headcount frozen at 21 and then trimmed to 20: owners' earnings land at \$2.09M in FY2030E rather than \$1.51M, a −1.4%/yr outcome. **The honest downside is roughly flat-to-slightly-down owners' earnings, not collapse.**

---

## 9. Internal consistency

Three checks that a forecast of this shape has to pass.

**Revenue per employee.** `AM25` states \$400,000 per employee for FY2024; \$6,840,146 ÷ 17 = \$402,362, which ties and confirms 17 as the FY2024 base.

| Period  | Revenue per employee |
|---------|----------------------|
| FY2024A | 402,362              |
| FY2025A | 464,212              |
| FY2026E | 437,155              |
| FY2027E | 418,292              |
| FY2028E | 421,505              |
| FY2029E | 431,901              |
| FY2030E | 440,860              |

The base case holds revenue per employee roughly **flat** at \$418–441k after the FY2026 hiring reset — it credits essentially **no** further productivity gain over five years, despite management's AI narrative. That is conservative and deliberate, and it is where the bull case gets its margin expansion from.

**Compensation as a share of revenue.** 36.5% (FY2023A) → 35.0% (FY2024A) → 34.7% (FY2025A) → 38.1% (FY2026E) → 43.3% (FY2030E). The base case assumes the FY2023–FY2025 operating leverage **reverses and does not return**. Anyone who believes management's AI productivity claims should regard the base case as too harsh; the "headcount +1/yr" sensitivity (+15% on FY2030E) is the relevant adjustment.

**Growth versus the market ceiling.** Base-case FY2030E revenue of \$11.46M is +45% on FY2025. At an unchanged ~8% share of US CIT vehicles NamSys would be nowhere near a market constraint — the constraint is the addressable *client* tier (the 25% of the US CIT market not held by Brinks, Loomis and Garda, where NamSys already has "a small majority" of clients; `AM26`), which is why the US ex-legacy rate decays to 7% rather than holding. International growth of ~14–15% on a base that reaches only USD 1.03M by FY2030E is a rounding error against a market management describes as "at least 10 times" the US; the forecast therefore does not require the international opportunity to be real in order to work, which is the right way round given that "at least 10 times" is an unaudited management truck-count proxy in a market that "is not covered by a lot of researchers" (`AM26`).

---

## 10. What I am confident about, and what I am not

**High confidence (arithmetic on disclosed figures plus a published exchange-rate series):**

- The constant-currency decomposition in §3. FX contributed a +2.9% tailwind in FY2025 and a −2.9% headwind in H1 FY2026, and the reported deceleration is substantially a currency artefact. This is arithmetic on Note 7 and Bank of Canada data (Knowledge Store ID 11).
- Roughly 8–9 points of the historical earnings growth was CAD depreciation (1.2878 → 1.4009), not the business — see the restatement immediately below.
- The largest historical account has shrunk in constant currency in each of FY2024, FY2025 and H1 FY2026, going from 24.9% of revenue (FY2023) to ~12.8% (H1 FY2026).
- The cost engine reproduces FY2025 owners' earnings to within \$1 (§2.1), so the forecast differs from history only through its driver assumptions, not through method.
- FY2026E is conservative relative to the reported H1 run rate (§6).

Restating FY2022 at FY2025 exchange rates (script §9c):

| Measure          | Reported FY2022–FY2025 CAGR | Constant-currency CAGR (0% / 20% USD cost share) |
|------------------|-----------------------------|--------------------------------------------------|
| Operating income | 21.5%                       | 12.5% / 13.6%                                    |
| Owners' earnings | 24.7% (`OE` §5)             | 14.6% / 15.8%                                    |

**Holding USD/CAD flat therefore removes most of the historical earnings tailwind by construction, and that — not a deteriorating business — is why the forecast growth rate is so much lower than history.** If a reader disagrees with flat FX, the FX rows in §7 are the adjustment, and they are large.

**Genuine uncertainty:**

- **Whether Mexico is one customer.** Four near-exact matches is strong circumstantial evidence, not disclosure. If wrong, §4.4's concentration warning is overstated and the international story is somewhat healthier than I present it. Testable at the next filing: if Mexico's share and the top-3 shares keep moving in lockstep, the inference holds.
- **The headcount path.** This is the single largest controllable driver (+15% / −25% on FY2030E) and it is a management choice with only one named data point (UK and Australia engineers, `AM26`). I have no visibility beyond FY2027.
- **Compensation per head.** The historical series implies 14.3% growth in FY2025 at flat headcount, which I cannot explain and have not modelled forward. The 5% sensitivity is the honest bound.
- **The forward rate on "US ex-legacy."** Two observations (17.3%, 14.1%) with a professional-services contamination on the second. A 3-point error either way is ±22–25% on FY2030E.
- **Whether the Mexican rollout is a rollout at all.** I infer it from the shape (34.9% then 50.8%) and from the one documented precedent (`AM25`'s FY2024 CIT rollout). If it is instead a growing multi-year relationship, the bull case is more likely; if it is a one-year implementation that reverses, the bear case is.
- **USD/CAD.** Held flat as a no-view assumption. I have no edge and make no claim. The ±5% and ±10% rows are the whole of my position.
- **Everything in `CM` §10's "management assertion, not independently verified" list** still applies: zero churn is a company statement with no cohort data, the "at least 10×" TAM is an anecdotal truck-count proxy, and the MCP/agent-interoperability moat (`AM26`) has produced no results and is symmetric by construction.

**One thing deliberately excluded.** Owners' earnings here exclude the return on the financial portfolio, per `OE` §4. Owners additionally receive whatever the ~\$7.37M of cash and short-term investments at April 30, 2026 yields — \$108k–\$133k after tax at the disclosed 2.0–2.45% GIC rates (`FSQ2` Note 15), i.e. 4–6% of owners' earnings, earning below any plausible inflation rate. Because invested capital is negligible and there is no debt (`OE` §3), essentially 100% of the owners' earnings forecast above is distributable each year without impairing the business — which is what the record shows (special dividends of \$1,350,477 in FY2024 and \$4,027,790 in March 2026, plus continuous buybacks; `MDA25`, `FSQ2` Note 6, `MDQ2`).

---

## 11. Monitorables

In order of diagnostic value, each falsifiable against the next two filings:

1. **The Mexico line in Note 7 read jointly with the top-3 customer shares.** If they keep matching to within ~0.1pp, the single-customer inference holds and §4.4's concentration warning stands. If they diverge, the inference fails and the international picture improves.
2. **Mexico's growth rate.** The base case needs +48% in FY2026 then deceleration to +18%. Sustained 40%+ into FY2027 is the bull trigger; a flat or declining Mexico line is the single most damaging observation available.
3. **US revenue in Note 7, converted at the period's average USD/CAD.** The base case needs ~+6% constant currency in FY2026 decaying to ~+5%. Reported CAD growth on its own is uninformative — it must be deflated.
4. **Note 14 compensation against average headcount disclosed at the annual meeting.** The base case needs compensation to grow ~8.5%/yr. Faster means the margin path is too optimistic; the H2 FY2026 figure is the first clean read at 21 staff.
5. **The top-3 share that is *not* Mexico.** The base case assumes the legacy account keeps shrinking ~20%/yr. If it stabilises, add ~19% to FY2030E.
6. **Professional services as a share of revenue** (`MDQ2`: 2.3% in H1 FY2026 versus 1.0% in FY2025). Sustained elevation is ambiguous — it is either a less-recurring mix (bad) or implementation work preceding subscription ramps (good). Read it alongside which geography is growing.
7. **Over-90-day trade receivables** (\$16,861 → \$126,998 → \$237,066; `FS25` Note 3, `FSQ2` Note 3). `CM` §7 reads this as the leading indicator of a growth-quality problem. Nothing in this forecast depends on it, but it is the cheapest early warning available.
8. **Any acquisition closing.** Would invalidate the capital-structure assumptions entirely. Management has been unsuccessful "for several years... but it is not for lack of trying," and now questions the logic itself: "is it cheaper for us to build that rather than buy it?" (`AM26`).

---

## 12. Source index

| Reference                                                  | Used for                                                                                        |
|------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| `primary_sources/FY2023/Namsys_-_Annual_FS_-_Feb262024.md` | FY2022/FY2023 statements; Note 7 geography; Note 14 compensation                                |
| `primary_sources/FY2024/NamSys_AFS_021925.md`              | FY2024 statements; Note 7 geography and customer concentration; Note 14                         |
| `primary_sources/FY2025/NamSys_AFS_022426.md`              | FY2025 statements; Notes 3, 4, 6, 7, 13, 14, 15                                                 |
| `primary_sources/FY2025/NamSys_MDA_022426.md`              | Tax rate; staffing commentary; selling-expense drivers; Risk Factors                            |
| `primary_sources/2Q2026/FS_Q2_NamSys_Apr_30_26_FINAL.md`   | H1 FY2026 statements; Notes 6, 7, 11, 13, 14, 15                                                |
| `primary_sources/2Q2026/MDA_Q2_NamSys_Apr_30_26_FINAL.md`  | Quarterly revenue table; recurring vs professional services; expense drivers                    |
| `fetched_docs/namsys_2025_annual_meeting_transcript.md`    | Headcount 17; NRR 112%; zero churn; FY2024 CIT rollout; reseller failure; competitive landscape |
| `fetched_docs/namsys_2026_annual_meeting_transcript.md`    | Headcount 21; 8% of US CIT vehicles; big-three 75%; pricing; AI; UK/Australia hires             |
| `fetched_docs/namsys_newswire_list_sep2026.md`             | Historical Q3 release dates (Sept 25, 2024; Sept 26, 2023)                                      |
| `work_products/owners_earnings_and_roic.md`                | Owners' earnings definition, normalisations and FY2022–FY2025 actuals                           |
| `work_products/causal_model.md`                            | Causal structure; the claims corrected in §3 and §4                                             |
| Knowledge Store ID 4                                       | ISO/IEC 27001:2022 certification, February 2026                                                 |
| Knowledge Store ID 11                                      | Bank of Canada FXMUSDCAD fiscal-year average exchange rates                                     |
| Knowledge Store ID 12                                      | Federal Reserve 2026 Diary of Consumer Payment Choice                                           |
| `work_products/forecast_earnings_calcs.py`                 | All calculations in this document                                                               |
