# Boyd Group Services (BYD.TO / BGSI): Intrinsic Valuation

*Prepared 2026-09-28. US$ millions unless stated. Every number comes from `work_products/valuation.py` (run `uv run python work_products/valuation.py`). That script imports the FY2026E–FY2031E forecast from `work_products/forecast_earnings.py` and the end-2031 terminal values from `work_products/terminal_value.py`, so the cash flows, scenarios and terminal multiples are exactly those in the earlier work products. The discount rate is the variable `ValuationSettings.discount_rate = 0.10`. Boyd's share price is not used anywhere.*

**Source key** (citations use "short name, line xx"):

| Short name   | File                                                        |
|--------------|-------------------------------------------------------------|
| Forecast     | `work_products/forecast_earnings.md`                        |
| TV           | `work_products/terminal_value.md`                           |
| OE & ROIC    | `work_products/owners_earnings_and_roic.md`                 |
| Q2FY26 FS    | `primary_sources/Q2FY26/BoydGroup_Q2.md`                    |
| Q2FY26 MD&A  | `primary_sources/Q2FY26/BoydGroup_MDA.md`                   |
| FY2025 AFS   | `primary_sources/FY2025/BoydGroup_AFS.md`                   |
| FY2025 MD&A  | `primary_sources/FY2025/BoydGroup_MDA.md`                   |
| JH release   | `fetched_docs/boyd_joe_hudsons_acquisition_announcement.md` |
| Script (n)   | `work_products/valuation.py`, printed section (n)           |

---

## 1. Headline answer

*Revised r2 (judge): (a) the headline now includes the no-growth-capex case; (b) the tax-shield asset now covers all goodwill and intangibles. It uses Boyd's own ~$150M for Joe Hudson's (JH) and an estimate for the rest. Together these moved the headline from US$86.7 to US$91.8. *Revised r3 (judge):* the legacy shield now uses a ratio method: Boyd's $150M JH figure × (legacy goodwill + intangibles ÷ JH goodwill + intangibles). The headline is now US$91.7.*

| US$M, 10% discount rate    | Bear  | Base  | No growth | Bull  | **Weighted** |
|----------------------------|-------|-------|-----------|-------|--------------|
| Weight                     | 25%   | 25%   | 25%       | 25%   |              |
| PV of 2026–31 distributable| 256   | 344   | 925       | 426   | 488          |
| Terminal value, end-2031   | 1,964 | 4,771 | 3,794     | 7,331 | 4,465        |
| PV of terminal value       | 1,220 | 2,962 | 2,356     | 4,552 | 2,772        |
| **Enterprise value**       | 1,475 | 3,306 | 3,280     | 4,978 | **3,260**    |
| + Standalone assets        | 282   | 282   | 282       | 282   | 282          |
| − Debt and debt-like items | (984) | (984) | (984)     | (984) | (984)        |
| **Equity value**           | 773   | 2,604 | 2,578     | 4,276 | **2,558**    |
| **US$ per diluted share**  | 27.7  | 93.4  | 92.4      | 153.3 | **91.7**     |
| C$ per share (×1.421)      | 39.4  | 132.7 | 131.3     | 217.8 | **130.3**    |

*Script (3a), (4). Diluted shares: 27.90M. C$ conversion uses the C$/US$ rate implied by Boyd's own Jun-30-2026 balance sheet (§6), not a current market rate.*

**How the weights were set.** The no-growth case keeps every base-case operating driver but opens no stores from 2026 (Forecast, lines 42-43). It is therefore an alternative capital-allocation path *under base conditions*, and it takes half of the base's 50% weight. That keeps the operating-driver mix at 25/50/25 bear/base/bull, as in the forecast (Forecast, lines 32-37). Because the base and no-growth cases are worth almost the same (US$93.4 vs US$92.4), the weighting choice moves the headline by only US$0.2: the old 25/50/25 weights with the new bridge give US$91.9 (Script, 4).

