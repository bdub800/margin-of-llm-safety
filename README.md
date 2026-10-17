# Research Report: Can LLMs Actually Value Stocks?
Oct 14, 2026

Note: This report is entirely written by hand without AI assistance.

Disclaimer: For informational purposes only, not investment advice. The author may at any time acquire or dispose of positions in any security discussed without notice.

---

>"But solving problems is only a tool and proxy for achieving the primary goal of conceptual understanding and insight."
>
> -- [A Severe Misalignment of AI in Mathematics](https://mathandai.org/)

## Why is this Interesting?

Large Language Models (LLMs) are billed as a more general form of AI than previous technologies. People have speculated that it will take over a large portion of the economy and lead to mass unemployment. We have seen it become very good, perhaps even *superhuman*, in software engineering and math. This begs the question: are LLMs good at every kind of cognitive task? 

Fundamental valuation of stocks as a use case have some interesting properties:
- The answer anyone gives is not immediately or easily verifiable as it depends on future financial performance of the underlying business (in contrast with mathematics or software engineering which have more high signal ways of verification).
- It needs to have a causal understanding of (at least a part of) the world. Accurately predicting future earnings of a business involves understanding the drivers of the business (e.g. what will cause revenue to grow or shrink).
- It involves understanding people as management decisions affect company value.
- The future is inherently uncertain so the analyst may need to imagine multiple possible trajectories of the world.
- Compared to generic forecasting of world events, valuation of stocks is an economically fruitful task with many professionals in the field.
- Because of the regulatory requirement for publicly listed companies to disclose all material information to the public, it is feasible to test on real companies. Consequently the test cases in this study are fully realistic and not synthetic examples that are meant to approximate real world tasks.

## Main Takeaways

1. In this study, the LLM-based system did a reasonable job on valuing simple businesses while struggling to value a complicated business. The complexity came from the business being a serial acquirer (evaluation case 3).

2. LLMs are able to output accurate causal factors of the financial performance of the business. Though since these are discussed in detail in company filings and earnings calls, the requirement for LLMs to have good causal models of the business domain may simply be reduced to writing high quality summaries.

3. They tend to bias towards focusing on what is available rather than what is important. The task of valuation is composed of subtasks. Certain subtasks are more important than others. However, LLMs in this study tended to focus on subtasks that are easier to answer with the existing data rather than seeking new information to answer the more important but harder to answer questions. **Humans need to ask the right questions here.**

4. However, if the information is already there, or just one or two internet queries away, LLMs can be quite persistent and detail oriented. Consequently, **they have the potential to uncover insights not widely appreciated by humans in some situations**. In the case of NamSys (evaluation case 1) it was for things that can be numerically reverse engineered.

5. Human understanding is still the bottleneck. Especially for complex tasks with no immediate way to verify correctness of end result (i.e. If it tells you XYZ company is worth $13/share, is that right or wrong?), the ability to evaluate the **process** through which it came up with an answer becomes critical. To make process evaluation easier, the system ideally is designed to be **legible**; defined as giving succinct and easy to understand (to humans) answers but with an underlying structure to optionally trace the work process and judge its validity. For this study, I use the following techniques to increase legibility (1) causal modeling before forecasting; (2) prover-verifier-(human) judge structure to make it easier to fix minor issues and focus human attention on higher level questions; and (3) the Excel spreadsheet output format which is more intuitive for humans to inspect and work off of.

## Methodology - How the LLM was Used to Value Stocks

The valuation task is broken down into several steps, each step has a prompt and associated input output files. An LLM inside an agent harness outfitted with web search, web page retrieval, and code execution tools is used to complete each of these steps in sequence.

Here are the steps in code at a high level:
```python
Step(
    id="primary_sources",
    title="Primary Sources",
    model=SONNET5,
    prompt=lambda ctx: get_primary_srcs_msg(ctx.company),
    produces=("primary_sources/","pv/primary_sources/scripts/"),
),
Step(
    id="overview",
    title="Overview",
    model=SONNET5,
    prompt=lambda ctx: overview_msg(ctx.company),
    reads=("primary_sources/",),
    produces=("work_products/overview.md",),
),
Step(
    id="owners_earnings",
    title="Owners' Earnings",
    model=OPUS55,
    prompt=lambda ctx: owners_earnings_msg(),
    reads=("primary_sources/",),
    produces=("work_products/owners_earnings_and_roic.md", ),
    requires_verifier=True,
    requires_human=True,
    budget_usd=10.0,
),
Step(
    id="causal_model",
    title="Causal Model",
    model=OPUS55,
    prompt=lambda ctx: "Give me the causal model of the business.",
    reads=("primary_sources/", "work_products/"),
    produces=("work_products/causal_model.md",),
    requires_verifier=True,
    requires_human=True,
    budget_usd=7.0,
    effort="medium"
),
Step(
    id="forecast_earnings",
    title="Forecast Earnings",
    model=OPUS55,
    prompt=lambda ctx: forecast_earnings_msg(years=5),
    reads=("primary_sources/", "work_products/"),
    produces=("work_products/forecast_earnings.md",),
    requires_verifier=True,
    requires_human=True,
    budget_usd=15.0,
    effort="high"
),
Step(
    id="terminal_value",
    title="Terminal Value",
    model=OPUS55,
    prompt=lambda ctx: terminal_value_msg(),
    reads=("primary_sources/", "work_products/forecast_earnings.md"),
    produces=("work_products/terminal_value.md",),
    requires_verifier=True,
    requires_human=True,
    budget_usd=15.0,
    effort="high"
),
Step(
    id="sotp",
    title="Sum of the Parts",
    model=OPUS55,
    prompt=lambda ctx: sum_parts_msg(discount_rate="10%"),
    reads=("primary_sources/", "work_products/"),
    produces=("work_products/valuation.md",),
    requires_verifier=True,
    requires_human=True,
    budget_usd=10.0,
    effort="high"
),
Step(
    id="excel_model",
    title="Transform to Excel Sheet",
    model=OPUS55,
    prompt=lambda ctx: excel_model_msg(),
    reads=("work_products/",),
    produces=("work_products/valuation.xlsx",),
    requires_verifier=True,
    requires_human=True,
    budget_usd=15.0,
    effort="high"
)
```

### Step 1. Primary Sources

Given the company name and ticker, retrieves from the internet latest quarterly report and last three years worth of annual reports. Also retrieves the latest three quarterly earnings call transcripts. It saves these materials in a folder called `primary_sources` under the project directory for later use.

### Step 2. Overview

This step is mainly to make it easy for a human analyst to get up to speed with the company. It makes internet searches for recent news about the company. Using that and the primary sources, summarizes the business of the company, recent developments, and key issues.

### Step 3. Owners' Earnings

This is an interrogation of historical financial statements to adjust reported earnings into owners' earnings; defined as the amount of earnings leftover after satisfying all obligations (except interest on debt, i.e. it is an enterprise-level measure in this study) and can be distributed to shareholders or re-invested into the business or used to pay down debt. We will later use this as a base to forecast future earnings of the company and the dividends it can theoretically pay out each year to shareholders. The sum of the dividends the company can pay out over its entire lifetime is added up to form the valuation of the company's equity. This is known as the Discounted Cash Flow framework (DCF).

### Step 3 Technical Note: Prover-Verifier-HumanJudge to Guide Human Attention

Step 3 is the first step in the process that uses the prover-verifier-(human) judge structure.

The structure involves a LLM that does the work (prover) and a LLM that checks the work (verifier). Moreover, a human can see the discussion between the two and either decide the final outcome or ask questions to the prover, verifier or both. When faced with AI generated output that is difficult to verify, humans often either over or under-rely on the generated output. This structure aims for a middle path that guides human attention. It allows a human to listen to two sides of a discussion and zero in on important points of contention. Another benefit is the verifier can check details such as are the numbers transcribed accurately or whether the code written by the prover does the calculations as claimed. This frees up human attention to more high level things (e.g. methodology).

Note on the choice of verifier model: Ideally one wants to choose a verifier model that is equally intelligent to maximize the chances of finding errors. However, due to budget constraints I chose the verifier as one class weaker than the prover (Sonnet vs Opus).

- Reference: [Prover-Verifier Games improve legibility of LLM outputs](https://arxiv.org/pdf/2407.13692)

### Step 4. Causal Model

This step distills the primary sources into drivers for each of the income statement line items such as revenue, gross margin, operating margin, etc. They are then used as a decomposition framework to forecast future earnings. For instance for a cable tv business, revenue can be decomposed into number of subscribers and average price per subscriber; this decomposition is what management actually uses to run the business.

### Step 4 Technical Note: Why is the Causal Model Useful?

Having the causal model speeds up human understanding of the business since it is what analysts intuitively try to construct by reading the financial reports and listening to earnings calls. It also gives them a framework to organize observations (such as news items). LLMs benefit too by having this conceptual model since it can decompose its forecasting and valuation work into more granular factors (that is intuitive to humans).

One may think this does not have to be an explicit step you tell the LLM to do because it will do it automatically when forecasting. This is not reliably true. They may not necessarily reason from first principles or pay attention to causal mechanisms. Previous attempts by the author show they may just forecast overall revenue growth rates, margins, etc. This makes it difficult to (a) tell whether the forecasting assumptions are reasonable; and (b) play around with the assumptions to see how various scenarios will play out.

### Step 5. Forecast Earnings

Using the drivers for financial performance developed in the causal model, and the historical owners' earnings, the LLM forecasts owners' earnings for the next X years (in this study 5 years). For companies with significant growth capital expenditures (capex), this step will also forecast the amount of distributable earnings after growth investments. The LLM can access the internet to do further research before making the forecast. The forecast usually is a range, split into bear/base/bull scenarios.

### Step 6. Terminal Value

Estimates the value of the company (enterprise value) at the end of the forecasted time period. This is implemented as a multiple assigned to the owners' earnings in the last year of the forecast. Again, the LLM can access the internet and all of its previous work to do research. It is mandated in the prompt that it will at minimum need to look up trading multiples of its peers to benchmark what is a reasonable range of multiples to assign (split into the same scenarios as the earnings forecast).

### Step 7. Sum of the Parts

Putting all the previous work together, it sums the distributable earnings from step 5 and the terminal value from step 6. Both discounted back to present value using a user specified discount rate. This step further adds to the sum any non-operating assets and subtracts any non-operating liabilities (such as debt) to arrive at the intrinsic value of the company's equity. Lastly, it divides the intrinsic value by the number of shares outstanding to arrive at value per share. This is the valuation. 

Note on price blindness: Throughout the valuation exercise, the LLM is not given the current trading price of the company's stock and told not to look it up so as to not bias its analysis. There was a small leakage in the Adobe case (evaluation section). It got price information via an internet search for the previous “overview” step since it was using an older prompt. Nonetheless, price was not used for this valuation step.

### Step 8. Transform into Excel spreadsheet

For all the previous work, the LLM writes up its findings in a Markdown file and does its calculations in Python scripts. To make the work more legible to humans, this step transforms all of the valuation calculations into a traditional financial model in Excel. This includes (1) the historical owners' earnings showing all adjustments made; (2) projected owners' earnings; (3) the estimated terminal value; and (4) the sum of the parts at the end.

## Evaluation Criteria

What constitutes "good" valuation:
- Basics: writing is clear, math is correct, good citations
- Notices important aspects of the business
- Accounting adjustments appropriate for owners' earnings
- Quality of forecasting
- DCF mechanics and valuation assumptions reasonable
- For convenience: how close is the number to professional analysts' consensus

## Empirical Results

**NOTE: The actual output files from the system (and evaluated in this section) can be inspected under the `examples` folder [here](https://github.com/bdub800/margin-of-llm-safety).**

### Case 1: NamSys Inc. (CTZ.V)

Why interesting as a test case:

- Simple business, simple capital structure, and simple financial statements. It's a Canadian microcap.
- Does not have a lot of information available other than SEDAR filings, no earnings calls, no analyst coverage. Since the company's presence is so small, almost certainly not well represented in the LLM's training data so it can't memorize answers.
- Clean case for a real world company. Can see whether the LLM can do the fundamentals: understanding accounting, focus on key uncertainties, identify business drivers, and the mechanics of a DCF.

Evaluation result:

- For convenience: how close is the number to professional analysts' consensus
    * No price targets since no analyst coverage
    * At the time of writing, the trading price of CTZ.V is $1.13 CAD
    * Estimated value per share (CAD) at 10% discount rate is $0.78 to $2.47, with the base case at $1.46

- Basics: writing is clear, math is correct, good citations
    * Clearly lays out methodology and reasoning
    * Did a bunch of spot checks on math, all good
    * Citations are good
    * 5/5

- Identifies important aspects of the business: 
    * Correctly found the annual investor meeting transcripts even though was not instructed explicitly to do so, and noticed that it is the closest thing to earnings transcripts (the company does not have earnings calls)
    * Correctly identified the shareholder base change with the large block held by estate of former chairman distributed/sold
    * Correctly listed key issue of AI disruption for a SaaS business
    * Conclusion drawn from the ROIC calculation is insightful: "incremental growth has required negligible incremental capital"
    * Correctly identifies the large pile of cash on balance sheet that has failed to be deployed and earns low returns
    * The business drivers considered are indeed causal rather than mere association. Good.
    * Good breakdown of components of revenue and operating expenses
    * Correctly calls out the US revenue deceleration, and after help from the verifier model, concedes that the "cause is ambiguous between broad-base US saturation and a single large account contracting", but good investigation of the possible mechanisms behind the deceleration
    * The compensation cost driver is correct, but the explanation is more complicated than necessary
    * Correctly identifies the operating leverage, and importantly the operating de-leverage from losing a top customer given the level of customer concentration. Though there was a small error (e.g. claiming 100% of lost customer revenue would cut to the bottom line). Corrected with human feedback.
    * Noticed the transition of growth from US to international
    * Overall got the big themes right but minor issues, 4.5/5

- Accounting adjustments appropriate for owners' earnings
    * Correctly excluded the interest income from the large pile of cash on the balance sheet, though the prompt for calculating owners' earnings did say to exclude interest income. So LLM correctly followed instruction rather than autonomously made the correct judgement.
    * The bad debt adjustment normalization is reasonable, and the math is correct, but initially said it reduces FY2025 earnings which is wrong directionally. This is a minor mistake that had to be fixed with human feedback.
    * Correctly accounts for share based compensation as economic expense (it's in the instruction given), and normalizes by averaging over multiple years given the lumpiness of the timing of grant. Reasonable but not ideal. Would have been better to account for this expense as the amount of cash required to buy back an equal number of stock to avoid dilution of existing shareholders. This methodology was not in the prompt and the LLM did not independently come up with it either.
    * Uses the correct income tax rate disclosed in the MD&A and accounts for deviations from the standard rate as disclosed in the notes to financial statements. Good.
    * Adds back depreciation and subtracts actual capex for PP&E. Good.
    * Cross checks the calculated owners' earnings with an operating FCF method and the two agree. Signifies that the owners' earnings are indeed convertible into distributable cash. Good.
    * Overall good with minor issues, 4/5

- Quality of forecasting
    * Correctly strips out currency effects to focus on USD growth since almost all revenue in USD and discover that the recent deceleration in growth is mostly due to forex fluctuations
    * Deduced that revenue from Mexico is actually one large customer and it's growing fast
    * Deduced that the largest customer each year (excluding Mexico) from FY2023 onwards must be US based and it's shrinking, and that excluding this large customer each year, US region sales has actually been growing in double digits. (This does not necessarily mean this large US customer each year is the same entity.)
    * The above three points are **genuine insights** from inspecting financial disclosures and not repeating analysis written down elsewhere. Impressive. Note that the discoveries here are more quantitative in nature, and LLMs probably were trained on analogous math problems.
    * Good analysis on the drivers behind rest-of-US growth from US market structure, Federal Reserve's research on consumer cash use, and pricing power revealed by management.
    * Decomposes the revenue forecast into a shrinking US large customer and growing rest-of-US, growing Mexico, accelerating rest of International, and Canada. Methodology is reasonable but still extrapolating from historical trends.
        - Exception: for the rest of International, it forecasts an acceleration based on recent sales efforts. Given the small base, not that material to valuation.
    * Did not get trapped trying to forecast FX moves: "For FX, since I have no real edge on USD/CAD, I'll just hold the rate at the most recent observable level rather than guessing at movement." Good.
    * Spent a lot of tokens thinking about the math behind compensation expense (biggest category of cost). Perhaps this is because it has something to test against, the historical growth in headcount, revenue per head, cost per head, margins. Forecasts number of employees and cash cost per employee separately. Seems complicated and the simpler method could be to assume management would like to keep the margin stable (as they have said). Either way inherently uncertain so I don't think you can be too precise about it.
    * Spent many tokens checking whether the forecasted operating income CAGR makes sense and in the process discovered that the historical growth had a large part due to weakening of the CAD relative to USD. Good sanity check.
    * Correctly calls out customer retention and foreign exchange (earns revenue in USD, cost mostly CAD, does not hedge) as the largest swing factors on forecasted earnings
    * Did not really have any analysis on AI's impact on the business other than a reference to management mentioning it being a headwind to pricing power
    * Notably did NOT research the top 3 CIT companies in the US market - Brinks, Loomis and Garda. It was not prompted specifically to research competitors but seems reasonable given the market is dominated by these big 3.
    * Scenarios are reasonable given the prior work on forecasting drivers
    * Bull case considers comment by management that "the total addressable market worldwide is at least 10 times what it is in the US." and models in a new big customer. Good.
    * The base case assumes the FY2023–FY2025 operating leverage reverses and does not return. Operating margin at the end of the forecast is about 5 percentage points lower than 2025. This seems rather harsh.
    * The bear case does not capture the true downside of AI dis-intermediating the business. Generally speaking given the large customer concentration and how small they are relatively to the market, the modeled scenarios are too narrow in range.
    * Would be great to have more commentary on potential for the company to be acquired since that's goal of management; though in calculating terminal value it did indeed look up acquisition multiples on small software companies
    * Did not consider the company utilizing the large pile of cash to make an acquisition, instead just assumed it would be returned. However, given the lack of deal information or a track record, it is hard to say anything concrete.
     * 3.5/5

- DCF mechanics and valuation assumptions reasonable
    * In determining the terminal multiple takes into account business quality as well as a reasonable set of peers such as small vertical software vendors or those in the cash logistics industry (Loomis, Brink's)
    * Initially 4 of the chosen peers' multiples did not have a source backing but was remedied after the verifier model's review
    * Cross checks terminal value with a simple perpetual growth model. Good.
    * Discount rate is 10% which is specified by the user
    * Did not use the most recent disclosed share count in the "Outstanding Securities Data" section of the MD&A, instead used the weighted diluted shares number in the most recent quarter. The difference is immaterial in this case. However, the LLM probably did not look for it since US filings do not have this convention.
    * The non-compensation selling expense forecasted numbers were somewhat arbitrary, impact is small. Human feedback fixed it to be a growth rate on top of a starting number.
    * Overall the valuation mechanics are correct, 4/5


### Case 2: Adobe Inc. (ADBE)

Why interesting as a test case:

- More well known company compared to first case; a US large cap
- Business model is subscription based software, so relatively simple, however there are multiple lines of businesses with different products
- Difficulty is in knowing how AI will impact this business

Evaluation result:

- For convenience: how close is the number to professional analysts' consensus
    * Yahoo Finance ADBE => Analysts' targets (USD) low $195.00; average $275.06; high $373.00; 
    * AI estimated value per diluted share (USD) @ 10% discount rate => severe $120.54; bear $213.76; base $350.47; bull $576.53

- Basics: writing is clear, math is correct, good citations
    * Clearly shows methodology
    * Reasoning is legible
    * Spot checks on arithmetic - all good
    * Comprehensive citations
    * 5/5

- Identifies important aspects of the business
    * Called out ROIC is very high and the operating business consumes no capital
    * Concluded that growth is therefore not constrained by capital
    * Identified the uncertainty in management's growth strategy of trading ARR for freemium users
    * Identified disintermediation risk from AI
    * Did a good job of distilling the filings and calls to core drivers of the business, including the fast growing AI hosting cost
    * 5/5

- Accounting adjustments appropriate for owners' earnings
    * Two methods for calculating owners' earnings, first is from normalizing operating income; second method from cash from operations, used as cross check. Two methods agree. Good.
    * Share based compensation is deducted from earnings, good but not great. Would have been better to account for this expense as the amount of cash required to buy back an equal number of stock to avoid dilution of existing shareholders. This methodology was not in the prompt and the LLM did not independently come up with it either.
    * The only material non-recurring expense added back is the Figma acquisition termination fee of $1B, which is reasonable as truly one-time since there is a limited number of other companies that can result in an acquisition break-up of this scale
    * Maintenance capex correctly called out as not too material, the estimate is reasonable and also small in scale (so it doesn't matter either way)
    * The assumed tax rate is reasonable, and based on management disclosed guidance. However, its explanation of the difference between the GAAP rate and the cash rate as "forced capitalisation of domestic R&D, which shows up as a $2,065M 'capitalized expenses' deferred tax asset at FY2025 year-end (10-K Note 10)" is questionable. The contents of Note 10 to the financial statements do not call out the $2,065M number as specifically capitalisation of R&D. Possibly a hallucination. 
    * Good reasoning on the difference between FCF and owners' earnings. The main differences are stock based comp and deferred revenue. Both of which have good economic reasons to not count as earnings. 
    * Good adjustments for calculating total invested capital for the ROIC calculation. The main source of uncertainty is whether to include the off balance sheet purchase obligation. The LLMs chose to show both with and without. ROIC is high enough in either case to not matter.
    * Overall good with minor issues, 4/5

- Quality of forecasting
    * Models different business lines separately. Good.
    * For the Business Professionals & Consumers line, forecasted MAU and avg revenue per MAU are reasonable, though it is still an extrapolation of past trends. There was a nice cross check on the total number of people that could be using Acrobat/Express.
    * The forecast for Creative Cloud apps revenue decomposed into unit growth and pricing/mix. LLM actually modeled the trade off between volume and price (management strategy) in the forecast which is good. Actually lists good reasons for volume change (number of professionals not growing/competitor substitution/AI substitution)
    * Digital Experience, Semrush lines were forecasted as extrapolation of past trends, not particularly insightful but reasonable
    * Good analysis on gross margin, from dissecting the current numbers to listing out the variables that affect the future
    * Flagged R&D expense ratio uncertainty b/c of AI training compute though the forecasted numbers do not incorporate drastic change
    * Depreciation and capex were modeled as constant growth rate off of a starting year, rather than as percentage of revenue. Seems reasonable in this case since the business is not capital intensive.
    * Overall, I think the **key weakness** is the LLM did not realize to ask certain important questions and try to get an answer to it rather than just going through the motions of forecasting each financial line item
        - AI disintermediation risk, how real is it, or how can it play out
        - Competitive threat from cheaper newer alternatives like Canva
    * 3/5
    
- DCF mechanics and valuation assumptions reasonable
    * Good qualitative analysis of advantages and risks supported by quotes from filings
    * Noted missing key data points retention rate, churn rate, and free-to-paid conversion rate. Good.
    * Reasonable set of peers to benchmark multiple
    * Reasonable choice of terminal multiples that takes into account qualitative factors, peer multiples, and a perpetual growth formula
    * Used the balance sheet end date shares outstanding count of 399M instead of the more recent 397.5M shares on the cover page of the 10-Q as of June 11, 2026 => small difference but suboptimal
    * One column name description that was not accurate
    * Lists as material judgement call of whether to treat operating lease liabilities and off-balance-sheet hosting commitments as debt-like to be subtracted from enterprise value. This is the main point surfaced during the prover-verifier-human review process. The LLM points out that operating expenses associated with these are "fully embedded in EBIT every year, and are never excluded from owners' earnings the way debt interest is". So perhaps the reasonable thing is to not deduct them again as debt. However, the hosting commitments may not be fully utilized but the company still has to pay all of it. To be conservative both are deducted. Not deducting them results in an additional $17/share on the base case.
    * Overall, the calculations of the DCF as it appears in the output Excel spreadsheet is correct.
    * 4.5/5


### Case 3: Boyd Group Services Inc. (BGSI / BYD.TO)

Why interesting as a test case:

- Compared to previous cases, materially more complicated business as it starts new and acquires existing car repair shops to consolidate a fragmented industry, just did the largest acquisition ever in company history
- Significant debt and growth capex
- The collision repair industry also has moving parts like miles driven, weather trends, and collision-advoidance technology
- Lease and purchase accounting complexity is a test for the LLM to understand underlying economics
- Midcap Canadian company with some analysts following, unlikely to be prominently featured in LLMs' training data

Evaluation result:

- For convenience: how close is the number to professional analysts' consensus:
    * Yahoo Finance BGSI => Analysts' targets (USD) low $120.00; average $148.46; high $181.82;
    * Intrinsic value per diluted share estimate (USD) by LLM @ 10% discount rate => bear $27.71; base $93.35; no growth capex (all earnings paid out) $92.42; bull $153.28;

- Basics: writing is clear, math is correct, good citations
    * Initially had some labels "**[R]** = historical reported data; **[G]** = management guidance or opinion; **[I]** = my inference*" that is hard to follow, had to prompt to fix
    * Citations are good
    * Did a number of spot checks and found no arithmetic errors
    * Good overall, 4.5/5

- Identifies important aspects of the business
    * Noticed change in capital allocation strategy of management that now includes buybacks
    * Identified leverage is high relative to historical levels
    * Good breakdown of revenue drivers: claim volume, total cost of repair, share gain, new locations 
    * Identified that return on capital is mediocre if the capital base includes goodwill and intangibles, so basically prices paid for acquisitions were not great
    * Identified cost of repair being the main swing factor
    * Called out end customer (insurers) concentration
    * Overall good job distilling the key things talked about in filings and calls, 5/5

- Accounting adjustments appropriate for owners' earnings
    * Correctly noticed "leases represent a genuine recurring operating cost of running a leased-shop business" and treats "full cash rent (principal plus interest) as an operating expense" even though the accounting capitalizes leases and labels the rent as depreciation (with the actual cash outlay in financing cashflows). This is done without any lease specific instructions in prompt. Good.
    * Includes "Software purchases and licensing" in maintenance capex, which is reasonable and conservative.
    * Excludes "Proceeds on sale / leaseback agreements" from maintenance capex, again reasonable. Though the reasoning it gave is somewhat fumbled: "One-off cash in, permanent rent out. Netting these would double-count the benefit because the resulting rent is already charged above." The sale/leaseback is for recycling capital deployed to new locations; and we are not considering growth capital here.
    * Correctly noticed that the acquisition transaction costs are in reality a recurring expense. Accounted for it using a normalized number.
    * The taxes used for calculating owners' earnings is too high compared to cash taxes paid. There are additional depreciation and amortization that reduce tax. However, the LLM acknowledged it as a conservative simplification. This is material though.
    * Distinguished between return on total capital (<10%) vs return on tangible capital (>20%). Good.
    * Overall, 3.5/5

- Quality of forecasting
    * Included a no new locations scenario to isolate value of existing network of shops. Good.
    * Revenue drivers (claims volume, cost of repair, and share gains) are all reasonable, it is however an extrapolation based on existing filings and management commentary
    * Modeling of Project 360 and Joe Hudson (JH) savings, operating leverage margin expansion, and capex and tax are all reasonable given prior work; though EBITDA margin could be slightly more conservative
    * Major Weakness: had a lot of trouble analyzing the economics on new locations (acquired or start-up) which is the main growth mechanism of this company
        - Did not include glass business locations in calculating the total number of locations acquired, and therefore the revenue and price paid per acquired location is incorrect
        - Used the wrong (and more complicated) method to calculate revenue per new start-up location at maturity. I had to prompt it to fix.
        - Concluded that new locations earn about 5% to 7% on capital which seems very low, and value destructive if true. The actual return from growth capital is not clear but management had indicated on the Q2FY25 call they are targeting ROIC north of 20%. 
    * The LLM is not good at picking a structure for modeling the business financially
        - Originally used the same corporate EBITDA margin for the existing business and new locations. One would expect incremental margin on new locations to be higher. To be fair, the filings are not clear on new location economics.
        - Used convoluted method to calculate revenue per new location
        - Used convoluted method to forecast rent with arbitrary assumptions on sale lease back activity
        - The above had to be fixed by manually specifying the modeling methodology
    * Given the complexity of this business, the python script for financial modelling is now too messy and hard to understand. Needed to prompt LLM explicitly to clean it up so I can actually follow what it did. **Legibility is not the default for LLMs, especially for long outputs and complex tasks.**
    * The reasoning for forecasted number of new locations were a little muddied at first as well, though upon prompting the reasoning seems sound
    * Overall, had to do a lot of manual guiding, 2/5

- DCF mechanics and valuation assumptions reasonable
    * Used a set of loosely adjacent public auto-aftermarket businesses as peers for benchmarking multiples since the actual collision repair peers are private => not that informative, prompted to look at actual peers, this is material
    * Peer multiples are reported as EV/EBITDA, yet LLM chose to convert to an EV/Owners' Earnings multiple by further adjusting by the OE/EBITDA ratio in the last forecasted year. This mathematically works out but now incorporates assumptions for maintenance capex and tax in the projected earnings which is unnecessary complexity. Slight negative.
    * Used a growth in perpetuity formula for an alternative to calculating terminal value, which is reasonable theoretically but the the assumed re-investment rate seems arbitrary
    * Correctly points out the difference in IFRS and US GAAP treatment of operating lease expenses and accounts for that in the terminal multiple applied. Good.
    * Except for Joe Hudson's Collision Center, there is limited information on private market transaction multiples returned by the internet search. This reduces the quality of the terminal multiple analysis but is not a weakness of the LLM itself but what information it has access to.
    * Analysis incorporated the qualitative aspects of Boyd into the range of peer multiples collected by internet search. Good.
    * Initially missed the no growth capex scenario terminal value, had to be prompted to fix. Small negative, inconvenient.
    * Added on terminal value of EBITDA from new locations that has not ramped up fully at the last forecasted year. Initially the math was unnecessarily complicated, prompted to use a simpler method (multiple x run-rate EBITDA). The numbers did not change materially.
    * The initial method for calculating tax shields from goodwill and intangibles had too many assumptions built in, prompted to use a simpler method. The value did not change drastically.
    * Unclear how reliable is the tax shield value of goodwill and intangibles. The company clearly pays below standard rate cash tax, yet the forecasted earnings all use standard rate, with the tax shield added on to equity value as a separate component. Alternative is to simply assume a lower cash tax rate. Judgement call.
    * The actual formulas for discounting future cash flows and adding up assets and liabilities are good
    * Chose to only add roughly half year's worth of earnings from 2026E because already using Q2FY26 balance sheet numbers, a little complicated but justified
    * Had various built in cross checks which are good
    * Overall, the mechanics of valuation were good, however the assumptions and methodologies needed to be re-worked, 2.5/5


## Discussion

| Criteria                                                                     | NamSys Inc. | Adobe Inc. | Boyd Group Services Inc. |
|------------------------------------------------------------------------------|-------------|------------|--------------------------|
| Basics: writing is clear, math is correct, good citations                    | 5/5         | 5/5        | 4.5/5                    |
| Notices important aspects of the business                                    | 4.5/5       | 5/5        | 5/5                      |
| Accounting adjustments appropriate for owners' earnings                      | 4/5         | 4/5        | 3.5/5                    |
| Quality of forecasting                                                       | 3.5/5       | 3/5        | 2/5                      |
| DCF mechanics and valuation assumptions reasonable                           | 4/5         | 4.5/5      | 2.5/5                    |
| For convenience: how close is the number to professional analysts' consensus | n/a         | close-ish  | not close                |

First, let's look at how the LLM did criteria by criteria.

- The first criteria, the basics, is about following particular writing styles, avoiding hallucination, and doing arithmetic correctly. These were well known problems maybe several years ago but have since been patched up pretty well. 
- The second criteria is about noticing the big issues and drivers of the business. Government filings and earnings calls do a good job of disclosing this kind of information in detail. The source materials are all given (retrieved in step 1 by design), so really the test here is to summarize and re-organize large volumes of information into an easy-to-digest form. The LLM did well here.
- The third criteria is similar to the second. All the information to calculate owners' earnings is already there in the financial statements and earnings calls. The test is really transforming all that text into a different form. The wrinkle on top is there is judgement required in what adjustments to include and exclude. And that requires understanding of financial concepts such as depreciation, maintenance capex, share based compensation, leases, etc. The LLM does well here with only minor issues. In the case of Boyd, the LLM did use a cash tax rate too high, however, it pointed that out as a simplification and accounted for it elsewhere in the valuation exercise.
- The fourth criteria on forecasting is where the LLM really struggled. Compared to the previous ones, this is not about a transformation of existing given text. The government filings, earnings calls, and a simple internet query will not give all the information one needs to forecast earnings. One would need to know to **ask the right questions**. This means knowing what is important and spending the majority of the thinking effort there. (For instance, go beyond primary sources and look at competitors, customers, or suppliers. While you can prompt for these, the right questions to ask differs case by case.) Instead the LLM focused on what is available, i.e. historical trends, business drivers disclosed in filings, and management guidance, and used those to make its estimates. This is not wrong, and is necessary for forecasting. **But since everyone else in the stock market also has done those analyses, the forecast produced by the LLM will not be particularly insightful.**
    * The one exception here is with NamSys. The LLM made insightful inferences such as foreign exchange played a key role in historical operating income growth or that Mexico region is one large customer. The disclosure by NamSys was not thorough compared to more established public companies, and the LLM uncovered things that were not said. This perhaps points to an advantage of LLMs - as long as the information is there, they can be more persistent and notice details overlooked by humans.
- The LLM overall did pretty well on the fifth criteria. The DCF valuation methodology is well known, and its application is akin to a complicated math word problem. The difficulty is in choosing the right set of peers and what terminal multiples to assign. (Discount rate in this study specified by the author.) And on this it sometimes struggled. Especially on Boyd, the LLM did not at first choose a comparable set of peers. Again, with a bias towards what is available vs. what is correct (Boyd's peers were private companies so not a lot of valuation info). There is also judgement in how one structures the valuation process such that it does not add unnecessary complexity. The LLM sometimes struggled with this. The previous observations can be summed up as the LLM is **relatively weak in knowing what is important**.
- The sixth criteria compares the LLM's estimate of value per share (the output of the DCF process) to professional analysts' price targets. This is quite noisy because human analyst price targets are generally shorter term focused and they don't necessarily agree with each other. However, if the LLM estimated number is completely off from the human price targets, then perhaps it's a clue for further investigation. In the case of Boyd specifically, because of the high debt load, equity value was more sensitive to valuation assumptions. This makes it easier to diverge materially from other people's estimates.

Second, let's compare the results from the perspective of the three companies analyzed.

- NamSys is a simple business. This test case was to see if the LLM can do the fundamentals, such as understanding accounting concepts to make adjustments, pick up on key business drivers from filings, and do a DCF. The answer is it indeed can. Where it fell short is that it didn't spend much effort on the AI risk at all and just repeated one line from management. It also did not spend much time on looking into competitors which were named and had public information. This points to the LLM's lack of ability to autonomously go beyond what was given and think of what secondary information would be important to know. (Though not many humans would do that either.) A counter point is that it did look into the Federal Reserve's research on cash use (mentioned by management) which is important for the industry it's in.
- Adobe is also a simple business. It however did have multiple segments and different drivers for each. The LLM did break it down by segment and separately analyzed each. Again the weakness in its analysis is it didn't go beyond the primary sources to dig more on AI risk and competitors. One can argue this just needs to be put into the prompt. However, which secondary information is important is situation dependent. Sometimes it's competitors, sometimes it's suppliers, sometimes it's new technology. The LLM in this study was given the tool to search and retrieve anything on the internet. There is an infinite amount of things it could have searched for, and knowing which one to focus on is perhaps the weakest link.
- Boyd is the hardest case. Its accounting was complex, it's a serial acquirer, and it just did a large acquisition. The test was to see how well the LLM can handle all this complexity. It did surprisingly well on the accounting aspects, not being fooled by the lease accounting at all when analyzing true economic earnings. It accounted for the Joe Hudson acquisition separately from the main business, which is also good. However, it got lost in the weeds when trying to model out growth capex through new stores. Its methods were too complicated but didn't address the core question of what is the return on investment of new stores. Part of the problem is the company's disclosures do not lend itself nicely to answer that question. The other part of the problem I hypothesize is this kind of roll-up business model is relatively rare, and it did not have enough training data to be able to mimic the corresponding analysis well.

Third, we move on to human factors. If I put on my hat as a human stock analyst, the first two cases were good. They had helped me get up to speed on the company; with a clear enough structure in my head to work off of. The third case (Boyd) did not feel like genuine effort was saved. I could imagine spending a similar amount of time doing the work myself and walking away with better understanding. 

If you assume we want a world where at least some human specialists still are in the loop for knowledge work, then the human rate of understanding is the bottleneck. They still have to be able to check what the AI is doing is reasonable. And they need to know where to trust AI and where not to.

LLMs are able to output vast amounts of text and calculations in a short amount of time. It is however a distinct skill to be able to represent a complicated piece of work in a manner that is succinct, easy to follow for humans, but with an underlying structure such that the work process can be traced and scrutinized if need be (i.e. legible). The LLM did okay in this regard for NamSys and Adobe, and not so for Boyd. Perhaps there is a correlation between the ability to be legible and the inherent complexity of the task. I attempted to increase legibility by (1) causal modeling before forecasting which helps form a mental model in the human user’s head; (2) the prover-verifier-(human) judge structure to save human attention; and (3) the Excel file output format that is natural for humans to inspect and work with. 

Points (1) and (3) are based on how some human analysts naturally work, and (2) came out of the mental exhaustion I felt after checking every detail in the output files after the first few times. Note (2) can also raise more high level concerns, an example being the treatment of off balance sheet commitments and operating leases in the Adobe case.

---

## Contact

conflicting.gradient@proton.me