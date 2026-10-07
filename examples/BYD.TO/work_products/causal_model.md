# Boyd Group Services (BYD.TO / BGSI) — Causal Model of the Business

*Prepared 2026-09-23 (citations revised 2026-09-24). US$ millions unless stated. Calculations are in `work_products/causal_model_calcs.py` (run `uv run python work_products/causal_model_calcs.py`). Any statement that is management's view rather than reported fact is labelled "management view". Anything that is my own reasoning is labelled "inference".*

**Source key** (citations below use "short name, lines xx-yy"):

| Short name     | File                                                 |
|----------------|------------------------------------------------------|
| Q2FY26 MD&A    | `primary_sources/Q2FY26/BoydGroup_MDA.md`            |
| Q2FY26 call    | `primary_sources/Q2FY26/earnings_call_transcript.md` |
| Q1FY26 call    | `primary_sources/Q1FY26/earnings_call_transcript.md` |
| FY2025 MD&A    | `primary_sources/FY2025/BoydGroup_MDA.md`            |
| FY2025 call    | `primary_sources/FY2025/earnings_call_transcript.md` |
| FY2024 MD&A    | `primary_sources/FY2024/Boyd_MDA.md`                 |
| FY2023 MD&A    | `primary_sources/FY2023/Boyd_MDA.md`                 |
| OE & ROIC      | `work_products/owners_earnings_and_roic.md`          |
| Script         | `work_products/causal_model_calcs.py`                |

## Summary: most important factors and assumptions

**Most important factors**

- **Structure:** sales = store count × same-store revenue. Same-store revenue ≈ industry repairable claims × average total cost of repair (TCOR) × Boyd's share of insurer direct-repair-program (DRP) volume.
- **New locations drive 2026 growth.** They added 27.1pp of Q2'26 sales growth, of which Joe Hudson's was 22.4pp, against 2.9pp from same-store sales (Q2FY26 MD&A, lines 231-233; Script, lines 4-12).
- **Industry claims are recovering.** They went from about −9% in 2024 (FY2024 MD&A, line 274) to "flat to down 2%" in Q2'26 (Q2FY26 MD&A, line 62). Flat insurance premiums (Q1FY26 call, line 353) and stable total-loss rates (Q2FY26 call, line 115) helped.
- **TCOR is the missing piece.** It "remained below historical levels, which limited the level of same-store sales growth" (Q2FY26 MD&A, line 232). It is the largest swing factor in organic growth.
- **Share gains carry same-store growth.** Same-store sales minus the industry-claims midpoint narrowed from +7.2pp (FY2024) to +3.9pp (Q2'26) (Script, line 19). Technician capacity is the constraint (Q2FY26 call, lines 163-165).
- **Gross margin rose** from 45.5% in FY2024 (FY2024 MD&A, line 281) to 47.4% in Q2'26 (Q2FY26 MD&A, line 239). Parts/paint procurement and in-house scanning and calibration drove the gain, partly offset by lower labor margin and Joe Hudson's lower-margin mix (same line).
- **Operating leverage and cost programs.** Same-store sales of −1.8% in FY2024 cut Adj. EBITDA margin from 12.5% to 10.9% (FY2024 MD&A, lines 274, 297). Project 360 and Joe Hudson's synergies lifted it to 13.4% in Q2'26 (Q2FY26 MD&A, lines 257-259).
- **OE is highly geared to margin.** Rent plus maintenance capex absorb ~55% of TTM Adj. EBITDA, and OE is ~32% of it. So +100bp of margin ≈ +$26.4M of OE, or +18% of the $145.9M TTM base (Script, lines 37-43; OE & ROIC, lines 100-105).
- **Acquisition prices cap ROIC.** It was 6.5% TTM on total capital, against 24.5% on tangible capital (OE & ROIC, lines 172-174).

**Most important assumptions**

- **Synergy drop-through (management view).** The remaining ~$65M (Q2FY26 MD&A, line 70) is worth up to +$47.8M of OE (+33%). Management's 14% margin target (Q2FY26 MD&A, line 221) implies only about +$31.5M (Script, lines 46-49). So part of the savings is likely absorbed by inflation (inference).
- **TCOR returns to 3–4% (management view).** Management has no view on timing: "Relative to timing, we don't really have a point of view" (Q2FY26 call, line 121). Each +1% of same-store sales adds at most ~$12.4M of OE (Script, line 45).
- **Share gains persist (management view, and inference on the capacity limit).** The lead over the industry is narrowing, and technician capacity may cap it.
- **Structural claim-frequency decline of 0 to −1%/yr (management view).** This combines −2% from collision-avoidance systems and +1% from miles driven (Q1FY26 call, line 67). A disputed +1% car-park term appears in FY2025 call, line 151. The figure is an assumption, not a measurement.
- **Maintenance capex ≈ 1.7% of sales (management guidance).** Guidance is 1.6–1.8% (FY2025 MD&A, line 526). Each ±0.3pp of sales is worth ∓~$7M of OE (OE & ROIC, line 200).
- **Insurer concentration is undisclosed.** The risk factors warn that losing a material DRP relationship "could have a material adverse effect" (FY2025 MD&A, line 746). The downside is asymmetric (inference).

---

## Stage 1: Net revenues (Sales)

TTM Jun-2026 sales were $3,594.4M (OE & ROIC, line 13). Q2'26 sales grew +29.9% to $1,013.7M. New locations added 27.1pp (Joe Hudson's alone 22.4pp) and same-store sales added 2.9pp (Q2FY26 MD&A, lines 229-233; Script, lines 4-12). Over time, revenue growth = same-store sales (SSS) growth + new-location growth. Management's long-term algorithm is 3–5% SSS plus 5–7% from new locations (FY2025 MD&A, line 130; management view).