**Answer: ~US$92 per diluted share (~C$130), probability-weighted.** The range that matters is **US$77–92**:

- **US$92** uses the terminal values in TV, which are set from collision-repair deal multiples (base 8.5x EBITDA after rent).
- **US$77** replaces them with a perpetuity at this model's own 10% rate. That is a 10%-consistent cross-check, and it implies 8.0x base EBITDA after rent (§4.2).

The gap exists because TV's multiples imply discount rates of 7.8–9.0% across the four cases (Bear 7.76%, Base 8.58%, No growth 8.98%, Bull 8.42%; TV, line 287; `valuation.xlsx` sheet 2, section 2.12), all below the 10% used here. §4.2 explains why I keep the deal-multiple version as the headline and show the other as the lower end.

**Four things carry the answer:**

1. **The terminal value is most of enterprise value.** It is ~90% in the growth cases and 72% in the no-growth case (Script, 3a). Each ±0.5x on the exit multiple moves value by ~±US$6 per share (Script, 5b).
2. **Leverage turns scenario spread into a much wider equity spread.** The bridge deducts $700M net, about a fifth of enterprise value. So bear equity (US$28) is 30% of base equity, while bear EV is 45% of base EV.
3. **Growth capex is roughly value-neutral.** The existing-business-only case, which opens no stores, is worth US$92.4, against US$93.4 for the base (Script, 3a). The answer does not depend on believing management's unit-growth plans.
4. **Tax shields add US$10.1 per share** ($281.5M, §5). US$5.4 of that is JH, on Boyd's own figure. US$4.7 is legacy goodwill and intangibles, scaled from the JH figure by their relative book size.

---

## 2. Method and timing convention

```
Enterprise value = Σ distributable_t / (1 + r)^t   for t = 0 (2026) … 5 (2031)
                 + TV_2031 / (1 + r)^5
Equity value     = Enterprise value + standalone assets − debt and debt-like items (Jun-30-2026)
Per share        = Equity value ÷ current diluted shares (27,898,409)
r = 10% (ValuationSettings.discount_rate)
```

The core of `valuation.py`:

```python
def discount_factor(year, rate):                      # 2026 -> t=0, 2031 -> t=5
    return 1.0 / (1.0 + rate) ** (year - SETTINGS.valuation_year)

def enterprise_value(name, rate, tv_method="exit", multiple=None):
    terminal = terminal_value_exit_multiple(name, multiple) if tv_method == "exit" \
        else terminal_value_perpetuity(name, rate)
    pv_cf = sum(cf * discount_factor(yr, rate) for yr, cf in cash_flows(name).items())
    pv_tv = terminal * discount_factor(SETTINGS.terminal_year, rate)
    return {"pv_cash_flows": pv_cf, "terminal_value": terminal, "pv_terminal": pv_tv, "ev": pv_cf + pv_tv}

def equity_value(ev, rate):
    return ev + standalone_assets(rate)["total"] - debt_items()["total"]
```

**Which earnings are discounted.** The cash flow is **distributable cash = Owners' Earnings (OE) − growth capex − one-off integration costs**, not OE alone. The terminal value capitalizes earnings from stores that 2026–31 growth capex pays for (TV, line 288). Discounting OE while ignoring that capex would count the growth twice. This is the pairing both prior work products require (Forecast, line 351; TV, line 288). OE is pre-interest and taxed at the 26.5% statutory rate (OE & ROIC, §2.6). It is charged full cash rent, so lease liabilities are not debt (OE & ROIC, line 274).

**Timing.** Per the task, 2026 is t=0 and is not discounted, 2027 is t=1, and so on to 2031 at t=5. The terminal value is an end-2031 value, so it is discounted at the same t=5 as the FY2031 cash flow (factor 0.621, Script, 1).

**The 2026 stub (only H2 is counted).** The bridge uses the Jun-30-2026 balance sheet, and H1-2026 cash is already inside that net debt. Counting all of FY2026E distributable would count H1 twice. The stub is:

- **H2 OE** = FY2026E OE × H2 share of EBITDA after rent. H1 EBITDA after rent was actual: $258.3M − $107.9M rent = $150.4M (Forecast, lines 157, 341). The H2 share is 53.1% in the base.
- **Less H2 growth capex** = FY2026E growth capex − H1 actual net growth spend of $32.9M (Forecast, line 200).
- **Less one-off costs.** The forecast's one-offs already start in Jul-2026 (Forecast, line 353), so all of the 2026 amount counts.

Base: $93.3M − $83.0M − $19.1M = **−$8.8M**, against FY distributable of $40.8M (Script, 2). The capex term is conservative: the 31 units left for H2 at the forecast's unit costs would cost ~$67M, not $83M (inference; ~US$0.6 per share).

**Scenarios.** Four cases are weighted 25% each: the forecast's bear, base and bull, plus the no-growth-capex case (§1). Each case's cash flows are paired with its own terminal value. The bridge and share count are the same in all four.

---

## 3. Explicit-period cash flows

| Distributable (US$M) | 2026 H2 | 2027  | 2028  | 2029  | 2030  | 2031  | PV @10% |
|----------------------|---------|-------|-------|-------|-------|-------|---------|
| t / discount factor  | 0/1.000 | 1/.909| 2/.826| 3/.751| 4/.683| 5/.621|         |
| Bear                 | −9.1    | 67.1  | 77.1  | 75.2  | 67.6  | 59.8  | 256     |
| **Base**             | −8.8    | 44.6  | 77.8  | 102.3 | 121.6 | 142.0 | **344** |
| Bull                 | −13.0   | 37.4  | 85.1  | 127.9 | 164.5 | 203.9 | 426     |
| No growth capex      | 74.2    | 184.2 | 215.1 | 233.9 | 246.4 | 259.5 | 925     |

*Script (2). Base OE is $176M in 2026E and $302M in 2031E. Base growth capex is $116–160M a year (Forecast, lines 33, 38).*

The explicit period is small: 10% of base EV. Growth capex absorbs most of OE until 2028. In the bear, distributable cash is higher than in the base in 2027, because the bear opens fewer stores (Forecast, line 183).

---

## 4. Terminal value

### 4.1 Headline: TV's deal-multiple values

| End-2031 (TV, l.35-41)    | EBITDA-R 2031E | Multiple | Ramp uplift | **TV**    | PV @10% |
|---------------------------|----------------|----------|-------------|-----------|---------|
| Bear                      | 312            | 6.0x     | 93          | 1,964     | 1,220   |
| **Base**                  | 520            | 8.5x     | 348         | **4,771** | 2,962   |
| Bull                      | 666            | 10.0x    | 670         | 7,331     | 4,552   |
| No growth capex           | 446            | 8.5x     | 0           | 3,794     | 2,356   |

*EBITDA-R = Adjusted EBITDA after rent. The terminal value is an enterprise value, with rent already deducted (TV, §2). The ramp uplift is the multiple applied to new-store earnings that capex has already paid for but that are not yet earned in 2031 (TV, §9).*

TV sets the multiples from collision-repair valuation evidence. Platform-grade MSOs trade at 8–12x (Knowledge Store ID 11), and Boyd's own Joe Hudson's price was 9.3x after synergies (JH release, line 43). Boyd sits in the lower half of that range because of insurer concentration, total-capital ROIC near its cost of capital, and no synergies left to sell (TV, §3, §6).

### 4.2 Cross-check: a perpetuity at this model's 10%

I also recomputed the terminal value with TV's own value-driver formula (TV, §8) at r = 10% instead of 8%:

- **Formula:** OE multiple = (1 + g)(1 − reinvestment) ÷ (r − g). Base g is 2.5% and reinvestment 6.5% (`terminal_value.py`, `STEADY`).
- **What it is applied to:** run-rate FY2031E OE, meaning 2031E OE plus the OE of 2026–31 stores still ramping. That is $302M + $24M in the base (Forecast, line 352).

