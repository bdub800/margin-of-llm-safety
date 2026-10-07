# Boyd Group Services (BYD.TO / BGSI): Terminal Value at End-2031

*Prepared 2026-09-28. Revision history:*

- *r1 (verifier): the Joe Hudson's cross-check uses Boyd's disclosed run-rate basis.*
- *r2 (judge): listed non-peers removed. The multiple is set from collision-repair valuation evidence plus qualitative analysis, with the formula demoted to a cross-check.*
- *r3 (judge): the multiple is applied directly to EBITDA after rent, with no conversion to Owners' Earnings (OE).*
- *r4 (judge): all sections updated to that basis, and a terminal value added for the no-growth-capex scenario. The bear multiple was lowered from 7x to 6x after the cross-check in §8.*
- *r5 (judge): the ramp uplift is simplified to the same multiple × the ramp gap, with no timing deduction. Base TV rises $25M, to $4,771M.*

*US$ millions. Every number comes from `work_products/terminal_value.py` (run `uv run python work_products/terminal_value.py`), which imports the FY2026E–FY2031E forecast from `work_products/forecast_earnings.py`. Terminal values are stated at end-2031 and are **not** discounted. Boyd's own share price is not used anywhere.*

**Source key** (citations use "short name, line xx"):

| Short name   | File                                                        |
|--------------|-------------------------------------------------------------|
| Forecast     | `work_products/forecast_earnings.md`                        |
| OE & ROIC    | `work_products/owners_earnings_and_roic.md`                 |
| Causal model | `work_products/causal_model.md`                             |
| Overview     | `work_products/overview.md`                                 |
| FY2025 MD&A  | `primary_sources/FY2025/BoydGroup_MDA.md`                   |
| FY2025 AFS   | `primary_sources/FY2025/BoydGroup_AFS.md`                   |
| Q2FY26 call  | `primary_sources/Q2FY26/earnings_call_transcript.md`        |
| Q1FY26 call  | `primary_sources/Q1FY26/earnings_call_transcript.md`        |
| JH release   | `fetched_docs/boyd_joe_hudsons_acquisition_announcement.md` |
| KS nn        | Knowledge Store ID nn                                       |
| Script (n)   | `work_products/terminal_value.py`, printed section (n)      |

---

## 1. Headline answer

**TV₂₀₃₁ = EV/EBITDA-R multiple × FY2031E EBITDA-R + ramp uplift**, where EBITDA-R is Adj. EBITDA after rent.

| US$M, end-2031      | EBITDA-R 2031E | EV/EBITDA-R | TV on EBITDA-R | + Ramp | **Terminal value** |
|---------------------|----------------|-------------|----------------|--------|--------------------|
| Bear (25%)          | 312            | 6.0x        | 1,871          | 93     | **1,964**          |
| **Base (50%)**      | **520**        | **8.5x**    | 4,423          | 348    | **4,771**          |
| Bull (25%)          | 666            | 10.0x       | 6,661          | 670    | **7,331**          |
| **Probability-wtd** | 505            | ~8.6x       | 4,344          | 365    | **4,709**          |
| *No growth capex*   | *446*          | *8.5x*      | *3,794*        | *0*    | ***3,794***        |

*Script (3). "Ramp" = the same multiple × new-location EBITDA-R that 2029–31 growth capex has already paid for but that is not yet earned in 2031 (base 8.5 × $40.9M = $348M; §9). "No growth capex" is the forecast's existing-business-only case: base drivers, no locations opened from 2026 (Forecast, lines 42-43). It is a separate forecast, not a fourth weighted scenario.*

**In one line:** base ~$4.7bn and probability-weighted ~$4.7bn, from 8.5x FY2031E EBITDA after rent. That is the lower half of the platform-grade collision range (8–12x), just below the 9.3x post-synergy price Boyd itself paid for Joe Hudson's. **With no growth capex, the terminal value is ~$3.8bn.** It is $977M lower, but Boyd would have kept $767M more cash in 2026–31 (Forecast, line 297). Compounded to 2031, the growth program is roughly value-neutral (+$38M, §7).

