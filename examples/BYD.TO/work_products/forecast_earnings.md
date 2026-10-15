# Boyd Group Services (BYD.TO / BGSI): Owners' Earnings Forecast, FY2026E–FY2031E

*Prepared 2026-09-25 (ROIC-method rework). All figures are US$ millions. Every number in this document comes from `work_products/forecast_earnings.py` (run `uv run python work_products/forecast_earnings.py`), except the unit-count history and funding check in §6.1a, which come from `work_products/unit_growth_capital_check.py` (it imports the forecast model and reads its outputs). Owners' Earnings (OE) is defined exactly as in `work_products/owners_earnings_and_roic.md` ("OE & ROIC"), and the drivers follow `work_products/causal_model.md` ("Causal model"). The stock price is not used anywhere. The previous margin-method model is kept as `work_products/forecast_earnings_margin_method.py` (still imported by `new_location_unit_economics.py`).*

**Source key** (citations use "short name, line xx"):

| Short name     | File                                                            |
|----------------|-----------------------------------------------------------------|
| Q2FY26 MD&A    | `primary_sources/Q2FY26/BoydGroup_MDA.md`                       |
| Q2FY26 FS      | `primary_sources/Q2FY26/BoydGroup_Q2.md`                        |
| Q2FY26 call    | `primary_sources/Q2FY26/earnings_call_transcript.md`            |
| Q1FY26 call    | `primary_sources/Q1FY26/earnings_call_transcript.md`            |
| Q2FY25 call    | `primary_sources/Q2FY25/earnings_call_transcript.md`            |
| Q1FY25 call    | `primary_sources/Q1FY25/earnings_call_transcript.md`            |
| FY2025 MD&A    | `primary_sources/FY2025/BoydGroup_MDA.md`                       |
| FY2025 AFS     | `primary_sources/FY2025/BoydGroup_AFS.md`                       |
| FY2025 call    | `primary_sources/FY2025/earnings_call_transcript.md`            |
| FY2024 MD&A    | `primary_sources/FY2024/Boyd_MDA.md`                            |
| FY2024 AFS     | `primary_sources/FY2024/Boyd_AFS.md`                            |
| FY2023 MD&A    | `primary_sources/FY2023/Boyd_MDA.md`                            |
| JH release     | `fetched_docs/boyd_joe_hudsons_acquisition_announcement.md`     |
| OE & ROIC      | `work_products/owners_earnings_and_roic.md`                     |
| Unit econ.     | `work_products/new_location_unit_economics.md`                  |
| Unit check     | `work_products/unit_growth_capital_check.py` (script output)    |

---

## 1. Headline answer

| Owners' Earnings (US$M)                 | 2026E   | 2027E   | 2028E   | 2029E   | 2030E   | 2031E   |
|-----------------------------------------|---------|---------|---------|---------|---------|---------|
| Bear (25%), new-location ROIC 9%        |     156 |     158 |     158 |     158 |     153 |     148 |
| **Base (50%), new-location ROIC 13%**   | **176** | **200** | **225** | **254** | **277** | **302** |
|   of which existing business            |     176 |     197 |     215 |     234 |     246 |     259 |
|   of which locations opened 2026+       |       0 |       3 |       9 |      20 |      31 |      43 |
| Bull (25%), new-location ROIC 17%       |     188 |     229 |     269 |     317 |     359 |     405 |
| **Probability-weighted OE**             | **174** | **197** | **219** | **246** | **267** | **289** |
| Base: growth capex                      |   (116) |   (143) |   (147) |   (151) |   (156) |   (160) |
| Base: one-off integration cost          |    (19) |    (13) |       – |       – |       – |       – |
| **Base: distributable**                 |  **41** |  **45** |  **78** | **102** | **122** | **142** |
| Weighted distributable                  |      39 |      48 |      79 |     102 |     119 |     137 |
| *Existing business only: OE*            |     176 |     197 |     215 |     234 |     246 |     259 |
| *Existing business only: distributable* |     157 |     184 |     215 |     234 |     246 |     259 |

*Rows are rounded independently, so components may differ from totals by ±1.*

*What changed in this revision.* New locations opened from 2026 no longer earn the network EBITDA margin. They now have their own earnings stream: **mature store EBITDA after rent = ROIC × location cost**. That stream ramps on a simple schedule (0 in the year the capex is spent, then 1/3, 2/3 and full earnings in the following three years) and is added to the existing-business earnings. Maintenance capex, software capex and tax are then applied at the corporate level to the combined business. Base OE was $2–13M/yr lower than in the margin-method version, mostly because new capex earns nothing in its first year. *Second revision (judge):* the ramp was simplified from a mid-year linear schedule to 0 / 1/3 / 2/3 / 1; OE changes by ≤ $3M in any year. The mature economics are almost the same, because a 13% ROIC implies the same unit margin the old model assumed (network + ~1pp) (§6.3). *Third revision (judge):* the separate revenue-ramp build for the 2022–25 location cohorts was removed. The existing business is now just two parts, legacy Boyd and JH, each grown with SSS (§4.2). Base OE falls by $1–7M/yr (2031E $296M vs $303M). *Fourth revision (judge):* existing-business rent is now forecast in dollars as H1-2026 cash rent × 2, escalated each year, replacing the rent-ratio drift and sale-leaseback rent (§5.3). Base OE rises by $0–6M/yr (2031E $302M). *Fifth revision (reviewer):* §6.2 now shows, for each year, the sales and OE that all locations opened to date would earn if already mature. A new §6.1a justifies the unit counts against history, management's 5–7% target and a funding check. The forecast itself is unchanged. The one visible change is that the 2031 run-rate check now also grows cohorts with SSS after they mature, as the forecast already does: base ~$67M (was ~$66M), bull $115M (was $113M).

The historical anchors are TTM Jun-2026 OE of $145.9M and FY2025 OE of $108.9M (OE & ROIC, line 15).

**What drives the numbers.**

