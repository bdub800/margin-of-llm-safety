# NamSys Inc. (TSXV: CTZ) — Terminal Value at the End of FY2030E

*Prepared September 17, 2026. All figures in Canadian dollars. Fiscal year ends October 31, so "terminal value" here means the value of the **operating business** at October 31, 2030, expressed as a multiple of FY2030E owners' earnings. **It is deliberately not discounted to present value.** Every number is an output of `work_products/terminal_value_calcs.py`; run it with `uv run python work_products/terminal_value_calcs.py`. Each input in that script carries a source tag in a comment. This document is stock-price-blind: no NamSys quote, market capitalisation or NamSys-derived multiple is used anywhere, and the peer research was explicitly instructed to exclude them. No per-share figures are produced.*

Source tags used throughout:

| Tag     | Source                                                     |
|---------|------------------------------------------------------------|
| `FC`    | `work_products/forecast_earnings.md`                       |
| `OE`    | `work_products/owners_earnings_and_roic.md`                |
| `FS25`  | `primary_sources/FY2025/NamSys_AFS_022426.md`              |
| `MDA25` | `primary_sources/FY2025/NamSys_MDA_022426.md`              |
| `FSQ2`  | `primary_sources/2Q2026/FS_Q2_NamSys_Apr_30_26_FINAL.md`   |
| `AM25`  | `fetched_docs/namsys_2025_annual_meeting_transcript.md`    |
| `AM26`  | `fetched_docs/namsys_2026_annual_meeting_transcript.md`    |
| `PEER`  | `work_products/peer_multiples_scrape.py` (stockanalysis.com, scraped Sep 17, 2026). *Amended Sep 17, 2026 after verifier round 1: MNDO, NTWK, DOTD and IGP were added to the script's `PEERS` list so that it now reproduces every row of the §4.1 comp table; the four values were unchanged by the re-run.* |
| `DEAL`  | `work_products/peer_deal_multiples.py` (company / press-release URLs in the script) |

---

## 1. Headline

**Base case: 12× FY2030E owners' earnings of \$2,859,320 = \$34.3 million of operating-business value at October 31, 2030.**