---

## 2. Method

1. **Evidence.** Collect collision-repair valuation evidence only: private-market multiples by size tier, private-equity platform prices, the two Joe Hudson's transactions, and AMA Group, the only listed pure-play besides Boyd (§5).
2. **Placement.** Place Boyd within that evidence using the qualitative assessment (§3) and pick a multiple per scenario (§6).
3. **Application.** Apply the multiple directly to FY2031E EBITDA after rent, the basis the evidence is quoted on. Tax, maintenance capex and OE assumptions are therefore not stacked on the multiple. Add the ramp uplift (§9).
4. **Cross-checks (secondary).** Implied TV ÷ OE against the value-driver formula, TV ÷ invested capital, and Boyd's impairment-test assumptions (§8).

**What the terminal value is.** It is an enterprise value. Rent is already deducted in EBITDA-R, so lease liabilities must **not** be deducted again in the equity bridge (OE & ROIC, line 274).

**Basis caveat (applies to all of §5).** Industry sources quote "EBITDA" without defining it. US private collision operators report under US GAAP, where operating-lease rent sits in opex. JH's disclosed 13.3x and 9.3x must be after rent: on the $104M pre-rent figure, the $1,150M net price would be at most 11.1x (Script, 2). So I treat all quoted multiples as EV ÷ EBITDA after rent. For sources other than JH that is an **assumption**. If some are pre-rent, those multiples overstate value on Boyd's basis.

**The trade-off of the EBITDA basis.** EBITDA multiples do not see differences in capex intensity. The bear forecast carries 2.0% maintenance capex against 1.7% in the base (Forecast, line 161), so the same EBITDA multiple would overvalue the bear. The §8 cross-check catches this and is why the bear multiple is 6x, not 7x.

---

## 3. Qualitative assessment: what kind of business is being capitalized?

### 3.1 Quality and competitive position (supports the lower half of the platform range, not a premium)

**Strengths:**

* **Scale in a fragmented market.** Boyd has 1,300+ locations and, after Joe Hudson's, calls itself "the second largest independent collision repair operator". Its share is still "modest" in an industry of ~30,000 locations (FY2025 MD&A, line 69) worth ~$50bn a year (FY2025 MD&A, line 73).
* **Insurers favor scale.** They steer direct-repair-program (DRP) volume on "cycle time, quality of repair, customer satisfaction and cost of repair" (Causal model, Factor 1.3), and they have been concentrating DRP volume among fewer, larger operators (Overview, line 15). Scale also brings procurement and in-house calibration advantages that single shops lack (Causal model, Factors 2.1–2.2).
* **Excellent unit economics.** ROIC on tangible capital is 20.3–24.5% in FY2024–TTM (OE & ROIC, line 18). Working capital is structurally negative, because insurers pay reliably and suppliers fund the float (OE & ROIC, line 191).

**Weaknesses:**

* **Poor returns on the price paid for the network.** ROIC on total invested capital is 6.4–10.2% (OE & ROIC, line 17). The forecast lifts it only to 8.3% by 2031E (Forecast, line 299), roughly equal to the discount rate. In OE & ROIC's words, this is "the central tension in this business: excellent operating economics, mediocre returns on the price paid to acquire them" (OE & ROIC, line 237).
* **The advantage is relative, not a moat.** Boyd competes "with a small number of other multi-location collision repair operators in many markets" (FY2025 MD&A, line 782). Those rivals are large and PE-backed: Caliber, Crash Champions, Classic and Quality (Knowledge Store ID 11). The "Big 5" already hold 31.7% of industry revenue (Knowledge Store ID 11). Insurers, not end customers, hold the pricing power, and they set labor rates (Causal model, Factor 2.3).

### 3.2 Durability and predictability of earnings (a discount factor)