### Factor 1.1 — Industry repairable-claims volume (the cyclical driver)

- **Mechanism:** "A high percentage of the Company's revenues are derived from insurance companies" (FY2025 MD&A, line 746). "The automobile collision repair industry is dependent on the number of accidents which occur and become repairable insurance claims" (FY2025 MD&A, line 696).
- **Evidence:**
    * Industry repairable claims fell ~9% in 2024 (FY2024 MD&A, line 274).
    * They fell 5–7% in 2025, improving from −9–10% in Q1'25 to −2–4% in Q4'25 (FY2025 MD&A, lines 59, 306).
    * SSS followed: +15.8% in FY2023 (FY2023 MD&A, line 357), −1.8% in FY2024 (FY2024 MD&A, line 274), −0.2% in FY2025 (FY2025 MD&A, line 306), and +2.2% in H1'26 (Q2FY26 MD&A, line 292).
- **Recent direction:** improving. Claims were "flat to down 2%" in Q2'26 (Q2FY26 MD&A, line 62). **Stage effect:** a shrinking headwind to SSS.
- **Sub-factors:**
    * **Accident frequency.** Collision-avoidance systems, ride sharing and driverless vehicles can reduce claims (FY2025 MD&A, line 698). Management's framework assumes −2%/yr from collision avoidance, offset by +1%/yr from miles driven (Q1FY26 call, line 67; management view). The FY2025 call adds "a 1% increase in the car park" yet still concludes the market is "kind of down 1%" (FY2025 call, line 151). That does not reconcile (−2+1+1=0), so I treat the baseline as 0% to −1%/yr (inference).
    * **Insurance premiums and deductibles.** "Significant insurance premium inflation" can cause deferred repairs and unfiled claims (FY2025 MD&A, line 696). Auto premiums are now "all but, you know, kind of like flat" (Q1FY26 call, line 353). Direction: headwind fading.
    * **Total-loss rate, driven by used-car prices and car-park age.** Written-off cars are not repaired (FY2025 MD&A, line 698). "If used car prices continue to rise, you'll see total losses continue to come down" (Q2FY26 call, line 211). Total losses are "essentially flat on a year-on-year basis" (Q2FY26 call, line 115). Management expects a long-run drift of "3/10 a year" (Q2FY26 call, line 139; management view). Direction: stabilizing.
    * **Macro conditions, employment and fuel.** A downturn could reduce claims "due to fewer miles driven… or due to vehicle owners being less inclined to have their vehicles repaired" (FY2025 MD&A, line 740). Direction: not measurable from the sources.

