"""
Adobe Inc. (ADBE) - Five-year forecast of Owners' Earnings (FY2026E - FY2030E).

Companion to work_products/forecast_earnings.md.
Run with:  uv run python work_products/forecast_earnings_calcs.py

METHOD.  Forecast the ROOT-CAUSE drivers, not the downstream financials.

  Stage 1  Revenue, built bottom-up from four product lines, each with its own
           volume x monetisation drivers:
             BP&C (Acrobat/Express) = monthly active users x revenue per MAU
             Creative (CC flagship) = paid-unit volume + value-based price (+FX)
             Digital Experience     = enterprise seat expansion + cross-sell
             Semrush / run-off      = acquired book; P&A, product, services decay
  Stage 2  Gross profit, driven by the hosting / AI-inference cost ratio measured
           EXCLUDING purchased-intangible amortisation (which owners' earnings adds
           back), plus revenue mix across the three revenue lines.
  Stage 3  EBITA, driven by advertising intensity (the freemium funnel spend),
           other S&M operating leverage, R&D intensity and G&A.
  Stage 4  Owners' earnings = (EBITA + PP&E depreciation - maintenance capex)
           x (1 - normalised tax rate).  Identical construction to Method A in
           work_products/owners_earnings_and_roic.md, which it reproduces exactly
           for FY2025.

CROSS-CHECKS
  (a) FY2025 actuals reproduced through the whole chain (Section 8).
  (b) FY2026E reconciled to management's Q2 FY2026 revenue and GAAP-EPS guidance.
  (c) The EBITA -> EBIT bridge checked against Adobe's own DISCLOSED forward
      purchased-intangible amortisation schedule (Section 8b).

Every input is cited inline to primary_sources/, work_products/, fetched_docs/ or
the Knowledge Store. Judgments are labelled JUDGMENT.
"""

# ===========================================================================
# formatting helpers
# ===========================================================================
YRS = list(range(2026, 2031))


def hdr(t):
    print("\n" + "=" * 100)
    print(t)
    print("=" * 100)


def cols(w=46):
    print(f"{'':<{w}}" + "".join(f"{y:>10}" for y in YRS))


def row(label, vals, fmt="{:>10,.0f}", w=46):
    print(f"{label:<{w}}" + "".join(fmt.format(v) for v in vals))


def rowp(label, vals, w=46, dp=2):
    print(f"{label:<{w}}" + "".join(("{:>10." + str(dp) + "f}").format(v) for v in vals))


def chain(base, growths):
    """Compound `base` forward by a dict of annual growth rates."""
    out, p = {}, base
    for y in YRS:
        out[y] = p * (1 + growths[y])
        p = out[y]
    return out


def yoy(hist_base, series):
    p, g = hist_base, []
    for y in YRS:
        g.append(series[y] / p - 1)
        p = series[y]
    return g


# ===========================================================================
# SECTION 0 - HISTORICAL BASE
# ===========================================================================
hdr("SECTION 0 - HISTORICAL BASE AND THE FOUR-WAY REVENUE DECOMPOSITION")

# Consolidated Statements of Income, primary_sources/FY2025/financial_statements.md
# (verified against the filing, lines 80-98).
rev_total = {2023: 19_409, 2024: 21_505, 2025: 23_769}
rev_sub = {2023: 18_284, 2024: 20_521, 2025: 22_904}
rev_prod = {2023: 460, 2024: 386, 2025: 325}
rev_serv = {2023: 665, 2024: 598, 2025: 540}
cos_sub_t = {2023: 1_822, 2024: 1_799, 2025: 2_027}
cos_prod = {2023: 29, 2024: 25, 2025: 23}
cos_serv = {2023: 503, 2024: 534, 2025: 501}
rd = {2023: 3_473, 2024: 3_944, 2025: 4_294}
sm = {2023: 5_351, 2024: 5_764, 2025: 6_488}
ga = {2023: 1_413, 2024: 1_529, 2025: 1_573}
amort_opex = {2023: 168, 2024: 169, 2025: 157}
ebit = {2023: 6_650, 2024: 6_741, 2025: 8_706}

# Customer-group / segment subscription revenue, primary_sources/FY2025/md_and_a.md
sub_cmp = {2023: 13_425, 2024: 14_749, 2025: 16_303}   # Creative & Marketing Professionals
sub_bpc = {2023: 4_744, 2024: 5_662, 2025: 6_495}      # Business Professionals & Consumers
sub_dx = {2023: 4_331, 2024: 4_864, 2025: 5_409}       # Digital Experience segment subscription
sub_pa = {2023: 115, 2024: 110, 2025: 106}             # Publishing & Advertising subscription

# C&MP is defined in the FY2025 10-K MD&A as Digital Experience offerings PLUS the
# Creative Cloud flagship apps inside Digital Media, so "Creative" is derived by
# subtraction.  This is the only way to isolate the Creative franchise from
# Adobe's disclosure.
sub_creative = {y: sub_cmp[y] - sub_dx[y] for y in (2023, 2024, 2025)}
for y in (2023, 2024, 2025):
    assert abs(sub_cmp[y] + sub_bpc[y] + sub_pa[y] - rev_sub[y]) <= 1
    assert abs(rev_sub[y] + rev_prod[y] + rev_serv[y] - rev_total[y]) <= 1
    assert abs(rev_total[y] - cos_sub_t[y] - cos_prod[y] - cos_serv[y]
               - rd[y] - sm[y] - ga[y] - amort_opex[y]
               - (1_000 if y == 2024 else 0) - ebit[y]) <= 1