* **Demand is non-discretionary and insurance-paid,** so earnings are more durable than in most consumer services. Even so, industry repairable claims fell ~9% in 2024 (Causal model, Factor 1.1), a year when management cited the warmest winter in 129 years (Knowledge Store ID 15), and claims volumes swing with weather, premiums and total-loss rates (FY2025 MD&A, lines 696-698).
* **Historical OE is volatile.** It went $132.4M (FY2023) → $91.8M (FY2024, −31%) → $108.9M (+19%) → $145.9M TTM (+34%) (OE & ROIC, line 15; Script, history). OE & ROIC calls FY2023 a cyclical high and FY2024 a cyclical low (OE & ROIC, line 242).
* **Customer concentration is high.** The top five insurers are "approximately 54%" of sales. One is "approximately 19%" and a second "approximately 12%" (FY2025 MD&A, line 746). DRP agreements "are usually cancellable upon short notice" (FY2025 MD&A, line 748). A single program loss would be a step-down, not a trend, so the downside is asymmetric (Causal model, line 85, inference). The causal model calls concentration "undisclosed", but the FY2025 MD&A does disclose it. **This is a main reason Boyd sits in the lower half of the platform range (§6).**
* **Technology risk to accident frequency over a perpetuity.** Boyd lists "collision avoidance systems, driverless vehicles and other safety improvements" as risks to claim volume (FY2025 MD&A, line 698). Management's own framework already assumes collision avoidance cuts claims by 2%/yr (Q1FY26 call, line 67). Severity partly offsets this: 28.3% of estimates now include calibrations, versus 21.8% a year earlier (Knowledge Store ID 7), and newer cars cost ~$2,000 more to repair (Q2FY26 call, line 123). A terminal value covers decades, so a faster move to driverless fleets is a real tail risk. Its timing cannot be estimated from the sources (**speculation**).

### 3.3 Growth after 2031

* **Organic growth.** In the base forecast, 2028–31 same-store sales (SSS) growth is claims −1.0% + repair cost (TCOR) +3.0% + share +1.0% = 3.0% (Forecast, lines 116-119). For a perpetuity, share gains should fade, because the SSS-over-claims gap is narrowing and technician capacity is being "eaten up" (Forecast, line 127). Long-run growth of ~2–2.5% is consistent with the forecast's 2.5% terminal growth (Forecast, line 295) and below the 3% in Boyd's impairment test (FY2025 AFS, line 966).
* **Unit growth adds little value at the base ROIC.** A new location earns a ~7.7% after-tax OE yield at a 13% pre-tax ROIC (Forecast, line 291), only modestly above the ~6% it needs once organic growth is counted (§8). The no-growth-capex comparison confirms this: at 8.5x, the 2026–31 program is worth +$38M net at end-2031 (§7). **So the multiple should not depend much on how fast Boyd adds stores.** In the bear case (4.5% yield), growth destroys value.
* **Acquisition growth is getting harder.** Tuck-in prices have risen to ~$2.8M per location, against $2.3M on average in 2023–25 (Forecast, line 174). Boyd itself flags "increasing acquisition valuations" as a risk (FY2025 MD&A, line 646). As consolidation matures, acquired growth should earn less, not more (inference).

### 3.4 Management and capital allocation (neutral to slight negative)

* **Execution is good on operations.** Project 360 and the Joe Hudson's integration went ahead of plan, and the 2026 savings target was raised twice (Overview, line 39).
* **The capital-allocation record is mixed.** Boyd put 134–152% of OE into new units in 2023–25 (Forecast, line 225), at total-capital returns below its own 7–9% WACC. It paid 13.3x run-rate EBITDA-R for Joe Hudson's, or 9.3x after full synergies (§5). The new buyback program (NCIB) adds a choice besides reinvesting (KS 5), which reduces the risk that cash is forced into sub-par deals.

**Net qualitative read:** Boyd is a good, scaled operator in a durable, needs-based industry, and it belongs in the platform tier of collision valuations. But it is a price-taker from concentrated insurer customers, has a thin moat against similar-sized PE rivals, has moderately volatile earnings, and earns about its cost of capital on total capital. It also has no synergies left to sell a 2031 buyer. **That places it in the lower half of the platform range, not at a premium.**

---

## 4. Terminal-year earnings being capitalized

