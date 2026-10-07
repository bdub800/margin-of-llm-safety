# Adobe Inc. (ADBE) — Five-Year Forecast of Owners' Earnings, FY2026E–FY2030E

*Prepared 2026-08-31. All arithmetic is in `work_products/forecast_earnings_calcs.py` (run with `uv run python work_products/forecast_earnings_calcs.py`). The forecast starts from the historical owners' earnings in `work_products/owners_earnings_and_roic.md` and is driven by the factors in `work_products/causal_model.md`. Most recent primary source is the Q2 FY2026 10-Q and the June 11 2026 earnings call; Q3 FY2026 reports on September 10 2026 and is not reflected here (Knowledge Store IDs 27, 36).*

---

## 1. Answer first

| ($M unless stated)                        | FY2025A   | FY2026E   | FY2027E   | FY2028E   | FY2029E    | FY2030E    |
|-------------------------------------------|-----------|-----------|-----------|-----------|------------|------------|
| Total revenue                             | 23,769    | 26,496    | 29,001    | 31,232    | 33,363     | 35,267     |
| Revenue growth                            | +10.5%    | +11.5%    | +9.5%     | +7.7%     | +6.8%      | +5.7%      |
| EBITA (EBIT + purchased-intangible amort.)| 9,016     | 9,789     | 10,733    | 11,750    | 12,734     | 13,607     |
| EBITA margin                              | 37.9%     | 36.9%     | 37.0%     | 37.6%     | 38.2%      | 38.6%      |
| **Owners' earnings (base case)**          | **7,119** | **7,729** | **8,475** | **9,278** | **10,055** | **10,745** |
| Owners' earnings margin                   | 30.0%     | 29.2%     | 29.2%     | 29.7%     | 30.1%      | 30.5%      |
| Owners' earnings growth                   | +10.5%    | +8.6%     | +9.7%     | +9.5%     | +8.4%      | +6.9%      |

*(Computed, `forecast_earnings_calcs.py` §4, §6, §8. FY2025 actuals from `work_products/owners_earnings_and_roic.md`, which the script reproduces exactly: EBIT $8,706M + amortisation $310M = EBITA $9,016M, + depreciation $236M − maintenance capex $241M = $9,011M pre-tax, × (1 − 21%) = $7,119M.)*

**Base case: owners' earnings compound at 8.6% a year, roughly in line with revenue at 8.2%.** The margin dips in FY2026–FY2027 as the freemium advertising spend and rising AI inference cost bite, then recovers past the FY2025 level by FY2029 on sales-force operating leverage.