### Factor 1.2 — Average total cost of repair (TCOR / severity)

- **Mechanism:** TCOR is revenue per claim. Parts inflation, labor-rate inflation and vehicle complexity push it up. Older cars, aftermarket parts and repair-over-replace push it down (Q2FY26 call, lines 121-123).
- **Evidence:**
    * The framework assumes "3%-4% annual growth in average total cost of repair" (Q1FY26 call, line 67). TCOR has "historically been in that 4% range" (Q2FY26 call, line 233; management view).
    * Recently TCOR "remained below historical levels, which limited the level of same-store sales growth" (Q2FY26 MD&A, line 232). No TCOR figure is disclosed.
    * Repairing a vehicle aged 0–3 years costs "about $2,000 greater than the overall cost of a repair" (Q2FY26 call, line 123).
- **Recent direction:** flat to low. Q2 share gains produced SSS "with only limited contribution from total cost of repair ('TCOR') growth" (Q2FY26 MD&A, line 64).
- **Stage effect:** TCOR accounts for most of the gap between current SSS and the algorithm. With 0% TCOR, industry repairable dollars move −1% to 0% a year. With 3.5% TCOR they grow ~2.5–3.5% a year, depending on whether the car-park term is included (Script, line 24; inference).
- **Sub-factors:**
    * **Parts and labor inflation.** "Average labor rates for insurance carriers increase every single year… part prices increase… that's a simple pass-through" (Q1FY26 call, line 189; management view). Management says "we are not seeing pressure from labor rates with our insurance carriers" (FY2025 call, line 255).
    * **Mix: vehicle age, alternative parts, repair-vs-replace.** Higher total losses, more alternative parts and more repair-over-replace have held TCOR down (Q2FY26 call, lines 121-123; management view). Timing is unknown: "we don't really have a point of view on the timing" (Q2FY26 call, line 121).
    * **Tariffs.** Management assumes "tariff impacts are offset by client pricing" (Q2FY26 MD&A, line 94). There has been no material tariff impact to date (Q2FY26 MD&A, line 239).

### Factor 1.3 — Market-share gains within same-store (Boyd's controllable driver)

- **Mechanism:** insurers steer DRP volume to shops that perform well on "cycle time, quality of repair, customer satisfaction and cost of repair" (FY2025 MD&A, line 666). Capture rate and technician capacity decide how much of that demand becomes revenue (FY2025 MD&A, lines 700-704).
- **Evidence:**
    * SSS minus the industry-claims midpoint was +7.2pp (FY2024), +5.8pp (FY2025), +5.2pp (Q4'25) and +3.9pp (Q2'26) (Script, lines 14-19; my arithmetic). This spread includes TCOR, so it is not pure share.
    * Management credits a 2025 regional incentive realignment that ties field-leader pay to "the performance of their top 3 clients" (Q2FY26 call, line 171; management view).
    * July 2026 SSS was "positive in the low single digits, driven entirely by continued share gains" (Q2FY26 MD&A, line 66).