print("Identity checks (revenue lines, customer groups, full P&L to EBIT) -> OK")
print()
print(f"{'($M)':<46}{'FY2023':>10}{'FY2024':>10}{'FY2025':>10}{'24/23':>10}{'25/24':>10}")
for name, d in [("Creative (CC flagship, derived)", sub_creative),
                ("Digital Experience subscription", sub_dx),
                ("Business Prof. & Consumers (Acrobat/Express)", sub_bpc),
                ("Publishing & Advertising subscription", sub_pa)]:
    print(f"{name:<46}{d[2023]:>10,.0f}{d[2024]:>10,.0f}{d[2025]:>10,.0f}"
          f"{(d[2024]/d[2023]-1)*100:>9.1f}%{(d[2025]/d[2024]-1)*100:>9.1f}%")
print()
print("FY2025 expense lines as % of revenue (the ratios the forecast anchors on):")
for nm, d in [("R&D", rd), ("Sales & marketing", sm), ("G&A", ga)]:
    print(f"  {nm:<22}" + "".join(f"FY{y}: {d[y]/rev_total[y]*100:5.2f}%   " for y in (2023, 2024, 2025)))

# 1H FY2026 and 1H FY2025 actuals, primary_sources/2Q2026/financial_statements.md
h26 = dict(rev=13_016, sub=12_614, prod=179, serv=223, cos_sub=1_126, cos_prod=11,
           cos_serv=242, rd=2_308, sm=3_592, ga=1_009, amort_opex=72, ebit=4_656,
           amort_total=91, amort_in_cos=17)
h25 = dict(rev=11_587, sub=11_124, prod=183, serv=280, cos_sub=995, cos_prod=12,
           cos_serv=253, rd=2_108, sm=3_121, ga=744, amort_opex=82, ebit=4_272,
           amort_total=167, amort_in_cos=85)
print()
print("1H FY2026 vs 1H FY2025 expense ratios (2Q2026/financial_statements.md):")
for k, nm in [("rd", "R&D"), ("sm", "Sales & marketing"), ("ga", "G&A")]:
    print(f"  {nm:<22}1H FY2025: {h25[k]/h25['rev']*100:5.2f}%   "
          f"1H FY2026: {h26[k]/h26['rev']*100:5.2f}%   "
          f"growth {h26[k]/h25[k]-1:+6.1%}")

# ===========================================================================
# SECTION 1 - DRIVER: BP&C = MONTHLY ACTIVE USERS x REVENUE PER MAU
# ===========================================================================
hdr("SECTION 1 - ROOT DRIVER: BP&C (ACROBAT/EXPRESS) = MAU x MONETISATION PER MAU")

# Acrobat + Express monthly active users, exiting each fiscal period.
#   Q4 FY2025 call: MAU "surpassed 750 million ... growing 20% year-over-year"
#     -> FY2024 exit = 750/1.20 = 625M.
#   Q2 FY2026 call: MAU "from greater than 700 million to greater than 850 million
#     year-over-year", i.e. ~20% (Steve Day: "approximately 20%").
# See work_products/causal_model.md Factor 1.1.
MAU_FY24, MAU_FY25 = 625.0, 750.0
mau_exit = {2024: MAU_FY24, 2025: MAU_FY25}
# JUDGMENT: MAU growth decays as the easy distribution surfaces (Reader, Edge,
# Chrome, WhatsApp AI mode) saturate.  Not capped by the information-worker
# population (~1.14-1.25bn per Knowledge Store IDs 45/60) because Reader/Express
# reach consumers too; the binding constraint is monetisation, not reach.
mau_growth = {2026: 0.18, 2027: 0.13, 2028: 0.10, 2029: 0.08, 2030: 0.06}
for y in YRS:
    mau_exit[y] = mau_exit[y - 1] * (1 + mau_growth[y])
mau_avg = {y: (mau_exit[y - 1] + mau_exit[y]) / 2 for y in range(2025, 2031)}

# Revenue per average MAU is the OBSERVABLE composite of (free-to-paid conversion)
# x (price per paid seat).  Adobe discloses neither component (causal_model.md
# uncertainty #1), so the composite is what can be forecast honestly.
rpm = {2024: sub_bpc[2024] / ((MAU_FY24 / 1.20 + MAU_FY24) / 2),
       2025: sub_bpc[2025] / mau_avg[2025]}
print(f"FY2024 revenue per average MAU = ${rpm[2024]:.2f}")
print(f"FY2025 revenue per average MAU = ${rpm[2025]:.2f}   "
      f"({rpm[2025]/rpm[2024]-1:+.1%} YoY)")
print("Decomposition of the FY2025 actual (computed):")
print(f"  BP&C revenue growth {sub_bpc[2025]/sub_bpc[2024]-1:+.1%} "
      f"= average-MAU growth {mau_avg[2025]/((MAU_FY24/1.20+MAU_FY24)/2)-1:+.1%} "
      f"+ revenue-per-MAU change {rpm[2025]/rpm[2024]-1:+.1%}")
print("  If price per paid seat rose ~2.5%/yr (value-based pricing, Acrobat Studio")
print("  attach - 4Q2025 call), the implied PAID-SEAT growth was ~11.9%, i.e. paid")
print("  seats grew at roughly 0.6x the MAU growth rate. That 0.6x wedge is the")
print("  mechanical reason revenue per MAU falls while MAU compounds.")

# JUDGMENT: revenue per MAU keeps falling while MAU growth runs far ahead of paid
# seats, then stabilises as MAU growth decays toward the ~2-3% price contribution.
rpm_delta = {2026: -0.035, 2027: -0.025, 2028: -0.010, 2029: 0.000, 2030: 0.000}
for y in YRS:
    rpm[y] = rpm[y - 1] * (1 + rpm_delta[y])
f_bpc = {y: mau_avg[y] * rpm[y] for y in YRS}