| Scenario        | Perpetuity TV @10% | = × EBITDA-R | TV chosen multiple | US$/share (perp.) |
|-----------------|--------------------|--------------|--------------------|-------------------|
| Bear            | 1,553              | 5.0x         | 6.0x               | 18.6              |
| **Base**        | 4,173              | **8.0x**     | 8.5x               | 80.0              |
| Bull            | 6,263              | 9.4x         | 10.0x              | 129.5             |
| No growth capex | 3,308              | 7.4x         | 8.5x               | 81.6              |
| **Weighted**    | 3,824              |              |                    | **77.4**          |

*Script (3b), (5c). Weighted uses the four 25% weights.*

**Why the deal-multiple version is the headline, and the 10% perpetuity the low end:**

- **Both land inside the evidence.** At 10%, the perpetuity implies 8.0x base EBITDA-R. That is the bottom of the platform range (8–12x, Knowledge Store ID 11) and below Joe Hudson's 9.3x. The two methods therefore differ by only 0.5–1.0x of multiple, not in kind.
- **The headline reflects a realizable exit.** The deal multiple is what private buyers of collision platforms are observed to pay (Knowledge Store IDs 11, 19; JH release, line 43). Discounting it at 10% answers the question "what do I pay today to earn 10% if I can sell in 2031 at a normal platform price?"
- **The low end is the stricter case.** The perpetuity instead assumes the owner holds forever and demands 10% throughout. That is the more conservative question, and it is why US$77 is the low end of the range.
- **Stated plainly:** the headline assumes private-market buyers in 2031 will still accept returns of roughly 7.8–9.0% (8.6% in the base case) on Boyd-like earnings (TV, §8). If deal pricing converges to a 10% required return, value is US$77, not US$92.

---

## 5. Equity bridge: standalone assets and all debt (Jun-30-2026)