1. **2026E OE of ~$176M is almost all existing business and mostly in hand.** It comes from a full year of Joe Hudson's (JH), $65M of 2026 savings that are largely realized or scheduled (Q2FY26 MD&A, line 70), and H1 margins already reported. The implied H2-2026 margin of 13.9% is in line with management's ~+40bp-per-quarter cadence from Q2's 13.4% (Q2FY26 call, line 105). **High confidence.**
2. **The existing business grows OE ~8%/yr (176 → 259).** The drivers are ~3% same-store sales (SSS), ~20bp/yr of operating leverage and the last $35M of savings. This is the part the ROIC assumption does not touch.
3. **New locations add $43M of OE by 2031E, and ~$67M once the 2026–31 cohorts are all mature.** That return is on ~$873M of growth capex, a mature OE yield of ~7.7% at a 13% ROIC (§6.4). Growth spending creates modest value at an ~8% discount rate. In the bear case (9%) it roughly destroys value, and in the bull case (17%) it creates a lot.
4. **Management's "north of 20%" ROIC is not used in the base case.** At Boyd's current tuck-in prices and start-up costs, a blended 20% needs new units to run a ~21% pre-rent EBITDA margin. The existing network runs ~14%, and JH reaches that level only with 100% of synergies (§6.3). I use 13% for the base, 17% for the bull and 9% for the bear.
5. **The biggest swing factors are still industry repair cost (TCOR) and share gains.** New-location ROIC matters less over the forecast window. For FY2029E OE, TCOR ±1pp/yr moves it +9%/−15%, losing share gains −17%, and ROIC 20% instead of 13% only +5% (§8). The ROIC matters much more for value than for 2026–31 OE, because it decides whether ~$150M/yr of growth capex earns its cost of capital.

---

## 2. Load-bearing assumptions (base case) and confidence

| Driver                                  | Base assumption                   | Evidence                                          | Confidence |
|-----------------------------------------|-----------------------------------|---------------------------------------------------|------------|
| Industry repairable-claims volume       | −1.0%/yr                          | 0 to −2% in Q2'26; mgmt −2% + 1% miles framework  | Medium     |
| Avg total cost of repair (TCOR)         | 1.2% (2026), 2.0%, then 3.0%      | CCC 2025 +1.7%; used-car prices flat              | **Low**    |
| Boyd share gain                         | +2.0pp (2026) → +1.0pp by 2028    | SSS−claims spread 7.2→3.9pp and narrowing         | Medium-low |
| Savings retained (of $140M program)     | 80%                               | Mgmt 14% target < full drop-through               | Medium     |
| Operating leverage (existing business)  | 0.3 × (SSS − 2.3%), capped        | Mgmt ~20bp at 2–4% SSS; FY2024 −1.6pp             | Medium     |
| Rent (existing business, $)             | H1'26 × 2 = $216M, +2.5%/yr       | H1'26 actual; H1'25 × 2 within 1.3% of FY2025     | High       |
| New locations                           | 52 (2026), then 62/yr (4.6%→3.9%) | 75/yr 2023–25; pipeline 8/qtr × 2 ≈ 64 (§6.1a)    | Medium     |
| **New-location ROIC (pre-maint., tax)** | **13%** (bear 9%, bull 17%)       | Mgmt "north of 20%"; network parity ~11.7%        | **Low**    |
| Location cost                           | Tuck-in $2.8M; start-up $1.7M     | 2025 / H1'26 deals; 2022–25 pooled start-up cost  | Medium     |
| New-location sales at maturity          | Tuck-in $2.90M; start-up $2.95M   | 2025 pro-forma acquired revenue; revenue per loc. | Medium     |
| Ramp to maturity                        | 0, 1/3, 2/3, 1 (year of capex = 0)| "reach maturity by the end of their third year"   | Medium     |
| Maintenance + software capex            | 1.7% + 0.2% of all sales          | Mgmt guidance 1.6–1.8%                            | Medium     |
| Tax on OE                               | 26.5% statutory                   | OE & ROIC §2.6                                    | High       |

---

## 3. Method: two earnings streams, then corporate deductions

```
(A) EXISTING BUSINESS  = legacy Boyd (locations open at 31-Dec-2025) + Joe Hudson's (closed Jan-2026)
    SSS_t        = industry claims volume + TCOR + Boyd share gain
    Sales_t      = legacy_(t-1) × (1+SSS_t) + JH_t      [legacy_2025 = FY2025 pro-forma sales $3,235.8M]
    EBITDA_t     = legacy × underlying margin_t + JH × JH margin_t + 80% × program savings_t
                   underlying margin_t = margin_(t-1) + 0.3 × (SSS_t − 2.3%)   [capped +0.30 / −0.40pp]
    Rent_t       = Rent_(t-1) × (1 + escalator);  Rent_2026 = H1-2026 cash rent × 2 = $215.9M
(B) NEW LOCATIONS (opened 2026 onward: tuck-ins + start-ups)
    EBITDA after rent_t = Σ cohorts ROIC × location cost × ramp(age) × SSS growth after maturity
                   ramp = 0 in the capex year, then 1/3, 2/3, 1 (e.g. 2026 capex: 1/3 in 2027, full 2029)
    Sales_t      = Σ cohorts units × mature revenue × same ramp
CORPORATE
    OE_t = [(A) EBITDA − (A) rent + (B) EBITDA after rent
            − maint. capex % × (A+B) sales − software % × (A+B) sales − $5M deal cost] × (1 − 26.5%)
    Distributable_t = OE_t − growth capex (units × location cost) − one-off integration costs
```

**Why split the streams.** The two parts have different causes. The existing business depends on the industry (claims, TCOR), share gains, savings and operating leverage. New locations depend on how much Boyd spends and what that spending earns. With a single system-wide margin, the return on growth capex was an output buried inside the margin, so it could not be tested directly. Now it is an explicit input, the ROIC, and §6.3 tests it against the unit margins it implies.

**The ROIC definition** follows the task: mature store EBITDA after rent ÷ location cost, before maintenance capex and tax. This is the "pre-tax four-wall cash-on-cash" convention used in Unit econ., §4.4. Charging maintenance and software capex on new-location sales at the corporate rates makes the new stream bear its share of those costs.

**Existing business = legacy Boyd + JH.** Every location open at 31-Dec-2025 is legacy Boyd; its capex is sunk. JH closed on 9-Jan-2026 and its price is also sunk. Both parts grow only with SSS; there is no separate ramp for young locations (§4.2).

**Current year.** FY2026E is built as a whole year from FY2025, with H1-2026 actuals used only as a cross-check (§9) and to set 2026 rent and JH revenue.

---

## 4. Existing business: revenue drivers

### 4.1 Same-store sales = claims + TCOR + share

| SSS build (pp)                 | 2026E   | 2027E   | 2028E   | 2029E   | 2030E   | 2031E   |
|--------------------------------|---------|---------|---------|---------|---------|---------|
| Industry claims volume (base)  |    −1.0 |    −1.0 |    −1.0 |    −1.0 |    −1.0 |    −1.0 |
| TCOR (base)                    |     1.2 |     2.0 |     3.0 |     3.0 |     3.0 |     3.0 |
| Boyd share gain (base)         |     2.0 |     1.5 |     1.0 |     1.0 |     1.0 |     1.0 |
| **Base SSS**                   | **2.2** | **2.5** | **3.0** | **3.0** | **3.0** | **3.0** |
| Bear SSS                       |     2.0 |     1.0 |     1.5 |     1.5 |     1.5 |     1.5 |
| Bull SSS                       |     2.2 |     4.5 |     5.0 |     5.0 |     4.5 |     4.5 |