print()
cols()
row("MAU exiting year (millions)", [mau_exit[y] for y in YRS])
rowp("  MAU growth %", [mau_growth[y] * 100 for y in YRS], dp=1)
row("Average MAU (millions)", [mau_avg[y] for y in YRS])
rowp("Revenue per average MAU ($/yr)", [rpm[y] for y in YRS])
rowp("  change in revenue per MAU %", [rpm_delta[y] * 100 for y in YRS], dp=1)
row("BP&C subscription revenue ($M)", [f_bpc[y] for y in YRS])
rowp("  implied revenue growth %", [x * 100 for x in yoy(sub_bpc[2025], f_bpc)], dp=1)
print()
print("Implied paid-seat growth if price per seat rises 2.5%/yr (consistency check):")
rowp("  implied paid-seat growth %",
     [((1 + mau_growth[y]) * (1 + rpm_delta[y]) / 1.025 - 1) * 100 for y in YRS], dp=1)
rowp("  implied paid seats as multiple of FY2025 (index)",
     [__import__('math').prod([(1 + mau_growth[k]) * (1 + rpm_delta[k]) / 1.025
                               for k in range(2026, y + 1)]) for y in YRS])

# ===========================================================================
# SECTION 2 - DRIVER: CREATIVE = PAID-UNIT VOLUME + VALUE-BASED PRICE
# ===========================================================================
hdr("SECTION 2 - ROOT DRIVER: CREATIVE = PAID-UNIT VOLUME + VALUE-BASED PRICE (+FX)")

# The empirical volume/price split.  Q4 FY2025 call (CFO Dan Durn): "Over 75% of
# Digital Media net new ARR was driven by continued growth in subscriptions and
# cross-sell and upsell, with the remainder from value-based pricing"
# (primary_sources/4Q2025/earnings_call_transcript.md; causal_model.md Section 0).
g_cre_25 = sub_creative[2025] / sub_creative[2024] - 1
print(f"FY2025 Creative revenue growth (computed) = {g_cre_25:+.1%}")
print(f"  split 75/25 volume/price -> volume ~{g_cre_25*0.75:+.1%}, price ~{g_cre_25*0.25:+.1%}")

# JUDGMENT on the forward path.
#   Volume: the professional creative seat pool is roughly flat (US graphic-designer
#     employment projected to DECLINE 2% 2025-2035, Knowledge Store ID 35), so
#     volume growth must come from prosumer/freemium conversion against intensifying
#     AI-native competition (Canva, Figma - Knowledge Store IDs 15, 16, 23).
#     Decays from the FY2025 run-rate toward low single digits.
#   Price: ~0 in FY2026 because Adobe deliberately deferred the second-half Creative
#     Cloud "line optimizations" (2Q2026 call), then resumes at ~2%/yr - supported by
#     actual FY2026 price actions (CC Pro to $70/mo May 2026, Lightroom increases -
#     Knowledge Store IDs 37, 40).
#   FX: +2pp in FY2026 only (Q2 FY2026 FX added ~$94M net, ~13% of reported growth -
#     causal_model.md Factor 1.7).  Zero thereafter: no view on currencies.
cre_volume = {2026: 0.078, 2027: 0.060, 2028: 0.050, 2029: 0.040, 2030: 0.030}
cre_price = {2026: 0.005, 2027: 0.020, 2028: 0.020, 2029: 0.020, 2030: 0.020}
cre_fx = {2026: 0.020, 2027: 0.000, 2028: 0.000, 2029: 0.000, 2030: 0.000}
cre_g = {y: cre_volume[y] + cre_price[y] + cre_fx[y] for y in YRS}
f_cre = chain(sub_creative[2025], cre_g)

cols()
rowp("Paid-unit (volume) growth %", [cre_volume[y] * 100 for y in YRS], dp=1)
rowp("Value-based price / tier mix %", [cre_price[y] * 100 for y in YRS], dp=1)
rowp("FX translation %", [cre_fx[y] * 100 for y in YRS], dp=1)
rowp("= Creative revenue growth %", [cre_g[y] * 100 for y in YRS], dp=1)
row("Creative subscription revenue ($M)", [f_cre[y] for y in YRS])

# ===========================================================================
# SECTION 3 - DIGITAL EXPERIENCE, SEMRUSH AND THE RUN-OFF LINES
# ===========================================================================
hdr("SECTION 3 - DIGITAL EXPERIENCE (ENTERPRISE SEATS + CROSS-SELL), SEMRUSH, RUN-OFF")

# DX root driver: enterprise seat expansion and product attach.  Disclosed proxies:
# customers with >$10M ARR "growing greater than 20% year-over-year" and GenStudio/
# AEP/AEM ending ARR "growing over 20% year-over-year" (Steve Day, 2Q2026 call).
# But total DX SUBSCRIPTION revenue growth has been decelerating: 12.3% -> 11.2%.
# JUDGMENT: continues to grind down as the base grows and agentic-web competition
# rises; no re-acceleration assumed.
dx_growth = {2026: 0.090, 2027: 0.080, 2028: 0.075, 2029: 0.070, 2030: 0.065}
f_dx = chain(sub_dx[2025], dx_growth)

# Semrush: ~$1.9bn all-cash, closed April 2026, ~$480M acquired ARR, ~$40M of Q2
# FY2026 revenue and ~$280M expected in FY2026 (2Q2026/md_and_a.md; Steve Day,
# 2Q2026 call).  JUDGMENT: annualises to ~$500M in FY2027 then grows high single
# digit - below Semrush's standalone history, reflecting acquisition friction.
f_sem = {2026: 280.0, 2027: 500.0, 2028: 540.0, 2029: 578.0, 2030: 612.0}