- **Recent direction:** still positive, but the spread is narrowing as the industry recovers. **Stage effect:** share gains are currently the main source of positive SSS.
- **Sub-factors:**
    * **Insurer DRP relationships and concentration.** "The loss of any existing material DRP relationship… could have a material adverse effect" (FY2025 MD&A, line 746). Customer percentages are not disclosed. The downside is asymmetric (inference).
    * **Technician capacity and productivity.** There is "a limited pool of qualified technicians and estimators" (FY2025 MD&A, line 658). Management says "we do have a little bit of capacity utilization still left", and the SSS swing "is really eating up a chunk of that capacity utilization" (Q2FY26 call, lines 163-165; management view). Capacity becomes the binding constraint if TCOR and claims both recover (inference).
    * **Market density.** Management aims "to be a number 1 or 2 player in the markets we serve", and says density is "the foundation for market share gains" (Q1FY26 call, line 71; management view).

### Factor 1.4 — New locations (acquisitions, start-ups, large MSO deals)

- **Mechanism:** each new store adds a revenue base. Acquired single shops take 12–24 months to reach projected sales, and start-ups take 24–36 months (Q2FY26 MD&A, line 480).
- **Evidence:** in Q2'26, 340 non-comparable stores contributed $211.3M, including $174.8M from Joe Hudson's 258 stores (Q2FY26 MD&A, line 231). That is about $700M annualized (Script, line 12). There were 1,323 locations at August 11, 2026 (Q2FY26 MD&A, line 9).
- **Recent direction:** a sharp step up from Joe Hudson's, which will drop out of the growth rate in 2027 (inference). H2'26 plans are three start-ups in Q3 and 10 in Q4 (Q2FY26 MD&A, line 74; management guidance). **Stage effect:** the dominant driver of reported growth in 2026.
- **Sub-factors:**
    * **Industry fragmentation and seller supply.** The market is roughly $50 billion (FY2025 MD&A, line 73). Listed risks include "acquisition market conditions change and repair shop owner demographic trends change" (Q2FY26 MD&A, line 94).
    * **Capital availability and leverage.** Pro-forma net leverage is 2.8x (Q2FY26 call, line 36), under covenant limits (Q2FY26 MD&A, line 398). A September 2026 buyback program (NCIB) now competes for the same cash (Knowledge Store ID 5). Leverage caps the pace of M&A (inference).
    * **Adjacent services (glass, scanning/calibration, GNCS).** Q1'26 gross margin was hurt by "a lower mix of glass sales" (Q1FY26 call, line 81). Segment sales are not disclosed.

---

## Stage 2: Gross profit

Gross margin was 45.5% in FY2023 and FY2024 (FY2024 MD&A, line 281), 46.4% in FY2025 (FY2025 MD&A, line 313), 46.9% in H1'26 (Q2FY26 MD&A, line 303) and 47.4% in Q2'26 (Q2FY26 MD&A, line 239). Every Stage 1 factor flows through gross profit. The factors below move the margin *rate*.

### Factor 2.1 — Parts and paint procurement (scale purchasing, rebates)

- **Mechanism:** Boyd "currently makes its own part sourcing decisions" (FY2025 MD&A, line 734). Central contracts and supplier rebates widen the spread between what insurers pay for parts and what Boyd pays.
- **Evidence:**
    * "Improvements to parts margin are a result of Project 360 initiatives to enhance direct parts procurement" (FY2025 MD&A, line 313).
    * Q4'25 paint margin improvement "related to an increase in paint rebates" (FY2025 MD&A, line 536).
    * Q2'26 saw "increased paint and parts margins driven by Joe Hudson's synergy realization and Project 360" (Q2FY26 MD&A, line 239).
    * The Joe Hudson's systems switch-over moved "much of the supply chain to a common contract" (Q2FY26 call, line 177).
- **Recent direction:** up. **Stage effect:** gross margin up. Risk: clients could "source products directly, impose the use of certain parts suppliers" (FY2025 MD&A, line 734).

### Factor 2.2 — Scanning and calibration internalization (sublet → in-house labor)