| Item (US$M)                                       | Amount    | Source                          |
|---------------------------------------------------|-----------|---------------------------------|
| **Standalone assets**                             |           |                                 |
| Excess cash ($23.0M cash, below $25M op. need)    | 0.0       | Q2FY26 FS l.17; OE & ROIC l.189 |
| JH tax shield (Boyd's own estimate)               | 150.0     | JH release l.43                 |
| Legacy tax shield ($150M × 0.866 ratio)           | 129.9     | JH release l.43; Q2FY26 FS l.28 |
| Other 2026 acq. tax shield ($150M × 0.011 ratio)  | 1.6       | Q2FY26 FS l.249-258             |
| **Total standalone assets**                       | **281.5** |                                 |
| **Debt and debt-like items**                      |           |                                 |
| Revolver and swing line                           | 285.3     | Q2FY26 FS l.458                 |
| Term Loan A                                       | 125.0     | Q2FY26 FS l.459                 |
| Seller notes (deferred acquisition consideration) | 8.6       | Q2FY26 FS l.460                 |
| Senior notes 2030, C$525M principal               | 369.4     | Q2FY26 FS l.496                 |
| Senior notes 2033, C$275M principal               | 193.5     | Q2FY26 FS l.497                 |
| Dividends payable                                 | 3.1       | Q2FY26 FS l.34                  |
| Cross-currency swaps, net asset ($4.3M − $3.0M)   | (1.3)     | Q2FY26 FS balance sheet         |
| **Total debt and debt-like**                      | **983.5** |                                 |
| **Net (standalone assets − debt)**                | **(702.0)** |                               |

*Script (4). The debt total ties to Boyd's own "total debt before lease liabilities" of $976.0M (Q2FY26 MD&A, line 369), after four adjustments. (1) Notes are taken at principal, adding back $10.2M of unamortized financing costs. (2) The $4.4M embedded derivative is excluded. (3) The swaps are netted. (4) Dividends payable are added. Taken together these add $7.5M. Cash is not netted, for the reason below.*

**How each choice was made:**

- **Cash is operating, not excess.** OE & ROIC counts cash up to $25M as operating capital inside invested capital (OE & ROIC, line 189). The Jun-26 balance of $23.0M is below that, so none of it is standalone. OE & ROIC's own bridge added the $23.0M back (OE & ROIC, line 265), which is inconsistent with that treatment. Counting it would add US$0.8 per share (Script, 5d).
- **Tax shields on all goodwill and intangibles (asset, $281.5M, US$10.1 per share; judge r2, r3).**
  - *Why they are extra value.* OE is taxed at the full statutory rate with **no** deduction for goodwill or intangibles (OE & ROIC, §2.6). Every dollar of remaining tax basis is therefore value outside the cash flows. It is not in the terminal value either: TV's main anchor, JH's 9.3x, is a price "net of expected tax benefits" (JH release, line 43), so an EBITDA multiple does not pay for the shield.
  - *JH: $150.0M, Boyd's own figure.* The JH release says "expected tax benefits of approximately $150 million" (JH release, line 43). It matches the filings: $366.3M of deductible goodwill and $602.6M of deductible intangibles (Q2FY26 FS, lines 316, 318) × 26.5% ÷ 15 years is $17.1M a year. That is worth $152M at 8%, but $137M at this model's 10% (Script, 4). Boyd's figure is therefore ~US$0.5 per share more generous than a 10% discount would give. It also dates from the deal announcement, so it does not remove the H1-2026 deductions already used.
  - *Legacy (pre-2026) goodwill and intangibles: $129.9M, ratio method (judge r3).*

    | Goodwill + intangibles (US$M)   | Goodwill | Intangibles | Total   |
    |---------------------------------|----------|-------------|---------|
    | JH (revised provisional PPA)    | 521.8    | 700.8       | 1,222.6 |
    | Legacy (Dec-31-2025 book)       | 702.5    | 356.3       | 1,058.8 |
    | Other 2026 acquisitions         | 7.2      | 5.7         | 12.9    |

    - *Sources.* JH intangibles are $700.0M customer relationships + $0.5M brand + $0.3M intellectual property. JH and other-2026 amounts come from the acquisition table (Q2FY26 FS, lines 249-258). Legacy amounts are the Dec-25 balance sheet (Q2FY26 FS, line 28).
    - **Legacy = $150M × (1,058.8 ÷ 1,222.6 = 0.866) = $129.9M.** Other 2026 acquisitions = $150M × (12.9 ÷ 1,222.6) = $1.6M (Script, 4).
    - *What the ratio assumes.* The shield is proportional to book goodwill + intangibles, with the same deductible share, remaining tax life and discount as JH. Three differences push in opposite directions:
      - *Legacy is partly used up (points lower).* ~$294M of legacy basis has already been deducted: the $77.9M intangibles deferred tax liability ÷ 26.5% (FY2025 AFS, lines 857, 872).
      - *JH has a non-deductible slice (points higher).* $155.5M of JH goodwill and $97.9M of JH intangibles are not deductible (Q2FY26 FS, lines 316, 318).
      - *Legacy runs off sooner (points higher per dollar).* The remaining legacy basis is deducted over fewer years.
    - *Legacy deductibility.* 2023–25 goodwill is disclosed as deductible (FY2023 AFS, line 761; FY2024 AFS, line 658; FY2025 AFS, line 703). Earlier goodwill is assumed deductible too (*inference*).
    - *Cross-checks (Script, 4).*
      - A tax-basis ratio ($765M remaining legacy basis ÷ $968.8M JH deductible basis = 0.789) gives $118.4M.
      - The r2 build (PV at 10% of $85.5M a year of deductions over ~8.9 years) gave $131.6M.
      - The ratio result sits inside that range, and the spread is ~US$0.4 per share.
      - The implied ~$22.7M a year of legacy tax savings fits inside the observed gap between cash taxes and OE's normalized tax: $19.8M, $20.8M and $35.6M in FY2023–25 (OE & ROIC, lines 87, 105).
    - *Sensitivity.* Dropping the legacy and other-2026 shields entirely gives US$87.0 (Script, 5d).
  - *Other 2026 acquisitions: $1.6M* (ratio method, above).
  - *Not included:*
    - *Future tuck-in acquisitions.* The goodwill they create would also be deductible. That would slightly favor the growth cases over the no-growth case.
    - *Canadian goodwill.* In Canada it is deducted much more slowly (*internal AI model knowledge*: 5% declining balance). The ratio method implicitly treats the Canadian share of the legacy basis like US basis, a small overstatement.
    - *Taxable-income capacity.* The JH and legacy deductions together are ~$150M a year, against pre-tax OE of ~$240M before interest. They should be usable, but any deferral would lower the value (*inference*).
- **Lease liabilities ($1,050.9M): not deducted.** Full cash rent is already charged in OE, and EBITDA-R in the terminal value is after rent. Deducting them too would double-count (OE & ROIC, line 274). For scale, doing it anyway would cut value to US$54 per share (Script, 5d).
- **Net deferred tax liability ($94.3M): not deducted** (reconciled in r1, Script, 5e). This departs from OE & ROIC's bridge (OE & ROIC, line 269). The test is simple: does the liability create cash tax *above* the tax OE already charges? OE's baseline is 26.5% × (Adj. EBITDA − rent − maintenance capex), with **zero** deductions for goodwill or intangibles and tax depreciation equal to maintenance capex (OE & ROIC, line 89).
  - *Intangibles part ($77.9M at Dec-25; FY2025 AFS, lines 857, 872).* This liability equals 26.5% × (book value − tax basis). Future amortization deductions equal the remaining tax basis, which can never be negative. Against OE's zero-deduction baseline, the liability therefore never produces extra cash tax. It only means the legacy shield (counted above) is ~$294M of basis smaller than book value implies, which is exactly how the shield estimate uses it. **So the liability and the legacy shield are not mirror images relative to OE.** The liability measures how much of the shield has already been used. Deducting it would charge a second time for taxes OE already assumes are paid in full. Part of it is purely a bookkeeping entry: the $25.5M recorded on JH's non-deductible intangibles (Q2FY26 FS, line 318) reverses through book amortization, never through cash.
  - *Property part ($58.6M at Dec-25; FY2025 AFS, lines 856, 871).* This arises from accelerated (bonus) tax depreciation. It would cost cash only if future tax depreciation fell *below* maintenance capex. That can happen if new capex stops being expensed immediately and has to be depreciated over several years instead. Continued full expensing is *internal AI model knowledge* (the 2025 US tax law restored 100% bonus depreciation) and is not in the sources. Deducting this part alone would cost US$2.1 per share, which is the residual risk in this choice.
  - *Evidence the baseline is conservative.* Cash taxes ran $19.8M, $20.8M and $35.6M below OE's normalized tax in FY2023–25 (OE & ROIC, lines 87, 105; Script, 5e). There is no sign of reversal.
  - *Cost if deducted anyway.* Deducting the whole net liability costs US$3.3–3.4 per share (Script, 5d, 5e).
- **Pensions: none.** Boyd has only defined-contribution plans, whose cost is expensed as paid (FY2025 AFS, lines 1438-1440). There is no funding shortfall.
- **Off-balance-sheet items: none material.**
  - *Purchase obligations.* Boyd's contractual-obligations table lists them with repayment "nil" if conditions are met (FY2025 MD&A, lines 399-401).
  - *Contingent consideration.* No liability appears on the Jun-30 balance sheet (Q2FY26 FS, lines 30-45). The only related line is a $1K fair-value adjustment in H1-2025 (Q2FY26 FS, line 616).
  - *Leases not yet commenced.* None are disclosed.
- **Remaining integration costs.** Not deducted here, because they are already in the 2026–27 cash flows as one-offs (Forecast, line 353).
- **Cash-settled share units (DSU, 2023–24 RSU/PSU).** Not deducted separately. They sit in accrued liabilities, which OE treats as operating working capital (OE & ROIC, line 156). They are small: the deferred tax asset of $1.6M on DSUs (FY2025 AFS, line 861) implies a liability of ~$6M (inference).
- **Not counted (upside):**
  - *Tax losses.* US and Canadian losses of $37.4M and $24.4M (FY2025 AFS, line 903) are worth roughly $16M (inference).
  - *Interest tax shield.* Interest is deductible, but this OE framework ignores the saving.

---

## 6. Share count and currency

- **Diluted shares: 27,898,409.** That is 27,836,435 shares outstanding at Jun-30-2026 (Q2FY26 FS, line 88) plus 61,974 dilutive RSU/PSU units. The units are the gap between Q2 diluted and basic weighted shares (Q2FY26 FS, lines 128-129). Boyd notes that "no stock option plans" were dilutive in Q2 (Q2FY26 FS, line 669).
- **Option overhang is small.** Even if the whole 250,000-share option plan (FY2025 AFS, line 459) were issued with no exercise proceeds, value would fall only to US$90.9 (Script, 5d).
- **NCIB buybacks are not reflected.** Any purchases under the buyback program, which began on Sep-16-2026 (Knowledge Store ID 5), are not in the count. The share count used is the current one, not a forecast.
- **Currency.** Boyd reports in US$, but BYD.TO trades in C$. The C$ figures use C$1.421 per US$. That rate is implied by Boyd's own Jun-30 balance sheet: C$800M of notes principal (FY2025 MD&A, lines 25, 35) carried at US$563.0M (Q2FY26 FS, lines 496-497). No market data is used. The current rate may differ, so **treat the US$ value as primary.**

---

## 7. Sanity checks

| Check                                          | Result        | Reading                                   |
|------------------------------------------------|---------------|-------------------------------------------|
| Base EV ÷ 2026E / 2027E EBITDA after rent      | 10.3x / 9.3x  | Inside the platform range, 8–12x (KS 11)  |
| Base EV ÷ 2026E / 2027E OE                     | 18.8x / 16.5x | 5.3% OE yield: needs ~4–5% growth at 10%  |
| Base EV ÷ Jun-26 invested capital ex-leases    | 1.14x         | Modest premium to capital deployed        |
| No growth capex vs base (US$/share)            | 92.4 vs 93.4  | Growth program ≈ value-neutral            |
| JH shield: own formula @8% vs Boyd's figure    | $152M / $150M | Boyd's $150M ≈ an 8% discount rate        |
| Legacy shield: ratio / tax-basis / r2 build    | $130/118/132M | Three methods agree within ~$13M          |

*Script (4), (6).*

- **The EV/EBITDA-R cross-check is not independent, but it is coherent.** Paying 9.3x 2027E EBITDA-R is close to what Boyd paid for Joe Hudson's after synergies (9.3x, JH release, line 43).
- **EV/invested capital of 1.14x is plausible against ROIC.** Total-capital ROIC is 6.5–7.1% today and 8.3% by 2031E (OE & ROIC, line 17; Forecast, line 299), below a 10% required return. A premium to capital is still justified, because OE grows ~8% a year to 2031 from savings and price-led same-store growth that need no capital (Forecast, line 54). The premium would be hard to defend if those savings and margins do not arrive.
- **The 18.8x 2026E OE multiple is demanding.** It relies on base OE rising 72% to 2031, from $176M to $302M (Forecast, line 33). At a 14.0% existing-business margin in 2031, instead of the base's 14.9% (which exceeds management's target), the base terminal value would be $339M lower (TV, line 280). That is ~US$7.5 per share (inference: $339M × 0.621 ÷ 27.9M shares).