# Run-off lines.  P&A is being written down (the Q2 FY2026 goodwill impairment).
f_pa = chain(sub_pa[2025], {y: -0.05 for y in YRS})
# Product and services: 1H FY2026 annualised, then continued decline.
f_prod = chain(rev_prod[2025], {2026: -0.020, 2027: -0.050, 2028: -0.050,
                                2029: -0.050, 2030: -0.050})
f_serv = chain(rev_serv[2025], {2026: -0.200, 2027: -0.120, 2028: -0.100,
                                2029: -0.080, 2030: -0.080})
print(f"Product revenue: FY2025 {rev_prod[2025]}, 1H FY2026 annualised "
      f"{h26['prod']*2} -> FY2026E {f_prod[2026]:,.0f}")
print(f"Services revenue: FY2025 {rev_serv[2025]}, 1H FY2026 annualised "
      f"{h26['serv']*2} -> FY2026E {f_serv[2026]:,.0f}")
print()
cols()
rowp("DX organic growth %", [dx_growth[y] * 100 for y in YRS], dp=1)
row("DX subscription revenue ($M)", [f_dx[y] for y in YRS])
row("Semrush revenue ($M)", [f_sem[y] for y in YRS])
row("P&A subscription ($M)", [f_pa[y] for y in YRS])
row("Product revenue ($M)", [f_prod[y] for y in YRS])
row("Services and other revenue ($M)", [f_serv[y] for y in YRS])

# ===========================================================================
# SECTION 4 - REVENUE BUILD AND RECONCILIATION TO GUIDANCE
# ===========================================================================
hdr("SECTION 4 - TOTAL REVENUE BUILD, AND FY2026E RECONCILED TO MANAGEMENT GUIDANCE")

f_cmp = {y: f_cre[y] + f_dx[y] + f_sem[y] for y in YRS}
f_cg = {y: f_cmp[y] + f_bpc[y] for y in YRS}
f_subrev = {y: f_cg[y] + f_pa[y] for y in YRS}
f_rev = {y: f_subrev[y] + f_prod[y] + f_serv[y] for y in YRS}

cols()
row("C&MP subscription revenue", [f_cmp[y] for y in YRS])
row("BP&C subscription revenue", [f_bpc[y] for y in YRS])
row("Total customer-group subscription revenue", [f_cg[y] for y in YRS])
row("Total subscription revenue", [f_subrev[y] for y in YRS])
row("TOTAL REVENUE", [f_rev[y] for y in YRS])
rev_g = yoy(rev_total[2025], f_rev)
rowp("  total revenue growth %", [x * 100 for x in rev_g], dp=1)
rev_cagr = (f_rev[2030] / rev_total[2025]) ** 0.2 - 1
print(f"\nFY2025 -> FY2030E total revenue CAGR: {rev_cagr*100:.1f}%")

print("\nFY2026E reconciled to management's Q2 FY2026 FY-guidance [GUIDANCE, forward-looking]")
print("(primary_sources/2Q2026/earnings_call_transcript.md; Knowledge Store ID 13):")
print(f"  BP&C subscription    model {f_bpc[2026]:>8,.0f}   vs FY2026 guide  7,440 - 7,480")
print(f"  C&MP subscription    model {f_cmp[2026]:>8,.0f}   vs FY2026 guide 18,210 - 18,270")
print(f"  Total revenue        model {f_rev[2026]:>8,.0f}   vs FY2026 guide 26,500 - 26,600")
print("NOTE: 1H FY2026 is reported and Q3 FY2026 is guided, so only Q4 FY2026 is a")
print("genuine forecast. The FY2026E column is therefore a calibration year, not an")
print("independent test of the model.")

# ===========================================================================
# SECTION 6 - GROSS PROFIT: THE HOSTING / AI-INFERENCE COST RATIO
# ===========================================================================
hdr("SECTION 6 - COST DRIVER: HOSTING / AI-INFERENCE RATIO, EX-PURCHASED-INTANGIBLE AMORT.")

# Purchased-intangible amortisation sitting INSIDE cost of subscription revenue is
# stripped out, because owners' earnings adds it back.  FY2025: total amortisation of
# other intangibles $310M, "of these amounts, $151 million ... was included in cost of
# sales" (primary_sources/FY2025/financial_statements.md, Note 8, line 895).
# 1H FY2026: total $91M of which $17M in cost of revenue; 1H FY2025: $167M of which
# $85M (2Q2026/financial_statements.md, Note 7, line 610).
AMORT_IN_COS_25 = 151.0
r25 = (cos_sub_t[2025] - AMORT_IN_COS_25) / rev_sub[2025]
r_h25 = (h25["cos_sub"] - h25["amort_in_cos"]) / h25["sub"]
r_h26 = (h26["cos_sub"] - h26["amort_in_cos"]) / h26["sub"]
print(f"FY2025    cost of subscription ex-amortisation / subscription revenue = {r25*100:.2f}%")
print(f"1H FY2025 same ratio = {r_h25*100:.2f}%")
print(f"1H FY2026 same ratio = {r_h26*100:.2f}%    -> {(r_h26-r_h25)*1e4:+.0f}bp YoY")
print(f"  ex-amortisation cost of subscription grew {(h26['cos_sub']-h26['amort_in_cos'])/(h25['cos_sub']-h25['amort_in_cos'])-1:+.1%} "
      f"against subscription revenue {h26['sub']/h25['sub']-1:+.1%}")
print("REPORTED subscription gross margin looks nearly flat only because purchased-")
print("intangible amortisation inside cost of revenue fell from $85M to $17M, worth")
print(f"{(h25['amort_in_cos']-h26['amort_in_cos'])/h26['sub']*1e4:.0f}bp of subscription revenue - it masked almost the whole underlying")
print("deterioration. On the basis that matters for owners' earnings the hosting/AI")
print("cost ratio is deteriorating ~60bp/yr RIGHT NOW. This is the key cost finding.")

