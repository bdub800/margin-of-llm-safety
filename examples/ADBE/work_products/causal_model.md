# Adobe Inc. (ADBE) — Causal Model of the Business

*Prepared 2026-08-28. Sources: Adobe FY2025 Form 10-K (`primary_sources/FY2025/business.md`, `md_and_a.md`, `financial_statements.md`, `risk_factors.md`), Q2 FY2026 Form 10-Q (`primary_sources/2Q2026/md_and_a.md`, `financial_statements.md`, `risk_factors.md`), and the Q4 FY2025 / Q1 FY2026 / Q2 FY2026 earnings call transcripts (`primary_sources/4Q2025/`, `1Q2026/`, `2Q2026/`), plus `work_products/overview.md`. Every number below is either quoted from those sources or computed in `work_products/causal_model_calcs.py`. Most recent primary source is the Q2 FY2026 10-Q and the June 11, 2026 call; nothing here reflects Q3 FY2026, which had not been reported as of this writing (Knowledge Store ID 9).*

---

## 0. The spine of the model — read this first

Adobe is not a "software revenue" business in the causal sense. It is a **stock-and-flow business**: a stock of contracted annual recurring revenue that is released into the income statement ratably, plus a flow of net-new ARR added each period.

> "We generally recognize revenue from our subscription solutions ratably over the terms of their subscription agreements, which typically range from 1 to 36 months. As a result, most of the subscription revenue we report each quarter is the result of subscription agreements entered into during previous quarters." (`primary_sources/FY2025/risk_factors.md`)

Subscription was 96% of FY2025 revenue and 97% of Q2 FY2026 revenue (`primary_sources/FY2025/md_and_a.md`; `primary_sources/2Q2026/md_and_a.md`). So the causal chain is:

```
top-of-funnel traffic ──► MAU (free) ──► free-to-paid conversion ──► paid units
                                                                        │
                                        price / tier mix / credits ─────┤
                                        enterprise seat + cross-sell ───┤
                                        churn (negative) ───────────────┤
                                                                        ▼
                                                            NET-NEW ARR (the flow)
                                                                        │
                                                          + opening ARR (the stock)
                                                          + FX revaluation
                                                          + M&A (Semrush)
                                                                        ▼
                                                   ARR ──(ratable, ~1-3 qtr lag)──► NET REVENUE
```

Three consequences follow, and they organise everything below:

1. **Revenue is a lagging, smoothed function of ARR.** Q2 FY2026 revenue grew 13% while organic ARR grew ~10.5% (computed, `causal_model_calcs.py` §6). Reported revenue growth today is telling you about ARR decisions made two to six quarters ago. Anyone modelling Adobe off revenue growth is looking at the rear-view mirror.
2. **ARR itself is a *managed* variable, not just a market outcome.** Adobe can dial ARR up or down in the short run by choosing where to route web traffic and whether to run price optimisations. It did exactly that in FY2026 (§1.2, §1.3).
3. **Costs are increasingly *not* recognised ratably.** Advertising to fill the freemium funnel, and inference compute to serve free users, are incurred now; the ARR they produce arrives later. That timing mismatch — not gross margin erosion — is what is actually compressing operating margin right now (§3).

**The single most important structural fact I found:** on the Q4 FY2025 call, CFO Dan Durn disclosed that "*Over 75% of Digital Media net new ARR was driven by continued growth in subscriptions and cross-sell and upsell, with the remainder from value-based pricing*" (`primary_sources/4Q2025/earnings_call_transcript.md`, line 302). Applied to FY2025 Digital Media net-new ARR of $1.98B (computed from `primary_sources/FY2025/md_and_a.md`), that is **>$1.49B from volume/mix and <$0.50B from price** (computed, §6c). Adobe is roughly a three-quarters-volume, one-quarter-price growth engine. The FY2026 strategy pivot is, in essence, a deliberate decision to give up part of the price quarter to buy more of the volume three-quarters.

---

## Stage 1: Net revenues

FY2025 total revenue $23,769M (+11% YoY); Q2 FY2026 $6,618M (+13%); 1H FY2026 $13,016M (+12%) (`primary_sources/FY2025/md_and_a.md`; `primary_sources/2Q2026/md_and_a.md`).

### Factor 1.1 — Paid unit count (subscribers / seats). The dominant driver.

- **Mechanism.** Net revenue ≈ paid units × ARPU, recognised ratably. Because >75% of net-new ARR is volume rather than price (§0), paid-unit growth is the first-order revenue driver. Paid units are fed by a funnel: Adobe.com traffic → free MAU → conversion to paid.
- **Evidence.** Adobe does not disclose paid subscriber counts. It discloses the funnel inputs instead: Acrobat/Express MAU went "*from greater than 700 million to greater than 850 million year-over-year*" and creative freemium MAU "*from 50 million to 90 million year-over-year*" (Shantanu Narayen, `primary_sources/2Q2026/earnings_call_transcript.md`, lines 140, 156). CFO Steve Day gave the growth rates as "*approximately 20%*" and "*over 70%*" respectively (same transcript, lines 318, 320). Conversion evidence: "*Acrobat AI Assistant paid MAU grew over 150% year-over-year, and lifetime AI users in Acrobat tripled year-over-year*" (David Wadhwani, same transcript).
- **Direction of factor.** Sharply up, and accelerating — traffic to Adobe.com "*grew over 40% year-over-year*", with Creative traffic "*over 50%*" and BP&C traffic 35% (Wadhwani, `primary_sources/2Q2026/earnings_call_transcript.md`, lines 220, 232).
- **Direction of revenue.** Up, but **with a lag, and less than proportionally** — because the incremental MAU are free. This is the crux of the current investment debate. Free MAU adds cost today and revenue later, or never.
- **Confidence.** High on the MAU numbers (management-disclosed, consistent across three calls). **Low on the conversion rate**, which Adobe has never disclosed. This is the largest single unmeasurable in the model.

  - **Sub-factor 1.1a — Distribution surfaces.** Adobe licenses "*to end-user customers through app stores and our own website at adobe.com*" and distributes "*through sales channels, which include distributors, retailers, software developers, mobile app stores, systems integrators, independent software vendors and value-added resellers, as well as through original equipment manufacturers*" (`primary_sources/FY2025/business.md`). AI features have been pushed onto new surfaces: "*AI mode in Reader, Edge, Chrome, and WhatsApp*" (Narayen, `primary_sources/2Q2026/earnings_call_transcript.md`, line 140). Direction: expanding. Effect on revenue: positive on volume, but it introduces a **take-rate dependency** — "*We rely on third-party distribution platforms and are subject to changes in pricing structure, terms of service... at the discretion of the platform provider*" (`primary_sources/FY2025/risk_factors.md`). Adobe does not quantify app-store revenue share, so I cannot size this; flagged as unquantifiable.
  - **Sub-factor 1.1b — The Reader analogy.** Management's explicit thesis is that free Acrobat Reader built the paid Acrobat franchise over decades and freemium Firefly/Express will do the same: "*building on the success of the Adobe Reader model*" and "*like we've done with Reader, then pays off for decades*" (Narayen, `primary_sources/2Q2026/earnings_call_transcript.md`, lines 140, 526). **This is management's hypothesis, not evidence.** Flagged as an unproven analogy.