- **Mechanism:** this moves work from sublet, the lowest-margin category, to labor margin, "anywhere from 25-30 points of difference between those two categories" (FY2025 call, line 233; management view). Rising ADAS penetration grows the calibration pool (Q2FY26 call, line 203).
- **Evidence:** internalization was a gross-margin driver in FY2025 (FY2025 MD&A, line 313) and in Q2'26 (Q2FY26 call, line 91). It reached "80% to 85%, reaching a range management views as optimal" (Q2FY26 call, line 40).
- **Recent direction:** up, but near saturation. **Stage effect:** gross margin up. Future gains depend on calibration penetration growth, not on further internalization (inference).

### Factor 2.3 — Labor margin and insurer pricing (labor rates, performance-based pricing)

- **Mechanism:** insurers set labor rates and pay performance-based pricing tied to DRP KPIs. Labor margin is the gap between that rate and technician wages (FY2025 MD&A, line 658 on wage pressure).
- **Evidence:**
    * FY2024 gains "were offset by labor rate margins which remained below historical levels" (FY2024 MD&A, line 281).
    * Q2'26 gains were "partially offset by lower labor margins and variability in performance based pricing" (Q2FY26 MD&A, line 239).
    * FY2025 performance-based pricing improved through "improved alignment across our regional teams" (FY2025 call, line 93).
- **Recent direction:** negative and volatile. **Stage effect:** gross margin down, offsetting Factors 2.1 and 2.2.
- **Sub-factor: wage inflation versus insurer rate increases.** Management says "the price of a labor hour is gonna have to move commensurate with" labor costs (FY2025 call, line 255; management view). Any lag hits margin directly (inference).

### Factor 2.4 — Business mix (Joe Hudson's, glass, start-ups)

- **Mechanism:**
    * Joe Hudson's has a lower gross margin.
    * Glass has a different margin mix (FY2025 MD&A, line 732).
    * Start-ups may need "supplementing production staff wages" during ramp-up (Q2FY26 MD&A, line 480).
- **Evidence:**
    * "Offsetting these gross margin benefits is the impact of the lower gross margin percentage in the Joe Hudson's business" (Q2FY26 MD&A, line 239).
    * There was a lower glass mix in Q1'26 (Q1FY26 call, line 81).
- **Recent direction:** negative in 2026. **Stage effect:** gross margin down. The drag should fade as Joe Hudson's stores adopt Boyd's procurement and calibration practices (inference).

---

## Stage 3: Operating income (Adjusted EBITDA as the company-defined proxy)