# JUDGMENT on the forward drift.  Two opposing forces:
#   volume UP  - ~150M net new free Acrobat/Express MAU and ~40M free creative MAU
#     consuming credits, with traffic re-routing starting Q3 FY2026 (2Q2026 call);
#   unit cost DOWN - per-unit inference prices have been falling fast (a16z
#     "LLMflation" ~10x/yr per token; Epoch AI 9x-900x/yr depending on task -
#     fetched_docs/a16z_llmflation.md, fetched_docs/epoch_llm_inference_price_trends.md,
#     Knowledge Store IDs 19, 20, 58).
# Base case: volume wins in the near term (the ratio keeps deteriorating), unit-cost
# deflation catches up as free-MAU growth decelerates.  Drift decays 72bp -> 20bp.
cos_drift_bp = {2026: 72, 2027: 50, 2028: 35, 2029: 25, 2030: 20}


def cos_path(drift):
    r = {2025: r25}
    for y in YRS:
        r[y] = r[y - 1] + drift[y] / 1e4
    return r


r_sub = cos_path(cos_drift_bp)
cols()
rowp("Subscription cost ratio ex-amort. %", [r_sub[y] * 100 for y in YRS])
rowp("  annual drift (bp)", [cos_drift_bp[y] for y in YRS], dp=0)
print(f"Cumulative FY2025 -> FY2030E deterioration: "
      f"{(r_sub[2030]-r25)*1e4:.0f}bp, i.e. ${(r_sub[2030]-r25)*f_subrev[2030]:,.0f}M of "
      f"extra annual cost at FY2030E revenue.")

# Product and services cost ratios.
PROD_COST_RATIO = cos_prod[2025] / rev_prod[2025]
SERV_COST_RATIO = 1.05          # 1H FY2026 ran at 1.085; FY2025 at 0.928; services
                                # is now LOSS-MAKING (causal_model.md Factor 2.3)
print(f"Product cost ratio (FY2025 actual) {PROD_COST_RATIO:.3f}; services cost ratio "
      f"assumed {SERV_COST_RATIO:.3f} (1H FY2026 actual {h26['cos_serv']/h26['serv']:.3f})")


def gross_profit(y, rs):
    cost = f_subrev[y] * rs[y] + f_prod[y] * PROD_COST_RATIO + f_serv[y] * SERV_COST_RATIO
    return f_rev[y] - cost


gp = {y: gross_profit(y, r_sub) for y in YRS}
row("Gross profit ex-amortisation ($M)", [gp[y] for y in YRS])
rowp("  gross margin ex-amortisation %", [gp[y] / f_rev[y] * 100 for y in YRS])
gm25 = (rev_total[2025] - (cos_sub_t[2025] - AMORT_IN_COS_25) - cos_prod[2025]
        - cos_serv[2025]) / rev_total[2025]
print(f"FY2025 actual gross margin, same ex-amortisation basis: {gm25*100:.2f}%")

# ===========================================================================
# SECTION 7 - OPERATING EXPENSE DRIVERS
# ===========================================================================
hdr("SECTION 7 - OPERATING EXPENSE DRIVERS: ADVERTISING INTENSITY IS THE ROOT CAUSE")

# Advertising expense disclosed in primary_sources/FY2025/financial_statements.md Note 1.
adv_hist = {2023: 970.0, 2024: 1_040.0, 2025: 1_370.0}
for y in (2023, 2024, 2025):
    print(f"FY{y}: advertising {adv_hist[y]:>7,.0f} = {adv_hist[y]/rev_total[y]*100:4.2f}% of revenue "
          f"({adv_hist[y]/adv_hist[y-1]-1:+6.1%} YoY)" if y > 2023 else
          f"FY{y}: advertising {adv_hist[y]:>7,.0f} = {adv_hist[y]/rev_total[y]*100:4.2f}% of revenue")
    print(f"        other S&M {sm[y]-adv_hist[y]:>7,.0f} = {(sm[y]-adv_hist[y])/rev_total[y]*100:5.2f}% of revenue")

# JUDGMENT.  Total S&M intensity is anchored by management's non-GAAP operating-margin
# guidance (~45% FY2026, ~44% Q3 FY2026 - 2Q2026 call, Knowledge Store ID 13) and by
# the 1H FY2026 actual (S&M 27.60% of revenue vs 26.94% a year earlier).  The split
# between advertising and other S&M is an inference from the MD&A attribution
# ("primarily due to increases in advertising expenses and, to a lesser extent,
# compensation costs") and is illustrative, not disclosed.
adv_pct = {2026: 0.0690, 2027: 0.0695, 2028: 0.0650, 2029: 0.0610, 2030: 0.0580}
oth_sm_pct = {2026: 0.2100, 2027: 0.2070, 2028: 0.2040, 2029: 0.2015, 2030: 0.1995}
# R&D pinned at ~18% of revenue for four straight years (18.07% FY2025, 17.73% 1H
# FY2026).  JUDGMENT: held flat at 18.0%; model TRAINING compute sits here and will
# grow, but Adobe attributes R&D increases to compensation, not compute.
rd_pct = {y: 0.180 for y in YRS}
# G&A: FY2025 actual 6.62%.  JUDGMENT: 6.7% forward, i.e. FY2025 plus ~8bp of
# normalised annual legal provision (owners_earnings_and_roic.md Section 2.1 flags
# $30-50M/yr as defensible), with the Q2 FY2026 impairment/settlement treated as
# non-recurring.
ga_pct = {y: 0.067 for y in YRS}