| Scenario (FY2030E owners' earnings, `FC` §1)   | 9×          | **12×**         | 15×         |
|------------------------------------------------|-------------|-----------------|-------------|
| Bull (\$4,649,840)                             | 41,848,560  | 55,798,080      | 69,747,600  |
| **Base (\$2,859,320)**                         | 25,733,880  | **34,311,840**  | 42,889,800  |
| Bear, management right-sizes (\$2,094,988)     | 18,854,892  | 25,139,856      | 31,424,820  |
| Bear, no cost response (\$1,505,664)           | 13,550,976  | 18,067,968      | 22,584,960  |

The multiple and the earnings path are **not independent** — a scenario in which earnings compound at 15.6%/yr is also one in which the business has demonstrably become less concentrated and more repeatable, and vice versa. Reading the table across a single multiple therefore understates the true spread. The scenario-consistent diagonal:

| Scenario                     | Multiple | FY2030E owners' earnings | Terminal value | Why this multiple                                                                       |
|------------------------------|----------|--------------------------|----------------|-----------------------------------------------------------------------------------------|
| Bull                         | 15×      | 4,649,840                | 69,747,600     | A second Mexico-sized international account (`FC` §8) proves the motion repeats and cuts concentration |
| **Base**                     | **12×**  | **2,859,320**            | **34,311,840** | See §3–§5                                                                               |
| Bear, management right-sizes | 8×       | 2,094,988                | 16,759,904     | A top-3 account has been lost; a shrinking, still-concentrated microcap                 |
| Bear, no cost response       | 8×       | 1,505,664                | 12,045,312     | As above, and management has also demonstrated it will not defend margin                |

**Two things this number is not.** It excludes the financial portfolio — ~\$7.37M of cash and short-term investments at April 30, 2026 (`OE` §1) — because owners' earnings deliberately exclude interest income on it (`OE` §4). That portfolio is a separate asset to be added alongside the operating value, not capitalised at 12×. It also excludes any acquisition NamSys might complete, which management has pursued unsuccessfully "for several years... but it is not for lack of trying" (`AM26`).

---

## 2. What is being multiplied, and how it maps onto peer metrics

The forecast object is owners' earnings: normalised operating income, plus depreciation less maintenance capex, taxed at the 26.5% statutory rate, with share-based compensation treated as non-deductible, and with interest income excluded (`OE` §2, `FC` §2.1). Because operating invested capital is negligible (~\$0.99M at FY2025 year-end, 12.6% of revenue — `OE` §3.1) and there is no debt, **essentially 100% of owners' earnings is distributable each year without impairing the business** (`OE` §5). That is what makes a simple multiple defensible here: there is no reinvestment wedge to model between earnings and cash to owners.

Peers are quoted on EV/EBIT and EV/EBITDA, so a conversion is needed:

| Quantity (FY2030E base case, `FC` §1)         | Value      |
|-----------------------------------------------|------------|
| Revenue                                       | 11,462,356 |
| Operating income (EBIT)                       | 3,936,580  |
| Owners' earnings                              | 2,859,320  |
| Owners' earnings ÷ EBIT                       | 0.7263     |
| (1 − 26.5% statutory tax rate), for reference | 0.7350     |

So **a peer EV/EBIT multiple of X is equivalent to X × 1.377 turns of owners' earnings.** The 0.7263 factor is only 0.9pp below the plain after-tax factor, the gap being the non-deductible share-based compensation and the small depreciation-versus-maintenance-capex adjustment (`FC` §5.2). Depreciation was \$7,465 in FY2025 against total property and equipment of \$34,689 (`FS25` Note 4), so **EBITDA and EBIT differ by 0.19%** for NamSys and EV/EBITDA and EV/EBIT multiples can be treated as interchangeable for this company. They cannot be for capital-intensive peers such as Brink's or Loomis, which is one reason those comps are used only as a cross-check.

---

## 3. The qualitative case — what the multiple has to reflect

A terminal multiple is a statement about the **perpetuity beyond FY2030**, not about the five forecast years, which are already in the earnings number. The question is therefore narrow: how durable and predictable are owners' earnings of roughly \$2.9M after FY2030, and what growth do they carry?

### 3.1 What genuinely supports a premium multiple

**Revenue is about as recurring as it gets.** FY2025 revenue of \$7,891,605 splits \$7,811,909 "software subscriptions, hosted services, maintenance and product support" versus \$79,696 professional services (`FS25` Note 7) — **99.0% recurring**, corroborated by management ("99% of that revenue remains recurring", `AM26`).

**Churn is near zero, and the product is genuinely mission-critical.** "As in previous years, we experienced no customer churn... Our systems are truly mission critical to their business" (`AM25`); "Historically, we've had little or no churn of customer accounts" (`AM25`). The Currency Controller product "is mission critical as it handles most of the cash and transit to bank integration" (`AM25`). Net revenue retention was 112% in FY2024 (`AM25`). This is the single strongest fact in the terminal-value case: the earnings stream is a subscription annuity on infrastructure the customer cannot easily switch off.

**Margins are high and management believes they are stable.** FY2025 operating margin 39.9%, owners'-earnings margin 28.5% (§2 of the script, on `FS25`/`OE` figures). "Margins remained consistent with last year, with gross margins of 64% and a net margin of 32%. And we feel that these margins will remain stable going forward" (`AM26`). The base-case forecast is *more* conservative than that, letting the owners'-earnings margin drift to 24.9% by FY2030E (`FC` §1).

**Capital intensity is effectively nil, so earnings equal cash to owners.** ROIC on period-end operating invested capital was 227% in FY2025 (`OE` §3.2); NamSys "added ~\$2.5M of revenue and ~\$1.1M of owners' earnings over three years while consuming roughly \$150k of additional operating capital" (`OE` §3.2). Even the deliberately punitive definition that capitalises three years of all cost-of-sales compensation leaves ROIC at ~37% (`OE` §3.3). The honest finding is "ROIC is very high and not a constraint," not any point estimate (`OE` §5) — and that is exactly what a multiple needs: growth does not have to be bought.

**No debt, and a demonstrated willingness to return capital.** Special dividends of \$1,350,477 (FY2024) and \$4,027,790 (March 2026) plus continuous buybacks (`MDA25`, `FSQ2` Note 6). Shareholders are actually paid the owners' earnings; this is not a company where distributable cash disappears into unexplained reinvestment.

**The demand substrate is stable, on independent evidence.** The Federal Reserve's 2026 Diary of Consumer Payment Choice found cash used for about 1 in 7 US payments and that "U.S. consumer payment use remained largely consistent over the past three years" (Knowledge Store ID 12). This matters because the cost driver is physical, not monetary: "it doesn't matter if you are handling \$500 or \$5,000, the cost to move and count those notes is the same" (`AM26`), so demand tracks endpoint counts — trucks, safes, vaults — rather than the dollar value of cash. Note the Fed data *corrects* management's "approximately one in five payments" claim (`AM25`) on level, while corroborating the load-bearing stability claim.

### 3.2 What forces a discount — and these are large

**Customer concentration is severe and is not improving.** Three customers accounted for 15.9%, 12.3% and 10.7% of FY2025 revenue (`FS25` Note 7), 20.0%/8.9%/8.9% in FY2024, and 13.1%/12.8%/11.4% in H1 FY2026 (`FSQ2` Note 7 via `FC` §4.1) — **37–39% of revenue in the top three in every period**. Forty-nine percent of trade receivables were owed by three customers at October 31, 2025 (`FS25` Note 3). The base case has concentration *increasing*, with the inferred single Mexican account going from 10.7% of revenue in FY2025 to 15.8% by FY2030E (`FC` §4.4). Losing that account in FY2028 costs 41% of FY2030E owners' earnings (`FC` §7). A perpetuity on a revenue base where one phone call can remove a seventh of it does not deserve a high multiple, and — critically — the scenario table in `FC` §7 covers that risk only inside the FY2026–FY2030 window, whereas the multiple must price it **recurring forever**.

**And the mechanism by which such an account disappears is documented by the company itself:** "When two banks merge, the continuing entity usually selects one technology provider for a given function... the provider with the largest installed base in the combined entity will replace the provider with the smaller installed base" (`MDA25`, Market Condition Risks). NamSys is by construction the smaller installed base in most such comparisons.

**"Zero churn" is true at the account level and misleading at the dollar level.** The largest historical account went 24.9% → 20.0% → 15.9% of revenue (FY2023–FY2025) and to ~12.8% in H1 FY2026, shrinking ~11%/yr and then ~19% in constant currency (`FC` §4.2), and management confirms it was not lost ("we experienced no customer churn", `AM25`). So dollar retention inside retained accounts can be sharply negative. That is a material qualification on the durability claim above, and it is the reason I do not treat the annuity as bond-like.

**There is a hard structural ceiling on the core market.** "Approximately 75% of that market on the CIT side is controlled by Brinks and Loomis and Garda, of the remaining 25%, we feel we've got a small majority of those clients" (`AM26`). NamSys runs on ~8% of US cash-in-transit vehicles (`AM26`). By FY2030 the base case has the accessible US client tier largely worked through, which is why the US ex-legacy growth rate decays to 7% (`FC` §4.3, §9). The terminal state is a saturated domestic niche.

**Pricing power is weak and management says so.** Over five years "approximately 75% of it came from purely organic growth amongst our customers. Almost none of it came from price increases" (`AM26`); "routinely increasing prices is not something that we're planning to do"; and "pricing power is something that has been impacted by AI as well, honestly" (`AM26`). A perpetuity without a reliable price escalator cannot carry a high real growth rate — this is the main reason I do not use a terminal growth rate above inflation.

**The competitive position is asymmetric across the three products.** In Cirreon Retail (~40% of revenue, `AM26`) NamSys faces vertical integration by its own hardware ecosystem: "we are seeing more competition from the hardware manufacturers themselves... many are developing their own proprietary software" (`AM25`), and this is the product management repackaged "to try to reinvigorate growth for future years" (`AM25`) — i.e. the product it concedes is not growing. Two-fifths of revenue sits in the weakest competitive position.

**The claimed moat is prospective, not demonstrated.** "Effectively, you know, this becomes our moat... having Cirreon be embedded in the industry and be able to interconnect with all the different parts of this system" via MCPs and agent interoperability (`AM26`). This is a plan with no results in the accounts, and it is symmetric by construction — management concedes "we are not the only one with this tool... everybody now has access to agents and agentic coding" (`AM26`). I give it no weight in the multiple.

**Scale, key-person and liquidity risks.** Twenty-one employees (`AM26`); `MDA25` Risk Factors flag "Dependence on Management" and that "the loss of the services of key personnel could make it more difficult to successfully operate the Company's business." The company is TSXV-listed (`MDA25`, Market for Securities), and comparable TSXV/microcap names trade on 20-day volumes two to three orders of magnitude thinner than mid-cap software (`PEER`). Illiquidity is a genuine, if hard-to-size, multiple drag.

**Currency adds volatility to the terminal number that NamSys does not manage.** ~96% of revenue is USD against a majority-CAD cost base, and "we generally have not implemented hedging programs" (`MDA25`). Owners' earnings have ~2.6× elasticity to USD/CAD (`FC` §7), so a ±10% move shifts FY2030E owners' earnings by ±26%. The forecast holds USD/CAD flat at 1.39 as an explicit no-view assumption (`FC` §2.2); the terminal value inherits that assumption unchanged. This is a reason for a wider uncertainty band on the *earnings*, not a reason to lower the multiple, since the exposure is symmetric.

### 3.3 The one risk a five-year forecast cannot capture

The forecast horizon ends in 2030; a terminal multiple prices everything after it. The dominant post-2030 question is whether the cash endpoint universe is stable in perpetuity. The Fed data supports stability over a three-year window (Knowledge Store ID 12) and management notes "cash usage has at least historically increased during recessions" (`AM25`), but nothing in any source speaks to 2035 or 2045, and cash share of payments in most developed economies has trended down over decades. **This is not sourced in the materials available to me and I flag it as inference from general knowledge.** It is the principal reason I cap the terminal growth rate at roughly inflation rather than allowing the mid-single-digit growth that a 15×+ multiple would require.

### 3.4 Net qualitative verdict

This is a **genuinely high-quality small business with a genuinely fragile revenue base**. The quality is in the unit economics — 99% recurring, ~40% operating margin, three-digit ROIC, no capital needs, no debt. The fragility is in the customer list and the market ceiling — 37–39% in three accounts, a documented bank-merger displacement mechanism, a saturated domestic tier, no pricing escalator, and a 40%-of-revenue product under vertical-integration attack. Both statements are well sourced, and they pull the multiple in opposite directions by roughly similar amounts. That is why the answer lands in the low teens rather than at either the Enghouse-style high single digits or the Cerillion/ReposiTrak high teens.

---

## 4. Three anchors for the multiple

### 4.1 Anchor A — peer trading multiples (`PEER`)

Peer data was gathered from stockanalysis.com on September 17, 2026 and restated as turns of owners' earnings using the 1.377 factor from §2. *Caveat: this is third-party aggregator data, not audited filings, and is a snapshot of one day's prices. The peer research was cross-checked against a second independent aggregator, Simply Wall St (`fetched_docs/test_sws_engh.md`), on two names (Enghouse P/E 13.4 vs 13.41; VitalHub market capitalisation C\$467.4M vs C\$468.0M); cross-check attempts against GuruFocus (`fetched_docs/test_gf_engh.md`, HTTP 403) and the Wall Street Journal (`fetched_docs/test_wsj_engh.md`, CAPTCHA) were blocked and yielded nothing. Figures were also reconciled internally (market cap − net cash = EV; EV/Sales ÷ operating margin = EV/EBIT), but it carries more measurement risk than anything else in this document.*

| Peer                     | EV/EBIT | ⇒ × owners' earnings | Relevance                                                                |
|--------------------------|---------|----------------------|--------------------------------------------------------------------------|
| Mind C.T.I. (MNDO)       | 2.9     | 4.0                  | Shrinking high-margin microcap — floor observation                       |
| Enghouse (TSX:ENGH)      | 7.6     | 10.5                 | **Closest Canadian structural analogue**: mature, net cash, −4.7% growth |
| NetSol (NTWK)            | 7.8     | 10.7                 | Microcap software, low margin                                            |
| Dotdigital (AIM:DOTD)    | 8.1     | 11.2                 | Microcap SaaS, +2.2% growth, 16.0% EBIT margin                           |
| Glory (TYO:6457)         | 8.7     | 12.0                 | Cash-handling hardware incumbent                                         |
| Open Text (OTEX)         | 8.8     | 12.1                 | Mature, +1.5% growth, 22.9% EBIT margin, levered                         |
| eGain (EGAN)             | 9.0     | 12.4                 | Microcap SaaS, +3.1% growth                                              |
| Cerillion (AIM:CER)      | 11.7    | 16.1                 | **Closest margin analogue**: 39.5% EBIT margin, but −6.4% growth         |
| Evertz (TSX:ET)          | 11.7    | 16.1                 | Canadian small-cap, +3.9% growth (hardware, not SaaS)                    |
| Loomis (STO:LOOMIS)      | 12.1    | 16.7                 | Cash-logistics incumbent, capital intensive                              |
| Brink's (BCO)            | 13.0    | 17.9                 | Cash-logistics incumbent, capital intensive                              |
| ReposiTrak (TRAK)        | 16.4    | 22.6                 | **Closest quality analogue**: 32.2% EBIT margin, +6.6% growth            |
| Intercede (AIM:IGP)      | 17.4    | 24.0                 | Microcap, 18.4% EBIT margin, −1.3% growth                                |
| Constellation (TSX:CSU)  | 22.7    | 31.3                 | +17.7% growth serial acquirer — upper bound, not a comp                  |
| Descartes (TSX:DSG)      | 25.6    | 35.2                 | 32.0% EBIT margin but +13.2% growth, large and liquid                    |

Groupings, in turns of owners' earnings:

| Cluster                                                              | Range       | Mean  |
|----------------------------------------------------------------------|-------------|-------|
| Mature, low-growth microcap software (ENGH, OTEX, DOTD, NTWK, EGAN, CER, ET) | 10.5–16.1× | 12.7× |
| High-margin microcap software (CER, TRAK, IGP)                        | 16.1–24.0×  | 20.9× |
| Cash-ecosystem incumbents (Glory, Loomis, Brink's)                    | 12.0–17.9×  | 15.5× |

**Reading.** Dispersion in the small-cap software group is enormous (4.0× to 35×), and what separates the top from the bottom is **credible growth, not margin**: Cerillion at 39.5% EBIT margin but −6.4% growth gets 16.1×, while ReposiTrak at a lower 32.2% margin but +6.6% growth gets 22.6×. NamSys at FY2030E looks like a 34.3% operating margin business growing 6.2% (`FC` §1) — on margin-and-growth alone that argues for the 16–23× zone. It does not get there because of everything in §3.2, above all the concentration: none of Cerillion, ReposiTrak, Dotdigital or Enghouse has a third of revenue in three accounts.

### 4.2 Anchor B — take-private multiples (`DEAL`)

This anchor matters more than usual here, because management explicitly frames NamSys as an eventual acquisition target: "we think that from a shareholder value point of view, if we're the target of an acquisition, we're much more valuable as a focused company in this very narrow vertical... we think the exit value of NAMSYS and the premium for shareholders is worth remaining focused on this particular industry" (`AM26`).

| Transaction                                     | EV/EBITDA   | ⇒ × owners' earnings | Relevance                                                     |
|-------------------------------------------------|-------------|----------------------|---------------------------------------------------------------|
| Quorum Info Tech (TSXV: QIS) → Valsoft, Dec-25  | 7.2–8.7×    | 9.9–12.0×            | **The most relevant single datapoint available**              |
| CoreCard (CCRD) → Euronet, Oct-25               | 14.9–18.2×  | 20.4–25.1×           | US\$248M payments software                                    |
| Sapiens (SPNS) → Advent, Dec-25                 | ~25.6×      | ~35.2×               | US\$2.5B insurance VMS — mid-cap, not a comp                  |

**Quorum is the closest thing to a controlled experiment in the whole comp set**: a TSX Venture-listed, ~99%-recurring vertical-market software microcap (C\$40M revenue, auto-dealer systems) taken private by a vertical-software serial acquirer at ~1.5× revenue and ~7–9× adjusted EBITDA — i.e. **~10–12× owners' earnings** on NamSys's conversion factor. Two adjustments in opposite directions: Quorum was materially *lower* quality (48.7% gross margin, 6.4% operating margin against NamSys's 64%/40%), which makes 10–12× a floor for NamSys; but Quorum was five times NamSys's revenue, which cuts the other way.

The takeover premium paid was only +14% over the pre-announcement price, versus +64% for mid-cap Sapiens (`DEAL`). **So the private-market bid for an illiquid TSXV software microcap did not clear the public microcap multiple by much** — which is the honest rebuttal to any argument that the terminal multiple should be set at a strategic-buyer level well above public comps.

### 4.3 Anchor C — Gordon growth cross-check

Because ~100% of owners' earnings is distributable with no reinvestment requirement (`OE` §5), the multiple reduces to 1/(r − g) with no reinvestment wedge — an unusually clean application. The short risk-free anchor is **sourced**: NamSys's own cashable GICs yielded 2.00%–2.45% (`FSQ2` Note 15), midpoint 2.25%. **The equity risk premium and the size/illiquidity/concentration premium on top of that are analyst judgement, flagged as such**, and land a required return of roughly 11%–13% for a TSXV microcap with 37–39% customer concentration and unhedged FX.

| r ↓ / g → | 0.0% | 1.0% | 2.0% | 3.0% | 4.0% |
|-----------|------|------|------|------|------|
| 10.0%     | 10.0 | 11.1 | 12.5 | 14.3 | 16.7 |
| 11.0%     | 9.1  | 10.0 | 11.1 | 12.5 | 14.3 |
| 12.0%     | 8.3  | 9.1  | 10.0 | 11.1 | 12.5 |
| 13.0%     | 7.7  | 8.3  | 9.1  | 10.0 | 11.1 |

Read in reverse — what perpetual owners'-earnings growth each candidate multiple requires:

| Multiple | (r − g) | Implied g at r = 11.5% | Implied g at r = 12.5% |
|----------|---------|------------------------|------------------------|
| 9×       | 11.11%  | 0.39%                  | 1.39%                  |
| 10×      | 10.00%  | 1.50%                  | 2.50%                  |
| **12×**  | 8.33%   | **3.17%**              | **4.17%**              |
| 15×      | 6.67%   | 4.83%                  | 5.83%                  |
| 18×      | 5.56%   | 5.94%                  | 6.94%                  |

**This is the anchor that argues hardest for restraint, and I want to be explicit about the tension rather than hide it.** At 12× and an 11.5% required return, the implied perpetual growth is 3.2% — roughly inflation, with essentially no real growth. I judge that attainable: endpoint counts are stable (Knowledge Store ID 12), the international base is still tiny and growing (`FC` §4.5), and some contractual repricing ability now exists ("as we've renewed contracts, we've changed them to a more flexible model where we do have the ability to change pricing more frequently", `AM26`). But at a 12.5% required return, 12× requires 4.2% perpetual growth, which I would **not** defend given no price escalator and a saturated domestic tier. So Gordon supports 9–12×, not more, and 12× sits at its top edge. 15× and above needs ~5% perpetual growth and is not supportable by this route.

---

## 5. Reconciling the anchors and choosing 12×

| Anchor                                                | Implied × owners' earnings |
|-------------------------------------------------------|----------------------------|
| Mature low-growth microcap software (trading)          | 10.5–16.1× (mean 12.7×)    |
| Enghouse, the closest structural analogue (trading)    | 10.5×                      |
| Quorum, the closest TSXV take-private (transaction)    | 9.9–12.0×                  |
| Cash-ecosystem incumbents (trading)                    | 12.0–17.9×                 |
| High-margin microcap software (trading)                | 16.1–24.0×                 |
| Gordon growth, r = 11.5–12.5%, g = 1–3%                | 9.1–12.5×                  |

Three of the six anchors centre on 10–13×. The two that argue higher (high-margin microcap software; cash-ecosystem incumbents) are the two where the specific NamSys discounts bite hardest — the high-margin software names are all diversified across many customers, and Brink's and Loomis are capital-intensive businesses whose EV/EBIT is flattered relative to a software company's on an owners'-earnings basis.

**I select 12×, with a defensible range of 9× to 15×.** The reasoning, in order:

1. Start from Enghouse at 10.5× and Quorum at ~10–12× — the two closest analogues on listing venue, scale and maturity.
2. Add roughly two turns for quality that is *not* present in either. The margin comparison must be made on the FY2030E margin actually being capitalised, not on the higher FY2025A figure: **34.3% in FY2030E** (`FC` §1) against Enghouse's 18.6% (`PEER`) and Quorum's 6.4% (`DEAL`) — **1.85× and 5.37× respectively** (script §2). On FY2025A's 39.9% those ratios would be 2.14× and 6.23×, so using the terminal-year margin narrows the gap but does not close it. Alongside the margin: revenue is 99% recurring with near-zero account churn (`FS25` Note 7, `AM25`); ROIC is three-digit on negligible capital (`OE` §3.2); and NamSys is still growing 6.2% at FY2030E while Enghouse is shrinking 4.7% (`PEER`).
3. Do **not** add the further four to ten turns that the Cerillion/ReposiTrak/Intercede cluster would imply, because of concentration (37–39% in three accounts, `FS25`/`FSQ2` Note 7), the documented bank-merger displacement mechanism (`MDA25`), the saturated US client tier (`AM26`), absent pricing power (`AM26`), competitive attack on 40% of revenue (`AM25`), key-person dependence (`MDA25`), and TSXV illiquidity.
4. Sanity-check against Gordon: 12× requires ~3% perpetual growth at an 11.5% required return. That is the top of what I would defend, which is precisely why 12× is the base and 15× is the high case rather than the base.

**Honest statement of precision: I am confident the right multiple is in the 9×–15× band and that 10×–13× is the central zone. I would not defend 12× against 11× or 13× on the evidence available.** The spread from 9× to 15× is \$25.7M to \$42.9M on base-case earnings — a ±25% band around \$34.3M — and that band is real, not decorative.

---

## 6. Cross-checks on 12×

| Check on the base-case terminal value of \$34,311,840 | Value  | Comment                                                                                       |
|--------------------------------------------------------|--------|-----------------------------------------------------------------------------------------------|
| Implied EV / FY2030E revenue                           | 2.99×  | See the margin-matched comparison below                                                       |
| Implied EV / FY2030E EBIT                              | 8.72×  | Above Enghouse (7.6×), below Cerillion (11.7×) — the intended position                        |
| Implied EV / FY2030E EBITDA                            | 8.70×  | Essentially identical, since D&A is 0.19% of EBIT                                             |
| Implied owners'-earnings yield                          | 8.33%  | i.e. 1/12; a fully distributable 8.3% yield on a 99%-recurring revenue base                   |
| Implied multiple of FY2025A owners' earnings            | 15.25× | The FY2030 value is 15.3× *today's* earnings — the growth path does a third of the work        |

**Margin-matched EV/Sales check (`PEER`).** The implied 2.99× revenue at a 34.3% FY2030E operating margin sits sensibly inside the observed margin/EV-Sales relationship:

| Company                        | EV/Sales | EBIT margin |
|--------------------------------|----------|-------------|
| Descartes (TSX:DSG)            | 8.19×    | 32.0%       |
| ReposiTrak (TRAK)              | 5.27×    | 32.2%       |
| Cerillion (AIM:CER)            | 4.62×    | 39.5%       |
| **NamSys FY2030E at 12× OE**   | **2.99×**| **34.3%**   |
| Quorum take-private (`DEAL`)   | 1.50×    | 6.4%        |
| Enghouse (TSX:ENGH)            | 1.41×    | 18.6%       |
| Dotdigital (AIM:DOTD)          | 1.29×    | 16.0%       |

At 34.3% operating margin NamSys is priced at ~40% below Cerillion's revenue multiple and ~57% below ReposiTrak's, while sitting at roughly twice Enghouse's — which is the same relative position the EV/EBIT comparison produces. **The two cross-checks agree, which is the point of running both.**

**A consistency check against the forecast.** The multiple must not smuggle in growth the forecast already spent. `FC` §9 holds revenue per employee flat at \$418–441k through FY2030E and lets compensation rise to 43.3% of revenue, i.e. it credits no AI productivity gain; and `FC` §4.3 decays US ex-legacy growth to 7% on the market-structure ceiling. The 12× multiple assumes ~3% *perpetual* growth thereafter — **lower** than the 6.2% FY2030E revenue growth in the forecast, and lower than the 4.9% five-year owners'-earnings CAGR. So the multiple continues the forecast's deceleration rather than reversing it. Had I used the bull path's earnings with the bull path's 15× multiple, the implied perpetual growth would be ~4.8% at an 11.5% required return — which is internally consistent only *because* that scenario requires a second large international account to have landed (`FC` §8), i.e. a demonstrably repeatable international motion. That is exactly the conditionality the diagonal in §1 is meant to express.

---

## 7. What I am confident about, and what I am not

**High confidence:**

- The arithmetic. Terminal value = multiple × FY2030E owners' earnings, computed in `work_products/terminal_value_calcs.py`, with FY2030E owners' earnings taken unchanged from `FC` §1.
- The conversion factor between peer EV/EBIT multiples and owners'-earnings multiples (1.377×), and that EBITDA ≈ EBIT for NamSys to within 0.19% (`FS25` Note 4).
- That ~100% of owners' earnings is distributable, so a simple multiple needs no reinvestment adjustment (`OE` §3.2, §5).
- The quality facts: 99.0% recurring revenue (`FS25` Note 7), near-zero account churn (`AM25`), 39.9% FY2025 operating margin, three-digit ROIC (`OE` §3.2), no debt.
- The fragility facts: 37–39% of revenue in three customers in every disclosed period (`FS25`/`FSQ2` Note 7), a documented bank-merger displacement mechanism (`MDA25`), a saturated addressable US client tier (`AM26`), and management's own concession on pricing power (`AM26`).
- That **in the base-case quality regime** — the top-3 accounts all retained and the business still growing modestly — the correct band is roughly 9×–15×, and that both the Constellation/Descartes zone (31–35×) and the Mind C.T.I. zone (4×) are wrong for this business. That band is conditional, not universal: the §1 diagonal deliberately assigns 8× to the two bear scenarios, in which a top-3 account has been lost and the business is shrinking, because the multiple and the earnings path co-move.

**Genuine uncertainty:**

- **The point multiple.** 12× versus 10× or 14× is judgement, and it moves terminal value by roughly ±\$6M. Anyone who weights the Gordon anchor most heavily should use 10×; anyone who weights the margin-matched software comps most heavily should use 15×.
- **The required return.** The 2.25% short risk-free anchor is sourced (`FSQ2` Note 15); the ~9–10 points of premium on top of it are not sourced at all and are my judgement. A reader who prefers 10% lands at 12.5–14.3× for the same growth assumptions; one who prefers 13% lands at 9.1–10×.
- **Perpetual growth beyond FY2030.** The single most consequential input, and the least sourced. Nothing in the materials speaks to cash-endpoint counts beyond a three-year stability window (Knowledge Store ID 12). My long-run view that cash share of payments declines in developed economies is **from internal AI model knowledge, not from any source here**, and it is why I cap g at roughly inflation.
- **Whether the FY2030E earnings base is the right thing to capitalise at all.** It inherits every assumption in `FC`, including flat USD/CAD (±10% currency moves the base ±26%, `FC` §7) and the inference that Mexico is a single customer (`FC` §4.1). If the Mexican account is instead several customers, the concentration discount in §3.2 is overstated and the multiple should be a turn or two higher. If it is one customer and it leaves, both the earnings *and* the multiple fall together — which is what the §1 diagonal shows.
- **The peer data itself.** One day's snapshot from a third-party aggregator (`PEER`), not audited filings. Two names were cross-checked against a second source, and the deal multiples are computed from primary company/press URLs (`DEAL`), but the trading table has more measurement risk than any other input here. The M&A anchor is also thin: three transactions, only one of which is genuinely comparable, and survey-based medians for sub-\$50M-EV software deals were **not found**.

**A deliberate omission.** No illiquidity or minority discount is applied on top of the multiple. Doing so would double-count: the peer anchors that carry most weight (Enghouse, Quorum, Dotdigital, eGain) are themselves illiquid small-caps, so the discount is already embedded in the observed multiples. The Quorum evidence that a private buyer paid only a 14% premium for a TSXV software microcap (`DEAL`) supports treating those observed multiples as the right level rather than as something to be discounted further.

---

## 8. Source index

| Reference                                                 | Used for                                                                                     |
|-----------------------------------------------------------|----------------------------------------------------------------------------------------------|
| `work_products/forecast_earnings.md`                      | FY2030E owners' earnings for all four scenarios; revenue and EBIT; FX and sensitivity context |
| `work_products/owners_earnings_and_roic.md`               | Owners'-earnings definition; invested capital; ROIC; distributability; net cash               |
| `primary_sources/FY2025/NamSys_AFS_022426.md`             | Note 3 receivable concentration; Note 4 PP&E and depreciation; Note 7 revenue mix and top-3 customer shares; Note 13 termination commitment |
| `primary_sources/FY2025/NamSys_MDA_022426.md`             | Statutory tax rate; Risk Factors — key personnel, unhedged FX, bank-merger displacement, competition; TSXV listing |
| `primary_sources/2Q2026/FS_Q2_NamSys_Apr_30_26_FINAL.md`  | Note 7 H1 FY2026 top-3 customer shares; Note 15 GIC yields; Note 6 dividend and buybacks      |
| `fetched_docs/namsys_2025_annual_meeting_transcript.md`   | Zero churn; mission-critical; NRR 112%; competitive landscape by product; reseller failure    |
| `fetched_docs/namsys_2026_annual_meeting_transcript.md`   | 99% recurring; margin stability; big-three 75% / ~8% of US CIT vehicles; pricing power and AI; MCP moat; acquisition strategy; NamSys as acquisition target |
| Knowledge Store ID 12                                     | Federal Reserve 2026 Diary of Consumer Payment Choice — cash ~1 in 7 payments, stable         |
| `work_products/peer_multiples_scrape.py`                  | Peer trading multiples and margins, stockanalysis.com, September 17, 2026                     |
| `work_products/peer_deal_multiples.py`                    | Quorum/Valsoft, CoreCard/Euronet, Sapiens/Advent transaction multiples and premiums           |
| `work_products/terminal_value_calcs.py`                   | All calculations in this document                                                             |