**Claims volume, −1%/yr.** Claims recovered from −9–10% in Q1'25 (FY2025 MD&A, line 59) to "flat to down 2%" in Q2'26 (Q2FY26 MD&A, line 62). Premium inflation "has almost turned to a deflationary category" and total losses are "essentially flat" (Q2FY26 call, lines 113-115). The long-run level is management's framework of −2%/yr from collision-avoidance systems offset by +1% from miles driven (Q1FY26 call, line 67). That is an assumption, not a measurement (Causal model, Factor 1.1).

**TCOR is the least certain input.** Management has "no point of view on the timing" (Q2FY26 call, line 121). TCOR "remained below historical levels" in Q2'26 (Q2FY26 MD&A, line 232), and industry TCOR rose only 1.7% in 2025, the slowest since 2017 (Knowledge Store ID 7). The recovery mechanism management relies on is higher used-car prices cutting total losses (Q2FY26 MD&A, line 516), but Manheim values were only +0.4% YoY in August 2026 after two monthly declines (Knowledge Store ID 8). I hold 1.2% in 2026 and 2.0% in 2027, then 3.0%. That is below the historical "4% range" (Q2FY26 call, line 233). Structural support comes from calibrations, now on 28.3% of estimates against 21.8% a year earlier (Knowledge Store ID 7), and from ~$2,000 higher repair costs on 0–3-year-old cars (Q2FY26 call, line 123). The bear case holds 1.5–2.0%, and the bull case reaches 4%.

**Share gains, +2.0pp fading to +1.0pp.** July 2026 SSS was positive "driven entirely by continued share gains" (Q2FY26 MD&A, line 66). Management credits insurer-aligned incentives (Q2FY26 call, line 171). I fade the gain because the SSS-minus-claims spread is narrowing (7.2pp to 3.9pp, Causal model, line 27) and technician capacity is being "eaten up" (Q2FY26 call, lines 163-165) (inference). The 2026 split was chosen to match H1'26 SSS of 2.2% (Q2FY26 MD&A, line 292), so that match is by construction and does not test the model.

### 4.2 The two parts: legacy Boyd and Joe Hudson's

* **JH.** Sales were $722M and the Adj. EBITDA margin (pre-rent) 14.4% in the twelve months to June 2025 (JH release, line 14). 2026 sales are set at $700M, because H1 was $342.6M (Q2FY26 MD&A, line 291) and conversion disruption "continued into the third quarter" (Q2FY26 MD&A, line 72). The 2026 margin is 13.0%: ~$22M of lost sales × ~46% gross margin ≈ $10M (inference). From 2027, sales return to the $722M run rate grown with SSS, at the 14.4% pre-synergy margin. JH synergies sit in the savings line (§5.1).
* **Legacy Boyd** starts from FY2025 pro-forma revenue of $3,235.8M, i.e. revenue "if 2025 acquisitions had been acquired on January 1, 2025" (FY2025 AFS, line 713). This annualizes the 43 locations bought during 2025 (+$93.0M over reported $3,142.8M). From then on it grows with SSS only. That is reasonable because SSS "includes only those locations in operation for the full comparative period" (FY2025 MD&A, line 232): a young store's later ramp shows up in SSS once it has been open a full year, and the SSS inputs are calibrated to reported SSS (§4.1). The FY2025 underlying margin (ex-savings) is applied to the whole pro-forma base. That is an assumption, since the 2025 acquisitions lost $2.0M on $31.5M of in-year revenue (FY2025 AFS, line 713). *What this simplification misses:* ramp revenue from stores opened in 2025 that are not yet in the SSS base, and 2026 openings in their first year. The script's seasonality check puts base H2-2026 sales ~$46M (1.2% of FY sales) below the FY2025 H2/H1 pattern, worth roughly $2M of OE (§9). I accept that small understatement in exchange for dropping the cohort ramp inputs (judge direction).

---

## 5. Existing business: margin and cost drivers

### 5.1 Project 360 and JH savings, retained at 80%

Savings in the P&L relative to 2024 costs are $40M in 2025, $105M in 2026 and $140M by 2029 (Q2FY26 MD&A, lines 70, 221). I keep 80% and assume 20% is absorbed by inflation or reinvestment (inference). Full drop-through would take the TTM 12.8% margin to ~14.6%, above management's 14% target (Causal model, Factor 3.2). Bear keeps 60%, bull 100%.

### 5.2 Operating leverage, 0.3 × (SSS − 2.3%)

Two anchors set the coefficient. Management expects "a steady level of same-store sales growth in that 2%-4% range… kind of a 20 basis point improvement" (FY2025 call, line 281). In FY2024, SSS of −1.8% came with a 1.6pp margin decline (FY2024 MD&A, lines 274, 297). Technician wage inflation runs "at call it CPI levels" (Q1FY26 call, line 303). The +0.30pp/yr cap (technician capacity) and −0.40pp/yr floor (management cost response) are inference.

| Adj. EBITDA margin                  | 2026E | 2027E | 2028E | 2029E | 2030E | 2031E |
|-------------------------------------|-------|-------|-------|-------|-------|-------|
| Existing business, bear             | 13.0% | 13.0% | 12.9% | 12.8% | 12.6% | 12.3% |
| Existing business, base             | 13.4% | 13.9% | 14.2% | 14.6% | 14.7% | 14.9% |
| Existing business, bull             | 13.7% | 14.4% | 14.8% | 15.3% | 15.4% | 15.6% |
| Consolidated, base (memo)           | 13.4% | 13.9% | 14.2% | 14.6% | 14.7% | 14.8% |

The consolidated memo line adds new-location EBITDA grossed up for rent at the network ratio. It is close to the existing business because ramping units earn little. The base existing-business margin passes management's 14% target (Q2FY26 MD&A, line 221) in 2028 and reaches 14.9% by 2031. **That is above management's target and is a flag.** For reference, FY2023 was 12.5% and FY2025 12.0%.

### 5.3 Rent (existing business)