| FY2031E (Script, 1)                     | Bear  | Base  | Bull  | No growth capex |
|-----------------------------------------|-------|-------|-------|-----------------|
| Sales                                   | 4,799 | 5,469 | 6,140 | 4,648           |
| **EBITDA after rent (EBITDA-R)**        | 312   | 520   | 666   | 446             |
| of which locations opened 2026–31       | 31    | 74    | 120   | 0               |
| Ramp gap (paid for, not yet earned)     | 15.6  | 40.9  | 67.0  | 0               |
| Existing-business Adj. EBITDA margin    | 12.3% | 14.9% | 15.6% | 14.9%           |
| *Memo: Owners' Earnings (cross-checks)* | *148* | *302* | *405* | *260*           |

**Flag:** the base existing-business margin of 14.9% is above management's 14% target and above any historical year. FY2023 was 12.5% (Forecast, line 153). At 14.0%, base EBITDA-R would be $480M, 8% lower, and the terminal value $339M lower (Script, 5d). I handle this through scenario weighting (the bear runs 12.3%) and by placing Boyd in the lower half of the peer range. I do not also cut the base EBITDA, because that would count the same risk twice.

---

## 5. Peer valuation evidence (primary basis)

### 5.1 What exists, and what does not

**There is no listed North American peer.** Boyd's large rivals are all private: Caliber (Hellman & Friedman, Leonard Green, OMERS), Crash Champions (Clearlake), Classic Collision (TPG) and Quality Collision (Susquehanna) (KS 11). Most platform deals did not disclose terms:

- Caliber–ABRA (2019) (KS 22) and the 2013 Caliber consortium buyout (KS 27).
- TPG's 2024 purchase of Classic Collision from New Mountain (KS 20).
- Crash Champions–Service King (2022), a debt-for-equity conversion after Clearlake "acquired a control position in the Service King bonds" (KS 17). Blackstone had valued Service King at ~$650M in 2014, but EBITDA was not disclosed (KS 24).
- Caliber filed confidentially for a NYSE IPO in July 2025. Its revenue, EBITDA and valuation are still undisclosed (KS 18, 23). *If it prices, it becomes the key benchmark.*

### 5.2 The evidence that does exist

| Datapoint (EV ÷ EBITDA-R, basis assumed)      | Multiple        | Source           |
|-----------------------------------------------|-----------------|------------------|
| Single shops                                  | 3.0–5.0x        | KS 11, 28        |
| Small / medium MSOs bought by consolidators   | 5.0–7.0x        | KS 20, 28        |
| Market average, 2025 (weak claims year)       | ~7x             | KS 19            |
| MSOs with strong DRP relationships            | 7.0–10.0x       | KS 11            |
| **Platform-grade MSOs**                       | **8.0–12.0x**   | KS 11            |
| PE platform recapitalization (illustrative)   | 10x             | KS 21            |
| PE platforms raising capital (2024)           | 12.0–14.0x      | KS 20, 21        |
| Joe Hudson's to TSG, 2019 ("north of 13x")    | >13x            | KS 25            |
| Joe Hudson's to Boyd, 2025, run-rate pre-syn. | 13.3x           | JH release, l.43 |
| **Joe Hudson's to Boyd, 2025, post-synergy**  | **9.3x**        | JH release, l.43 |
| AMA Group (ASX), FY26 / FY27 guidance         | 3.8x / 3.2–3.4x | KS 26            |

*Joe Hudson's: $1.3bn price less ~$150M of expected tax benefits = $1,150M net. $1,150M ÷ 13.3 = $86.5M run-rate EBITDA-R, versus $63M reported TTM (a +$23.5M run-rate adjustment). $1,150M ÷ 9.3 implies $37.2M of synergies, inside the disclosed $35–45M (JH release, lines 37, 43, 45; Script, 2). AMA: EV A$257M (market cap A$238M, from a search summary of stockanalysis.com, moderate confidence, plus A$18.4M net debt) ÷ normalized pre-AASB 16 EBITDA of A$68M, or FY27 guidance of A$75–80M (KS 26).*

### 5.3 How to read it