### Factor 1.2 — Funnel routing policy (a management choice, not a market variable)

- **Mechanism.** Adobe controls whether a visitor to adobe.com lands on a direct-to-paid page or a free product experience. Routing traffic to free suppresses near-term ARR and builds MAU.
- **Evidence.** Steve Day: the FY2026 ARR target "*now reflects both the addition of the Semrush book of business, as well as the strategic choice to accelerate MAU freemium growth and defer previously planned Creative Cloud line optimizations*" (`primary_sources/2Q2026/earnings_call_transcript.md`). Narayen split the effect roughly evenly: "*maybe half of the impact of ARR is as a result of what we are doing around deferring that Creative price line optimizations, and the other half is about going full steam on what it takes to deliver the freemium experience*" (same transcript, line 410).
- **Sizing — and this is where two independent methods agree.** On the Q4 FY2025 call, Durn guided FY2026 total-Adobe ARR growth to 10.2% and stated explicitly "*Our targets do not include any contribution from Semrush*" (`primary_sources/4Q2025/earnings_call_transcript.md`, line 332). At Q2 FY2026 the *same* 10.2% headline was reaffirmed, but now including Semrush's $480M of acquired ARR (`primary_sources/2Q2026/md_and_a.md`). Substituting: 10.2% on the $25.66B opening base = ~$2.62B of net-new ARR (ties to Durn's "*approximately $2.6 billion*"); less $480M of Semrush leaves **~$2.14B organic, i.e. ~8.3% implied organic ARR growth — an organic guidance cut of ~$480M, or ~1.9pp** (computed, `causal_model_calcs.py` §6b). Separately, Alex Zukin of Wolfe Research put it at "*about $0.5 billion adjustment to the organic ARR downward*" on the call, and Narayen did not dispute the figure (`primary_sources/2Q2026/earnings_call_transcript.md`, line 514). The two methods agree to within ~4%.
- **Direction of factor.** Newly and aggressively engaged, starting Q2 FY2026, with more to come: Narayen said the traffic changes would be made "*in Q3*" and would "*play out, I think, over 2027*."
- **Direction of revenue.** Negative near-term (roughly −$480M of FY2026 ARR, which flows into FY2026–FY2027 revenue with the ratable lag), intended positive later.
- **Correction to a prior work product.** `work_products/overview.md` states organic 1H FY2026 ARR growth was "~3.7%" and compares it to Adobe's double-digit growth history. That comparison is not valid: 3.7% is a *half-year sequential* figure being set against *year-over-year* rates. Adobe's net-new ARR is heavily H2-weighted — Narayen: H2 ARR "*typically pay out 40% and 60% in Q3 and Q4*" (`primary_sources/2Q2026/earnings_call_transcript.md`). The correct like-for-like series is **organic YoY ARR growth of 11.5% (FY2025 exit) → 10.9% (Q1 FY2026) → ~10.5% (Q2 FY2026)** (computed, `causal_model_calcs.py` §6). That is a ~100bp grind, not a collapse. The deceleration is real but the overview overstated it by roughly 3x.

### Factor 1.3 — Price and package mix (ARPU)

