# Adobe Inc. (ADBE) — Terminal Value at the End of FY2030

*Prepared 2026-08-31. All arithmetic is in `work_products/terminal_value_calcs.py` (run with `uv run python work_products/terminal_value_calcs.py`). The earnings base is `work_products/forecast_earnings.md`; the quality and capital inputs are `work_products/owners_earnings_and_roic.md`; the qualitative evidence is `primary_sources/` (FY2025 10-K, Q2 FY2026 10-Q, and the Q4 FY2025 / Q1 FY2026 / Q2 FY2026 earnings calls); market and peer multiples are from `fetched_docs/` as of August 31 2026. Terminal value is stated **undiscounted** and **in aggregate** — no present value, no per-share figures, both explicitly out of scope for this step.*

---

## 1. Answer first

| Scenario                  | Probability | FY2030E owners' earnings | Terminal multiple | Terminal value | Share of weighted TV |
|---------------------------|-------------|--------------------------|-------------------|----------------|----------------------|
| SEVERE                    | 15%         | $6,022M                  | 7×                | $42.2bn        | 4%                   |
| BEAR                      | 25%         | $8,105M                  | 11×               | $89.2bn        | 15%                  |
| BASE                      | 40%         | $10,745M                 | **15×**           | **$161.2bn**   | 43%                  |
| BULL                      | 20%         | $13,035M                 | 22×               | $286.8bn       | 38%                  |
| **Probability-weighted**  |             | **$9,835M**              | **15.3×**         | **$150.4bn**   |                      |