print()
cols()
rowp("Advertising % of revenue", [adv_pct[y] * 100 for y in YRS])
rowp("Other S&M % of revenue", [oth_sm_pct[y] * 100 for y in YRS])
rowp("= Sales & marketing % of revenue", [(adv_pct[y] + oth_sm_pct[y]) * 100 for y in YRS])
rowp("R&D % of revenue", [rd_pct[y] * 100 for y in YRS])
rowp("G&A % of revenue", [ga_pct[y] * 100 for y in YRS])
row("Advertising expense ($M)", [adv_pct[y] * f_rev[y] for y in YRS])
rowp("  advertising growth %", [x * 100 for x in yoy(adv_hist[2025],
     {y: adv_pct[y] * f_rev[y] for y in YRS})], dp=1)
row("Total S&M expense ($M)", [(adv_pct[y] + oth_sm_pct[y]) * f_rev[y] for y in YRS])
rowp("  total S&M growth %", [x * 100 for x in yoy(sm[2025],
     {y: (adv_pct[y] + oth_sm_pct[y]) * f_rev[y] for y in YRS})], dp=1)

# ===========================================================================
# SECTION 8 - EBITA AND OWNERS' EARNINGS
# ===========================================================================
hdr("SECTION 8 - EBITA AND OWNERS' EARNINGS (BASE CASE)")

TAX = 0.21          # normalised rate per work_products/owners_earnings_and_roic.md 2.3
dep = chain(236.0, {y: 0.05 for y in YRS})      # FY2025 PP&E depreciation, 10-K Note 6
mcx = chain(241.0, {y: 0.05 for y in YRS})      # 3-yr average capex, owners' earnings 2.2


def run(rs, advp, othp, rdp, gap, tax=TAX, rev=None, subrev=None,
        prod=None, serv=None):
    rev = rev or f_rev
    subrev = subrev or f_subrev
    prod = prod or f_prod
    serv = serv or f_serv
    out = {}
    for y in YRS:
        cost = subrev[y] * rs[y] + prod[y] * PROD_COST_RATIO + serv[y] * SERV_COST_RATIO
        ebita = rev[y] - cost - rev[y] * (advp[y] + othp[y] + rdp[y] + gap[y])
        pre = ebita + dep[y] - mcx[y]
        out[y] = dict(rev=rev[y], ebita=ebita, pre=pre, oe=pre * (1 - tax))
    return out


base = run(r_sub, adv_pct, oth_sm_pct, rd_pct, ga_pct)

# FY2025 actual on the IDENTICAL construction.
AMORT_TOTAL_25 = 310.0
ebita25 = ebit[2025] + AMORT_TOTAL_25
pre25 = ebita25 + dep[2025] - mcx[2025] if 2025 in dep else ebita25 + 236.0 - 241.0
oe25 = pre25 * (1 - TAX)
print(f"FY2025 replication: EBIT {ebit[2025]:,} + amortisation {AMORT_TOTAL_25:,.0f} = "
      f"EBITA {ebita25:,.0f}; + dep 236 - maint. capex 241 = pre-tax owners' earnings "
      f"{pre25:,.0f}; x (1-21%) = {oe25:,.0f}")
print(f"  work_products/owners_earnings_and_roic.md reports 9,011 / 7,119 -> ties exactly.")

print()
cols()
row("EBITA ($M)", [base[y]["ebita"] for y in YRS])
rowp("  EBITA margin %", [base[y]["ebita"] / f_rev[y] * 100 for y in YRS])
row("+ PP&E depreciation", [dep[y] for y in YRS])
row("- maintenance capex", [-mcx[y] for y in YRS])
row("= pre-tax owners' earnings", [base[y]["pre"] for y in YRS])
row("OWNERS' EARNINGS (21% normalised tax)", [base[y]["oe"] for y in YRS])
rowp("  owners' earnings margin %", [base[y]["oe"] / f_rev[y] * 100 for y in YRS])
oe_g = yoy(oe25, {y: base[y]["oe"] for y in YRS})
rowp("  YoY growth %", [x * 100 for x in oe_g], dp=1)
oe_cagr = (base[2030]["oe"] / oe25) ** 0.2 - 1
print(f"\nFY2025 ({oe25:,.0f}) -> FY2030E ({base[2030]['oe']:,.0f}) owners' earnings CAGR: "
      f"{oe_cagr*100:.1f}%   (revenue CAGR {rev_cagr*100:.1f}%)")
print(f"FY2025 EBITA margin {ebita25/rev_total[2025]*100:.2f}% -> FY2026E "
      f"{base[2026]['ebita']/f_rev[2026]*100:.2f}% -> FY2030E "
      f"{base[2030]['ebita']/f_rev[2030]*100:.2f}%")

# --- 8b. The EBITA -> EBIT bridge against Adobe's DISCLOSED amortisation schedule --
hdr("SECTION 8b - CROSS-CHECK: EBITA -> GAAP EBIT USING THE DISCLOSED AMORT. SCHEDULE")
# primary_sources/2Q2026/financial_statements.md Note 7: estimated aggregate
# amortisation of other intangibles - remainder of FY2026 $131M, FY2027 $208M,
# FY2028 $151M, FY2029 $146M, FY2030 $143M.  FY2026 total = $91M actual 1H + $131M.
amort_sched = {2026: 91.0 + 131.0, 2027: 208.0, 2028: 151.0, 2029: 146.0, 2030: 143.0}
cols()
row("Disclosed purchased-intangible amortisation", [amort_sched[y] for y in YRS])
row("Implied GAAP EBIT (EBITA - amortisation)", [base[y]["ebita"] - amort_sched[y] for y in YRS])
rowp("  implied GAAP operating margin %",
     [(base[y]["ebita"] - amort_sched[y]) / f_rev[y] * 100 for y in YRS])