Rent is forecast directly in dollars (judge direction). FY2026E = H1-2026 cash rent × 2: property and vehicle lease principal of $72.6M + $2.9M and lease interest of $31.9M + $0.5M = $107.9M (Q2FY26 FS, lines 167-168, 171-172), × 2 = $215.9M. This includes JH. Doubling H1 is a fair full-year proxy: on the same basis 2025 gives $79.7M × 2 = $159.4M against actual FY2025 cash rent of $161.6M (−1.3%; OE & ROIC, line 100). The shortfall mostly reflects stores added during the year, which from 2026 sit in the new-location stream. After 2026, rent grows by the escalator: 2.5% base and bull, 3.0% bear (assumption). The existing footprint is fixed, so rent does not grow with sales, and the rent ratio drifts from 5.39% to 5.25% of sales by 2031E in the base (5.80% in the bear, where SSS of 1.5% lags the 3% escalator). The escalator is not directly sourced. Boyd attributes rising right-of-use costs to "location growth and lease renewals" (FY2025 MD&A, line 335) but discloses no escalation terms. A 3.0% instead of 2.5% escalator costs ~$3M of FY2029E OE (§8). *Sale-leasebacks are dropped from the model.* They used to add rent at a 7.5% yield plus cash proceeds in the leverage check. Removing only the rent would count the cash without its cost. Removing both is consistent, and it fits Boyd's switch to outsourced start-up development, where "ownership will transfer directly to a leasing company" (FY2025 MD&A, line 376). The cost is that base leverage is 0.05–0.17x higher than in the previous version, which had $30M of 2026 and $20M/yr later proceeds (§7).

### 5.4 Capex, deal costs, tax (applied to the combined business)

* **Maintenance capex:** 1.7% of total sales in the base, the midpoint of the 1.6–1.8% guidance (Q2FY26 MD&A, line 486). Bear 2.0%, in line with the 1.95–2.52% of FY2023–24 (OE & ROIC, lines 59-62). Bull 1.6%. H1'26 ran at 1.4% of sales excluding JH (Q2FY26 MD&A, line 484), so 1.7% is conservative for 2026.
* **Software capex:** 0.2% of sales (actuals 0.16–0.26%, OE & ROIC, line 103).
* **Deal costs and tax:** $5M normalized deal cost and 26.5% statutory tax (OE & ROIC, §2.5–2.6). Cash taxes will run lower while Boyd acquires (JH alone carries ~$150M of expected tax benefits, JH release, line 43). This is excluded from OE and can be valued separately.

---

## 6. New locations: a separate ROIC-based earnings stream

### 6.1 Unit count, location cost and location sales