- **Multiples rise steeply with scale and DRP quality,** from 3–5x for a single shop to 8–12x for a platform (KS 11). PE runs this as multiple arbitrage: buy shops at 5–7x, raise capital at 12–14x (KS 20). Those 12–14x marks are prices for **growth platforms with the arbitrage still ahead of them.** They are a ceiling, not a steady-state price for a mature consolidator.
- **Joe Hudson's is the one disclosed platform price.** It was a 258-shop, dense network with strong DRP relationships, sold through a process run by Harris Williams and BofA (JH release, line 59). A 2031 buyer of Boyd buys earnings that already contain synergies, so the relevant comparison is **9.3x post-synergy**, not 13.3x. That 9.3x was also a control price, paid by the one buyer who owned the synergies. TSG reportedly paid "north of 13x" in 2019 (KS 25, a single secondary source).
- **The 2025 downturn shows the cyclical low.** Multiples "remained relatively stable at approximately 7x", but "declining revenue and lower EBITDA reduced enterprise values" (KS 19). Buyers paid ~7x on trough EBITDA in expectation of recovery.
- **AMA Group is a real listed peer, but not of comparable quality.** It is Australia's collision consolidator (Capital SMART), and it just returned to profit and paid its first dividend since 2019 (KS 26). At ~3.5x, it shows how low public markets price a subscale, recovering operator: a floor, not a guide.
- **Service King shows that platforms can fail.** A leveraged, PE-owned consolidator ended in a creditor-led recapitalization (KS 17). This argues against the top of the range.

---

## 6. Where Boyd sits, and the chosen multiples

| Factor (§3)                                              | Direction                 |
|----------------------------------------------------------|---------------------------|
| Top-2 scale, dense markets, procurement and calibration  | ↑ platform tier, not MSO  |
| Tangible ROIC ~20%+, negative working capital            | ↑                         |
| Synergies already in 2031 earnings (no second round)     | ↓ vs JH pre-synergy 13.3x |
| Top insurer 19%, top five 54%, DRPs cancellable          | ↓                         |
| Total-capital ROIC ≈ cost of capital; rising deal prices | ↓                         |
| Mature consolidation by 2031; growth ~2–2.5%             | ↓ vs 12–14x growth marks  |
| Base terminal margin 14.9%, above the 14% target         | ↓                         |

| Scenario        | EV/EBITDA-R | Anchor in the evidence                                                |
|-----------------|-------------|-----------------------------------------------------------------------|
| Bear            | **6.0x**    | Mid 5–7x MSO band; structural, not cyclical weakness                  |
| Base            | **8.5x**    | Lower half of platform range (8–12x); just below JH post-synergy 9.3x |
| Bull            | **10.0x**   | Platform midpoint / PE recap level (KS 11, 21); below 12–14x marks    |
| No growth capex | **8.5x**    | Same as base (§7)                                                     |

**Why base 8.5x and not 9–10x.** Joe Hudson's 9.3x was a control price for synergy-inclusive earnings, and a 2031 valuation of Boyd has no synergies left to pay for. The ↓ factors also put Boyd in the lower half of the platform range. At 8.0x the base would be $4,490M; at 9.0x, $5,051M; at JH's 9.3x, $5,220M (Script, 3).

**Why bear 6x (r4, was 7x).** The bear is permanent weakness: margins fall every year from 13.0% to 12.3% (Forecast, line 148), and maintenance capex is heavier at 2.0%. The 2025 market's ~7x was paid on trough earnings by buyers expecting recovery (KS 19). A buyer in the bear world would not expect it, so I use the middle of the 5–7x band paid for non-platform MSOs. At 7x, the §8 cross-check showed the bear valued at 15.4x its OE, which implies an unreasonably low 6.8% discount rate given its heavier capex.

**This is judgment within sourced ranges,** not a calculated point.

---

## 7. Terminal value with no growth capex

**The case.** The forecast's "existing business only" case keeps every base driver (claims, TCOR, share gains, savings, rent, 1.7% maintenance capex) but opens no locations from 2026. There is therefore no growth capex (Forecast, lines 42-43). FY2031E EBITDA-R is $446M, against $520M in the base. The $74M difference is the EBITDA of 2026–31 openings. There is no ramp gap (Script, 1).