print(f"FY2025 actual GAAP operating margin: {ebit[2025]/rev_total[2025]*100:.2f}%")
print("(The schedule excludes intangibles from FUTURE acquisitions - e.g. Topaz Labs,")
print(" agreed June 25 2026, Knowledge Store ID 18 - so it is a floor on amortisation")
print(" and the implied GAAP margins are a ceiling. Owners' earnings are unaffected.)")

# --- 8c. FY2026E against management's GAAP EPS guidance ---------------------------
GAAP_EPS_MID, SH26 = 17.95, 399.0   # FY2026 guided diluted share count ~399M
gaap_ni = GAAP_EPS_MID * SH26
gaap_pre = gaap_ni / (1 - 0.225)          # FY2026 guided GAAP tax rate ~22.5%
implied_ebita = gaap_pre + amort_sched[2026] + 70.0 + 92.0
print(f"\nFY2026E vs guidance: GAAP EPS mid ${GAAP_EPS_MID} x {SH26:.0f}M shares = "
      f"{gaap_ni:,.0f} net income; / (1-22.5%) = {gaap_pre:,.0f} pre-tax;")
print(f"  + amortisation {amort_sched[2026]:.0f} + goodwill impairment 70 + FTC contingency 92 "
      f"= {implied_ebita:,.0f} implied EBITA")
print(f"  model FY2026E EBITA {base[2026]['ebita']:,.0f} "
      f"({base[2026]['ebita']/implied_ebita-1:+.1%}). Note this ignores non-operating")
print("  income, which is now near zero (1H FY2026 net non-operating income $4M).")

# ===========================================================================
# SECTION 9 - SCENARIOS
# ===========================================================================
hdr("SECTION 9 - SCENARIOS ON THE LOAD-BEARING DRIVERS")


def scenario(mau_g, rpm_d, cvol, cpr, dxg, drift, advp, othp, rdp, gap=None,
             sem=None, tax=TAX):
    gap = gap or ga_pct
    me = {2025: MAU_FY25}
    for y in YRS:
        me[y] = me[y - 1] * (1 + mau_g[y])
    ma = {y: (me[y - 1] + me[y]) / 2 for y in YRS}
    rp = {2025: rpm[2025]}
    for y in YRS:
        rp[y] = rp[y - 1] * (1 + rpm_d[y])
    bpc = {y: ma[y] * rp[y] for y in YRS}
    cre = chain(sub_creative[2025], {y: cvol[y] + cpr[y] + cre_fx[y] for y in YRS})
    dx = chain(sub_dx[2025], dxg)
    s = sem or f_sem
    subrev = {y: cre[y] + dx[y] + s[y] + bpc[y] + f_pa[y] for y in YRS}
    rev = {y: subrev[y] + f_prod[y] + f_serv[y] for y in YRS}
    return run(cos_path(drift), advp, othp, rdp, gap, tax=tax,
               rev=rev, subrev=subrev)


# BEAR: AI substitution bites Creative, the freemium advertising spend never comes
# down, inference cost keeps compounding, BP&C monetisation keeps eroding.
bearO = scenario(
    mau_g={2026: 0.18, 2027: 0.11, 2028: 0.08, 2029: 0.06, 2030: 0.04},
    rpm_d={2026: -0.045, 2027: -0.045, 2028: -0.035, 2029: -0.030, 2030: -0.030},
    cvol={2026: 0.070, 2027: 0.035, 2028: 0.020, 2029: 0.010, 2030: 0.000},
    cpr={2026: 0.005, 2027: 0.010, 2028: 0.010, 2029: 0.010, 2030: 0.010},
    dxg={2026: 0.085, 2027: 0.060, 2028: 0.050, 2029: 0.045, 2030: 0.040},
    drift={2026: 80, 2027: 75, 2028: 65, 2029: 60, 2030: 55},
    advp={2026: 0.0700, 2027: 0.0730, 2028: 0.0730, 2029: 0.0730, 2030: 0.0730},
    othp={y: 0.2130 for y in YRS},
    rdp={y: 0.187 for y in YRS})

# SEVERE: the causal model's highest-consequence risk actually happens - generative
# AI substitutes Adobe's creative workflows the way it substituted Adobe Stock, and
# Adobe defends with price cuts and more advertising.
severeO = scenario(
    mau_g={2026: 0.17, 2027: 0.08, 2028: 0.04, 2029: 0.02, 2030: 0.00},
    rpm_d={2026: -0.055, 2027: -0.070, 2028: -0.060, 2029: -0.050, 2030: -0.045},
    cvol={2026: 0.060, 2027: 0.000, 2028: -0.040, 2029: -0.050, 2030: -0.050},
    cpr={2026: 0.000, 2027: 0.000, 2028: 0.000, 2029: 0.000, 2030: 0.000},
    dxg={2026: 0.080, 2027: 0.040, 2028: 0.025, 2029: 0.020, 2030: 0.015},
    drift={2026: 90, 2027: 100, 2028: 90, 2029: 80, 2030: 70},
    advp={y: 0.0760 for y in YRS},
    othp={y: 0.2180 for y in YRS},
    rdp={y: 0.195 for y in YRS},
    gap={y: 0.069 for y in YRS},
    sem={2026: 280.0, 2027: 470.0, 2028: 470.0, 2029: 470.0, 2030: 470.0})