Adj. EBITDA margin was 12.5% (FY2023) and 10.9% (FY2024) (FY2024 MD&A, line 297), 12.0% (FY2025) (FY2025 MD&A, line 329), and 13.4% (Q2'26) (Q2FY26 MD&A, line 257). The opex ratio was 33.0% and 34.6% (FY2024 MD&A, line 287), 34.4% (FY2025 MD&A, line 321), and 33.9% (Q2FY26 MD&A, line 245) over the same periods. Management's target is "returning to an Adjusted EBITDA margin of 14%" (Q2FY26 MD&A, line 221; management view). IFRS-16 rent sits below EBITDA and is handled in Stage 4.

### Factor 3.1 — Same-store volume (operating leverage on fixed costs)

- **Mechanism:** store fixed costs are spread over more or fewer repair orders.
- **Evidence:** the FY2024 margin decline "was primarily the result of declines in repairable claims volumes… which resulted in same-store sales declines and a higher ratio of operating expenses" (FY2024 MD&A, line 297). That works out to roughly 0.9pp of margin per 1% of SSS, a crude figure that also includes new-store drag (Script, line 33; inference). In Q2'26 the lower opex ratio "was also supported by the mitigating effect of same-store sales growth" (Q2FY26 MD&A, line 245).
- **Recent direction:** positive, "4 quarters in a row of positive same-store sales growth" (Q2FY26 call, line 233). **Stage effect:** margin up. This is the main channel through which the Stage 1 cycle reaches earnings.

### Factor 3.2 — Cost programs: Project 360 and Joe Hudson's synergies

- **Mechanism:** an indirect staffing model and consolidation of back office and procurement take cost out permanently.
- **Evidence:**
    * About $40M of savings were realized in 2025 (FY2025 MD&A, line 117), with indirect staffing savings "of more than $30 million" (FY2025 MD&A, line 321).
    * H1'26 synergy realization was about $35M, including about $15M in Q2 (Q2FY26 MD&A, lines 259, 319).
    * The $140M program's 2026 savings target was raised to $65M, with $35M more in 2027–2029 (Q2FY26 MD&A, line 70).
- **Recent direction:** up. **Stage effect:** margin up.
- **Consistency check:** the remaining ~$65M equals ~1.8pp of TTM sales. That would lift the 12.8% TTM margin to ~14.6%, above the 14% target (Script, lines 46-49). Management is therefore implicitly allowing for part of the savings to be offset by inflation or reinvestment (inference).

### Factor 3.3 — Wage and cost inflation versus pricing pass-through

- **Mechanism:** wages, facility costs and energy rise every year. Boyd must pass them through to clients or offset them with productivity (FY2025 MD&A, lines 658, 730, 926).
- **Evidence:** FY2025 opex savings were partly offset by "an investment in facilities maintenance costs, with spend in the year being elevated due to pent-up demand" (FY2025 MD&A, line 321).
- **Recent direction:** a steady headwind, not quantified. **Stage effect:** margin down, currently more than offset by Factors 3.1 and 3.2.

### Factor 3.4 — New-store ramp (start-up drag, Joe Hudson's opex profile)

- **Mechanism:** start-ups incur pre-opening costs "without sales revenue to offset these costs", and ramping stores leverage fixed costs poorly (Q2FY26 MD&A, line 480).
- **Evidence:**
    * New locations ran at a 36.9% opex ratio versus 34.6% overall in FY2024 (FY2024 MD&A, line 287).
    * The comparable figures were 36.1% versus 34.4% in FY2025 (OE & ROIC, line 242).
    * In H1'26, "a lower operating expense ratio in new stores, driven by the Joe Hudson's acquisition, positively contributed" (Q2FY26 MD&A, line 309).
- **Recent direction:** small positive in 2026. The start-up drag continues, with "32 startup locations already planned for 2026" (FY2025 call, line 139). **Stage effect:** minor, roughly $2–3M of excess opex (OE & ROIC, line 242).

---

## Stage 4: Owners' Earnings

OE was $132.4M (FY2023), $91.8M (FY2024), $108.9M (FY2025) and $145.9M (TTM Jun-26) (OE & ROIC, line 15). ROIC on total invested capital was 10.2%, 6.4%, 7.1% and 6.5%. On tangible capital it was 38.6%, 20.3%, 20.8% and 24.5% (OE & ROIC, lines 172-174). OE = Adj. EBITDA − cash rent − maintenance capex − software capex − normalized acquisition cost − 26.5% normalized tax (OE & ROIC, lines 30-38). All Stage 3 factors flow through to OE.

### Factor 4.1 — Occupancy cost (rent) and the leased-store model

- **Mechanism:** Boyd leases substantially all its shops and sells owned property in sale-leasebacks (OE & ROIC, line 47). Rent therefore scales with store count and lease renewals. It absorbs 41.2% of TTM Adj. EBITDA (Script, lines 37-42).
- **Evidence:** cash lease payments were $131.4M, $149.7M, $161.6M and $189.8M (FY2023–TTM) (OE & ROIC, line 100). Right-of-use depreciation rose due to "location growth and lease renewals" (FY2025 MD&A, line 335).
- **Recent direction:** up ~17% TTM versus FY2025 as Joe Hudson's leases were added ($189.8M / $161.6M − 1; my arithmetic). **Stage effect:** OE down in dollars. Rent is roughly stable as a share of sales (inference).

### Factor 4.2 — Maintenance capital intensity (equipment for vehicle complexity)

- **Mechanism:** shops must "upgrade or replace equipment to meet increased complexity of newer vehicles" (FY2025 MD&A, line 524).
- **Evidence:** guidance is 1.6–1.8% of sales for 2026 (FY2025 MD&A, line 526; management guidance). Actual equipment capex was 1.95%, 2.52%, 1.73% and 1.48% of sales (FY2023–TTM) (OE & ROIC, lines 59-64).
- **Recent direction:** low. H1'26 was 1.23% of sales, likely due to integration timing (OE & ROIC, line 66; inference). **Stage effect:** each 0.3pp of sales ≈ $7M of OE (OE & ROIC, line 200). Rising vehicle complexity pushes intensity up over time (inference).

### Factor 4.3 — Price paid for growth (acquisition multiples → goodwill → ROIC)

- **Mechanism:** acquisition prices do not change OE, but they set ROIC. About $2.3bn of goodwill and intangibles dilutes shop-level returns (OE & ROIC, line 20).
- **Recent direction:** worse. Invested capital nearly doubled to $2,902.5M at Jun-26, including $1,321.4M for Joe Hudson's, before a full year of Joe Hudson's OE (OE & ROIC, lines 152, 185). **Stage effect:** ROIC is 6.5% TTM, or ~8.6% pro forma if the remaining synergies land (OE & ROIC, line 185; inference).

### Factor 4.4 — Taxes (tax-deductible goodwill shields)

- **Mechanism:** tax-deductible acquisition goodwill and bonus depreciation keep cash taxes ($3.7M in FY2025) far below the ~26.5% statutory rate (OE & ROIC, line 87).
- **Direction:** the shield continues as long as acquisitions continue. OE uses the statutory rate, so reported cash generation exceeds OE (OE & ROIC, line 87). This is not a lever on the underlying economics.

---

## Sensitivity: which factors matter most for OE (TTM base OE $145.9M)

| Driver change                                  | OE impact  | % of OE | Source / caveat                        |
|------------------------------------------------|------------|---------|----------------------------------------|
| Remaining ~$65M synergies fully drop through   | +$47.8M    | +33%    | Script, line 47; partly offset       |
| +100bp Adj. EBITDA margin (any source)         | +$26.4M    | +18%    | Script, line 43                      |
| +1% SSS at ~47% gross-margin flow-through      | +$12.4M    | +9%     | Script, line 45; upper bound         |
| +0.3pp of sales in maintenance capex           | −~$7M      | −5%     | OE & ROIC, line 200                  |

## What is confident vs uncertain

**Confident (reported data):**

- Revenue is driven by industry claims × TCOR × share, plus store additions. The 2024–25 claims downturn and the 2026 recovery show up clearly in SSS and margins (Factor 1.1 citations).
- Operating leverage on same-store volume is large: −1.8% SSS cost 1.6pp of margin in FY2024 (FY2024 MD&A, lines 274, 297).
- Procurement and calibration internalization lifted gross margin by 140bp (H1'26 versus FY2024) to 190bp (Q2'26), net of the Joe Hudson's mix drag (FY2024 MD&A, line 281; Q2FY26 MD&A, lines 239, 303).
- Rent and maintenance capex absorb ~55% of Adj. EBITDA, and OE is ~32% of it (Script, lines 37-42).

**Uncertain:**

- **TCOR timing** is the largest swing factor, and management has no view on it (Q2FY26 call, line 121).
- **Durability of share gains:** the spread is narrowing and capacity may cap it (inference).
- **Net synergy drop-through:** the 14% target implies part is offset (inference).
- **Structural decline in claim frequency:** the −2%/yr figure is management's assumption (Q1FY26 call, line 67).
- **Insurer concentration** is undisclosed, and the downside is asymmetric (inference).