- **Mechanism.** Adobe rarely takes headline list-price increases. It raises realised ARPU by migrating users up a tier ladder — Creative Cloud → Creative Cloud Pro, Acrobat → Acrobat Studio — where the higher tier bundles more generative AI capacity. Durn calls this "*value-based pricing*."
- **Evidence.** FY2025 Digital Media subscription revenue growth was "*driven by strength in Creative Cloud Pro and other flagship apps as well as Acrobat*" (`primary_sources/FY2025/md_and_a.md`); Q2 FY2026 growth drivers include "*growth in Creative Cloud driven by the CC Pro offering*" (Steve Day, `primary_sources/2Q2026/earnings_call_transcript.md`, line 320). Acrobat Studio attach: "*nearly 50% of Acrobat commercial ETLAs renewed in Q4 already upgrading to this offering*" (Wadhwani, `primary_sources/4Q2025/earnings_call_transcript.md`). Pricing power rests on switching costs and on commercially-safe/indemnified AI: Adobe's differentiation is "*commercially safe first-party and leading partner AI models*" giving "*brand safety, compliance, intellectual property protection*" (`primary_sources/2Q2026/md_and_a.md`).
- **Direction of factor.** **Deliberately paused.** "*we have made the decision to defer previously planned Creative Cloud second half line optimizations*" (Narayen, `primary_sources/2Q2026/earnings_call_transcript.md`). Narayen framed it as recoverable: "*that one is just a phase shift... we're deferring it, but not closing it.*"
- **Direction of revenue.** Roughly **−$240M of FY2026 ARR** from this half of the pivot (computed as half of the ~$480M, per Narayen's 50/50 split, `causal_model_calcs.py` §6b). Whether it is genuinely recoverable is a judgment call, not a fact.

  - **Sub-factor 1.3a — Mix drift toward the cheaper customer group.** Business Professionals & Consumers (Acrobat/Express) subscription revenue grew 14.7% in FY2025 and 16.2% in Q2 FY2026, versus Creative & Marketing Professionals at 10.5% and 12.9% (computed, `causal_model_calcs.py` §13, from `primary_sources/FY2025/md_and_a.md` and `primary_sources/2Q2026/md_and_a.md`). BP&C rose from 28.5% to 29.0% of customer-group subscription revenue. The faster-growing group is the lower-priced one, so **revenue mix is drifting toward lower revenue-per-user even as total revenue accelerates**. This is a slow, persistent headwind to blended ARPU that is largely invisible in headline growth. (Inference: Adobe does not disclose per-user pricing, but Acrobat/Express list prices are far below Creative Cloud's — internal AI model knowledge; the *direction* is supported by the growth-rate differential, which is computed.)

### Factor 1.4 — Consumption-based monetisation (generative credits): a genuinely new revenue vector

- **Mechanism.** This is the first material break from Adobe's pure per-seat model. "*Our Creative Cloud and Firefly subscriptions include a monthly plan-specific number of generative credits... and our free plans include a limited number of generative credits*" (`primary_sources/FY2025/business.md`). Wadhwani described the mechanics: when users "*deplete their credits, they can get more credits in one of two ways. They can upgrade to a higher-end plan and/or they can purchase generative credit add-on packs*" (`primary_sources/4Q2025/earnings_call_transcript.md`). He described the growth algorithm as "*a multiplier across four different things... the number of apps that have these generative capabilities, times the number of media types... times the number of use cases and workflows... times the number of models.*"
- **Evidence and direction.** Steeply up. Generative credit consumption "*increased 3x quarter-over-quarter*" (Q4 FY2025), then "*over 45% quarter-over-quarter*" (Q1 FY2026), and Firefly ARR "*grew approximately 50% quarter-over-quarter*" in Q2 FY2026 to "*approaching $300 million*" (`primary_sources/4Q2025/`, `1Q2026/`, `2Q2026/earnings_call_transcript.md`). Total AI-first ARR is "*greater than $500 million*", up 3x YoY (Narayen, `primary_sources/2Q2026/earnings_call_transcript.md`, line 186).
- **Direction of revenue.** Positive and compounding, but **small in absolute terms**: $500M of AI-first ARR is ~1.8% of the $27.10B ARR base (computed). The growth rate is spectacular; the base is not yet material. I would not underwrite this as the near-term revenue engine.
- **Important second-order effect:** unlike a seat, a credit has a *direct variable cost* (inference). This is the mechanism by which revenue growth now drags cost of revenue with it — see Stage 2.

### Factor 1.5 — Enterprise seat expansion and cross-sell

- **Mechanism.** Large enterprise agreements (ETLAs) expand by seat count and by attaching adjacent products (Experience Platform, GenStudio, Experience Manager, Firefly Services).
- **Evidence.** "*enterprise customers with over $10 million in ARR growing greater than 20% year-over-year*" (Steve Day, `primary_sources/2Q2026/earnings_call_transcript.md`, line 320), from "*over 150*" such customers a year earlier (Wadhwani, `primary_sources/4Q2025/earnings_call_transcript.md`). "*ending ARR across GenStudio, AEP and apps, and AEM and agentic web growing over 20% year-over-year*" (Day, Q2 FY2026).
- **Direction.** Up, steadily; also the one part of the book management says is *not* being disturbed by the pivot — "*continued strength in retention across the enterprise customer base*" (Day, Q2 FY2026).
- **Timing distortion.** Enterprise deals are back-loaded and lumpy: "*a higher percentage of a quarter's total sales occur during the final weeks of each quarter*" and revenue is exposed to "*longer-than-expected sales, contract negotiation and implementation cycles*" (`primary_sources/FY2025/risk_factors.md`). AI contracting is making this worse: generative/agentic capabilities "*increase the complexity of technical or contractual assurances... leading to extended sales cycles*" (`primary_sources/2Q2026/risk_factors.md`).

### Factor 1.6 — Churn and substitution by AI-native tools

- **Mechanism.** Net-new ARR is gross adds less churn. Churn rises if a cheaper or AI-native substitute is good enough for a workflow.
- **Evidence.** Adobe discloses **no** churn or net-revenue-retention figure in any of the three transcripts or either filing — only qualitative "*continued strength in retention*." But there is one concrete, quantified substitution data point: Adobe Stock. Narayen: Stock is "*about a $450 million book of business*" and "*if you take out the Stock business, like-for-like, instead of the 10.9% growth, it would have been approximately 11.2% growth*" (`primary_sources/1Q2026/earnings_call_transcript.md`, line 584), with Wadhwani adding it "*saw a steeper decline than we expected. This shift is playing out more quickly than we had planned for.*" Decomposing this correctly requires the *same-period* prior-year base: the Q1 FY2026 call gives total ARR of $26.06B "*growing 10.9% year-over-year*" (line 344), implying a Q1 FY2025 base of ~$23.50B. Solving the weighted-average identity (T₂−S₂)/(T₁−S₁) = 1.112 gives **Stock ARR declining roughly 4–5% year-over-year** — 3.9% if the "$450M" is the current-year book, 4.5% if it is the prior-year book; management does not say which, so this is a range, not a point estimate. Stock is ~1.7% of the ARR base and its drag on total ARR growth is ~0.3pp, as disclosed (computed, `causal_model_calcs.py` §6d).

  > **Correction (verifier round 1, conceded).** An earlier version of this document stated Stock was "shrinking roughly 17% YoY," derived by dividing the ~$77M growth drag by Stock's own $450M book. That conflates *drag as a share of Stock's book* with *Stock's growth rate*, and used the FY2026-opening $25.66B ARR base against Q1 figures whose correct base is Q1 FY2025. The 17% figure was wrong by a factor of ~3–4x. The corrected 4–5% materially softens — but does not eliminate — the "canary" reading below.
- **Direction of factor.** Adverse and, in the one measurable case, faster than management modelled. The 10-K names the cause: "*increasing competition from companies offering generative and agentic AI solutions*", in markets with "*limited barriers to entry, short product life cycles, customer price sensitivity*" that "*may increase downward pressure on pricing and gross margins and adversely affect our renewal, upsell and cross-sell rates*" (`primary_sources/FY2025/risk_factors.md`).
- **Direction of revenue.** Negative, currently small (~0.3pp of ARR growth, on a line declining ~4–5%). **Adobe Stock is a canary, not the coal mine** — it was the most commoditisable thing Adobe sold (undifferentiated licensed imagery, exactly what a diffusion model replaces). Photoshop/Premiere workflows are far more defended. It establishes that AI substitution of an Adobe revenue line is no longer hypothetical, and management conceded it was faster than planned. But at a corrected 4–5% decline on 1.7% of ARR, it is a *mild* canary: the honest reading is that the one measurable instance of AI substitution at Adobe is so far modest, and the alarm should come from the fact that it exists at all and surprised management, not from its magnitude. This remains the highest-consequence, lowest-visibility factor in the model — because it is nearly unmeasurable, not because the measured instance is large.

### Factor 1.7 — Foreign exchange

- **Mechanism.** 41% of FY2025 revenue was non-Americas (`primary_sources/FY2025/md_and_a.md`). Translation moves reported revenue; a cash-flow hedging programme offsets part of it, and ARR is separately revalued once a year at opening rates.
- **Evidence and direction.** **Flipped from neutral to a meaningful tailwind.** FY2025: FX cut revenue by ~$18M, offset by $22M of hedging gains — net ~$4M on $2,264M of growth, i.e. ~0% (`primary_sources/FY2025/md_and_a.md`; computed). Q2 FY2026: the dollar "*primarily weakened against EMEA currencies*", adding ~$116M of revenue, partially offset by $22M of hedging *losses* — **net +$94M, or ~13% of the $745M of reported revenue growth** (computed, `causal_model_calcs.py` §7, from `primary_sources/2Q2026/md_and_a.md`). Reported Q2 growth 12.7%; ex-FX ~11%, matching management's stated constant-currency figure. Separately, the annual ARR revaluation added $460M to the opening FY2026 ARR base (Durn, `primary_sources/4Q2025/earnings_call_transcript.md`).
- **Direction of revenue.** Positive, and **flattering**. Roughly an eighth of Q2's revenue growth was currency. Note the hedge is working *against* Adobe on the way up, exactly as designed: "*Our hedging activities have not, and may not in the future, offset more than a portion of the adverse financial impact*" (`primary_sources/FY2025/risk_factors.md`).

### Factor 1.8 — Acquisitions

- Semrush: ~$1.9B all-cash, agreed November 18 2025, closed April 2026, adding "*approximately $480 million*" of ARR and ~$40M of Q2 revenue, with ~$280M expected in FY2026 revenue (`primary_sources/FY2025/md_and_a.md`; `primary_sources/2Q2026/md_and_a.md`; Steve Day, `primary_sources/2Q2026/earnings_call_transcript.md`). Direction: one-time step-up in the ARR base. Its causal significance is less the revenue than the fact that it **masked the organic guidance cut** (§1.2).

### Non-factors I am deliberately excluding

Product revenue ($325M, 1% of FY2025) and services and other ($540M, 2%) are both shrinking (−16% and −10% in FY2025) and are immaterial to the causal model (`primary_sources/FY2025/md_and_a.md`). Piracy is named in the risk factors ("*we continue to lose revenue due to illegal use of our software*") but is unquantified and, in a subscription/cloud model, structurally less relevant than in the perpetual-licence era — **inference**.

---

## Stage 2: Gross profit

FY2025 gross profit $21,218M (89.3% margin); Q2 FY2026 $5,903M (89.2%); 1H FY2026 $11,637M (89.4%) (computed, `causal_model_calcs.py` §1–2). **Gross margin has been almost perfectly stable: +0.23pp FY2024→FY2025 and +0.06pp in Q2 FY2026 YoY.**

That stability is the headline finding of this stage, and it cuts against the common narrative. Below is why, and what could break it.

### Factor 2.1 — Hosting, data-centre and AI inference cost. The one variable cost that matters.

- **Mechanism.** Adobe explicitly places AI compute in cost of revenue: "*Cost of subscription revenue consists primarily of third-party hosting services and data center costs, including expenses related to operating our network infrastructure and AI inferencing costs*" (`primary_sources/2Q2026/md_and_a.md`, identical in FY2025). Every generative action by a paid *or free* user consumes inference. The risk factors are blunt: "*Developing, testing and deploying AI systems and third-party AI models may continue to increase the cost of our solutions, including due to the nature of the computing costs involved... These costs could adversely impact our margins*" (`primary_sources/FY2025/risk_factors.md`).
- **Evidence — the acceleration is real and quantifiable.** Adobe publishes a components-of-change table for cost of subscription revenue. Hosting/data-centre costs contributed **8pp of the 13% FY2025 increase**, i.e. ~$144M of the $228M rise (63% of it). In Q2 FY2026 they contributed **16pp of the 16% increase**, i.e. ~$81M — effectively *all* of the increase, with amortisation of intangibles a −6pp offset (computed, `causal_model_calcs.py` §5, from `primary_sources/FY2025/md_and_a.md` and `primary_sources/2Q2026/md_and_a.md`). **The hosting-cost contribution to cost growth roughly doubled year-on-year.**
- **But the margin has held.** Subscription gross margin: 91.2% (FY2024) → 91.2% (FY2025) → 90.9% (Q2 FY2026) (computed, §5). Only ~30bp of erosion.
- **Why the two facts are compatible.** Subscription *revenue* is also compounding at 13–14%, and hosting starts from a small base (cost of subscription revenue is only ~9% of subscription revenue). Hosting can grow much faster than revenue for a while before it shows up in the margin. Management claims active cost engineering: "*we now track tokens and token usage within the company... below the surface, we're actually constantly getting more efficient, as it relates to our spend*" (Narayen, `primary_sources/1Q2026/earnings_call_transcript.md`).
- **Direction of factor.** Up, and accelerating.
- **Direction of gross profit.** Essentially flat as a margin so far; gross profit dollars up 13%. **My assessment: the AI-cost risk to Adobe's gross margin is real but has not yet materialised, and it is being over-anticipated by the market narrative.** The honest caveat is in §2.2.

  - **Sub-factor 2.1a — The free-MAU cost wedge (the genuine risk).** Free users get "*a limited number of generative credits*" (`primary_sources/FY2025/business.md`). Adobe has just added ~150M Acrobat/Express MAU and ~40M creative freemium MAU year-over-year (§1.1) with *zero* associated revenue. Every one of those users that touches a generative feature consumes inference that lands in cost of subscription revenue while the offsetting revenue sits in a future period — or never arrives. This is the one mechanism by which gross margin could deteriorate materially, and **it is the mechanism management's own strategy is deliberately amplifying**. It has not shown up yet (subscription gross margin fell just 18bp year-over-year in Q2 FY2026 — computed, `causal_model_calcs.py` §14), but the freemium push materially scaled only in Q2 FY2026 and Narayen said the traffic re-routing happens "*in Q3*". **I would expect the first real test of this in Q3/Q4 FY2026 results.** Flagged as forward-looking inference, not observed fact.

### Factor 2.2 — Third-party model licensing and dependency

- **Mechanism.** Adobe deliberately aggregates rather than builds everything: "*We partner with an extensive ecosystem of third-party models across categories*" alongside its own Firefly models (`primary_sources/FY2025/business.md`). Partner models carry usage-based costs Adobe does not control, and royalty costs sit in cost of subscription revenue.
- **Evidence.** Royalty costs contributed +1pp to the Q2 FY2026 cost-of-subscription increase — small (`primary_sources/2Q2026/md_and_a.md`). But the strategic exposure is escalating in Adobe's own language. The FY2025 10-K said other companies "*may in the future prevent, limit or interfere with our ability to use third-party models in our solutions*"; the Q2 FY2026 10-Q **broadened** this to "*...in our solutions or make, use or sell our own AI solutions*" (`primary_sources/FY2025/risk_factors.md` vs `primary_sources/2Q2026/risk_factors.md`). Adobe also depends on the same hyperscalers it competes with for attention: "*we are huge users of their cloud services*" (Narayen, `primary_sources/2Q2026/earnings_call_transcript.md`).
- **Direction.** Dependency rising; cost impact currently immaterial; strategic risk rising (the risk-factor language change is a genuine signal — companies do not broaden that wording casually).
- **Direction of gross profit.** Neutral today; asymmetric downside. **Sized:** because Adobe rents rather than owns its compute (§4.3), vendor repricing is a live channel. Adobe does not disclose the hosting share of the $2,027M FY2025 cost-of-subscription line, so this is a band under an assumption of 50–70% (**inference**): a +25% shock costs ~$253–355M (2.9–4.1% of FY2025 EBIT), +50% costs ~$507–709M (5.8–8.1%), and a doubling costs ~$1.0–1.4B (**11.6–16.3% of FY2025 EBIT**) (computed, `causal_model_calcs.py` §15). Material, but bounded and one-time, versus the free-user *volume* channel (§2.1a), which is unbounded. Both channels are consolidated into uncertainty item #2 below.

### Factor 2.3 — Revenue mix across the three revenue lines

- **Mechanism.** Subscription carries ~91% gross margin. Services and other carries a *negative* gross margin: FY2025 revenue $540M against cost of $501M (7% gross margin), and Q2 FY2026 revenue $113M against cost of $124M — **a gross loss** (`primary_sources/FY2025/md_and_a.md`; `primary_sources/2Q2026/md_and_a.md`).
- **Direction of factor.** Services and other is shrinking fast (−22% in Q2 FY2026), so mix is shifting toward the high-margin line.
- **Direction of gross profit.** **Positive — and this is the quiet offset that has been paying for the rising AI compute bill.** A full rate/mix bridge of the Q2 FY2026 gross margin ties exactly to the observed +0.06pp (computed, `causal_model_calcs.py` §14):

  | Effect                                              | Impact on total gross margin |
  |-----------------------------------------------------|------------------------------|
  | **Rate** — subscription margin (hosting/AI inference) | **−0.17pp**                  |
  | **Rate** — services margin collapsing (+11.8% → −9.7%) | −0.51pp                     |
  | **Rate** — product                                    | +0.01pp                      |
  | **Mix** — services shrinking 2.5% → 1.7% of revenue, subscription rising 96.0% → 96.9% | **+0.74pp** |
  | **Total**                                             | **+0.06pp**                  |

  Two things fall out of this that matter. First, **the AI/hosting drag on *total* gross margin in Q2 FY2026 was only about 17 basis points** — an order of magnitude smaller than the prevailing narrative implies. Second, the services line is now running at a *negative* gross margin, and the mix lever that offset the rate drag is finite and one-way: services is already down to 1.7% of revenue, so there is very little left to harvest if subscription margin starts eroding in earnest.

### Factor 2.4 — Support, network operations and implementation headcount

- **Mechanism.** Compensation for "*network operations, implementation, account management and technical support personnel*" sits in cost of subscription revenue (`primary_sources/2Q2026/md_and_a.md`).
- **Evidence and direction.** Contributed +2pp to the FY2025 increase and +5pp to Q2 FY2026 — modest and rising. Adobe mitigates via labour arbitrage: it hires "*in countries where exceptional technical knowledge and other expertise are offered at lower costs*", with offshore employees rising from ~50% (FY2025 10-K) to ~52% (Q2 FY2026 10-Q). But that lever is eroding — "*competition for talent in those countries has increased... [which] may increase our compensation-related expenses*" (both `risk_factors.md` files).
- **Direction of gross profit.** Mildly negative, well controlled.

---

## Stage 3: Operating income

FY2025 EBIT $8,706M (36.6% margin); Q2 FY2026 $2,238M (33.8%); 1H FY2026 $4,656M (35.8%) (computed, `causal_model_calcs.py` §1–2). **Q2 FY2026 GAAP operating margin fell 2.09pp year-over-year.**

The single most useful thing I can do at this stage is decompose that 2.09pp, because the answer is counterintuitive. Every line as a percentage of revenue, Q2 FY2026 vs Q2 FY2025 (computed, `causal_model_calcs.py` §3 — the components sum exactly to −2.09pp):

| Line                | Q2 FY2025 | Q2 FY2026 | Margin impact |
|---------------------|-----------|-----------|---------------|
| Cost of revenue     | 10.9%     | 10.8%     | **+0.06pp**   |
| Research & development | 18.4%  | 18.1%     | **+0.32pp**   |
| Sales & marketing   | 27.7%     | 28.5%     | **−0.78pp**   |
| General & administrative | 6.4% | 8.3%      | **−1.83pp**   |
| Amortisation of intangibles | 0.7% | 0.6%  | **+0.14pp**   |
| **Total**           |           |           | **−2.09pp**   |

**AI compute did not compress Adobe's operating margin. R&D did not either — it delevered *favourably*. Roughly 88% of the compression came from G&A, and G&A's increase was overwhelmingly two non-recurring legal/impairment items.** That is a materially different story from the one implied by the share price reaction and the sell-side downgrade (Knowledge Store ID 9).

### Factor 3.1 — Sales & marketing intensity, specifically advertising (the *persistent* driver)

- **Mechanism.** Filling a freemium funnel requires paid customer acquisition *now*, against ARR that converts later. This is the P&L expression of the funnel strategy in §1.2.
- **Evidence.** Both filings attribute the increase the same way: S&M rose "*primarily due to increases in advertising expenses and, to a lesser extent, compensation costs*" (`primary_sources/2Q2026/md_and_a.md`, and identically in `primary_sources/FY2025/md_and_a.md`). Narayen confirmed the intent and refused to cap it: "*we are spending on this, and we will continue to, whether it's on the models, whether it's in marketing, whether it's in the product... we will not be short-term focused on this*" (`primary_sources/2Q2026/earnings_call_transcript.md`).
- **Direction of factor.** Up. S&M grew 16% in Q2 FY2026 against 13% revenue growth.
- **Direction of operating income.** Negative, −0.78pp in Q2. **This is the item to watch, because unlike the G&A items it is structural to the strategy and will persist through FY2027.** Management's own quarterly non-GAAP operating margin guidance confirms the trajectory: 47.4% actual in Q1 FY2026, ~44.5% guided for Q2, ~44% guided for Q3, with the full year held at ~45% (`primary_sources/1Q2026/`, `2Q2026/earnings_call_transcript.md`). **[GUIDANCE — forward-looking, not reported.]**

### Factor 3.2 — Legal, regulatory and impairment charges in G&A (the *transitory* driver)

- **Mechanism.** Adobe books goodwill impairment and litigation loss contingencies through G&A (`primary_sources/2Q2026/md_and_a.md`).
- **Evidence.** Q2 FY2026 G&A rose 45% YoY. Adobe's components-of-change table attributes 19pp of that to goodwill impairment and 8pp to loss contingency, i.e. ~$72M and ~$30M of the $169M increase (computed, `causal_model_calcs.py` §4). This ties to the segment footnote: goodwill impairment $70M, loss contingency $30M for the quarter and $92M for the half (`primary_sources/2Q2026/financial_statements.md`). **Together these two items are ~$100M of the $169M Q2 G&A increase — about 1.5pp of the 2.09pp total margin compression.**
- **Root causes, which are two different things:**
  - *Goodwill impairment* — $70M against the Publishing & Advertising reporting unit (`primary_sources/2Q2026/financial_statements.md`, Note on goodwill). Non-cash, but it is **not** economically meaningless: it is Adobe writing down a legacy business whose earning power has genuinely deteriorated. Publishing & Advertising revenue was $256M and shrinking 7% in FY2025 (`primary_sources/FY2025/md_and_a.md`).
  - *Loss contingency* — the FTC/DOJ ROSCA case over Adobe's "*disclosure and subscription cancellation practices*", filed June 2024, motion to dismiss denied May 2025, **settled March 12 2026** (`primary_sources/2Q2026/financial_statements.md`, Note 13). The causal significance goes beyond the cash: consumer-protection enforcement on cancellation friction constrains a *revenue* practice, not just a cost line. The DOJ complaint *alleged* that Adobe "*failed to provide a simple cancellation mechanism*" (Note 13) — that is the government's allegation, **not** a disclosed settlement obligation. Adobe discloses no settlement terms at all. Adobe's historical subscription retention may have benefited to some unknown degree from cancellation friction, but whether — or how much — that friction changes going forward is **unknown from the filings**. Flagged as an unquantifiable and directionally uncertain link back into Stage 1 churn. *(Correction, verifier round 1, conceded: an earlier version framed this as "a settlement that mandates 'a simple cancellation mechanism'," which misattributed a complaint allegation as a settlement term and contradicted the same sentence's admission that terms are undisclosed.)*
- **Direction.** Both items are one-time in Q2 FY2026. Expect G&A to normalise.

### Factor 3.3 — R&D: compensation-driven, and currently *positive* for margin

- **Mechanism.** R&D is "*primarily compensation and contracted costs associated with software development, third-party hosting services and data center costs including AI training costs*" (`primary_sources/2Q2026/md_and_a.md`). Note that model *training* compute sits here, while *inference* sits in cost of revenue.
- **Evidence and direction.** R&D grew 11% in Q2 FY2026 against 13% revenue growth, so it **delevered favourably by +0.32pp** and has been pinned at exactly 18% of revenue for four straight years (FY2023, FY2024, FY2025, Q2 FY2026) (computed, `causal_model_calcs.py` §3; `primary_sources/FY2025/md_and_a.md`). Both filings attribute the increase "*primarily due to increases in compensation costs*" — **not** to AI training compute.
- **Direction of operating income.** Slightly positive. **This is a genuinely notable finding: Adobe is not visibly spending more, as a share of revenue, on R&D to compete in AI.** Whether that is admirable discipline or under-investment against AI-native competitors is the open question, and I cannot resolve it from the filings. Narayen's own framing — "*we get a lot of Anil's products relatively cheap... our efficiency on that is probably better than anybody else in the industry*" (`primary_sources/2Q2026/earnings_call_transcript.md`) — is a claim of efficiency; a bear would read the same number as complacency.

### Factor 3.4 — Headcount, wage inflation and stock-based compensation

- **Mechanism.** Adobe employed 31,360 people at FY2025 year-end with 9.9% attrition (`primary_sources/FY2025/business.md`). Compensation is the dominant cost across all four expense lines, and SBC is a large non-cash component of it.
- **Evidence.** SBC was $1,942M in FY2025 (8.2% of revenue) and $1,045M in 1H FY2026 (8.0%) — of which R&D absorbs the majority ($1,010M of $1,942M in FY2025) (`primary_sources/FY2025/financial_statements.md`; `primary_sources/2Q2026/financial_statements.md`; computed, §9). Revenue per employee rose from $758k (FY2025) to ~$830k (1H FY2026 annualised, on an unchanged headcount base) (computed, §12). Wage pressure is acknowledged: "*We have experienced, and may continue to experience, higher compensation costs to retain and recruit senior management or highly skilled personnel that may not be offset by innovation, improved productivity or increased sales*" (`primary_sources/FY2025/risk_factors.md`).
- **Direction of factor.** Headcount roughly flat with revenue growing — productivity up ~10%. SBC intensity flat to slightly down.
- **Direction of operating income.** Positive. Adobe is getting operating leverage from a static headcount, which is what has funded the advertising increase without a larger margin hit.

### Factor 3.5 — Leadership discontinuity (a real causal factor, not a governance footnote)

- Narayen announced his transition out of the CEO role after 18+ years in March 2026 (`primary_sources/1Q2026/earnings_call_transcript.md`), and CFO Dan Durn's departure was announced on the June 2026 call with Steve Day as interim CFO (`primary_sources/2Q2026/earnings_call_transcript.md`). Per web search, no successor had been named as of August 2026 (Knowledge Store ID 8).
- **Mechanism, and why it belongs in a causal model:** the freemium pivot (§1.2, §3.1) is a multi-year bet whose payback lands in FY2027 — "*that will play out, I think, over 2027*" (Narayen). An incoming CEO inherits an unfinished, margin-dilutive, ARR-dilutive strategy they did not choose, at the exact moment Narayen said the goal was to have them "*put their stamp on planning for fiscal 2027*." A reversal would swing both S&M spend and ARR guidance. **The probability and direction of that reversal is genuinely unknowable from available sources — speculation, flagged as such.**

---

## Stage 4: Owners' earnings

Using the definition in `CLAUDE.md` — cash truly available to owners after all obligations. I have deliberately used the simplest defensible construction rather than a multi-step normalisation, because Adobe's cash conversion is clean and extra machinery would add false precision.

| Basis                                        | FY2025    | 1H FY2026 | Source                                    |
|----------------------------------------------|-----------|-----------|-------------------------------------------|
| Cash flow from operations                     | $10,031M  | $5,123M   | FY2025 10-K / Q2 FY2026 10-Q cash flows    |
| Less capital expenditure                      | ($179M)   | ($95M)    | same                                       |
| = Free cash flow                              | $9,852M   | $5,028M   | computed, `causal_model_calcs.py` §9       |
| FCF margin                                    | 41.4%     | 38.6%     | computed                                   |
| Less stock-based compensation (a real cost)   | ($1,942M) | ($1,045M) | FY2025 FS Note 12 / Q2 FY2026 FS Note 9    |
| **= SBC-adjusted owners' earnings**           | **$7,910M** | **$3,983M** | computed                                 |
| As % of revenue                               | 33.3%     | 30.6%     | computed                                   |

### Factor 4.1 — Cash conversion and the deferred-revenue float

- **Mechanism.** Customers pay in advance; Adobe recognises revenue later. The gap is deferred revenue, which is an interest-free source of funding and the reason CFO exceeds net income by a wide margin.
- **Evidence.** Deferred revenue $6.26B → $7.03B → $7.25B across FY2024, FY2025 and Q2 FY2026 (`primary_sources/FY2025/financial_statements.md`; `primary_sources/2Q2026/financial_statements.md`). FY2025 CFO of $10.03B against net income of $7.13B. FY2025 CFO grew 25%, though note the flattering comparison — "*Fiscal 2024 cash flows from operations were adversely impacted by payment of the $1 billion Figma termination fee*" (`primary_sources/FY2025/md_and_a.md`).
- **Direction.** Deferred revenue up 12.3% in FY2025 but only 3.1% sequentially in 1H FY2026 (computed, §8). RPO $22.52B at FY2025 year-end, $22.27B at Q2 FY2026 — up 13% YoY but **down $0.25B sequentially** (computed, §8). And the 12-month conversion share of RPO rose from 65% to 67%, meaning the contracted backlog got slightly *shorter* (`primary_sources/FY2025/financial_statements.md`; `primary_sources/2Q2026/financial_statements.md`).
- **Direction of owners' earnings.** Still strongly positive, but the float is no longer expanding as fast. This is a soft early-warning indicator worth tracking; I would not over-read one quarter of enterprise renewal lumpiness.

### Factor 4.2 — Cash tax rate. The largest single mover of FY2026 owners' earnings.

- **Mechanism.** Effective tax rate is driven by jurisdictional profit mix, SBC windfalls/shortfalls, non-deductible items, and statutory change.
- **Evidence.** ETR: 20% (FY2023) → 20% (FY2024) → 18% (FY2025) → 23% (1H FY2026), 24% in Q2 alone (`primary_sources/FY2025/md_and_a.md`; `primary_sources/2Q2026/md_and_a.md`). Adobe attributes the rise to "*a decrease in the net tax benefit from effects of non-U.S. operations, an increase in state taxes, and a goodwill impairment charge which is not deductible*", plus "*an increase in the net tax expense related to stock-based compensation*."
- **Magnitude.** On 1H FY2026 pre-tax income of $4,660M, holding the prior-year 18% rate would have given tax of ~$839M against the actual $1,059M — **~$220M of incremental tax, ~6% of net income**. This is why 1H FY2026 net income grew only 2.8% ($3,502M → $3,601M) while EBIT grew 9.0% (computed, `causal_model_calcs.py` §10).
- **Offsetting item.** The One Big Beautiful Bill Act "*restores immediate expensing of domestic research and development costs*", and Adobe says it "*anticipate[s] a reduction to our effective rates for cash taxes paid for fiscal 2026 and beyond*" (`primary_sources/2Q2026/md_and_a.md`). So the **GAAP** rate is rising while the **cash** rate should fall — and owners' earnings follow cash. Management's guidance splits the same way: FY2026 GAAP tax rate raised from ~20.5% to ~22.5% across the three calls, while the non-GAAP rate was held at ~18% throughout (`primary_sources/4Q2025/`, `2Q2026/earnings_call_transcript.md`). **[GUIDANCE.]**
- **Direction of owners' earnings.** GAAP earnings materially depressed; cash owners' earnings much less so. Anyone reading Adobe's flat GAAP net income as an operating problem is misreading a tax-mix effect.

### Factor 4.3 — Capital intensity: Adobe rents its AI compute rather than buying it

- **Mechanism.** Adobe runs on third-party cloud, so AI capacity is procured as an operating cost, not capitalised. This is the opposite of the hyperscaler model.
- **Evidence.** Capex is trivial: $179M in FY2025 (0.8% of revenue) and $95M in 1H FY2026 (0.7%) (`primary_sources/FY2025/financial_statements.md`; `primary_sources/2Q2026/financial_statements.md`; computed §9). The real commitment sits off the balance sheet: **$6.82B of non-cancellable purchase obligations "*primarily relating to contracts with vendors for third-party hosting and data center services*"** (`primary_sources/FY2025/md_and_a.md`) — 0.7x FY2025 free cash flow and ~3.4x FY2025 cost of subscription revenue (computed, §9).
- **Direction and interpretation.** **This is the most under-appreciated line in Adobe's financials.** It means (a) reported FCF is *not* flattered by under-investment in compute — the spend is already in the P&L; (b) Adobe carries ~$6.8B of contracted spend that must be absorbed regardless of whether the freemium users convert; and (c) the risk factors warn that if Adobe is "*unable to renew our agreements with them on favorable terms or at all, our expenses could significantly increase*" (`primary_sources/FY2025/risk_factors.md`). Adobe has no owned-infrastructure fallback. It is a price-taker on the input that is becoming its main variable cost.

### Factor 4.4 — Stock-based compensation and the buyback. The binding constraint.

- **Mechanism.** SBC is a real cost to owners because it dilutes them; buybacks are the offset. If buybacks exceed owners' earnings, the gap must be funded by cash drawdown or debt, and is therefore not sustainable indefinitely.
- **Evidence.** Buybacks: $11.28B in FY2025 and $4.59B in 1H FY2026 (`primary_sources/FY2025/md_and_a.md`; `primary_sources/2Q2026/md_and_a.md`). Against SBC-adjusted owners' earnings, that is **1.43x in FY2025 and 1.15x in 1H FY2026** (computed, §9). The funding gap is visible: cash and equivalents fell from $7.61B (Nov 2024) to $5.43B (Nov 2025) to $4.92B (May 2026), stockholders' equity fell to $11.52B, working capital swung from −$37M to **−$3.01B**, and Adobe drew commercial paper from **zero outstanding at FY2025 year-end to $494M at Q2 FY2026** (`primary_sources/FY2025/md_and_a.md`; `primary_sources/2Q2026/md_and_a.md`). A further $1.35B of senior notes was reclassified to current, which Adobe "*intend[s] to refinance*."
- **Effect.** Share count fell from 410.5M (January 2026 10-K cover) to 397.5M (June 2026 10-Q cover), −3.2% in five months (computed, §11); Durn said FY2025 buybacks reduced shares "*by over 6%*" (`primary_sources/4Q2025/earnings_call_transcript.md`). Authorisation is not the constraint — a new $25B authorisation in April 2026 left $26.78B available (`primary_sources/2Q2026/md_and_a.md`).
- **Direction of owners' earnings.** Aggregate OE roughly flat-to-down in 1H FY2026; **per-share OE growing ~6–7pp/year faster** because of the shrinking denominator. **But the buyback is being run above what the business generates, and the balance sheet shows it.** Authorisation is ample; *cash* is the binding constraint. If FCF conversion softens as the freemium spend builds, the buyback — the largest single support for per-share owners' earnings — is the most reversible item in the whole model.

### Factor 4.5 — Interest expense and leverage

- $6.15B of senior notes outstanding, plus $494M of commercial paper (`primary_sources/2Q2026/md_and_a.md`). FY2025 interest expense was $263M, up 56% on the January 2025 note issuance; Q2 FY2026 interest expense was $65M, roughly flat YoY (`primary_sources/FY2025/md_and_a.md`; `primary_sources/2Q2026/md_and_a.md`). Interest *income* is falling — other income fell "*primarily due to decreases in interest income driven by lower average overall cash balances and interest rates*" (`primary_sources/2Q2026/md_and_a.md`), a direct consequence of §4.4. Net non-operating income has collapsed from $190M (FY2024) to $28M (FY2025) to $4M (1H FY2026). Direction: modestly negative and worsening, driven by the buyback-funded decline in the cash pile rather than by the debt itself.

### Explicitly excluded from this stage

Goodwill impairment ($70M), amortisation of purchased intangibles ($85M in 1H FY2026) and the deferred-tax swing are GAAP artefacts, not causal drivers of owners' earnings, and per the brief I have not treated them as factors. The goodwill impairment *is* however a signal about the economics of the Publishing & Advertising unit, which is why it appears in §3.2.

---

## What I am confident about vs. what is genuinely uncertain

**High confidence (directly computed from filings, arithmetic checked in `causal_model_calcs.py`):**

- The Q2 FY2026 operating-margin decline is ~88% a G&A story (goodwill impairment + FTC settlement contingency, ~$100M of the $169M increase), not an AI-cost story. Cost of revenue and R&D both *helped* margin.
- Gross margin is essentially unchanged (89.0% → 89.3% → 89.2%). A full rate/mix bridge shows the AI/hosting drag on total gross margin in Q2 FY2026 was only ~17bp, offset by mix shifting out of a now loss-making services line.
- The FY2026 organic ARR guide was cut by ~$480M (~1.9pp) while the 10.2% headline was held, because Semrush's acquired ARR filled the hole. Two independent methods agree.
- Organic YoY ARR growth is 11.5% → 10.9% → ~10.5%, a ~100bp grind. `work_products/overview.md` overstated this deceleration roughly threefold by comparing a half-year sequential rate to annual rates.
- ~13% of Q2 FY2026 revenue growth was FX, versus ~0% in FY2025.
- The ETR rise from 18% to 23% cost ~$220M in 1H FY2026 and explains why net income grew 2.8% while EBIT grew 9.0%.
- Buybacks are running at 1.15–1.43x SBC-adjusted owners' earnings, funded by cash drawdown and, newly, commercial paper.

**Moderate confidence (sourced but requiring judgment):**

- The ~$500M ARR cost of the pivot. This is **analyst arithmetic (Alex Zukin, Wolfe Research) that management did not dispute but also did not confirm**, corroborated by my independent Semrush-substitution calculation. Note this is a correction to `work_products/overview.md`, which attributes the $500M figure to management.
- That the deferred Creative Cloud price optimisation is recoverable. Narayen says "*deferring it, but not closing it*" — that is an assertion about the future.
- That subscription gross margin holds from here. The −17bp observed in Q2 FY2026 is a fact; that it stays small once 150M new free users are actively routed through generative features (from Q3 FY2026) is an assumption, and the offsetting mix lever is nearly exhausted.

**Genuinely uncertain — the four things that actually decide the outcome:**

1. **Free-to-paid conversion rate.** Never disclosed. The entire freemium thesis rests on it. Without it, MAU growth of 150M users is an input with an unknown coefficient.
2. **Whether inference economics break the gross margin.** Two distinct channels, and I under-weighted the second in an earlier version:
   - *Volume (observed, rising, unbounded).* 150M new free MAU consuming credits. It has not bitten yet — subscription gross margin fell just 18bp YoY in Q2 FY2026 — but traffic re-routing happens in Q3 FY2026, so Q3/Q4 are the first real test. Forward-looking inference.
   - *Vendor repricing (unobservable, bounded, one-time).* Adobe owns no AI infrastructure; it rents all of it, and the 10-K warns that if Adobe is "*unable to renew our agreements with them on favorable terms or at all, our expenses could significantly increase*" (`primary_sources/FY2025/risk_factors.md`). Adobe does **not** disclose the hosting share of cost of subscription revenue, so this can only be a band: assuming hosting is 50–70% of the FY2025 $2,027M line (**inference** — the MD&A says "primarily," supporting >50%, but gives no number), a +25% vendor price shock costs ~$253–355M (2.9–4.1% of FY2025 EBIT) and a doubling costs ~$1.0–1.4B (**11.6–16.3% of FY2025 EBIT**) (computed, `causal_model_calcs.py` §15). Two things bound it: Adobe has real counterparty leverage — "*we are huge users of their cloud services, which at the end of the day is a significant revenue stream for them*" (Narayen, `primary_sources/2Q2026/earnings_call_transcript.md`) — and it is multi-sourced across "*an extensive ecosystem of third-party models*" plus first-party Firefly (`primary_sources/FY2025/business.md`). The $6.82B of non-cancellable purchase obligations (3.4x FY2025 cost of subscription revenue, i.e. roughly three years pre-committed) dampens near-term repricing but removes the option to walk away. A common counter-argument — that unit inference costs are falling industry-wide — is **internal AI model knowledge, unsourced in this repository, and I flag it as the weakest leg of the bull case here**; the only *sourced* statement on the topic points the other way.
3. **Whether Adobe Stock's ~4–5% decline is idiosyncratic or the leading edge.** Stock was Adobe's most commoditisable product; Photoshop/Premiere workflows are far more defended. The decline is modest in size, but it is a real, measured instance of AI substituting an Adobe revenue line, it ran ahead of management's own plan, and the 10-K now concedes "*increasing competition from companies offering generative and agentic AI solutions*." The uncertainty is about read-across, not about this line's magnitude.
4. **CEO succession and strategic continuity.** The pivot's payback lands in FY2027, under a CEO who has not been named and did not choose it. Unknowable from available sources.

**The one thing I would tell someone who only reads one paragraph:** Adobe's revenue engine is ~75% volume and ~25% price, and management has just chosen to give up part of the price quarter to buy more of the volume three-quarters, funding it with advertising spend that hits the P&L two to six quarters before the ARR arrives. The near-term financials therefore *look* worse than the business is — the margin compression is mostly one-time legal/impairment items, the flat net income is mostly a tax-mix effect, and gross margin has barely moved. The real risks are not the ones showing up in the current numbers: they are the undisclosed conversion rate, the untested inference cost of 150 million new free users, and a buyback running above cash generation.

---

*All arithmetic: `work_products/causal_model_calcs.py` (run with `uv run python work_products/causal_model_calcs.py`).*