# BULL: freemium converts, unit inference cost deflation outruns volume growth,
# advertising normalises after FY2027, price optimisations resume in full.
bullO = scenario(
    mau_g={2026: 0.19, 2027: 0.15, 2028: 0.12, 2029: 0.10, 2030: 0.08},
    rpm_d={2026: -0.030, 2027: -0.005, 2028: 0.010, 2029: 0.015, 2030: 0.015},
    cvol={2026: 0.085, 2027: 0.085, 2028: 0.075, 2029: 0.065, 2030: 0.055},
    cpr={2026: 0.005, 2027: 0.030, 2028: 0.030, 2029: 0.030, 2030: 0.030},
    dxg={2026: 0.095, 2027: 0.095, 2028: 0.090, 2029: 0.085, 2030: 0.080},
    drift={2026: 60, 2027: 25, 2028: 10, 2029: 0, 2030: -10},
    advp={2026: 0.0680, 2027: 0.0660, 2028: 0.0590, 2029: 0.0540, 2030: 0.0510},
    othp={2026: 0.2090, 2027: 0.2040, 2028: 0.1990, 2029: 0.1950, 2030: 0.1910},
    rdp={y: 0.178 for y in YRS})

SCEN = [("SEVERE", severeO), ("BEAR", bearO), ("BASE", base), ("BULL", bullO)]
cols()
for nm, sc in SCEN:
    row(f"Revenue - {nm}", [sc[y]["rev"] for y in YRS])
print()
for nm, sc in SCEN:
    row(f"Owners' earnings - {nm}", [sc[y]["oe"] for y in YRS])
print()
print(f"{'Scenario':<12}{'FY30E OE':>11}{'OE CAGR':>10}{'Rev CAGR':>10}"
      f"{'FY30E OE margin':>18}")
for nm, sc in SCEN:
    print(f"{nm:<12}{sc[2030]['oe']:>11,.0f}"
          f"{((sc[2030]['oe']/oe25)**0.2-1)*100:>9.1f}%"
          f"{((sc[2030]['rev']/rev_total[2025])**0.2-1)*100:>9.1f}%"
          f"{sc[2030]['oe']/sc[2030]['rev']*100:>17.1f}%")

# Probability weighting.  JUDGMENT - these are subjective weights, not sourced.
W = {"SEVERE": 0.15, "BEAR": 0.25, "BASE": 0.40, "BULL": 0.20}
print(f"\nProbability-weighted (JUDGMENT weights "
      f"{', '.join(f'{k} {v:.0%}' for k, v in W.items())}):")
wt = {y: sum(W[nm] * sc[y]["oe"] for nm, sc in SCEN) for y in YRS}
cols()
row("Weighted owners' earnings ($M)", [wt[y] for y in YRS])
rowp("  YoY growth %", [x * 100 for x in yoy(oe25, wt)], dp=1)
print(f"Weighted FY2025 -> FY2030E owners' earnings CAGR: "
      f"{((wt[2030]/oe25)**0.2-1)*100:.1f}%")

# ===========================================================================
# SECTION 10 - SINGLE-DRIVER SENSITIVITIES
# ===========================================================================
hdr("SECTION 10 - SINGLE-DRIVER SENSITIVITIES (FY2030E OWNERS' EARNINGS, BASE CASE)")

b30 = base[2030]["oe"]
tests = [
    ("hosting/AI cost drift flat at 60bp/yr",
     lambda: run(cos_path({y: 60 for y in YRS}), adv_pct, oth_sm_pct, rd_pct, ga_pct)),
    ("hosting/AI cost drift doubled",
     lambda: run(cos_path({y: v * 2 for y, v in cos_drift_bp.items()}), adv_pct,
                 oth_sm_pct, rd_pct, ga_pct)),
    ("hosting/AI cost drift zero after FY2026",
     lambda: run(cos_path({2026: 72, 2027: 0, 2028: 0, 2029: 0, 2030: 0}), adv_pct,
                 oth_sm_pct, rd_pct, ga_pct)),
    ("advertising stays at its FY2027 peak (6.95%)",
     lambda: run(r_sub, {y: 0.0695 for y in YRS}, oth_sm_pct, rd_pct, ga_pct)),
    ("no operating leverage in other S&M (21.0% flat)",
     lambda: run(r_sub, adv_pct, {y: 0.210 for y in YRS}, rd_pct, ga_pct)),
    ("R&D rises to 19.0% of revenue",
     lambda: run(r_sub, adv_pct, oth_sm_pct, {y: 0.190 for y in YRS}, ga_pct)),
    ("normalised tax 18% (management non-GAAP rate)",
     lambda: run(r_sub, adv_pct, oth_sm_pct, rd_pct, ga_pct, tax=0.18)),
    ("normalised tax 25% (recent cash-tax experience)",
     lambda: run(r_sub, adv_pct, oth_sm_pct, rd_pct, ga_pct, tax=0.25)),
]
for lbl, fn in tests:
    o = fn()[2030]["oe"]
    print(f"{lbl:<50}{o:>11,.0f}   ({o/b30-1:+6.1%})")
# Revenue-side single drivers (rebuild the whole revenue stack).
rev_tests = [
    ("Creative volume growth 2pp lower every year",
     dict(cvol={y: cre_volume[y] - 0.02 for y in YRS})),
    ("Creative volume growth 2pp higher every year",
     dict(cvol={y: cre_volume[y] + 0.02 for y in YRS})),
    ("BP&C revenue per MAU falls 2pp/yr faster",
     dict(rpm_d={y: rpm_delta[y] - 0.02 for y in YRS})),
    ("BP&C MAU growth 3pp lower every year",
     dict(mau_g={y: mau_growth[y] - 0.03 for y in YRS})),
]
defaults = dict(mau_g=mau_growth, rpm_d=rpm_delta, cvol=cre_volume, cpr=cre_price,
                dxg=dx_growth, drift=cos_drift_bp, advp=adv_pct, othp=oth_sm_pct,
                rdp=rd_pct)
for lbl, over in rev_tests:
    kw = dict(defaults)
    kw.update(over)
    o = scenario(**kw)[2030]["oe"]
    print(f"{lbl:<50}{o:>11,.0f}   ({o/b30-1:+6.1%})")

hdr("END")