| Input                         | Value                  | Source                                                             |
|-------------------------------|------------------------|--------------------------------------------------------------------|
| Units (base)                  | 25+27 (2026), 30+32/yr | See below                                                          |
| Tuck-in cost per location     | $2.8M                  | $120.8M / 43 (2025); $18.9M / 7 (H1'26) = $2.69M                   |
| Tuck-in sales per location    | $2.90M                 | 2025 acquisitions' pro-forma revenue $124.5M / 43                  |
| Start-up cost per location    | $1.7M                  | 2022–25 pooled $133.7M / 79; mgmt $1.2–1.4M; 2025 $2.0M            |
| Start-up sales at maturity    | $2.95M                 | Avg. revenue per location: network $3.10M, JH $2.80M               |
| Cost inflation                | 3%/yr                  | Assumption                                                         |

* **Tuck-in cost and sales.** In 2025, 21 acquisitions added 43 collision locations and one calibration business for total consideration of $120.8M (FY2025 AFS, lines 644, 662). Had they been owned all year, revenue would have been $3,235.8M instead of $3,142.8M, and they contributed $31.5M after acquisition (FY2025 AFS, line 713). That gives $124.5M of pro-forma revenue, or $2.90M per location, bought at 0.97x sales. H1'26 tuck-ins cost $18.9M (Q2FY26 FS, line 261) for 3 + 4 locations (Q2FY26 MD&A, lines 55-56), or $2.69M each. Both years are above the 2023–25 average used before ($2.3M), so I update the price to the recent level.
* **Start-up cost.** Leaseholds and equipment per opening were $0.95M, $1.62M, $1.92M and $2.00M in 2022–25, pooled $1.69M (Unit econ., §4.2; FY2025 MD&A, line 520). Management describes the outsourced greenfield model as "a 1,200,000.0 to $1,400,000 investment in the location" (Q2FY25 call, line 146), where a developer builds and a leasing company takes ownership (Q2FY25 call, line 74). I use $1.7M, between the forward-looking claim and the latest actual. Pre-opening losses are not included in the cost (Q2FY26 MD&A, line 480), so the true all-in cost is somewhat higher (not quantified).
* **Start-up sales** use average revenue per collision location as the maturity proxy (network $3,142.8M ÷ avg. of 984 and 1,043 locations = $3.10M, Knowledge Store ID 10, Q1FY26 call, line 71; JH $722M ÷ 258 = $2.80M, JH release, line 14).
* **Units.** 2026 is 52: 9 acquisitions and 14 start-ups through Aug-11 (Q2FY26 MD&A, lines 55-58), 13 start-ups planned for H2 (Q2FY26 MD&A, line 74) and ~16 more acquisitions in H2. The 16 is inference (the 25 assumed for the year less 9 through Aug-11). Management gives only the direction: "expect acceleration as we get into the back half of the year" and "a really strong fourth quarter" (Q2FY26 call, lines 155-157). From 2027 it is 62/yr: 32 start-ups ("8 or so a quarter", Q2FY26 call, line 159) plus 30 tuck-ins, close to management's ~50/50 mix (FY2025 MD&A, line 95). Bear adds 35/yr, bull 76/yr. **Large MSO deals like JH are excluded.** §6.1a compares these counts with history and management's target and checks whether Boyd can fund them.
* **New-location sales** drive only maintenance/software capex and the memo sales line. For simplicity they follow the same ramp as earnings. Base new-location sales are $0 in 2026, $175M in 2028 and $821M in 2031. This understates acquired shops' early revenue, which arrives on day one; the effect on OE is under $1M/yr (1.9% capex × ~$30–50M of missing revenue, inference).


### 6.1a Are the unit counts reasonable? History, target and funding

All numbers in this subsection come from `work_products/unit_growth_capital_check.py`. This is a rough check, not a second model.

**Where the 62/yr comes from.** It is not derived from a growth rate. It is the start-up pipeline times two. Management targets "8 or so a quarter" start-ups (Q2FY26 call, line 159), from a pipeline of "approximately 8 to 10 new start-up locations per quarter", and expects "approximately 50% of new location growth to come from start-ups" (FY2025 MD&A, line 95). That gives 32–40 start-ups and 64–80 total units a year. The base uses the bottom of that range, slightly shaded: 32 start-ups + 30 tuck-ins = 62. The earlier write-up called this "~4.5% unit growth". More precisely, it is **4.6% of the opening location count in 2027, falling to 3.9% by 2031**, because the count is held flat while the network grows. Measured as mature revenue added, it is 4.7% of prior-year sales in 2027 and 4.2% in 2031 (Unit check).

**Comparison with history.**

| Period     | Acq. | Start-ups | Total | Net growth spend | Per unit | Net spend ÷ OE |
|------------|------|-----------|-------|------------------|----------|----------------|
| 2023       |   78 |        28 |   106 | $177.5M          | $1.67M   | 134%           |
| 2024       |   37 |        12 |    49 | $127.6M          | $2.60M   | 139%           |
| 2025       |   43 |        27 |    70 | $165.3M          | $2.36M   | 152%           |
| H1-2026    |    7 |        14 |    21 | $32.9M           | $1.56M   | –              |
| Base 2027E |   30 |        32 |    62 | $143M            | $2.30M   | 71%            |
| Base 2031E |   30 |        32 |    62 | $160M            | $2.59M   | 53%            |

*Units: FY2023 MD&A, line 33; FY2024 MD&A, line 43; FY2025 MD&A, lines 45-51; Q2FY26 MD&A, lines 55-56. Net growth spend = "Acquisition and development of businesses" less sale-leaseback proceeds (FY2024 AFS, lines 291, 294; FY2025 AFS, lines 310, 312; Q2FY26 FS, lines 178, 180, less JH cash paid of $1,304.8M, line 261). OE from OE & ROIC, line 15. I net out sale-leasebacks because the model has none (§5.3): under the outsourced model the developer funds the land and building.*

1. **Count.** 2023–25 averaged 75 units a year (53 acquisitions, 22 start-ups). Gross unit growth was ~5.2% in 2024 (49 on ~935 locations, before 2024 closures, which are not disclosed) and 7.1% in 2025 (70 on 984, Knowledge Store ID 10). Net of 11 closures, 2025 growth was 6.0% (984 + 70 − 1,043; the 1,043 is 1,301 less JH's 258, Knowledge Store ID 6). The base's 62 is below the 2023–25 average in absolute terms, and ~4–4.6% is below the 5–7% of 2024–25 in percentage terms. The mix is different: fewer acquisitions (30 vs 53) and more start-ups (32 vs 22). The start-up count is supported by the 27 in 2025 and the pipeline. The acquisition count is supported only weakly: 2026 YTD is just 9 (Q2FY26 MD&A, line 58), against 43 in 2025.
2. **Cost per unit.** The model's blended $2.23M (2026) to $2.59M (2031, with 3%/yr inflation) is above the pooled 2023–H1'26 net spend of $2.05M per unit, and close to 2025's $2.36M. The unit cost is not understated. If anything it is slightly conservative.
3. **Against management's target.** The 5–7% target is stated "over the long-term" (FY2025 MD&A, line 91) and restated as "5%-7% average annual unit growth" (Q1FY26 call, line 69), so it is correct to compare it with unit counts. On the enlarged base it would take 68–95 units in 2027, rising to 80–112 by 2031. The base is below the low end in every year. Closures (11 in 2025) are not modeled, so the net rate would be ~1pp lower still if they recur (inference).

**Can Boyd fund it? Base-case sources and uses.** "Available" = OE − one-offs − after-tax interest ($60M × (1 − 26.5%) = $44M, Q2FY26 MD&A, line 390) − dividends ($13M). OE is taxed at the statutory rate, so this understates cash: actual cash taxes are far lower while goodwill is being amortized for tax (OE & ROIC, §2.6).

| Base (US$M)                        | 2026E | 2027E | 2028E | 2029E | 2030E | 2031E |
|------------------------------------|-------|-------|-------|-------|-------|-------|
| Available before growth            |   100 |   130 |   168 |   196 |   220 |   245 |
| Growth capex                       |  −116 |  −143 |  −147 |  −151 |  −156 |  −160 |
| Coverage (available ÷ growth)      |   86% |   91% |  114% |  130% |  141% |  153% |
| Surplus (buybacks / debt paydown)  |   −16 |   −12 |    21 |    45 |    64 |    85 |
| Net debt ÷ (EBITDA − rent)         | 3.00x | 2.73x | 2.41x | 2.06x | 1.76x | 1.46x |
| Extra debt capacity at 2.7x        |     – |    97 |   103 |   123 |   105 |   111 |

*2026 net debt moves only by the H2 cash flow, because the starting point is Jun-26 net debt (§7). "Extra debt capacity" = 2.7x × the year's increase in EBITDA − rent. That is how much more Boyd could borrow each year while holding leverage at 2.7x, the level the JH release targets "potentially as early as the end of 2027" (JH release, line 47). This is the same ratio definition as the model: net debt before leases ÷ Adj. EBITDA after lease payments.*

* **2026–27 is the binding constraint.** Modeled internal cash covers only 86–91% of growth capex, so the 62/yr is funded partly with debt, and leverage falls only because EBITDA grows. YE-2027 lands at 2.73x, on management's 2.7x target. *On the model's own cash build*, then, there is no room for buybacks in 2026–27 without running above target. In May 2026 the CFO said buybacks over growth were "not in the cards in the near term" (Q1FY26 call, line 259). Yet management authorized an NCIB in September 2026 as "another capital allocation option ... while continuing to pursue strategic acquisitions" (Knowledge Store ID 5; size not in the sources). Two things reconcile this, and both are rough (Unit check, NCIB line). (a) The model taxes OE at the statutory 26.5%. If cash taxes stay at their FY2023–25 ratio to normalized tax (37%, OE & ROIC, line 87), actual cash is ~$66M higher over H2-2026 and 2027 ($20M + $46M). That would pay for a buyback of about that size with no change to the leverage path. (b) Management may accept running above target for a while: each $100M bought back by YE-2027 adds \~0.28x (2.73x → 3.01x). So the 2026–27 buyback capacity consistent with the 2.7x target is **\~$0–65M, not zero**. That is small next to growth capex of ~$201M over the same period, so it does not change the 62/yr unit count.
* **From 2028 cash is not the constraint.** OE covers growth capex 1.1–1.5x. Cumulative 2028–31 surplus is $215M. If all of it went to buybacks with net debt held at the YE-2027 level, leverage would still fall to 1.87x by 2031 through EBITDA growth. On top of that, holding leverage at 2.7x would support ~$100–120M/yr of extra borrowing. So the flat 62/yr from 2028 is a **choice**, not a funding limit. My judgment is that Boyd splits the post-2027 surplus between buybacks, deleveraging and units, and the NCIB points that way. That is an assumption, not a sourced fact.
* **Reinvestment rate is well below history.** Boyd put 134–152% of OE into new units in 2023–25. In 2023–24, net growth spend exceeded OE by $80.9M, and that gap plus interest and dividends was funded with debt: net debt before leases rose $142.2M, from $345.1M at end-2022 to $399.2M at end-2023 (FY2023 MD&A, line 432) and $487.3M at end-2024 (FY2024 MD&A, line 350). *(Corrected in r1: the previous version quoted $963.0M → $1,231.6M, which is total debt net of cash **including** lease liabilities, the wrong basis.)* 2025 is not comparable, because the JH financing (US IPO and senior notes, FY2025 AFS, line 962) was raised in Q4 and left Boyd with net cash of $290.7M before leases at year-end (FY2025 call, line 107). The base reinvests 71% of OE in 2027 and 53% by 2031. That fits a company deleveraging after a $1.3bn acquisition. But if management goes back to its historical habit after 2027, units and growth capex will be higher than modeled.

**What faster growth would do (base case, 50/50 mix, 2026 unchanged, interest on the extra debt at the 5.5% senior-note coupon, FY2025 AFS, line 962, after tax):**

| Unit growth from 2027 | Units/yr | Leverage YE-27 | YE-29 | YE-31 | OE 2031E | Run-rate new-loc. OE 2031E |
|-----------------------|----------|----------------|-------|-------|----------|----------------------------|
| Base (62/yr flat)     | 62       | 2.73x          | 2.06x | 1.46x | 302      | 67                         |
| 5% of opening count   | 68–82    | 2.77x          | 2.21x | 1.74x | 308      | 80                         |
| 7% of opening count   | 95–124   | 2.95x          | 2.65x | 2.40x | 325      | 112                        |

* **5%** is fundable. It misses the 2.7x YE-2027 target only slightly (2.77x) and leaves little for buybacks until 2029. It adds only $6M to 2031E OE, because new units earn nothing in their first year and ramp over three.
* **7%** is not consistent with the stated deleveraging plan: cash after interest and dividends is −$56M to −$90M every year from 2027, and leverage stays above 2.7x until 2029. It would also rule out buybacks.
* **Conclusion.** The base's 62/yr is internally consistent with the 2026–27 leverage target and with some buybacks from 2028. It is conservative against history and against management's target after 2027. Because a 13% ROIC only modestly exceeds the 10% break-even (§6.4), extra units at the base ROIC change value little. Units matter a lot only if the ROIC is far from 13%. **Confidence: medium for 2026–27, medium-low for 2028–31**, where the count is a capital-allocation choice that could plausibly land anywhere from ~50 to ~100 a year.

### 6.2 The earnings stream: ROIC × cost, ramped

| Base (US$M)                                | 2026E | 2027E | 2028E | 2029E | 2030E | 2031E |
|--------------------------------------------|-------|-------|-------|-------|-------|-------|
| Growth capex (location cost × units)       |   116 |   143 |   147 |   151 |   156 |   160 |
| New-location sales                         |     0 |    53 |   175 |   370 |   589 |   821 |
| New-location EBITDA after rent (13% ROIC)  |   0.0 |   5.0 |  16.2 |  33.8 |  53.3 |  74.0 |
| less maint. + software capex (1.9%), tax   |   0.0 |  −2.1 |  −6.7 | −14.1 | −22.4 | −31.1 |
| **OE from new locations**                  |   0.0 |   2.9 |   9.5 |  19.7 |  31.0 |  42.9 |
| *Memo: if all opened to date were mature*  |       |       |       |       |       |       |
| Locations opened since 2026 (cumulative)   |    52 |   114 |   176 |   238 |   300 |   362 |
| Mature run-rate sales                      |   155 |   349 |   555 |   773 | 1,004 | 1,248 |
| Mature run-rate EBITDA after rent          |  15.1 |  33.6 |  52.7 |  72.3 |  93.0 | 114.9 |
| **Mature run-rate OE**                     |   8.9 |  19.8 |  31.0 |  42.4 |  54.4 |  67.0 |
| OE still ramping (run-rate − actual OE)    |   8.9 |  16.9 |  21.5 |  22.7 |  23.4 |  24.1 |

* **Mature run-rate rows (memo, reviewer request).** For each year, these rows take every location opened from 2026 up to that year and show what it would earn if it were already fully ramped: sales = units × mature sales per unit at that year's prices; EBITDA after rent = ROIC × location cost, grown with SSS after the cohort's maturity year, as in the forecast; OE = that less 1.9% maintenance + software capex on the run-rate sales, after 26.5% tax. Nothing here feeds OE. Two readings: (1) run-rate OE is ~7.7% of cumulative growth capex (e.g. $67M on $873M by 2031), the mature OE yield in §6.4; (2) the gap between run-rate and reported new-location OE settles at ~$22–24M/yr from 2028. At a steady ~62 units a year, about that much OE is always still ramping. It is earnings already paid for but not yet reported, and it is the terminal-year adjustment in §10.
* **Ramp (judge-directed simple method).** Capex spent in year t earns nothing in t, 1/3 of mature earnings in t+1, 2/3 in t+2 and 100% from t+3. For example, the 2026 cohort earns 1/3 in 2027, 2/3 in 2028 and full in 2029. This fits management's "newly developed locations would reach maturity by the end of their third year" (Q2FY26 MD&A, line 480). The zero in the capex year also roughly absorbs pre-opening and integration losses (Q2FY26 MD&A, line 480): the 2025 acquisitions lost $2.0M on $31.5M of in-year revenue (FY2025 AFS, line 713).
* **After maturity,** unit earnings grow with SSS, because the store joins the same-store base.
* **Tuck-ins also ramp on this schedule.** Acquired shops take "12-24 months to add the necessary employees and DRP relationships to drive sales to projected levels" (Q2FY26 MD&A, line 480). The 2023–24 cohorts matured later than planned (Q1FY25 call, line 172).

### 6.3 Sanity check: what unit margins does a given ROIC imply?

By definition, EBITDA after rent as a share of sales = ROIC × (location cost ÷ unit sales). Adding a rent ratio gives the pre-rent EBITDA margin. I use the existing network's rent ratio (5.3% in 2028E) as the reference. JH, a mature leased network, pays 5.7% (Unit econ., line 84). Developer-built start-ups probably pay more, since the developer's building cost is recovered through rent (inference). So each start-up figure below is a lower bound, and ~1pp should be added if its rent is 1pp higher.

**References.** The base 2028E existing business earns 14.2% pre-rent and 8.9% after rent. FY2025 earned 12.0% pre-rent and 6.8% after rent (FY2025 MD&A; FY2025 rent 5.14%). JH earned 14.4% pre-rent before synergies and ~20% with 100% of synergies (Unit econ., line 16).

| Unit (cost / sales)          | Cost ÷ sales | ROIC 9%     | ROIC 13%    | ROIC 17%    | ROIC 20% (mgmt) |
|------------------------------|--------------|-------------|-------------|-------------|-----------------|
| Tuck-in ($2.8M / $2.90M)     | 0.97         | 8.7 / 14.0  | 12.6 / 17.9 | 16.4 / 21.8 | 19.3 / 24.7     |
| Start-up ($1.7M / $2.95M)    | 0.58         | 5.2 / 10.5  | 7.5 / 12.8  | 9.8 / 15.1  | 11.5 / 16.9     |
| Blend 30 / 32 ($2.23M/$2.92M)| 0.76         | 6.9 / 12.2  | 9.9 / 15.3  | 13.0 / 18.3 | 15.3 / 20.6     |
| Start-up at $1.3M (mgmt)     | 0.44         | 4.0 / 9.3   | 5.7 / 11.1  | 7.5 / 12.8  | 8.8 / 14.1      |
| Start-up at $2.0M (2025)     | 0.68         | 6.1 / 11.4  | 8.8 / 14.1  | 11.5 / 16.9 | 13.6 / 18.9     |

*Cells show implied EBITDA after rent % / implied pre-rent EBITDA % of sales, at a 5.3% rent ratio.*

**Break-even ROIC.** This is the ROIC at which a new unit just matches the base 2028E network's 8.9% after-rent margin. It is 9.2% for a tuck-in, 15.4% for a start-up at $1.7M (20.2% at $1.3M) and **11.7% for the base blend**.

**What the sanity check says.**

1. **Management's 20% is not credible as a blended unit return at today's prices.** A 30/32 blend needs a 20.6% pre-rent margin, and a tuck-in at 0.97x sales needs 24.7%. The network earns ~14%, and JH reaches ~20% only with every synergy. The target is plausible for a start-up built at management's $1.3M cost: 14.1% pre-rent, network-level. It also fits markets where cheap early acquisitions dominate the capital base. Kaner framed it that way, as a market blend where infill "blend[s] the average return on invested capital in a particular market up" (Q2FY25 call, line 256). It is also close to Boyd's ROIC on *tangible* capital (20.3–24.5%, Unit econ., §4.2, point 3). My inference is that the metric excludes goodwill or is otherwise not like-for-like.
2. **Base 13%.** New units earn a 9.9% after-rent / 15.3% pre-rent margin, the 2028E network margin plus ~1pp. The premium is justified by three things: central overhead a new shop does not add; density synergies ("when we're building density in a marketplace, there tends to be a lot more synergies", Q2FY25 call, line 278); and acquired shops lifting revenue to "projected levels" (Q2FY26 MD&A, line 480). The 1pp size is **speculation**. It equals the margin assumption of the previous model, which is why mature economics barely changed.
3. **One blended ROIC hides a large gap between types.** If both types earn the same 9.9% after-rent margin, a tuck-in earns a 10.3% ROIC and a start-up 17.2%. Mix therefore matters: a shift toward start-ups raises the blended ROIC with no change in unit margins.
4. **Bull 17%.** This is start-ups at management's $1.3M cost plus a 2pp margin premium on the bull network (9.7% + 2pp after rent), giving 16.4% blended, rounded to 17%. It implies an 18.3% pre-rent unit margin.
5. **Bear 9%.** New units earn 6.9% after rent, the same as the FY2025 network at the bottom of the claims cycle (6.8%). This fits the 2023–24 cohorts, which "haven't matured at the same level" (Q1FY25 call, line 172), and higher new-build rents. It is just below bear-case network parity (9.7%).

### 6.4 What growth capex is worth

| Scenario | ROIC | Mature OE yield on cost | Value per $1 (8% disc., 2.5% growth) |
|----------|------|-------------------------|--------------------------------------|
| Bear     | 9%   | 4.5%                    | 0.82                                 |
| Base     | 13%  | 7.7%                    | 1.40                                 |
| Bull     | 17%  | 10.8%                   | 1.96                                 |

* **OE yield** = (ROIC × cost − 1.9% × mature sales) × (1 − 26.5%) ÷ cost, using the base 30/32 blend.
* **Value per $1** = yield ÷ (8% − 2.5%), a simple perpetuity that ignores the ramp, so it is slightly generous. The 8% is the midpoint of Boyd's 7–9% impairment-test WACC (OE & ROIC, §5).
* **Reading.** At 13%, growth creates modest value. Below a 10.0% ROIC, the yield falls under 5.5% (= 8% − 2.5%) and growth destroys value (script, break-even line). That is close to the 11.7% network-parity ROIC, so **whether new units beat the existing network decides whether growth creates value**.
* **Cumulative effect.** Base growth capex over 2026–31 is $873M. It buys $43M of OE in 2031E and ~$67M once every cohort is mature, consistent with 7.7% × $873M. The existing-business-only case distributes $767M more cash over 2026–31 (1,296 vs 529) but forgoes that growing stream.

Base ROIC on total invested capital, using the same average-capital convention as OE & ROIC §5 and starting from $2,902.5M at Jun-26, rises from 6.0% in 2026E to 8.3% in 2031E. It improves as savings accrue and new capital earns more than the goodwill-heavy existing base.

---

## 7. Can the business fund this? Leverage check

The check deducts after-tax cash interest ($60M run rate, Q2FY26 MD&A, line 390) and ~$13M of dividends (sale-leaseback proceeds are no longer added, §5.3), and starts from Jun-26 net debt before leases of $953.1M (Q2FY26 MD&A, line 361). The ratio is net debt ÷ (Adj. EBITDA − rent), with new-location EBITDA after rent included.

| Net debt (ex-leases) / (EBITDA − rent) | 2026E | 2027E | 2028E | 2029E | 2030E | 2031E |
|----------------------------------------|-------|-------|-------|-------|-------|-------|
| Bear                                   | 3.16x | 3.07x | 2.98x | 2.88x | 2.87x | 2.90x |
| Base                                   | 3.00x | 2.73x | 2.41x | 2.06x | 1.76x | 1.46x |
| Bull                                   | 2.89x | 2.50x | 2.10x | 1.67x | 1.30x | 0.94x |

* **Base.** YE-2026 at 3.0x is above the 2.8x pro forma at Q2 (Q2FY26 call, line 36). 2027E at 2.7x is about a year behind management's "2.6 times as early as the end of 2026" (Q1FY26 call, line 91) and in line with the JH-release target of 2.7x by end-2027 (JH release, line 47). Free cash after interest and dividends is negative in 2026–27 (−$16M and −$13M full-year), then $21–85M/yr. With the previous version's sale-leaseback proceeds, base leverage was 0.05–0.17x lower (2.95x in 2026E, 1.29x in 2031E). Without them, deleveraging depends on EBITDA growth.
* **Bear.** Leverage stays at 2.9–3.2x, inside the 3.5x covenant (Q2FY26 MD&A, line 398), with −$22M to +$20M/yr of free cash. Management would likely slow unit growth (inference). With a 9% ROIC that would also be the value-maximizing response.
* **Lease liabilities** ($1,050.9M) are excluded, because rent is charged in full inside OE (OE & ROIC, §7).

---

## 8. Sensitivity: base FY2029E OE of $254M

| Change (one at a time)                    | FY2029E OE | Δ vs base  |
|-------------------------------------------|------------|------------|
| TCOR +1pp/yr from 2027                    |        277 | +23 (+9%)  |
| TCOR −1pp/yr from 2027                    |        216 | −37 (−15%) |
| No share gains from 2027                  |        210 | −43 (−17%) |
| Claims −2%/yr instead of −1%              |        216 | −37 (−15%) |
| Savings retention 100% (vs 80%)           |        267 | +14 (+5%)  |
| Savings retention 60%                     |        240 | −14 (−5%)  |
| Maintenance capex 2.0% (vs 1.7%)          |        243 | −10 (−4%)  |
| Rent escalator 3.0% (vs 2.5%)             |        251 |  −3 (−1%)  |
| New-location ROIC 20% (mgmt) vs 13%       |        267 | +13 (+5%)  |
| New-location ROIC 10% vs 13%              |        248 |  −6 (−2%)  |
| No new locations from 2026                |        234 | −20 (−8%)  |

Same-store volume and price still explain most of the spread in OE. The new-location ROIC moves 2029E OE little, because most of the capital is still ramping. Its real importance is in value (§6.4) and in the terminal year: a 20% ROIC would add ~$45M to the run-rate OE of the 2026–31 cohorts once mature (script, run-rate check).

---

## 9. Cross-checks and internal consistency

* **FY2026E against reported H1.** Base FY2026E sales are $4,007M and Adj. EBITDA $536M (13.4%), which implies H2 sales of $1,997M at 13.9% against H1's $2,010.3M and $258.3M (Q2FY26 MD&A, line 317). Management's trajectory (Q2'26 13.4%, "40 basis point expansion… I expect that to continue", Q2FY26 call, line 105) points to ~14.0% for H2. **Margin consistent.** Sales are slightly light: FY2025 H2 sales were 1.016× H1, which would put H2-2026 at ~$2,043M, $46M (1.2% of FY sales) above the model, worth roughly $2M of OE (script, seasonality line). The cause is that 2026 openings earn nothing under the simple ramp, and 2025 openings not yet in the SSS base get no separate ramp (§4.2).
* **ROIC vs unit margins.** The base 13% implies a 15.3% pre-rent unit margin against 14.2% for the network, with the ~1pp gap explained (§6.3). Management's 20% was tested and rejected as a blended unit figure.
* **ROIC vs value.** A 13% pre-tax ROIC is a ~7.7% OE yield, just below the 8% discount rate, but it grows with SSS. The DCF should therefore capitalize new-location growth only modestly (§10).
* **Growth vs market size.** Base 2031 sales of $5.5bn are ~11% of an industry of ~$50bn in 2024 (FY2025 MD&A, line 73), growing ~2%/yr (inference). SSS of 3% is at the bottom of management's 3–5% range. Unit growth of 4.6% in 2027, falling to 3.9% by 2031, is below its 5–7% (FY2025 MD&A, line 91; §6.1a).
* **Margin vs cost drivers.** The existing-business margin rises from 13.4% to 14.9% on three sources: the last $35M of savings × 80%, SSS operating leverage of ~0.2pp/yr, and JH's return from its disrupted 13.0% 2026 margin to 14.4%+. Rent falls from 5.39% to 5.25% of sales because 3% SSS outgrows the 2.5% rent escalator on a fixed footprint. The 14.9% is above management's 14% target (flag).

---

## 10. Notes for DCF use

1. Use **distributable** (OE − growth capex − one-offs) for explicit-period cash flows in any case with new-unit growth.
2. **Terminal year.** 2031E OE understates the run rate of capital already spent. The 2026–31 cohorts earn $43M of OE in 2031E but ~$67M once mature in the base case ($23M bear, $115M bull; §6.2 run-rate rows). Either add the ~$24M uplift to terminal OE or carry the ramp one more year. Beyond 2031, organic growth is ~3% SSS. Extra growth from new units needs matching reinvestment at ~7.7% OE yield (base), which adds little value at 8%.
3. **One-offs** are the remaining transformation opex (\~$15.9M pre-tax) and JH integration capex (\~$20.2M) from Jul-2026 (Q2FY26 MD&A, line 223).
4. **Do not deduct lease liabilities** (rent is inside OE). Do deduct the $1,049.1M net non-operating position (OE & ROIC, §7). The goodwill tax shield is excluded from OE.

---

## 11. What I am confident about vs. what is genuinely uncertain

**Confident:**

* **2026E OE of $170–190M.** It is almost entirely existing business, H1 is reported, and the required H2 margin matches management's run rate.
* **The existing business's cost structure.** Rent of $216M in 2026E (H1 × 2), escalating 2.5%/yr, maintenance capex 1.6–1.8% (guided), 26.5% tax.
* **Location costs.** Tuck-ins at ~$2.7–2.8M (~1x sales) come from 2025 and H1'26 disclosures. Start-ups cost $1.2–2.0M.
* **Management's 20% ROIC does not hold as a blended unit return at current tuck-in prices.** It would need ~21% pre-rent unit margins, versus ~14% for the network.

**Uncertain:**

* **New-location ROIC (base 13%, range 9–17%).** Boyd discloses no unit returns (Unit econ., line 31). The base rests on network parity plus a speculative ~1pp premium. This is the key input for whether growth capex creates value, though not for 2026–31 OE.
* **Start-up cost and rent under the outsourced model.** At $1.3M instead of $1.7M, a start-up's ROIC at the same margin rises by ~5pp. But developer-funded buildings likely mean higher rent. The FY2026 MD&A's per-opening investment will settle the cost.
* **TCOR timing and level.** This is the dominant OE risk. Management has no view (Q2FY26 call, line 121), and the used-car mechanism is not yet working (Knowledge Store ID 8).
* **Durability of share gains.** They drove all positive SSS in 2025–26 (Q2FY26 MD&A, line 66), and the lead over the industry is narrowing. Loss of a major insurer program would be asymmetric (FY2025 MD&A, line 746).
* **Structural claims decline.** The −1%/yr is a framework, not a measurement. At −2%/yr, 2029E OE is 15% lower.
* **Unit count after 2027 and capital allocation.** The base's 62/yr is the start-up pipeline × 2. It sits below the 2023–25 average of 75 and below management's 5–7% (68–95 units in 2027). Cash constrains it only in 2026–27. From 2028 it is a choice between units, buybacks (the NCIB, Knowledge Store ID 5, size not disclosed in the sources) and deleveraging. 5% growth is fundable (YE-2027 leverage 2.77x). The live NCIB fits with this: 2026–27 room is only ~$0–65M, mostly from cash taxes running below statutory. 7% would keep leverage above the 2.7x target until 2029 (§6.1a). At a 13% ROIC the choice moves 2031E OE by only +$6M to +$23M. It matters for value only if the ROIC is far from 13%. MSO deals like JH are not modeled.