*(Computed, `terminal_value_calcs.py` §4. FY2030E owners' earnings and the probability weights are taken unchanged from `work_products/forecast_earnings.md` §1. The four terminal multiples are my judgment; §5–§6 below is the entire justification.)*

**The headline: a terminal multiple of 15× on base-case FY2030 owners' earnings of $10.7bn, giving a terminal enterprise value of ~$161bn. Probability-weighting across the four scenarios gives ~$150bn, an implied blended 15.3×.**

Three things about that answer matter more than the number itself.

**First, 15× is not a premium multiple — it is roughly what Adobe trades at today.** At $116.28bn of market capitalisation on August 31 2026 (`fetched_docs/adbe_statistics_aug2026.md`), Adobe is at 15.0× its own FY2026E owners' earnings and 16.3× FY2025 actual (computed, §1). Applying 15× in FY2030 says: *the disruption question that has cut Adobe's P/E from 40.9× (FY2024) to 16.7× (today) is still unresolved in FY2030.* That is a deliberately unheroic assumption and I defend it in §6.

**Second, I apply a different multiple in each scenario rather than one multiple to blended earnings.** Earnings and multiple are positively correlated: the world in which FY2030 owners' earnings are $6.0bn is also the world in which the market pays 7× for them, not 15×. Applying a single 15× to the probability-weighted $9,835M would give $147.5bn — only 1.9% away from the correct answer here (computed, §4), so in this instance the shortcut happens not to matter much. But it understates the *spread*, and the spread is the honest content of this document.

**Third, and least comfortable: 38% of the probability-weighted terminal value comes from the 20%-probability bull case** (computed, §4). The weighted answer is therefore more fragile to the right tail than to the left. Cutting the bull multiple from 22× to 18× takes the weighted terminal value down 6.9% to $140.0bn (computed, §6b). I flag this rather than bury it.

---

## 2. What the multiple is being applied to, and what the product is

The earnings base is **owners' earnings as constructed in `work_products/owners_earnings_and_roic.md` §2** — EBIT, plus purchased-intangible amortisation, plus PP&E depreciation, less maintenance capex, taxed at a normalised 21%. Three properties follow, and each governs how the multiple must be read:

1. **It is unlevered.** Interest expense and interest income sit below the operating line and are excluded (`work_products/owners_earnings_and_roic.md` §2). So **multiple × owners' earnings is an *enterprise* value, not an equity value.** The bridge to equity is a net-debt adjustment at FY2030, deferred to the valuation step (see §10).
2. **Stock-based compensation is fully expensed inside it** ($2,892M in FY2030E, 27% of base-case owners' earnings — computed, §5). No add-back, so no double-count and no need to haircut the multiple for dilution economics.
3. **Purchased-intangible amortisation is added back**, with the corresponding goodwill and intangibles left in invested capital (`work_products/owners_earnings_and_roic.md` §2.1).

**Is an owners'-earnings multiple comparable to a peer P/E?** For Adobe specifically, almost exactly. TTM owners' earnings of $7,490M (`work_products/owners_earnings_and_roic.md` §1) are only +3.6% above TTM GAAP net income of $7,230M (`fetched_docs/adbe_statistics_aug2026.md`); the two add-backs and the tax normalisation nearly cancel (computed, §1). The implied P/E from those inputs is 16.1× against the 16.67× stockanalysis.com reports — a 3% gap, consistent with using a period-average versus a spot share count. **So peer trailing P/Es can be read against my owners'-earnings multiples directly, without a conversion factor.** One caveat I will not paper over: this equivalence is Adobe-specific. For amortisation-heavy peers (Salesforce, Oracle), owners' earnings would exceed GAAP net income by more, so their *owners'-earnings* multiples would sit somewhat **below** their quoted P/Es. Peer P/Es are therefore a mildly generous anchor, and I have leaned against them accordingly.

---

## 3. Quality and competitive position — the strong leg

### 3.1 The business consumes no net capital, and that is the single most important quality fact

`work_products/owners_earnings_and_roic.md` §1 computes ROIC of **69.7% (FY2025) and 72.0% (TTM to Q2 FY2026)** on owners' earnings over average invested capital, with a conservative floor of 43–45% after adding the present value of hosting commitments to capital. More striking: **invested capital excluding acquisition goodwill is negative — −$3.9bn at Q2 FY2026** — because the deferred-revenue float ($7,250M) alone very nearly covers all operating assets outside goodwill and intangibles ($7,461M). An independent third-party calculation on a conventional definition agrees on the order of magnitude: ROIC of 60.74% currently and 59.33% in FY2025 (`fetched_docs/adbe_ratio_history_aug2026.md`).

Why this matters for a *multiple* and not just as a compliment: in a Gordon framework, value/earnings = (1 − g/ROIC)/(r − g). At ROIC of 70% and g of 3%, the reinvestment drag is 1 − 0.03/0.70 = **0.957** — about 96% of owners' earnings are genuinely distributable (computed, §3). A capital-hungry business growing at the same rate would be worth materially less per dollar of earnings. It also means, as `work_products/owners_earnings_and_roic.md` §1 concludes, that **ROIC is not the binding constraint on Adobe's growth**; demand and competition are.

Supporting margin evidence: gross margin 89.40%, operating margin 36.72%, FCF margin 40.80%, revenue per employee $803,508 on 31,360 employees (`fetched_docs/adbe_statistics_aug2026.md`).

### 3.2 The moat, stated as Adobe itself states it — which is thinner than the reputation

Adobe's own description of its advantage is integration and brand, not switching cost:

> "Our competitive differentiation comes from the increased value we provide customers by integrating the Adobe Experience Platform with our comprehensive set of solutions and embedding AI into our portfolio of solutions" — `primary_sources/FY2025/business.md`

> "we offer customers choice and flexibility without the friction of switching between workflows and platforms" — `primary_sources/FY2025/business.md`

Management's framing on the calls is more forceful and rests on data and workflow:

> "I think as it relates to differentiation, we always talk about content and the fact that we have these behaviors and we have the data as a huge differentiator for us." — Shantanu Narayen, CEO, `primary_sources/2Q2026/earnings_call_transcript.md`

> "It also is based on a complete confidence that we have that the Creative business is extremely stable. The amount of innovation that we have delivered in that space continues to make us a category of one as it relates to our focus on that particular market." — Shantanu Narayen, `primary_sources/2Q2026/earnings_call_transcript.md`

**But Adobe's own 10-K describes its markets in terms that are close to the opposite of a moat:**

> "The markets for our solutions are characterized by rapid technological innovation, new industry standards, evolving distribution and sales models, **limited barriers to entry**, short product lifecycles, customer price sensitivity, global economic conditions and the frequent entry of new solutions or competitors." — `primary_sources/FY2025/business.md` (emphasis added)

That is a company telling its shareholders, in its own competition section, that entry barriers in its markets are limited. I weight this heavily. Note also that neither the FY2025 10-K business section nor the risk factors invoke PDF's ISO standing or file-format lock-in as a barrier — a widely repeated moat argument for Adobe that its own filings do not make. Anyone using it is inferring, not citing.

There is one live regulatory item pointed the other way on switching costs: Adobe flags that "there may be certain aspects of the EU's Data Act that could apply to certain types of cloud services providers and require them to facilitate data portability (e.g., switching between services)" (`primary_sources/2Q2026/risk_factors.md`). A mandated data-portability regime is a direct erosion of whatever lock-in exists.

### 3.3 What genuinely is durable: distribution and installed base

The strongest evidence is scale of reach, and it is disclosed and growing:

- "Acrobat and Express MAU surpassed 850 million, growing approximately 20% year-over-year" — Steve Day, CFO-CXO BU, `primary_sources/2Q2026/earnings_call_transcript.md`
- "Our Acrobat solutions, from our freemium Acrobat Reader to Acrobat AI Assistant to our AI-powered productivity and creativity destination, Acrobat Studio, facilitate frictionless onboarding and scaled reach in serving the billions of potential users in this customer group." — `primary_sources/FY2025/business.md`
- "nearly 50% of Acrobat commercial ETLAs renewed in Q4 already upgrading to this offering" — David Wadhwani, `primary_sources/4Q2025/earnings_call_transcript.md`
- No customer-concentration risk factor appears in either the FY2025 10-K or the Q2 FY2026 10-Q risk factors — the revenue base is genuinely diversified.

**Verdict on quality: unambiguously high, and the capital-efficiency evidence is arithmetic rather than assertion. This leg alone would support a multiple well above 15×.**

---

## 4. Durability and predictability — the weak leg, and the one that sets the multiple

### 4.1 Near-term predictability is excellent, and is disclosed

Adobe is ~96–97% ratable subscription revenue (`primary_sources/FY2025/md_and_a.md`; `work_products/owners_earnings_and_roic.md` §2.1):

> "We generally recognize revenue from our subscription solutions ratably over the terms of their subscription agreements, which typically range from 1 to 36 months. As a result, most of the subscription revenue we report each quarter is the result of subscription agreements entered into during previous quarters." — `primary_sources/FY2025/risk_factors.md`

Remaining performance obligations were **$22.27bn at May 29 2026, up 13% from $19.69bn**, with cRPO also growing 13% (`primary_sources/2Q2026/md_and_a.md`; Steve Day, `primary_sources/2Q2026/earnings_call_transcript.md`). Total Adobe ARR was $27.10bn, +12.5% (same sources). A sell-side analyst characterised the visibility on the Q1 FY2026 call, unchallenged by the CFO:

> Jay Vleeschhouwer (Griffin Securities): "over the last number of years, we've seen that cRPO has fairly consistently been somewhere around 51%, 52% of your estimated next 12 month revenue on a rolling quarterly basis." — `primary_sources/1Q2026/earnings_call_transcript.md`

`work_products/forecast_earnings.md` §8(a) independently corroborates the mechanical stability of the ARR-to-revenue conversion: a constant K ≈ 0.953 reproduced across two separately measured years.

**But Adobe itself notes that this predictability cuts both ways:**

> "Lower sales and subscriptions, reduced demand for our solutions, and increases in our attrition rate in any given period may not be fully reflected in our results of operations until future periods." — `primary_sources/FY2025/risk_factors.md`

Ratable recognition means a deterioration in the underlying franchise arrives in reported revenue with a two-quarter-plus lag. For a *one-year* forecast that is comfort. For a *terminal* multiple it is the opposite: it means the reported numbers I can observe today are the weakest possible evidence about FY2030.

### 4.2 What is NOT disclosed, and it is the thing that matters most

**Adobe discloses no net revenue retention rate, no churn rate, and no free-to-paid conversion rate.** Across three earnings calls and two MD&As the strongest retention statement is a formulaic, repeated phrase — "continued strength in retention across the enterprise customer base" (Dan Durn, `primary_sources/1Q2026/earnings_call_transcript.md`; identically Steve Day, `primary_sources/2Q2026/earnings_call_transcript.md`). `work_products/forecast_earnings.md` §9 lists free-to-paid conversion as its number-one unresolvable uncertainty.

This is a real handicap on the terminal multiple. Figma, the smaller competitor, *does* disclose: net dollar retention of **136%** in Q2 2026 (`fetched_docs/figma_q2_2026_results.md`; Knowledge Store ID 16). A durability premium has to be earned with evidence, and here the evidence is qualitative assertion.

### 4.3 Five pieces of hard evidence that the terminal franchise is under real threat

These are the reasons the terminal multiple is 15× and not 25×.

**(a) The professional seat pool is projected to shrink over exactly the terminal horizon.** The US Bureau of Labor Statistics projects employment of graphic designers to **decline 2% from 2025 to 2035** (Knowledge Store ID 35; `fetched_docs/bls_ooh_graphic_designers.md`). Creative unit growth beyond FY2030 cannot come from the professional population.

**(b) AI substitution of an Adobe revenue line is already measured, not hypothetical.** Adobe Stock — a ~$450M book — is declining roughly 4–5% year-over-year, and management conceded it "saw a steeper decline than we expected" (`work_products/causal_model.md` §1.6). And Adobe recorded a **goodwill impairment on the Publishing & Advertising reporting unit in Q2 FY2026** — "In the second quarter of fiscal 2026, we recorded a goodwill impairment charge related to our Publishing & Advertising reporting unit" (`primary_sources/2Q2026/risk_factors.md`) — a realised, audited write-down of a legacy franchise, not a risk factor. The market's terminal verdict on a fully AI-substituted content franchise is visible in Shutterstock: market capitalisation of $210M on revenue of $901M, **0.23× sales**, after a −70% year (`fetched_docs/peer_multiples_disruption_set_2026.md`).

**(c) Adobe's own risk-factor language on AI disintermediation strengthened materially between the FY2025 10-K and the Q2 FY2026 10-Q.** The FY2025 formulation ends at "purpose-built AI agents"; the Q2 FY2026 version extends it to "purpose-built AI agents **and AI-enabled workflows, some of which are embedded within or operating across third-party AI platforms or domain-specific solutions**" (`primary_sources/2Q2026/risk_factors.md` vs `primary_sources/FY2025/risk_factors.md`). The same edit adds that AI is "**transforming how digital work is performed or automated and how, and the extent to which, our solutions are accessed and used**". The company is escalating, in its own words, the risk that agents embedded in *other* platforms route around Adobe's applications entirely.

**(d) Credible, scaled, free or near-free substitutes exist.** Canva: $4bn ARR at end-2025, 265M MAU, 31M paid users, B2B book of $500M growing 100% (`fetched_docs/canva_4b_revenue_techcrunch.md`; Knowledge Store ID 15), and it made the Affinity professional suite free (`fetched_docs/canva_42b_redomicile_2026.md`; Knowledge Store ID 23). Figma: revenue +48% to $370.1M in Q2 2026, FY2026 guidance $1.463–1.467bn (`fetched_docs/figma_q2_2026_results.md`). These are growing several times faster than Adobe from bases still small relative to Adobe's ~$10.9bn Creative line (`work_products/forecast_earnings.md` §4) — but compounding at 40–100% closes that gap inside the terminal horizon.

**(e) Pricing power has, at minimum, been deferred.** "we have made the decision to defer previously planned Creative Cloud second half line optimizations" — Narayen, `primary_sources/2Q2026/earnings_call_transcript.md`. Management frames it as "a phase shift... we're deferring it, but not closing it" and asserts it is a choice made from strength. An analyst put the cost at roughly "$0.5 billion adjustment to the organic ARR downward" (Alex Zukin, Wolfe Research, same call), which management did not dispute. Whether this is confidence or constraint is genuinely undecidable from the sources, and I have not resolved it.

### 4.4 Two further items that widen the terminal distribution

**Leadership.** Narayen announced his transition in March 2026 with no successor named as of August 2026, and CFO Dan Durn departed June 15 2026 with Steve Day interim (Knowledge Store IDs 8, 11, 14, 29, 44; `primary_sources/2Q2026/earnings_call_transcript.md`). An incoming CEO inherits an unfinished, margin-dilutive, ARR-dilutive freemium pivot at the point its payback is supposed to land. `work_products/forecast_earnings.md` §9 flags this as unmodelled in every scenario. It is a variance-widener, not a directional adjustment — I have not tried to price it beyond letting the scenario spread carry it.

**No long-term financial model exists to anchor to.** Across three calls and two MD&As, management gives only single-fiscal-year operating-margin targets (~45% non-GAAP for FY2026 — Steve Day, `primary_sources/2Q2026/earnings_call_transcript.md`). There is no multi-year margin roadmap. So the FY2030 margin in the forecast is my construction, not a company-anchored figure.

**Verdict on durability: near-term predictability is high and disclosed; five-year-plus durability is contested, undisclosed on the metrics that would settle it, and has already failed once inside Adobe's own portfolio. This leg caps the multiple.**

---

## 5. Peer trading multiples

All figures below are trailing P/E as of August 31 2026 from `fetched_docs/peer_multiples_compare_2026.md` and `fetched_docs/peer_multiples_disruption_set_2026.md` (stockanalysis.com). Per §2, these read directly against owners'-earnings multiples for Adobe, with the mild caveat noted there.

| Comparable set                       | Constituents                     | Trailing P/E                                        |
|--------------------------------------|----------------------------------|-----------------------------------------------------|
| Mature large-cap software            | MSFT, SAP, ORCL, CRM, INTU, ADSK | median **27.2×**, range 21.8× (INTU) – 33.8× (ADSK) |
| Ex-growth / disruption-discounted    | DBX, ZM, DOCU, GEN               | median **18.8×**, range 9.0× (ZM) – 41.6× (DOCU)    |
| AI-substituted content franchise     | SSTK                             | no P/E (loss-making); **0.23× sales**               |
| **ADBE today**                       |                                  | **16.67×**                                          |

*(Computed, §2. Individual constituents: MSFT 28.61×, SAP 28.77×, ORCL 25.87×, CRM 23.72×, INTU 21.75×, ADSK 33.78×; DBX 19.65×, ZM 9.01×, DOCU 41.56×, GEN 18.03×.)*

Three readings, and I think all three are true simultaneously:

**Adobe already trades at a 39% discount to the mature-software median** (16.67× vs 27.2×, computed §2), and *below* the median of the ex-growth/disrupted cohort. The market is not waiting for me to discover the disruption risk; it has priced a substantial amount of it. Corroborating the direction of sentiment: the street mean price target compressed "from $565 at the start of 2025 to around $327" and the consensus rating is Hold, with Morgan Stanley moving to Underweight in July 2026 on "concerns over Adobe's shift toward free-tier offerings, leadership uncertainty, elevated AI investments, and intensifying competition from AI-native rivals" (Knowledge Store IDs 43, 9).

**The de-rating has been violent and recent.** Adobe's own fiscal-year-end P/E: 60.8× (FY2021), 33.4× (FY2022), 51.4× (FY2023), 40.9× (FY2024), 18.8× (FY2025), 16.7× today — a **59% de-rating from the FY2021–FY2025 median of 40.9×** (computed, §2; `fetched_docs/adbe_ratio_history_aug2026.md`). Two implications pull opposite ways: the current multiple is *not* a stable, long-tested anchor, so anchoring the terminal multiple to it is anchoring to the low end of a fast-moving series; but equally, the speed of the fall is evidence of how quickly a franchise multiple can go when the durability question opens.

**The single closest comparable argues for a higher multiple than I have used.** Autodesk — professional design software, subscription model, high workflow embedding, similar customer type — trades at **33.78×**, the highest in the mature set. If Adobe's disruption question resolves favourably, 22× in the bull case is conservative against that anchor. That is the main reason I did not cut the bull multiple further.

Two peer figures I deliberately did **not** use as anchors: Canva's $42bn private secondary-market valuation (Knowledge Store ID 21) and Figma's $14.76bn market capitalisation on ~$1.28bn of revenue with no P/E (`fetched_docs/peer_multiples_disruption_set_2026.md`; Knowledge Store ID 25). Both are high-growth, largely pre-profit assets valued on revenue; mapping them onto a mature-franchise earnings multiple would require stacked assumptions for no gain in accuracy.

---

## 6. Choosing the four multiples

### 6.1 The perpetuity cross-check

Before judgment, a discipline: what multiple does a simple Gordon perpetuity imply, given Adobe's ~70% ROIC? Value/OE = (1 − g/ROIC)/(r − g) (computed, §3):

| g \ r | 8.0%  | 9.0%  | 10.0% | 11.0% |
|-------|-------|-------|-------|-------|
| −3%   | 9.5×  | 8.7×  | 8.0×  | 7.4×  |
| 0%    | 12.5× | 11.1× | 10.0× | 9.1×  |
| +1%   | 14.1× | 12.3× | 11.0× | 9.9×  |
| +2%   | 16.2× | 13.9× | 12.1× | 10.8× |
| +3%   | 19.1× | 16.0× | 13.7× | 12.0× |
| +4%   | 23.6× | 18.9× | 15.7× | 13.5× |

This is a *cross-check*, not the method — the brief asks for a multiple, and a multiple grounded in observable peer trading is more honest than a perpetuity built on an unobservable discount rate. But it disciplines the range. Note that a third-party WACC estimate for Adobe is 11.53% with a 5-year beta of 1.42 (`fetched_docs/adbe_statistics_aug2026.md`); I regard 11.5% as too high for a company with 89% gross margins, no net capital employed and only $1.45bn of net debt, and I use 8–10% as the plausible band. **Assumption, flagged.**

### 6.2 The four multiples, and the reasoning behind each

| Scenario | Multiple | Post-FY2030 world it prices                  | Anchors used                                                                                        |
|----------|----------|----------------------------------------------|-----------------------------------------------------------------------------------------------------|
| SEVERE   | 7×       | Terminal decline; AI substitutes the workflow | Gordon at g = −3%, r = 10% → 8.0×. Market precedent: ZM 9.0×; SSTK 0.23× sales after a −70% year.     |
| BEAR     | 11×      | Grinding share loss; ~0–1% perpetual growth   | Gordon at g = 0–1%, r = 9–10% → 10.0×–12.3×. Floor cohort DBX 19.7×, GEN 18.0×, ZM 9.0×.              |
| BASE     | 15×      | ~3% perpetual growth; question still open     | Gordon at g = 3%, r = 9% → 16.0×. Adobe's own current 15.0× on FY2026E owners' earnings.              |
| BULL     | 22×      | Franchise durable; AI is net accretive        | Gordon at g = 4%, r = 8.5% ≈ 21×. Mature-software median 27.2×; ADSK 33.8×. Set **below** both.       |

*(Gordon values computed, §3. Peer figures computed/quoted, §2. The multiples themselves are ANALYST JUDGMENT.)*

**Why 15× and not the peer median of 27× in the base case.** In the base case FY2030 owners' earnings are growing 6.9% and decelerating, revenue 5.7% and decelerating (`work_products/forecast_earnings.md` §1). Beyond FY2030 the BLS designer-employment decline (Knowledge Store ID 35) and the MAU deceleration the forecast already builds in imply a perpetual growth rate nearer 3% than 5%. At g = 3% and r = 9% the perpetuity says 16.0×. Independently, the peer set says a durable mature software franchise gets ~27× and one with an open disruption question gets 9–19×. **The base case is definitionally the world where the question is neither resolved nor realised, so 15× — near today's actual and between the two peer cohorts — is the internally consistent choice.**

**Why not higher on the strength of the quality leg.** Adobe's ROIC and negative ex-goodwill invested capital genuinely justify a premium. But a high ROIC on a *shrinking* earnings stream is worth very little; capital efficiency multiplies durability, it does not substitute for it. The durability leg (§4) is where the evidence is weakest, and it binds.

**Why not lower on the strength of the threat evidence.** Because Adobe's price already contains a 39% discount to peers and a 59% de-rating from its own five-year median (computed, §2). Cutting further would be double-counting the same fear that produced today's price.

---

## 7. Cross-checks on the base-case terminal value

If the base terminal value of $161.2bn is right, it should look sensible on metrics I did not use to build it (computed, §5):

| Implied at FY2030 on base-case financials | Base TV implies | ADBE today (`fetched_docs/adbe_statistics_aug2026.md`) |
|-------------------------------------------|-----------------|--------------------------------------------------------|
| EV / revenue                              | 4.57×           | 4.64×                                                  |
| EV / EBITA                                | 11.85×          | EV/EBIT 12.65×; EV/EBITDA 12.03×                       |
| Owners' earnings yield                    | 6.7%            | earnings yield 6.26%; FCF yield 8.90%                  |

All three land within a few percent of today's trading levels. **That is the plainest possible statement of what the base case assumes: Adobe in FY2030 is valued on the same terms the market applies in August 2026 — a bigger, slower business at an unchanged multiple.** It is a coherent, testable claim rather than a hopeful one.

Two honesty caveats on this table. **It is a consistency check, not independent confirmation** — I chose the base multiple partly by reference to today's level, so these three ratios largely reproduce that choice on different denominators. Their real value is confirming that the FY2030 *earnings* forecast and the FY2030 *multiple* do not contradict each other: the forecast's margin path does not silently require a multiple I have not justified. And separately, `work_products/forecast_earnings.md` §8 uses "market capitalisation held at 15× owners' earnings" as an *input* to its buyback share-count arithmetic. My arriving at 15× here is therefore **not** independent corroboration of that assumption — it is the same anchor (Adobe's actual trading level) used twice. The useful consequence is only that the two work products do not contradict each other.

---

## 8. Sensitivity — what moves the answer

Computed, §6:

| Change                                                       | Weighted terminal value | Δ      |
|--------------------------------------------------------------|-------------------------|--------|
| **Base case as stated**                                       | **$150.4bn**            | —      |
| Base multiple 12× (rest held)                                 | $137.5bn                | −8.6%  |
| Base multiple 18× (rest held)                                 | $163.3bn                | +8.6%  |
| Bull multiple 18× (rest held)                                 | $140.0bn                | −6.9%  |
| Bull multiple 27× (= peer median, rest held)                  | $163.5bn                | +8.7%  |
| All four multiples ×0.8                                       | $120.3bn                | −20.0% |
| All four multiples ×1.2                                       | $180.5bn                | +20.0% |
| Pessimist's weights (SEVERE 25 / BEAR 25 / BASE 30 / BULL 20) | $138.5bn                | −7.9%  |
| Optimist's weights (SEVERE 10 / BEAR 20 / BASE 40 / BULL 30)  | $172.5bn                | +14.7% |

**Reading this honestly: the defensible range for the FY2030 terminal enterprise value is roughly $120–180bn.** That is ±20%, and it is driven almost entirely by the multiple, because the earnings spread is already inside the scenario weights. No single input moves the answer more than about 9% on its own. The larger risk is correlated error — if my four multiples are systematically too generous by 20%, the answer is $120bn.

Note that the table understates the true left tail, because the scenario multiples and the scenario earnings were chosen consistently. If AI substitution runs faster than the severe case, both fall together and $42bn is not the floor.

---

## 9. What I am confident about, and what I am not

**Confident (computed from filings and observable market data):**

- Adobe trades at 15.0× FY2026E owners' earnings / 16.3× FY2025 actual as of August 31 2026, and at a 39% discount to the mature-software peer median of 27.2× (computed, §1–§2).
- Adobe's P/E has de-rated 59% from its FY2021–FY2025 median of 40.9× (`fetched_docs/adbe_ratio_history_aug2026.md`).
- Owners' earnings and GAAP net income are within 3.6% for Adobe, so peer P/Es are directly readable against my multiples (computed, §1).
- ROIC of ~70% makes the reinvestment drag on value negligible (~4% at g = 3%) and is not a growth constraint (computed, §3; `work_products/owners_earnings_and_roic.md` §1).
- The product of multiple and owners' earnings is an **enterprise** value; net debt today is $1.45bn and the FY2026–FY2030 buyback plan is ~93% funded out of cumulative owners' earnings, so FY2030 net debt should remain immaterial (~1%) against a ~$150bn enterprise value (computed, §7 of the script). *Approximate — ignores cash interest and cash-vs-normalised-tax timing.*

**Genuinely uncertain — these decide the answer:**

1. **The base multiple of 15× itself.** It is judgment anchored to Adobe's current price. If the market is currently mispricing Adobe — in either direction — that error propagates straight into my terminal value. I have no way to resolve this and I do not claim to.
2. **The bull multiple of 22×, because it carries 38% of the weighted value.** It is anchored to a peer median (27.2×) and to Autodesk (33.8×) — companies whose durability question is not open in the way Adobe's is. If the right comparison for a "resolved" Adobe is 18× rather than 22×, the weighted answer falls to $140.0bn.
3. **Whether generative AI substitutes creative workflows or augments them.** This is the same unresolved question that dominates `work_products/forecast_earnings.md` §9, and it now enters the answer *twice* — through FY2030 earnings and through the FY2030 multiple. That double-counting is deliberate and correct (the two really are correlated), but it means the terminal value is more sensitive to this one question than to anything else in the valuation.
4. **The absence of disclosed retention data.** I cannot verify the durability that a 15× multiple embeds. Figma discloses 136% net dollar retention; Adobe discloses nothing comparable. **A meaningful part of my base multiple rests on an undisclosed number.**
5. **Leadership.** No CEO named, CFO interim (Knowledge Store IDs 8, 14, 29, 44). Unmodelled in every scenario, here as in the forecast.

**What would change my mind fastest.** Q3 FY2026 reports September 10 2026 (Knowledge Store ID 27) — the first quarter reflecting the re-routed freemium traffic. If organic ARR ex-Semrush decelerates further, or the deferred Creative Cloud price optimisations are not reinstated for FY2027, weight should move from BASE toward BEAR, which on the pessimist's weights takes the terminal value to ~$138bn.

---

## 10. Handoff notes for the valuation step

1. **$150.4bn (weighted) / $161.2bn (base) is an ENTERPRISE value at FY2030, undiscounted.** Subtract FY2030 net debt to reach equity value. Per §9, net debt is likely of the same order as today's $1.45bn — but that depends on the buyback throttling to ~90% of owners' earnings as `work_products/forecast_earnings.md` §8 assumes. If Adobe keeps repurchasing at the FY2024–FY2025 pace of ~1.5× owners' earnings, FY2030 net debt will be materially larger and the equity bridge stops being immaterial.
2. **Do not re-apply a scenario probability weighting.** The $150.4bn figure is already probability-weighted. Discounting it at a single rate and adding it to a probability-weighted interim cash-flow stream is the consistent next step.
3. **Do not blend the multiple and the earnings separately.** Multiplying a weighted multiple by weighted earnings loses the earnings–multiple correlation; it happens to cost only 1.9% here (computed, §4) but the structure is wrong and will not stay small under different weights.
4. **Per-share figures are deliberately absent**, and not only because they are out of scope: FY2030 share count depends on the buyback path *and* on the price at which shares are retired — which is a function of the multiple being solved for. Doing it here would be circular.

---

*Calculations: `work_products/terminal_value_calcs.py`. Inputs traced to `work_products/forecast_earnings.md`, `work_products/owners_earnings_and_roic.md`, `work_products/causal_model.md`, `primary_sources/FY2025/`, `primary_sources/2Q2026/`, the Q4 FY2025 / Q1 FY2026 / Q2 FY2026 earnings call transcripts, `fetched_docs/adbe_statistics_aug2026.md`, `fetched_docs/adbe_ratio_history_aug2026.md`, `fetched_docs/peer_multiples_compare_2026.md`, `fetched_docs/peer_multiples_disruption_set_2026.md`, `fetched_docs/figma_q2_2026_results.md`, `fetched_docs/canva_4b_revenue_techcrunch.md`, `fetched_docs/canva_42b_redomicile_2026.md`, `fetched_docs/bls_ooh_graphic_designers.md`, and the Knowledge Store.*