---

## 8. Sensitivities

**Discount rate (US$ per share):**

| Discount rate | Weighted, exit TV | Base, exit TV | Weighted, perp. TV | No growth, exit TV |
|---------------|-------------------|---------------|--------------------|--------------------|
| 8%            | 102.3             | 104.4         | 120.6              | 102.2              |
| 9%            | 96.8              | 98.7          | 95.6               | 97.2               |
| **10%**       | **91.7**          | **93.4**      | **77.4**           | **92.4**           |
| 11%           | 86.8              | 88.3          | 63.6               | 87.9               |
| 12%           | 82.2              | 83.5          | 52.8               | 83.6               |

*Script (5a). All tax shields are held fixed (JH at Boyd's $150M; the others are ratios of it). The exit-multiple TV is held fixed. The perpetuity TV is recomputed at each rate, which is why it is far more rate-sensitive. The two columns cross near 9%, where the multiples and the formula agree (TV, line 287).*

**Exit multiple, all scenarios shifted (US$ per share, at 10%):**

| Shift       | −1.5x | −1.0x | −0.5x | **0**    | +0.5x | +1.0x |
|-------------|-------|-------|-------|----------|-------|-------|
| Weighted    | 74.4  | 80.2  | 85.9  | **91.7** | 97.4  | 103.2 |
| Base        | 74.6  | 80.9  | 87.1  | **93.4** | 99.6  | 105.8 |

*Script (5b).*

**Bridge alternatives (weighted, US$ per share):**

| Alternative                                  | Value |
|----------------------------------------------|-------|
| Headline                                     | 91.7  |
| Also deduct net deferred tax                 | 88.3  |
| Drop all goodwill/intangible tax shields     | 81.6  |
| Drop only legacy + other-2026 shields        | 87.0  |
| JH at own formula @10% ($137M) not $150M     | 91.2  |
| Count all $23.0M cash                        | 92.5  |
| Full 250k option overhang                    | 90.9  |

*Script (5d).*

---

## 9. What I am confident about vs. what is uncertain

**Confident:**

- **The bridge.** Debt is read straight off the Jun-30-2026 balance sheet and ties to Boyd's own $976.0M within $7.5M. Leases are correctly left out, because rent is in OE. There is no pension deficit and no material off-balance-sheet claim.
- **The pairing of cash flows and terminal value.** Distributable cash goes with the growth terminal value, and existing-only cash with the no-growth terminal value. The two give almost the same answer (US$93 vs US$92), so the value does not rest on the new-store return assumption, and weighting them together (judge r2) barely moves the headline.
- **The share count.** It is Boyd-reported, and dilution is immaterial.

**Uncertain (in order of impact):**

1. **The terminal value, ~90% of EV.**
   - *Method.* The choice between a deal multiple and a 10% perpetuity alone moves value from US$92 to US$77.
   - *Multiple.* ±1x of multiple is ±US$12.
   - *Evidence.* The peer data is thin and mostly secondary (TV, §11).
   - *Benchmark risk.* A Caliber IPO could reset it (Knowledge Store ID 23).
2. **2031 margin and OE.** The base existing-business margin of 14.9% is above management's 14% target (Forecast, line 153). Industry repair cost (TCOR) and share gains are the main swing factors for OE (Forecast, §8).
3. **Bear-case equity is thin.** At US$28 per share, leverage of ~3x EBITDA-R (Forecast, line 309) absorbs most of the bear EV. The four 25% weights are judgment.
4. **Tax items.**
   - *Shields.* They add US$10.1 per share: JH US$5.4 on Boyd's figure, and legacy US$4.7 from the JH ratio. The legacy part rests on inferred deductibility of pre-2023 goodwill. A tax-basis ratio would give US$4.2 instead.
   - *Deferred tax.* Deducting the property part of the deferred tax liability would cost US$2.1. That is the one piece with real reversal risk, if full expensing ends.
   - *Loss carryforwards.* Worth ~US$0.6 and not counted.
5. **Currency.** The C$ figure uses a Jun-30 book-implied rate, not a current market rate.

**Bottom line:** intrinsic value is **~US$92 per diluted share (~C$130)**, with **US$77–92** as the defensible range at a 10% required return. The range turns mainly on whether 2031 deal multiples hold at ~8.5x EBITDA after rent. The bear case (US$28) shows how much leverage magnifies any shortfall in the margin recovery.