**Multiple: 8.5x, the same as the base.**

- **The earnings are the same kind.** They come from the same pre-2026 network, and the pre-2026 network of ~1,300 locations (KS 6) is still platform scale.
- **The growth option passes to the buyer either way.** A buyer at end-2031 can restart openings whether or not Boyd grew in 2026–31, so the peer evidence does not point to a different tier.
- **Growth at base returns is roughly value-neutral** (below), so a lower multiple for the no-growth case would not be justified by forgone value.
- **Cross-check:** 8.5x implies 14.6x OE, which is the formula at 9.0%. That is in line with the base's 8.6% (§8).

**Result: TV = 8.5 × $446.3M = $3,794M** (Script, 3). Sensitivity: 8.0x gives $3,571M; 9.0x gives $4,017M.

| Base vs no growth capex (Script, 4)           | US$M                |
|-----------------------------------------------|---------------------|
| Extra end-2031 TV from 2026–31 locations      | +977                |
| of which 8.5x × 2031 new-location EBITDA-R    | +629                |
| of which ramp uplift                          | +348                |
| Distributable cash 2026–31: base vs no growth | 529 vs 1,296 (−767) |
| That cash difference compounded to 2031 at 8% | −939                |
| **Net value of the growth program, end-2031** | **+38**             |

**Reading.** At the base's 13% new-location ROIC and an 8.5x exit, the 2026–31 growth program roughly pays back its cost of capital and no more. This matches the forecast's finding that growth "creates modest value" at 13% and destroys it at 9% (Forecast, lines 295-296). **For the DCF, the two cases give similar present values by different routes.** The growth case has lower 2026–31 cash and a higher terminal value. The no-growth case has higher cash and a lower terminal value. The no-growth case is the less assumption-heavy of the two, since it needs no view on new-location ROIC.

*Note: this is the base-driver no-growth case only. Bear and bull no-growth variants were not modeled in the forecast.*

---

## 8. Cross-checks (secondary)

**Implied TV ÷ OE versus the value-driver formula.** The formula is OE multiple = (1 + g)(1 − reinvestment) ÷ (r − g). Here g is claims + TCOR (`forecast_earnings.py`, lines 202-219) plus 0.5pp of share gains bought with new capacity. The no-growth case has no share-gain growth and no reinvestment. r = 8%, the midpoint of Boyd's 7–9% impairment WACC (FY2025 AFS, line 966).

| Scenario        | Formula at 8% (OE ×) | Chosen TV ÷ OE | = formula at r |
|-----------------|----------------------|----------------|----------------|
| Bear            | 12.8x                | 13.3x          | 7.8%           |
| Base            | 17.4x                | 15.8x          | 8.6%           |
| Bull            | 19.6x                | 18.1x          | 8.4%           |
| No growth capex | 17.0x                | 14.6x          | 9.0%           |

*Script (5a). TV ÷ OE includes the ramp uplift.*

The peer-based terminal values imply discount rates of ~7.8–9.0%, clustered near 8.5%. The deal market prices Boyd-like earnings at ~0.5–1pp above Boyd's impairment rate, which is plausible for a leveraged, customer-concentrated operator (inference). The formula is very sensitive to r: 9% instead of 8% moves the base from 17.4x to 14.7x (Script, 5a). That sensitivity is why it is only a cross-check.

**Terminal value ÷ invested capital (end-2031, Script, 5b):**

- **Base:** 1.28x ($4,771M vs $3,737M).
- **No growth capex:** 1.30x ($3,794M vs $2,923M).
- **Bull:** 1.86x.
- **Bear:** 0.58x, $1,425M below the capital deployed, which implies a large impairment.

The network earns ~8–9% on total capital, so a no-growth value would be ~1.0x. The premium comes from price-led organic growth that needs little capital.

**Boyd's impairment assumptions** (3% growth, 7–9% WACC) imply 17.2–25.7x cash flow (Script, 5c). That is above every TV ÷ OE in the table: management's goodwill-test view is more generous than the deal market.