*(Note: this document forecasts owners' earnings at the company level only. It does not model per-share figures, buybacks, or SBC-driven dilution — that would require a view on future capital allocation and the multiple at which Adobe repurchases stock, which is a valuation question, not a forecast of the operating business.)*

### The four scenarios, and the honest expected value

| Scenario                       | Probability (judgment) | FY2030E owners' earnings | 5-yr OE CAGR | 5-yr revenue CAGR |
|--------------------------------|------------------------|--------------------------|--------------|-------------------|
| SEVERE — AI substitutes the creative workflow | 15%   | $6,022M                  | **−3.3%**    | +0.9%             |
| BEAR — grinding share loss, cost never abates | 25%   | $8,105M                  | +2.6%        | +5.1%             |
| BASE                                          | 40%   | $10,745M                 | +8.6%        | +8.2%             |
| BULL — freemium converts, unit costs deflate  | 20%   | $13,035M                 | +12.9%       | +10.8%            |
| **Probability-weighted**                      |       | **$9,834M**              | **+6.7%**    | —                 |

*(Computed, §9. The probability weights are my judgment and are not sourced. They are shown so the reader can substitute their own; the four scenario paths are the actual output.)*

**If I had to give one number, it is ~$9.8bn of owners' earnings in FY2030, a 6.7% CAGR — not the 8.6% base case.** The distribution is left-skewed: the downside scenarios are driven by a mechanism (generative AI substituting creative workflows) that has already been observed once at Adobe, in Adobe Stock, and that management conceded ran ahead of its own plan (`work_products/causal_model.md` §1.6).

---

## 2. The root-cause factor set, and why these and not others

The brief requires forecasting causes, not effects. Adobe's revenue is a *lagging, smoothed* release of a contracted ARR book (`work_products/causal_model.md` §0), so forecasting "revenue growth" would be forecasting an effect twice removed. The chain is:

```
   free monthly active users  ──►  free-to-paid conversion  ──►  paid units ─┐
   value-based tier migration ────────────────────────────►  price/unit ────┤
   enterprise seat + cross-sell ───────────────────────────────────────────┤
   AI-native substitution (churn) ─────────────────────────────────(minus)─┤
                                                                            ▼
                                                                  NET-NEW ARR
                                                                            │
                                                              ARR stock ────┤
                                                                            ▼
                                                     REVENUE (ratable, ~2-qtr lag)
                                                                            │
   inference cost per generation × generations per user × users ──(minus)───┤
   advertising per acquired user × users acquired ───────────────(minus)────┤
   R&D headcount × wage ─────────────────────────────────────────(minus)────┤
                                                                            ▼
                                                            OWNERS' EARNINGS
```

Seven drivers are forecast explicitly. Everything else is either immaterial (product revenue, 1.4% of FY2025) or derived.

| # | Root driver                                  | Where it is disclosed                             | Confidence |
|---|----------------------------------------------|---------------------------------------------------|------------|
| 1 | Acrobat/Express monthly active users         | Earnings calls (MAU counts)                       | High       |
| 2 | Monetisation per MAU (conversion × price)    | Derived; components never disclosed               | **Low**    |
| 3 | Creative paid-unit volume                    | Derived from the 75/25 net-new ARR split          | Medium     |
| 4 | Creative value-based price / tier mix        | Same split; corroborated by observed price actions| Medium     |
| 5 | Enterprise seat expansion and cross-sell (DX)| Segment subscription revenue; $10M+ customer count| Medium     |
| 6 | Hosting / AI-inference cost ratio            | Cost of subscription revenue, ex-amortisation     | Medium     |
| 7 | Advertising intensity (freemium acquisition) | 10-K Note 1 advertising expense                   | Medium     |

**Segments are modelled separately** because they behave completely differently: BP&C (Acrobat/Express) grew 14.7% in FY2025 on a volume engine, Creative grew 10.2% on a mixed engine, Digital Experience grew 11.2% on enterprise contracts, and Publishing & Advertising is shrinking and was written down (computed, §0, from `primary_sources/FY2025/md_and_a.md`).

**A definitional note that matters.** Adobe's FY2025 10-K MD&A states that "*Revenue associated with the Creative & Marketing Professionals customer group consists of Digital Experience offerings as well as Creative Cloud flagship apps such as Photoshop, Lightroom and Illustrator within Digital Media*" (`primary_sources/FY2025/md_and_a.md`). C&MP therefore *includes* all Digital Experience revenue. I isolate "Creative" by subtracting Digital Experience segment subscription revenue from C&MP — giving $9,094M / $9,885M / $10,894M for FY2023–FY2025 (computed, §0). This is the only way to see the Creative franchise on its own, and it is arithmetic, not estimation: Digital Media subscription $17,389M − BP&C $6,495M = $10,894M ties exactly.

---

## 3. Driver 1–2: Business Professionals & Consumers (Acrobat / Express)

### The facts

| Metric                                                     | FY2024 exit | FY2025 exit | Q2 FY2026 |
|------------------------------------------------------------|-------------|-------------|-----------|
| Acrobat + Express monthly active users                      | ~625M       | >750M       | >850M     |
| YoY MAU growth                                              | —           | +20%        | ~+20%     |
| BP&C subscription revenue ($M)                              | 5,662       | 6,495       | 1,850/qtr |
| **Revenue per average MAU ($/yr, computed)**                | **$9.88**   | **$9.45**   | —         |

*(MAU: "*Monthly active users of Acrobat and Express surpassed 750 million, growing 20% year-over-year*" — CFO Dan Durn, `primary_sources/4Q2025/earnings_call_transcript.md`; "*Acrobat and Express MAU surpassed 850 million, growing approximately 20% year-over-year*" — CFO Steve Day, `primary_sources/2Q2026/earnings_call_transcript.md`. FY2024 exit MAU of 625M is derived as 750/1.20 — **inference from the disclosed growth rate**. Revenue per MAU computed, §1.)*

**Caution, and I flag it because it is easy to get wrong:** the "850 million" quoted on the Q1 FY2026 call is a *different and broader* metric — Acrobat + Creative Cloud + Express + Firefly, growing 17% (`primary_sources/1Q2026/earnings_call_transcript.md`). Only the Q4 FY2025 and Q2 FY2026 figures are the Acrobat+Express series. I use the Q4-to-Q4 series only and do not build a sequential path from mixed definitions.

### The decomposition, and what it actually says

BP&C revenue growth of +14.7% in FY2025 = average-MAU growth of +20.0% compounded with a revenue-per-MAU change of −4.4% (computed, §1). Revenue per MAU is the *composite* of free-to-paid conversion and price per paid seat, and **Adobe has never disclosed either component** — this is the single largest unmeasurable in the model and in `work_products/causal_model.md` (uncertainty #1).

What I can do is bound it. If price per paid seat rose ~2.5% in FY2025 (consistent with the value-based-pricing quarter of net-new ARR, and with Acrobat Studio attach — "*nearly 50% of Acrobat commercial ETLAs renewed in Q4 already upgrading*", `primary_sources/4Q2025/earnings_call_transcript.md`), then **paid seats grew ~11.9%, i.e. about 0.6× the MAU growth rate**. That 0.6× wedge is the mechanical reason revenue per MAU falls while MAU compounds: the incremental user is free and converts at a lower rate than the installed base.

### The forecast

| Driver                          | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
|---------------------------------|---------|---------|---------|---------|---------|
| MAU growth                      | 18%     | 13%     | 10%     | 8%      | 6%      |
| MAU exiting year (M)            | 885     | 1,000   | 1,100   | 1,188   | 1,259   |
| Change in revenue per MAU       | −3.5%   | −2.5%   | −1.0%   | 0.0%    | 0.0%    |
| **BP&C revenue growth**         | **14.7%**| **12.4%**| **10.3%**| **9.0%**| **7.0%**|
| *Implied paid-seat growth at 2.5% price* | 11.1% | 7.5% | 6.2% | 5.4% | 3.4% |

*(Computed, §1. All five columns are JUDGMENT.)*

**Justification.** MAU growth decays because the distribution surfaces that produced it are one-time land-grabs — "*AI mode in Reader, Edge, Chrome, and WhatsApp*" (Narayen, `primary_sources/2Q2026/earnings_call_transcript.md`). Once Reader is instrumented on every major browser, the next 100M users are harder than the last. Revenue per MAU stops falling when MAU growth decelerates toward the price contribution — that is arithmetic, not optimism: at 6% MAU growth and ~2.5% price, flat revenue-per-MAU implies paid seats growing 3.4%, i.e. conversion still deteriorating.

**Sanity check on the level.** 1,259M MAU by FY2030 is large. Gartner put global knowledge workers past 1 billion in 2019 and at 1.14 billion by 2023 (Knowledge Store IDs 53, 60); Forrester estimated 1.25 billion information workers (Knowledge Store ID 45). So Adobe would be at roughly parity with the global information-worker population. **I do not treat that as a hard ceiling**, because Acrobat Reader and Express reach consumers and students, not only information workers, and Adobe explicitly targets a "*$300 billion TAM beyond professional designers*" through Express (Knowledge Store ID 24). But it is the reason MAU growth is forced down to 6% by FY2030 rather than held in double digits. **The binding constraint on this line is monetisation, not reach.**

**Where this could be wrong.** Canva has 265 million monthly active users and 31 million paid users, with MAU up 20% in 2025 (`fetched_docs/canva_4b_revenue_techcrunch.md`) — a directly competing funnel of comparable growth targeting the same prosumer segment. If Canva takes the marginal prosumer, Adobe's MAU still grows (Reader is not substitutable) but conversion falls faster. That is the bear case: revenue per MAU declining 3–4.5%/yr indefinitely.

---

## 4. Driver 3–4: Creative (Creative Cloud flagship apps)

### The empirical volume/price split

The single best-sourced structural fact about Adobe's growth engine: "*Over 75% of Digital Media net new ARR was driven by continued growth in subscriptions and cross-sell and upsell, with the remainder from value-based pricing*" (CFO Dan Durn, `primary_sources/4Q2025/earnings_call_transcript.md`; confirmed in `fetched_docs/adbe_q4fy25_script_slides.md`). Applied to Creative's computed FY2025 growth of +10.2%, that splits ~7.7pp volume and ~2.6pp price (computed, §2).

### The forecast

| Driver                          | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
|---------------------------------|---------|---------|---------|---------|---------|
| Paid-unit volume growth         | 7.8%    | 6.0%    | 5.0%    | 4.0%    | 3.0%    |
| Value-based price / tier mix    | 0.5%    | 2.0%    | 2.0%    | 2.0%    | 2.0%    |
| FX translation                  | 2.0%    | 0.0%    | 0.0%    | 0.0%    | 0.0%    |
| **Creative revenue growth**     | **10.3%**| **8.0%**| **7.0%**| **6.0%**| **5.0%**|

*(Computed, §2. JUDGMENT on all forward columns.)*

**Why price is ~0 in FY2026 and ~2% thereafter.** Management explicitly deferred the second-half price actions: "*we have made the decision to defer previously planned Creative Cloud second half line optimizations*", framed as "*a phase shift... we're deferring it, but not closing it*" (Narayen, `primary_sources/2Q2026/earnings_call_transcript.md`). I take the deferral as fact and the recoverability as an assertion. The evidence that Adobe still *can* price is real but partial: Creative Cloud All Apps was renamed Creative Cloud Pro at $70/month in May 2026, and Lightroom plans were raised in March and August 2026 (Knowledge Store IDs 37, 40 — note ID 37 is internally muddled about which Lightroom SKU rose from $9.99 to $34.99, so I use it only as directional evidence that price actions continued through FY2026, not as a quantified input).

**Why volume decays to 3%.** Three sourced reasons:

1. **The professional seat pool is not growing.** US Bureau of Labor Statistics projects employment of graphic designers to **decline 2% from 2025 to 2035** (Knowledge Store ID 35; `fetched_docs/bls_ooh_graphic_designers.md`). Creative's *unit* growth cannot come from the professional population; it must come from prosumers, which is the lower-priced, more contested segment.
2. **Credible substitutes exist and are scaling.** Canva reached $4bn ARR at end-2025 with a B2B book of $500M growing 100% (`fetched_docs/canva_4b_revenue_techcrunch.md`), and made the Affinity professional suite — Photo, Designer, Publisher — **free for everyone**, explicitly aimed at professionals "*who have historically lived inside Photoshop, Illustrator, and InDesign*" (`fetched_docs/adobe_creative_crown_slips_2026.md`, `fetched_docs/canva_42b_redomicile_2026.md`). Figma's revenue grew 48% year-over-year to $370.1M in Q2 2026 with 136% net dollar retention and FY2026 guidance of $1.463–1.467bn (`fetched_docs/figma_q2_2026_results.md`). Apple launched a Creator Studio bundle at $12.99/month in January 2026 (`fetched_docs/canva_4b_revenue_techcrunch.md`).
3. **AI substitution of an Adobe line is no longer hypothetical.** Adobe Stock, a ~$450M book, is declining roughly 4–5% year-over-year and Adobe conceded it "*saw a steeper decline than we expected*" (`work_products/causal_model.md` §1.6, correcting an earlier 17% error).

**The counter-evidence I am weighing against that.** Adobe's Creative funnel inputs are accelerating, not decelerating: creative freemium MAU went from >50M to >90M year-over-year, +70% (CFO Steve Day, `primary_sources/2Q2026/earnings_call_transcript.md`), and Creative traffic to adobe.com "*grew over 50% year-over-year*" (Wadhwani, same call). Adobe still holds an estimated ~58% share of the creative software industry (`fetched_docs/adobe_creative_crown_slips_2026.md` — **weak source, a secondary press citation of a BCG framing, flagged as such**). And Figma at a $1.47bn FY2026 run-rate is 13% of Adobe's ~$10.9bn Creative line, so its 48% growth is not yet arithmetically capable of stalling Adobe.

**Net judgment.** Volume growth decaying from 7.8% to 3.0% is the middle of these two bodies of evidence. Set against it: the bear case takes volume to 0% by FY2030 and the severe case to −5%. **I am not confident in the base case here.** It is the single driver with the widest defensible range, and Section 10 shows it is worth ±4% on FY2030 owners' earnings per 2pp of annual volume growth — which understates its importance, because in the severe case it also drags price and cost.

---

## 5. Driver 5: Digital Experience, Semrush, and the run-off lines

DX subscription revenue grew 12.3% (FY2024) then 11.2% (FY2025) (computed, §0). The disclosed forward indicators are strong — enterprise customers with over $10M ARR "*growing greater than 20% year-over-year*" and GenStudio/AEP/AEM ending ARR "*growing over 20% year-over-year*" (Steve Day, `primary_sources/2Q2026/earnings_call_transcript.md`) — but total DX growth is decelerating anyway, which tells you the large-customer cohort is being offset by weakness elsewhere in the book. **I forecast 9.0% decaying to 6.5%** and assume no re-acceleration (§3, JUDGMENT).

**Semrush** contributes $280M in FY2026 (management's own figure), annualising to ~$500M in FY2027 then growing 6–8% (§3). This is deliberately below Semrush's standalone growth history, reflecting acquisition friction; it is a judgment. Semrush's causal significance is not the revenue — it is that its $480M of acquired ARR exactly filled the hole left by the ~$480M organic ARR guidance cut, so the headline 10.2% ARR target was held while the organic target fell ~1.9pp (`work_products/causal_model.md` §1.2).

**Run-off lines**: Publishing & Advertising subscription declines 5%/yr from $106M; product revenue and services revenue decline from the 1H FY2026 annualised run-rates. Services is now *loss-making* — 1H FY2026 revenue $223M against cost of $242M (computed, §3, §6) — so its shrinkage is a small positive for gross profit and a small negative for revenue. Combined, these three lines are 3.2% of FY2025 revenue and cannot move the answer.

**Not modelled:** Topaz Labs, agreed June 25 2026 and expected to close in 2H 2026. Adobe disclosed **no purchase price and no revenue figure** (`fetched_docs/adbe_topaz_labs_acquisition.md`), so there is nothing to model. It is small relative to Semrush and is unmodelled upside to revenue and unmodelled downside to invested capital.

---

## 6. Driver 6: the cost of AI inference — the most important finding in this document

### The reported gross margin is misleading, and here is the arithmetic

`work_products/causal_model.md` §2.1 concluded that AI cost "*has not yet materialised*" in the gross margin, citing ~30bp of subscription-margin erosion and a ~17bp drag on total gross margin in Q2 FY2026. **That conclusion is correct on a reported basis but understates the underlying deterioration by roughly a factor of four, because purchased-intangible amortisation sitting inside cost of revenue collapsed at the same time and masked it.**

Adobe discloses the split. FY2025: total amortisation of other intangibles was $310M, "*of these amounts, $151 million... was included in cost of sales*" (`primary_sources/FY2025/financial_statements.md`, Note 8). 1H FY2026: total $91M, of which $17M in cost of revenue; 1H FY2025: total $167M, of which **$85M** (`primary_sources/2Q2026/financial_statements.md`, Note 7).

| Cost of subscription revenue **excluding** purchased-intangible amortisation | Ratio to subscription revenue |
|------------------------------------------------------------------------------|-------------------------------|
| FY2025                                                                       | 8.19%                         |
| 1H FY2025                                                                    | 8.18%                         |
| **1H FY2026**                                                                | **8.79%**                     |
| **Year-over-year change**                                                    | **+61bp**                     |

*(Computed, §6. Ex-amortisation cost of subscription revenue grew +21.9% against subscription revenue of +13.4%.)*

The $68M reduction in amortisation inside cost of revenue is worth 54bp of subscription revenue — it absorbed almost the entire 61bp underlying deterioration. **On the basis that matters for owners' earnings, which adds purchased-intangible amortisation back, Adobe's hosting and AI-inference cost ratio is deteriorating at about 60 basis points a year right now.** This is why the forecast has an EBITA margin dip in FY2026–FY2027 that a reported-gross-margin analysis would miss. It also matters that this masking effect is temporary and largely spent: the disclosed forward amortisation schedule falls from $222M (FY2026) to $143M (FY2030) (`primary_sources/2Q2026/financial_statements.md`, Note 7), so there is little left to hide behind.

### The forward path, and the genuinely two-sided evidence

Two forces oppose each other, and both are well documented.

**Volume up, and Adobe is deliberately amplifying it.** Free users get generative credits (`primary_sources/FY2025/business.md`). Adobe added ~150M free Acrobat/Express MAU and ~40M free creative MAU year-over-year, and the traffic re-routing to freemium happens "*in Q3*" FY2026 (Narayen, `primary_sources/2Q2026/earnings_call_transcript.md`). Consumption is compounding hard: generative credit consumption "*increased 3x quarter-over-quarter*" (Q4 FY2025), "*over 45% quarter-over-quarter*" (Q1 FY2026), and Firefly ARR grew ~50% quarter-over-quarter (`primary_sources/4Q2025/`, `1Q2026/`, `2Q2026/earnings_call_transcript.md`). And the mix is moving to the expensive modality: Adobe's own credit schedule charges ~1 credit per standard 1024×1024 image but **~100 credits per five-second video clip** — roughly 20× per second of output (Knowledge Store ID 47).

**Unit cost down, fast, for constant quality.** a16z measures ~10× per-year decline in the cost of an LLM of equivalent performance, with GPT-3-class inference falling from $60.00 to $0.06 per million tokens between November 2021 and November 2024 (`fetched_docs/a16z_llmflation.md`; Knowledge Store ID 19). Epoch AI finds declines of 9× to 900× per year across benchmarks, median 50× (`fetched_docs/epoch_llm_inference_price_trends.md`; Knowledge Store ID 20).

**But four pieces of evidence cut against a simple "costs will collapse" story, and I weight them heavily:**

1. **Volume has historically swamped unit price.** a16z's own data: "*total inference spending grew 320% even as per-token costs dropped 280-fold*" (Knowledge Store ID 19). This is the direct analogue of Adobe's situation.
2. **The frontier tier does not get cheaper.** "*OpenAI's leading model today, o1, has the same cost per output token as GPT-3 had at launch ($60 per million)*" (`fetched_docs/a16z_llmflation.md`). Adobe's differentiation depends on offering *good* models, not cheap ones.
3. **Image generation is moving up the price ladder, not down.** OpenAI's high-quality square image went $0.167 (gpt-image-1) → $0.133 (GPT Image 1.5) → **$0.211 (GPT Image 2)**; Google's went $0.039 (Gemini 2.5 Flash Image, 1024²) → $0.067 (Gemini 3.1 Flash Image, 1K) → $0.134 (Gemini 3 Pro Image) (`fetched_docs/openai_image_gen_guide_costs.md`, `fetched_docs/vertex_ai_genai_pricing_2026.md`). Adobe partners with 25+ third-party models including Google, OpenAI and Black Forest Labs (`fetched_docs/adbe_q4fy25_script_slides.md`), so it buys at these prices.
4. **Announced price increases exist.** Google Vertex has scheduled Gemini 3.7/3.6 Flash pricing to **double on January 1 2027** (`fetched_docs/vertex_ai_genai_pricing_2026.md`), with the current rate labelled promotional.

**Forecast:** the ex-amortisation subscription cost ratio drifts up 72bp in FY2026, decaying to 20bp by FY2030 — a cumulative 202bp deterioration from 8.19% to 10.21%, worth **$701M of extra annual cost at FY2030 revenue** (computed, §6). The decay reflects free-MAU growth decelerating (§3) while unit-cost deflation continues; the *level* reflects the four counter-arguments above. This is JUDGMENT, and Section 10 sizes it: doubling the drift costs 5.2% of FY2030 owners' earnings; eliminating it after FY2026 adds 3.3%. **The cost channel is real but, on any plausible parameterisation, it is second-order compared with the revenue drivers.** That is a genuinely useful conclusion: the market narrative has the emphasis in the wrong place.

*One channel I have deliberately not modelled: vendor repricing. `work_products/causal_model.md` §2.2 sizes a doubling of hosting cost at 11.6–16.3% of FY2025 EBIT. It is bounded and one-time, Adobe has real counterparty leverage, and it depends on an undisclosed hosting share of cost of revenue. Adding it would stack assumptions for no gain in accuracy.*

---

## 7. Driver 7: operating expense — advertising is the persistent item, everything else delevers

| % of revenue           | FY2023 | FY2024 | FY2025 | 1H FY2026 | FY2026E | FY2030E |
|------------------------|--------|--------|--------|-----------|---------|---------|
| Advertising            | 5.00%  | 4.84%  | 5.76%  | n/d       | 6.90%   | 5.80%   |
| Other sales & marketing| 22.57% | 21.97% | 21.53% | n/d       | 21.00%  | 19.95%  |
| = Sales & marketing    | 27.57% | 26.80% | 27.30% | 27.60%    | 27.90%  | 25.75%  |
| Research & development | 17.89% | 18.34% | 18.07% | 17.73%    | 18.00%  | 18.00%  |
| General & administrative| 7.28% | 7.11%  | 6.62%  | 7.75%     | 6.70%   | 6.70%   |

*(FY2023–FY2025 and 1H FY2026 computed from `primary_sources/FY2025/financial_statements.md` and `primary_sources/2Q2026/financial_statements.md`, §0. Advertising expense of $970M / $1.04bn / $1.37bn from FY2025 10-K Note 1 — Adobe discloses it only to two significant figures. Forward columns are JUDGMENT.)*

**Advertising is the causally correct variable.** Both filings attribute the S&M increase identically: S&M rose "*primarily due to increases in advertising expenses and, to a lesser extent, compensation costs*" (`primary_sources/2Q2026/md_and_a.md`, and identically in FY2025). Management refuses to cap it — "*we are spending on this, and we will continue to... we will not be short-term focused on this*" (Narayen, `primary_sources/2Q2026/earnings_call_transcript.md`). This is the P&L expression of the freemium funnel strategy, and it persists into FY2027 because the payback lands there.

**Honest limitation:** total S&M intensity is anchored (management guides non-GAAP operating margin to ~45% for FY2026 and ~44% for Q3 FY2026 — Knowledge Store ID 13, `primary_sources/2Q2026/earnings_call_transcript.md`), and 1H FY2026 S&M of 27.60% is an actual. **The split between advertising and other S&M is my inference from the MD&A attribution, not a disclosure.** The base case implies advertising grows 33% in FY2026 and other S&M grows 8.7% — I present that split because advertising is the causal driver, but the reader should treat the total (27.90%) as the anchored number and the split as illustrative.

**R&D held flat at 18.0%.** It has been pinned at ~18% for four consecutive years and Adobe attributes increases to compensation, not AI training compute (`work_products/causal_model.md` §3.3). Holding it flat is what the observed behaviour supports. **It is nonetheless an assumption I am uneasy about**: AI model *training* compute sits in R&D, and Adobe is now training first-party Firefly models across image, video and audio. If Adobe has to spend to 19.0%, FY2030 owners' earnings fall 2.6% (§10); the bear case uses 18.7% and the severe case 19.5%.

**G&A at 6.70%** = the FY2025 actual of 6.62% plus ~8bp of normalised annual legal provision. `work_products/owners_earnings_and_roic.md` §2.1 flags $30–50M/yr as defensible given the ongoing securities class action and derivative suits. The Q2 FY2026 goodwill impairment ($70M) and FTC/DOJ ROSCA contingency ($92M in 1H) are treated as non-recurring, consistent with the owners' earnings methodology.

---

## 8. From EBITA to owners' earnings

**Construction (identical to Method A in `work_products/owners_earnings_and_roic.md`):**

```
  EBITA  (= EBIT + purchased-intangible amortisation, so no add-back is needed)
+ PP&E depreciation
− maintenance capex
= pre-tax owners' earnings
× (1 − 21% normalised tax)
= OWNERS' EARNINGS
```

Depreciation ($236M FY2025) and maintenance capex ($241M, the three-year average) are both grown 5%/yr and **effectively cancel** — the net item is −$5M rising to −$7M. Adobe rents its compute rather than owning it, so capital intensity is not a forecastable driver here (`work_products/causal_model.md` §4.3). The 21% normalised tax rate is carried forward unchanged; management has fixed its non-GAAP tax rate at ~18% for FY2026 through FY2028 and guides GAAP to ~22.5% (`primary_sources/2Q2026/earnings_call_transcript.md`), and 21% sits between them. Sensitivity: 18% adds 3.8% and 25% costs 5.1% of FY2030 owners' earnings (§10).

### A cross-check that the forecast is not internally broken

**FY2026 against management's guidance.** Model revenue $26,496M vs guide $26,500–26,600M; BP&C $7,453M vs $7,440–7,480M; C&MP $18,192M vs $18,210–18,270M. Grossing management's GAAP EPS guidance of $17.90–18.00 on ~399M shares up through the ~22.5% GAAP tax rate and adding back amortisation, the goodwill impairment and the FTC contingency gives implied EBITA of $9,625M against the model's $9,789M, +1.7% (computed, §8c). **This is a calibration, not a test.** 1H FY2026 is reported and Q3 is guided, so only Q4 FY2026 is genuinely forecast; FY2026E cannot independently validate the model and I do not claim it does.

Separately, on net-new ARR in dollars (a real, sourced management figure, not a cross-check construction): Adobe's CFO guided FY2026 total-Adobe-ARR growth of 10.2% on a $25.66bn opening book, i.e. ~$2.6bn of net-new ARR, of which ~$480M is acquired Semrush ARR (`primary_sources/2Q2026/earnings_call_transcript.md`, line 322). That is flat in dollars against the $2.62bn added in FY2024 and $2.59bn in FY2025 (`fetched_docs/adbe_q4fy23_datasheet.md`, `fetched_docs/adbe_q4fy25_datasheet.md`), so **organic net-new ARR steps down ~18% to ~$2.1bn** even as the headline percentage is held. This is a useful sense-check on the plausibility of the revenue build, but I do not present it as an independent second forecast for FY2027–FY2030: I have no disclosed source for Adobe's ARR growth in those years, so extending it further would just be restating the revenue assumptions in a different unit.

---

## 9. What I am confident about, and what I am not

**High confidence (computed from filings; arithmetic checked):**

- The historical decomposition: Creative $10,894M, DX $5,409M, BP&C $6,495M, P&A $106M in FY2025, tying exactly to total subscription revenue.
- The hosting/AI cost ratio deteriorated **61bp year-over-year in 1H FY2026** on an ex-purchased-intangible-amortisation basis, and reported gross margin masked it because amortisation inside cost of revenue fell from $85M to $17M. This is disclosed arithmetic, not an estimate.
- Net-new Total Adobe ARR was flat in dollars at ~$2.6bn across FY2024 and FY2025, and the FY2026 organic figure steps down ~18% to ~$2.1bn.
- Depreciation and maintenance capex net to approximately zero; capital intensity is not a driver for Adobe.
- FY2025 owners' earnings of $7,119M, which the model reproduces exactly.

**Moderate confidence (sourced, requiring judgment):**

- Creative volume growth decaying 7.8% → 3.0%. Defensible from the BLS designer-employment decline and competitor scale, but the range is wide.
- BP&C MAU growth decaying 18% → 6%. The direction is near-certain; the pace is not.
- The advertising path peaking at ~6.95% of revenue in FY2027 and normalising. Management has explicitly refused to cap this spend.
- The hosting cost drift decaying from 72bp to 20bp per year. Both directions are well evidenced and I have taken the middle.
- The 21% normalised tax rate, carried over unchanged from the owners' earnings work product.

**Genuinely uncertain — these decide the answer:**

1. **Free-to-paid conversion.** Never disclosed. The entire freemium thesis, and the whole of driver 2, rests on a rate I can only infer as a composite with price. If conversion on the incremental 150M free MAU is materially worse than on the base — which it plausibly is, since Adobe routed them there deliberately — revenue per MAU falls faster than modelled for longer.
2. **Whether generative AI substitutes creative workflows rather than augmenting them.** Adobe Stock is the one measured instance and it is modest (4–5% decline on 1.7% of ARR), but it establishes the mechanism and it surprised management. Photoshop and Premiere workflows are far more defended, and I cannot resolve from any available source whether that defence holds for five years. This is what the 15%-weighted severe scenario is for, and it is the reason the probability-weighted answer (6.7%) sits well below the base case (8.6%).
3. **Whether inference unit-cost deflation outruns Adobe's deliberate volume expansion.** The evidence genuinely cuts both ways and I have shown both sides in §6. My model says it matters less than people think (±5% on FY2030 owners' earnings across a wide parameterisation) — but that conclusion depends on hosting being a modest share of a line that is only ~8–10% of subscription revenue, and Adobe does not disclose the split.
4. **Leadership.** Narayen announced his transition in March 2026 and no successor had been named as of August 2026; CFO Dan Durn left on June 15 2026 with Steve Day interim (Knowledge Store IDs 8, 11, 14, 29, 44; `primary_sources/2Q2026/earnings_call_transcript.md`). An incoming CEO inherits an unfinished, margin-dilutive, ARR-dilutive freemium pivot they did not choose, at the exact point its payback is supposed to land. A reversal would move advertising intensity, ARR guidance and the buyback simultaneously. **This is unknowable from any available source and is not modelled in any scenario** — flagged as speculation, and as a reason to treat all five years beyond FY2027 as scenario ranges rather than forecasts.

**What would change my mind fastest.** Q3 FY2026 reports September 10 2026 (Knowledge Store ID 27). Three things in it are diagnostic: (i) cost of subscription revenue net of the disclosed amortisation, which is the first quarter with the re-routed freemium traffic; (ii) organic ARR growth ex-Semrush; (iii) whether the deferred Creative Cloud price optimisations are reinstated for FY2027.

---

*Calculations: `work_products/forecast_earnings_calcs.py`. Inputs traced to `primary_sources/FY2025/`, `primary_sources/2Q2026/`, the Q4 FY2025 / Q1 FY2026 / Q2 FY2026 earnings call transcripts, `work_products/owners_earnings_and_roic.md`, `work_products/causal_model.md`, `fetched_docs/`, and the Knowledge Store.*