---

## 9. Ramp uplift (included) and exclusions

**Ramp uplift.** Locations opened in 2029–31 are still ramping in 2031. The forecast ramps new units 0, 1/3, 2/3, then fully mature (Forecast, line 256). So base new-location EBITDA-R is $74.0M actual against $114.9M if all were mature, a gap of $40.9M (Script, 1; Forecast, line 251).

I apply the scenario multiple to the gap: base 8.5 × $40.9M = $348M, bear 6.0 × $15.6M = $93M, bull 10.0 × $67.0M = $670M (Script, 3). For simplicity, there is no deduction for the fact that the gap is only fully earned by 2034. The 2031 cohort matures in 2034, the 2030 cohort in 2033 and the 2029 cohort in 2032 (Forecast, line 256). This slightly overstates the uplift: in r4, a 1–2 year timing deduction cut the base by $25M (0.5% of TV). Without it, the terminal value would undervalue $873M of 2026–31 growth capex (Forecast, line 297), which is the adjustment the forecast asks for (Forecast, line 352). It is not double counting: the multiple prices earnings from 2032 onward, and the uplift is a one-time step in the level of earnings, from capital spent before 2032.

**Excluded:**

- **The goodwill tax shield.** Cash taxes run below statutory while Boyd acquires (OE & ROIC, line 87; Forecast, line 163). Value it separately, if at all.
- **Lease liabilities.** Rent is already inside EBITDA-R (OE & ROIC, line 274).

---

## 10. Sensitivity

| EV/EBITDA-R | Base TV   | No-growth TV |
|-------------|-----------|--------------|
| 7.0x        | 3,929     | 3,124        |
| 7.5x        | 4,209     | 3,348        |
| 8.0x        | 4,490     | 3,571        |
| **8.5x**    | **4,771** | **3,794**    |
| 9.0x        | 5,051     | 4,017        |
| 9.3x (JH)   | 5,220     | 4,151        |
| 10.0x       | 5,613     | 4,463        |

*Script (3). Each 0.5x is worth ~$280M in the base case and ~$220M with no growth capex.*

---

## 11. Confidence

**Confident:**

- **Collision platforms change hands at roughly 8–12x EBITDA after rent.** Boyd's own Joe Hudson's price sits inside that range at 9.3x post-synergy.
- **Boyd belongs in the platform tier but not at its top.** The qualitative evidence is consistent on this.
- **At base returns, growth capex is roughly value-neutral** (+$38M at end-2031). The terminal-value difference between the growth and no-growth cases is mostly offset by the cash spent to get there.

**Uncertain:**

- **The peer data is thin and secondary.** Most ranges come from M&A advisors and trade press (KS 11, 19, 20, 21, 28), not audited disclosures, and the EBITDA basis is usually undefined. Only JH has a disclosed multiple and basis.
- **The Caliber IPO would reset the benchmark** if it prices (KS 18, 23).
- **The 2031 market regime.** Multiples compressed toward ~7x in the 2025 claims downturn (KS 19), and where the cycle will sit in 2031 is unknown.
- **The terminal margin (14.9%) is above target.** Normalizing to 14% cuts base TV by $339M (§4).
- **EBITDA multiples ignore capex intensity.** This matters most for the bear, which is why its multiple is set at 6x after the cross-check.

---

## 12. Notes for the DCF

1. **Discount the end-2031 terminal value from end-2031:** base $4,771M, probability-weighted $4,709M, no growth capex $3,794M. The multiples imply r ≈ 8.5–9%, so a DCF at ~9% is consistent. At 8%, the terminal value carries a deliberate ~0.5–1pp extra risk premium.
2. **Pair each terminal value with its own cash flows.** Use the growth case's distributable cash (OE − growth capex − one-offs) with the growth terminal value, and the existing-only distributable cash with the no-growth terminal value (Forecast, line 43). The ramp uplift is already inside the growth terminal value.
3. **Equity bridge.** Deduct the net non-operating position, but **not** lease liabilities (OE & ROIC, line 274). Value any goodwill tax shield separately.
