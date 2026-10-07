"""
Adobe Inc. (ADBE) — causal model supporting calculations.

Every input below is tagged with its primary source. No number in
`work_products/causal_model.md` is asserted unless it is either quoted
directly from a source or computed here.

Sources:
  FY25_MDA  = primary_sources/FY2025/md_and_a.md
  FY25_FS   = primary_sources/FY2025/financial_statements.md
  FY25_BUS  = primary_sources/FY2025/business.md
  Q226_MDA  = primary_sources/2Q2026/md_and_a.md
  Q226_FS   = primary_sources/2Q2026/financial_statements.md
  Q226_CALL = primary_sources/2Q2026/earnings_call_transcript.md
  Q126_CALL = primary_sources/1Q2026/earnings_call_transcript.md
  Q425_CALL = primary_sources/4Q2025/earnings_call_transcript.md
"""

def pct(x):
    return f"{x*100:.1f}%"


def pp(x):
    return f"{x*100:+.2f}pp"


out = []
def say(s=""):
    out.append(s)


# ---------------------------------------------------------------------------
# 1. Income statement history (FY25_FS lines 78-96; FY25_MDA revenue/cost tables)
# ---------------------------------------------------------------------------
fy = {
    #            revenue, cost_of_rev, R&D,   S&M,   G&A,  term_fee, amort
    2023: dict(rev=19409, cor=2354, rnd=3473, snm=5351, gna=1413, term=0,    amort=168),
    2024: dict(rev=21505, cor=2358, rnd=3944, snm=5764, gna=1529, term=1000, amort=169),
    2025: dict(rev=23769, cor=2551, rnd=4294, snm=6488, gna=1573, term=0,    amort=157),
}
for y, d in fy.items():
    d["gp"] = d["rev"] - d["cor"]
    d["opex"] = d["rnd"] + d["snm"] + d["gna"] + d["term"] + d["amort"]
    d["ebit"] = d["gp"] - d["opex"]
    d["gm"] = d["gp"] / d["rev"]
    d["om"] = d["ebit"] / d["rev"]

say("=== 1. FY income statement, margins (computed from FY25_FS p.74-96) ===")
for y in (2023, 2024, 2025):
    d = fy[y]
    say(f"FY{y}: rev ${d['rev']}M  GP ${d['gp']}M ({pct(d['gm'])})  "
        f"EBIT ${d['ebit']}M ({pct(d['om'])})")
say(f"FY25 EBIT ex-Figma-termination-fee comparison: FY24 EBIT ex-fee = "
    f"${fy[2024]['ebit'] + 1000}M, margin {pct((fy[2024]['ebit']+1000)/fy[2024]['rev'])}")
say(f"FY25 vs FY24 gross margin change: {pp(fy[2025]['gm'] - fy[2024]['gm'])}")
say(f"FY25 vs FY24 op margin change (as reported): {pp(fy[2025]['om'] - fy[2024]['om'])}")
say(f"FY25 vs FY24 op margin change (FY24 ex-fee):  "
    f"{pp(fy[2025]['om'] - (fy[2024]['ebit']+1000)/fy[2024]['rev'])}")
say()


# ---------------------------------------------------------------------------
# 2. Q2 FY2026 and 1H FY2026 (Q226_MDA revenue / cost of revenue / opex tables)
# ---------------------------------------------------------------------------
q = {
    "Q2FY25": dict(rev=5873, cor=638, rnd=1082, snm=1626, gna=377, amort=41),
    "Q2FY26": dict(rev=6618, cor=715, rnd=1198, snm=1884, gna=546, amort=37),
    "1HFY25": dict(rev=11587, cor=1260, rnd=2108, snm=3121, gna=744, amort=82),
    "1HFY26": dict(rev=13016, cor=1379, rnd=2308, snm=3592, gna=1009, amort=72),
}
for k, d in q.items():
    d["gp"] = d["rev"] - d["cor"]
    d["opex"] = d["rnd"] + d["snm"] + d["gna"] + d["amort"]
    d["ebit"] = d["gp"] - d["opex"]
    d["gm"] = d["gp"] / d["rev"]
    d["om"] = d["ebit"] / d["rev"]

say("=== 2. Q2/1H FY2026 vs FY2025 (computed from Q226_MDA) ===")
for k in ("Q2FY25", "Q2FY26", "1HFY25", "1HFY26"):
    d = q[k]
    say(f"{k}: rev ${d['rev']}M  GP ${d['gp']}M ({pct(d['gm'])})  "
        f"EBIT ${d['ebit']}M ({pct(d['om'])})")
say(f"Q2 gross margin YoY change: {pp(q['Q2FY26']['gm'] - q['Q2FY25']['gm'])}")
say(f"Q2 operating margin YoY change: {pp(q['Q2FY26']['om'] - q['Q2FY25']['om'])}")
say(f"1H operating margin YoY change: {pp(q['1HFY26']['om'] - q['1HFY25']['om'])}")
say(f"FY25 full-year op margin {pct(fy[2025]['om'])} vs 1HFY26 {pct(q['1HFY26']['om'])}: "
    f"{pp(q['1HFY26']['om'] - fy[2025]['om'])}")
say()


# ---------------------------------------------------------------------------
# 3. Operating-margin bridge Q2FY26 vs Q2FY25 — which cost line did the damage?
#    (each opex/COGS line as % of revenue, change in pp)
# ---------------------------------------------------------------------------
say("=== 3. Q2FY26 vs Q2FY25 operating margin bridge, by line (% of revenue) ===")
tot = 0.0
for line in ("cor", "rnd", "snm", "gna", "amort"):
    d26 = q["Q2FY26"][line] / q["Q2FY26"]["rev"]
    d25 = q["Q2FY25"][line] / q["Q2FY25"]["rev"]
    say(f"  {line:6s}: {pct(d25)} -> {pct(d26)}   margin impact {pp(-(d26 - d25))}")
    tot += -(d26 - d25)
say(f"  sum of line impacts = {pp(tot)} (ties to op margin change above)")
say()


# ---------------------------------------------------------------------------
# 4. G&A decomposition. Q226_MDA gives components of the +45% QTD / +36% YTD
#    change in G&A as percentage-points of the prior-year base.
# ---------------------------------------------------------------------------
say("=== 4. G&A increase decomposition (Q226_MDA components-of-change table) ===")
gna_base_q = q["Q2FY25"]["gna"]
gna_base_h = q["1HFY25"]["gna"]
comp_q = {"Impairment of goodwill": 19, "Loss contingency": 8, "Compensation": 9,
          "Software licenses": 6, "Other": 3}
comp_h = {"Impairment of goodwill": 10, "Loss contingency": 12, "Compensation": 7,
          "Software licenses": 5, "Other": 2}
say(f"Q2 G&A base ${gna_base_q}M; total +45% = +${q['Q2FY26']['gna']-gna_base_q}M actual")
for k, v in comp_q.items():
    say(f"  {k:24s}: {v}pp of base = ~${gna_base_q*v/100:.0f}M")
say(f"1H G&A base ${gna_base_h}M; total +36% = +${q['1HFY26']['gna']-gna_base_h}M actual")
for k, v in comp_h.items():
    say(f"  {k:24s}: {v}pp of base = ~${gna_base_h*v/100:.0f}M")
say("Cross-check vs Q226_FS segment table: goodwill impairment $70M (Q2 and 1H),")
say("loss contingency $30M (Q2) / $92M (1H) -> implied ~$71M and ~$89M above. Close.")
say()


# ---------------------------------------------------------------------------
# 5. Cost of SUBSCRIPTION revenue: the hosting/AI-inference driver.
#    Q226_MDA + FY25_MDA give components-of-change in pp of prior-year base.
# ---------------------------------------------------------------------------
say("=== 5. Cost of subscription revenue: hosting/data-center/AI-inference ===")
cos = {
    "FY2024": 1799, "FY2025": 2027,
    "Q2FY25": 505, "Q2FY26": 586,
    "1HFY25": 995, "1HFY26": 1126,
}
sub_rev = {
    "FY2024": 20521, "FY2025": 22904,
    "Q2FY25": 5641, "Q2FY26": 6416,
    "1HFY25": 11124, "1HFY26": 12614,
}
for k in cos:
    say(f"  {k}: cost of subs ${cos[k]}M on subs rev ${sub_rev[k]}M "
        f"= {pct(cos[k]/sub_rev[k])} of subscription revenue")
say(f"  Subscription gross margin FY2024 {pct(1-cos['FY2024']/sub_rev['FY2024'])} -> "
    f"FY2025 {pct(1-cos['FY2025']/sub_rev['FY2025'])} -> "
    f"Q2FY26 {pct(1-cos['Q2FY26']/sub_rev['Q2FY26'])}")
say()
say("  Hosting/data-center/AI-inference dollar contribution (pp of prior-year base):")
say(f"    FY2025: 8pp of ${cos['FY2024']}M = ~${cos['FY2024']*0.08:.0f}M of the "
    f"${cos['FY2025']-cos['FY2024']}M total increase "
    f"({0.08*cos['FY2024']/(cos['FY2025']-cos['FY2024'])*100:.0f}% of it)")
say(f"    Q2FY26: 16pp of ${cos['Q2FY25']}M = ~${cos['Q2FY25']*0.16:.0f}M of the "
    f"${cos['Q2FY26']-cos['Q2FY25']}M total increase "
    f"({0.16*cos['Q2FY25']/(cos['Q2FY26']-cos['Q2FY25'])*100:.0f}% of it)")
say(f"    1HFY26: 15pp of ${cos['1HFY25']}M = ~${cos['1HFY25']*0.15:.0f}M of the "
    f"${cos['1HFY26']-cos['1HFY25']}M total increase "
    f"({0.15*cos['1HFY25']/(cos['1HFY26']-cos['1HFY25'])*100:.0f}% of it)")
say("  Implied hosting cost growth rate acceleration: FY2025 hosting grew ~8% of the")
say("  prior COS base in a year; Q2FY26 alone grew 16% of the prior COS base in a quarter's")
say("  YoY comparison -> hosting is compounding roughly 2x faster than in FY2025.")
say()


# ---------------------------------------------------------------------------
# 6. ARR -> revenue linkage, and the organic vs Semrush decomposition
#    FY25_MDA: Total Adobe ARR $25.20B exiting FY25 (+11.5%); revalued to $25.66B
#              at FY26 opening FX.
#    Q226_MDA: Total Adobe ARR $27.10B at 5/29/26 (+12.5% vs $24.08B revalued),
#              "including approximately $480 million from the Semrush acquisition".
# ---------------------------------------------------------------------------
say("=== 6. ARR growth: reported vs organic (ex-Semrush) ===")
arr_open26 = 25.66      # $B, FY25-end revalued at FY26 rates (FY25_MDA)
arr_q226 = 27.10        # $B (Q226_MDA)
semrush = 0.48          # $B (Q226_MDA)
arr_q225_reval = 24.08  # $B (Q226_MDA)
say(f"  Reported YoY ARR growth: {pct(arr_q226/arr_q225_reval - 1)} (filing says 12.5%)")
say(f"  Organic YoY ARR growth ex-Semrush: "
    f"{pct((arr_q226-semrush)/arr_q225_reval - 1)}")
say("  Sequence of REPORTED YoY total-Adobe ARR growth (all sources: Q425_CALL,")
say("  Q126_CALL line 344, Q226_MDA):")
say("     FY2025 exit 11.5%  ->  Q1FY26 10.9% ($26.06B)  ->  Q2FY26 12.5% ($27.10B)")
say(f"  Q2FY26 ORGANIC (ex-Semrush) YoY: {pct((arr_q226-semrush)/arr_q225_reval - 1)}")
say("  -> organic YoY ARR growth path is 11.5% -> 10.9% -> ~10.5%. A gentle grind")
say("     down of ~90bps over two quarters, NOT a collapse.")
say()
say("  NOTE / CORRECTION to work_products/overview.md: that document computed a")
say("  '~3.7% organic H1 ARR growth' and compared it to double-digit annual growth.")
say("  That is a half-year SEQUENTIAL number set against a YoY rate - not comparable.")
say(f"  The sequential figures are: 1H net-new ARR ${arr_q226-arr_open26:.2f}B "
    f"({pct(arr_q226/arr_open26 - 1)} of the $25.66B opening base),")
say(f"  organic ${arr_q226-semrush-arr_open26:.2f}B "
    f"({pct((arr_q226-semrush)/arr_open26 - 1)}). Adobe's net-new ARR is heavily")
say("  H2-weighted (Narayen, Q226_CALL: H2 'typically pay out 40% and 60% in Q3 and")
say("  Q4'), so annualising a 1H sequential rate understates the run-rate. The")
say("  YoY organic figure of ~10.5% is the correct like-for-like comparison.")
say()

# --- 6b. The FY2026 ARR guidance: same headline, different composition --------
say("=== 6b. The FY2026 ARR guide: 10.2% held, but organic content was cut ===")
say("  Q425_CALL (Durn): FY2026 target 'total Adobe ending ARR book of business")
say("  growth of 10.2% year-over-year' AND explicitly 'Our targets do not include")
say("  any contribution from Semrush.'  -> 10.2% was an ORGANIC target.")
say("  Q226_CALL (Day): 10.2% reaffirmed, but 'now reflects both the addition of the")
say("  Semrush book of business, as well as the strategic choice to accelerate MAU")
say("  freemium growth and defer previously planned Creative Cloud line optimizations.'")
tgt_netnew = arr_open26 * 0.102
say(f"  Implied total FY2026 net-new ARR at 10.2%: ${tgt_netnew:.2f}B "
    f"(Durn said 'approximately $2.6 billion' - ties)")
say(f"  Less Semrush ${semrush:.2f}B  ->  implied ORGANIC net-new ARR "
    f"${tgt_netnew-semrush:.2f}B")
say(f"  Implied organic FY2026 ARR growth: {pct((tgt_netnew-semrush)/arr_open26)}")
say(f"  => the organic guide was cut by ~${semrush*1000:.0f}M, or "
    f"~{(semrush/arr_open26)*100:.1f}pp, while the headline stayed at 10.2%.")
say("  CROSS-CHECK (two independent methods agreeing): Alex Zukin of Wolfe Research")
say("  put the organic ARR reduction at 'about $0.5 billion' on the Q2 call")
say("  (Q226_CALL line 514) - his number and the Semrush-substitution arithmetic")
say(f"  above (${semrush*1000:.0f}M) agree to within ~4%. Narayen did not dispute the")
say("  figure. NOTE: the ~$500M is analyst arithmetic, NOT a company disclosure.")
say("  Narayen attributed it roughly 50/50: 'maybe half of the impact of ARR is as a")
say("  result of what we are doing around deferring that Creative price line")
say("  optimizations, and the other half is about going full steam on what it takes")
say("  to deliver the freemium experience' (Q226_CALL line 410).")
say(f"  So: deferred pricing ~${semrush*500:.0f}M and freemium traffic diversion")
say(f"  ~${semrush*500:.0f}M of FY2026 ARR.")
say()

# --- 6c. Volume vs price decomposition, the only one management gave ---------
say("=== 6c. Volume vs price split of net-new ARR (Q425_CALL line 302) ===")
say("  'Over 75% of Digital Media net new ARR was driven by continued growth in")
say("  subscriptions and cross-sell and upsell, with the remainder from value-based")
say("  pricing' (Durn, Q4 FY2025).")
say(f"  FY2025 Digital Media net-new ARR = 19.20 - 17.22 = ${19.20-17.22:.2f}B "
    f"(FY25_MDA revalued base)")
say(f"    -> >75% volume/mix = >${(19.20-17.22)*0.75:.2f}B; "
    f"<25% price = <${(19.20-17.22)*0.25:.2f}B")
say("  This is the single most important structural fact about Adobe's revenue:")
say("  roughly THREE QUARTERS of growth is unit/seat/cross-sell volume, only about")
say("  a quarter is price. The FY2026 pivot deliberately trades the price quarter")
say("  for more of the volume three-quarters.")
say()

# --- 6d. Adobe Stock: an observable AI-substitution data point ---------------
say("=== 6d. Adobe Stock decline (Q126_CALL line 584) ===")
say("  Narayen: Stock is 'about a $450 million book of business... if you take out")
say("  the Stock business, like-for-like, instead of the 10.9% growth, it would have")
say("  been approximately 11.2% growth.'")
say("  CORRECT derivation (weighted-average identity on the SAME-PERIOD base).")
say("  Q126_CALL line 344 gives Q1FY26 total ARR $26.06B '+10.9% year-over-year',")
T2 = 26.06
T1 = T2 / 1.109
say(f"  so the correct prior-year base is Q1FY25 ARR = 26.06/1.109 = ${T1:.2f}B")
say("  (NOT the $25.66B FY2026-opening base -- that is a different period).")
say("  Solve (T2 - S2)/(T1 - S1) = 1.112 for the Stock book S:")
S2a = 0.45; S1a = T1 - (T2 - S2a)/1.112
S1b = 0.45; S2b = T2 - 1.112*(T1 - S1b)
say(f"    Reading A ($450M = current-year Stock ARR): S1 = ${S1a:.3f}B "
    f"-> Stock YoY {(S2a/S1a-1)*100:+.1f}%")
say(f"    Reading B ($450M = prior-year Stock ARR):   S2 = ${S2b:.3f}B "
    f"-> Stock YoY {(S2b/S1b-1)*100:+.1f}%")
say("  => Stock ARR is declining roughly 4-5% YoY. Management does not say which")
say("     reading is intended, so this is a range, not a point estimate.")
say(f"  Stock is ~{0.45/T2*100:.1f}% of the Q1FY26 $26.06B ARR base; its drag on total")
say("  ARR growth is ~0.3pp (11.2% ex-Stock vs 10.9% reported), as disclosed.")
say("  SUPERSEDED: an earlier version of this script divided the ~$77M drag by")
say("  Stock's own $450M book to get '-17%'. That conflates 'drag as a share of")
say("  Stock's book' with 'Stock's growth rate' and used the wrong-period base.")
say("  The verifier caught this; -17% was wrong by a factor of ~3-4x.")
say()


# ---------------------------------------------------------------------------
# 7. FX contribution to reported revenue growth (Q226_MDA / FY25_MDA FX paragraphs)
# ---------------------------------------------------------------------------
say("=== 7. FX contribution to revenue growth ===")
fx_q2_gross, fx_q2_hedge = 116, -22     # $M, Q226_MDA
fx_1h_gross, fx_1h_hedge = 240, -71     # $M, Q226_MDA
d_rev_q2 = q["Q2FY26"]["rev"] - q["Q2FY25"]["rev"]
d_rev_1h = q["1HFY26"]["rev"] - q["1HFY25"]["rev"]
say(f"  Q2FY26: reported rev growth ${d_rev_q2}M ({pct(d_rev_q2/q['Q2FY25']['rev'])}); "
    f"FX net = ${fx_q2_gross+fx_q2_hedge}M = "
    f"{(fx_q2_gross+fx_q2_hedge)/d_rev_q2*100:.0f}% of the growth")
say(f"          ex-FX (net of hedge) growth = "
    f"{pct((d_rev_q2-(fx_q2_gross+fx_q2_hedge))/q['Q2FY25']['rev'])}")
say(f"          ex-FX (gross translation only) = "
    f"{pct((d_rev_q2-fx_q2_gross)/q['Q2FY25']['rev'])} "
    f"(management reported 11% constant currency)")
say(f"  1HFY26: reported rev growth ${d_rev_1h}M ({pct(d_rev_1h/q['1HFY25']['rev'])}); "
    f"FX net = ${fx_1h_gross+fx_1h_hedge}M = "
    f"{(fx_1h_gross+fx_1h_hedge)/d_rev_1h*100:.0f}% of the growth")
say(f"  FY2025 for contrast: FX gross -$18M, hedge gain +$22M, net +$4M on "
    f"${fy[2025]['rev']-fy[2024]['rev']}M of growth = ~0%")
say("  -> FX flipped from a non-factor in FY2025 to ~13% of Q2FY26 revenue growth.")
say()


# ---------------------------------------------------------------------------
# 8. Deferred revenue / RPO — the forward-visibility gauge
# ---------------------------------------------------------------------------
say("=== 8. Deferred revenue and RPO ===")
say("  Deferred revenue: $6.26B (11/29/24) -> $7.03B (11/28/25) -> $7.25B (5/29/26)"
    "   [FY25_FS, Q226_FS]")
say(f"    FY2025 YoY growth {pct(7.03/6.26-1)}; 1HFY26 SEQUENTIAL growth {pct(7.25/7.03-1)}")
say("  RPO: $19.96B (FY24) -> $22.52B (FY25, +13%) -> $22.27B (5/29/26, +13% YoY)"
    "   [FY25_MDA, Q226_MDA]")
say(f"    Note RPO fell ${22.52-22.27:.2f}B sequentially from FY25-end to Q2FY26 even")
say("    though the YoY comparison is +13%; RPO is lumpy on enterprise renewal timing.")
say("  Share of RPO expected to convert within 12 months: 65% (FY25) -> 67% (Q2FY26)")
say("    -> mild shortening of the contracted backlog duration.")
say()


# ---------------------------------------------------------------------------
# 9. Owners' earnings, rough. Simple method, deliberately.
#    CFO - maintenance capex, then SBC treated explicitly as a real cost.
# ---------------------------------------------------------------------------
say("=== 9. Owners' earnings (rough) ===")
cfo25, capex25, sbc25 = 10031, 179, 1942            # FY25_FS cash flow / SBC note
cfo1h26, capex1h26, sbc1h26 = 5123, 95, 1045        # Q226_FS
buyback25, buyback1h26 = 11280, 4590                # FY25_MDA, Q226_MDA
say(f"  FY2025: CFO ${cfo25}M - capex ${capex25}M = FCF ${cfo25-capex25}M "
    f"({pct((cfo25-capex25)/fy[2025]['rev'])} of revenue)")
say(f"          less SBC ${sbc25}M -> SBC-adjusted owners' earnings ~${cfo25-capex25-sbc25}M "
    f"({pct((cfo25-capex25-sbc25)/fy[2025]['rev'])} of revenue)")
say(f"  1HFY26: CFO ${cfo1h26}M - capex ${capex1h26}M = FCF ${cfo1h26-capex1h26}M "
    f"({pct((cfo1h26-capex1h26)/q['1HFY26']['rev'])} of revenue)")
say(f"          less SBC ${sbc1h26}M -> ~${cfo1h26-capex1h26-sbc1h26}M "
    f"({pct((cfo1h26-capex1h26-sbc1h26)/q['1HFY26']['rev'])} of revenue)")
say(f"  SBC as % of revenue: FY2025 {pct(sbc25/fy[2025]['rev'])}, "
    f"1HFY26 {pct(sbc1h26/q['1HFY26']['rev'])}")
say(f"  Buybacks vs SBC-adjusted OE: FY2025 ${buyback25}M vs ${cfo25-capex25-sbc25}M "
    f"= {buyback25/(cfo25-capex25-sbc25):.2f}x")
say(f"                               1HFY26 ${buyback1h26}M vs ${cfo1h26-capex1h26-sbc1h26}M "
    f"= {buyback1h26/(cfo1h26-capex1h26-sbc1h26):.2f}x")
say("  -> buybacks have been run at 1.1-1.4x SBC-adjusted owners' earnings, i.e. ABOVE")
say("     what the business generates, funded by drawing down cash ($7.61B -> $4.92B")
say("     of cash+equivalents between 11/29/24 and 5/29/26) and, in 1HFY26, by $494M")
say("     of commercial paper. This is a real constraint on the buyback pace.")
say()
say(f"  Capex intensity: FY2025 {pct(capex25/fy[2025]['rev'])} of revenue; "
    f"1HFY26 {pct(capex1h26/q['1HFY26']['rev'])}. Adobe RENTS its AI compute:")
say("  FY25_MDA discloses $6.82B of non-cancellable purchase obligations 'primarily")
say("  relating to contracts with vendors for third-party hosting and data center")
say(f"  services' -- {6820/(cfo25-capex25):.1f}x FY2025 free cash flow, and ~{6820/2027:.1f}x")
say("  FY2025 cost of subscription revenue. Compute cost sits in COGS/opex, not capex.")
say()


# ---------------------------------------------------------------------------
# 10. Tax rate effect on owners' earnings
# ---------------------------------------------------------------------------
say("=== 10. Tax ===")
say("  Effective tax rate: FY2023 20%, FY2024 20%, FY2025 18%, "
    "Q2FY26 24%, 1HFY26 23%   [FY25_MDA, Q226_MDA]")
pbt_1h26 = 4660  # Q226_FS segment table
say(f"  1HFY26 income before taxes ${pbt_1h26}M. Holding the 1HFY25 18% rate would give")
say(f"  tax of ${pbt_1h26*0.18:.0f}M vs actual $1059M -> ~${1059-pbt_1h26*0.18:.0f}M of")
say(f"  incremental tax, i.e. ~{(1059-pbt_1h26*0.18)/3601*100:.0f}% of 1HFY26 net income")
say("  of $3,601M. This is why net income was ~flat YoY despite EBIT growth.")
say(f"  Cross-check: 1HFY26 net income $3,601M vs 1HFY25 $3,502M = "
    f"{pct(3601/3502-1)} growth, while EBIT grew "
    f"{pct(q['1HFY26']['ebit']/q['1HFY25']['ebit']-1)}.")
say()


# ---------------------------------------------------------------------------
# 11. Share count / per-share leverage
# ---------------------------------------------------------------------------
say("=== 11. Share count ===")
sh_jan26, sh_jun26 = 410.5, 397.5   # cover pages, FY2025 10-K and 2Q2026 10-Q
say(f"  Shares outstanding {sh_jan26}M (Jan 2026 cover) -> {sh_jun26}M (Jun 2026 cover) = "
    f"{pct(sh_jun26/sh_jan26-1)} in ~5 months")
say(f"  Annualised pace: {pct((sh_jun26/sh_jan26)**(12/5)-1)}")
say("  Q425_CALL (Durn): FY2025 buybacks 'reducing our shares outstanding by over 6%'.")
say("  -> per-share owners' earnings have been growing ~6-7pp/yr faster than aggregate")
say("     owners' earnings. This is a first-order driver of per-share OE and is the")
say("     most cash-hungry, and therefore most reversible, of the four stages.")
say()


# ---------------------------------------------------------------------------
# 12. Revenue per employee (unit economics sanity check)
# ---------------------------------------------------------------------------
say("=== 12. Revenue per employee ===")
emp25 = 31360   # FY25_BUS, as of 11/28/25
say(f"  FY2025: ${fy[2025]['rev']}M / {emp25} employees = "
    f"${fy[2025]['rev']*1e6/emp25:,.0f} per employee")
say(f"  1HFY26 annualised: ${q['1HFY26']['rev']*2}M / {emp25} (headcount not restated) = "
    f"${q['1HFY26']['rev']*2*1e6/emp25:,.0f} per employee")
say()


# ---------------------------------------------------------------------------
# 13. Customer-group revenue growth (the real volume/price split we can observe)
# ---------------------------------------------------------------------------
say("=== 13. Customer group subscription revenue ===")
cg = {
    "Creative & Marketing Pro": dict(fy24=14749, fy25=16303, q225=4019, q226=4537),
    "Business Pro & Consumer":  dict(fy24=5662,  fy25=6495,  q225=1595, q226=1853),
}
for k, d in cg.items():
    say(f"  {k}: FY24->FY25 {pct(d['fy25']/d['fy24']-1)}; "
        f"Q2FY25->Q2FY26 {pct(d['q226']/d['q225']-1)}")
say(f"  Mix: BP&C was {pct(cg['Business Pro & Consumer']['fy25']/(cg['Business Pro & Consumer']['fy25']+cg['Creative & Marketing Pro']['fy25']))} "
    f"of customer-group subs revenue in FY2025, "
    f"{pct(cg['Business Pro & Consumer']['q226']/(cg['Business Pro & Consumer']['q226']+cg['Creative & Marketing Pro']['q226']))} in Q2FY26")
say("  -> the faster-growing group is the LOWER-priced one (Acrobat/Express), so revenue")
say("     mix is drifting toward lower ARPU per user even as total revenue accelerates.")
say()


print("\n".join(out))


# ---------------------------------------------------------------------------
# 14. Why total gross margin held flat despite hosting cost acceleration:
#     decompose Q2FY26 vs Q2FY25 total gross margin into (a) subscription
#     margin change and (b) revenue mix shift across the three revenue lines.
# ---------------------------------------------------------------------------
say("=== 14. Gross margin bridge: subscription margin vs revenue mix ===")
lines = ["Subscription", "Product", "Services and other"]
rev25 = {"Subscription": 5641, "Product": 88, "Services and other": 144}
cst25 = {"Subscription": 505,  "Product": 6,  "Services and other": 127}
rev26 = {"Subscription": 6416, "Product": 89, "Services and other": 113}
cst26 = {"Subscription": 586,  "Product": 5,  "Services and other": 124}
R25, R26 = sum(rev25.values()), sum(rev26.values())
gm25 = {k: 1 - cst25[k]/rev25[k] for k in lines}
gm26 = {k: 1 - cst26[k]/rev26[k] for k in lines}
w25 = {k: rev25[k]/R25 for k in lines}
w26 = {k: rev26[k]/R26 for k in lines}
tot25 = sum(w25[k]*gm25[k] for k in lines)
tot26 = sum(w26[k]*gm26[k] for k in lines)
for k in lines:
    say(f"  {k:20s}: GM {pct(gm25[k])} -> {pct(gm26[k])} ; "
        f"mix {pct(w25[k])} -> {pct(w26[k])}")
say(f"  Total GM {pct(tot25)} -> {pct(tot26)} = {pp(tot26-tot25)}")
rate_eff = sum(w25[k]*(gm26[k]-gm25[k]) for k in lines)
mix_eff = sum((w26[k]-w25[k])*gm26[k] for k in lines)
say(f"  RATE effect (margins changing, weights held at FY25): {pp(rate_eff)}")
say(f"     -- of which subscription alone: "
    f"{pp(w25['Subscription']*(gm26['Subscription']-gm25['Subscription']))}")
say(f"  MIX  effect (weights changing):                       {pp(mix_eff)}")
say(f"     -- of which services/other shrinking 2.5%->1.7% of revenue: "
    f"{pp((w26['Services and other']-w25['Services and other'])*gm26['Services and other'] + (w26['Subscription']-w25['Subscription'])*gm26['Subscription'])}")
say(f"  rate + mix = {pp(rate_eff+mix_eff)} (ties to total)")
say("  CONCLUSION: total gross margin was flat (+0.06pp) as the NET of two much")
say("  larger offsetting forces:")
say("    - RATE -0.68pp, of which only -0.17pp is subscription (hosting/AI")
say("      inference). The larger -0.51pp comes from the services line's own")
say("      margin collapsing from +11.8% to -9.7% (revenue $144M->$113M against")
say("      an only slightly lower cost base of $127M->$124M).")
say("    - MIX +0.74pp, driven by the loss-making services line shrinking from")
say("      2.5% to 1.7% of revenue while the ~91%-margin subscription line grew")
say("      from 96.0% to 96.9%.")
say("  So the AI/hosting drag on TOTAL gross margin in Q2FY26 is only ~17bp -- an")
say("  order of magnitude smaller than the market narrative implies. But note the")
say("  mix lever is finite and one-way: services is already down to 1.7% of")
say("  revenue, so there is little left to harvest if subscription margin erodes.")
say()

PRINT_TAIL = (out.index("=== 14. Gross margin bridge: subscription margin vs revenue mix ==="))


# ---------------------------------------------------------------------------
# 15. Third-party compute/model VENDOR REPRICING sensitivity (Factor 2.2/4.3).
#     Adobe rents all of its AI compute. It does NOT disclose the hosting share
#     of cost of subscription revenue, so this is a BAND under an assumption,
#     not a computed fact. FY25_MDA says cost of subscription revenue "consists
#     primarily of third-party hosting services and data center costs" -- that
#     supports >50% but gives no number. 50-70% is my INFERENCE.
# ---------------------------------------------------------------------------
say("=== 15. Vendor repricing sensitivity on third-party compute ===")
cos_sub25 = cos["FY2025"]          # $2,027M, FY25_MDA
say(f"  FY2025 cost of subscription revenue ${cos_sub25}M; FY2025 revenue "
    f"${fy[2025]['rev']}M; FY2025 EBIT ${fy[2025]['ebit']}M")
say("  Hosting share of that line: NOT DISCLOSED. Band of 50-70% is inference.")
for share in (0.50, 0.70):
    base = cos_sub25 * share
    say(f"  -- hosting assumed {share:.0%} of the line = ~${base:,.0f}M --")
    for shock in (0.25, 0.50, 1.00):
        d = base * shock
        say(f"     +{shock:.0%} vendor price: +${d:,.0f}M = {d/fy[2025]['rev']*100:.2f}pp "
            f"of revenue = {d/fy[2025]['ebit']*100:.1f}% of FY2025 EBIT")
say(f"  Pre-committed spend: $6,820M of non-cancellable purchase obligations "
    f"(FY25_MDA) = {6820/cos_sub25:.1f}x FY2025 cost of subscription revenue,")
say("  i.e. roughly three years of compute already contracted. That DAMPENS")
say("  near-term repricing risk but removes the option to walk away.")
say("  Offsetting considerations (mixed evidential quality):")
say("    (a) SOURCED - counterparty leverage. Narayen, Q226_CALL: 'we are huge")
say("        users of their cloud services, which at the end of the day is a")
say("        significant revenue stream for them.'")
say("    (b) SOURCED - multi-sourcing. FY25_BUS: 'We partner with an extensive")
say("        ecosystem of third-party models across categories', alongside")
say("        first-party Firefly models -> substitution across vendors exists.")
say("    (c) SOURCED, POINTS THE OTHER WAY. FY25 risk_factors: if Adobe is")
say("        'unable to renew our agreements with them on favorable terms or at")
say("        all, our expenses could significantly increase.'")
say("    (d) UNSOURCED / internal AI model knowledge, flagged as the weakest")
say("        leg: unit inference costs have been falling industry-wide.")
say("  CONCLUSION: a doubling of compute prices costs ~12-16% of FY2025 EBIT.")
say("  Material, but bounded and one-time, versus the free-user VOLUME channel")
say("  which is unbounded. Both belong in the same uncertainty bullet.")
say()

print("\n".join(out[PRINT_TAIL:]))
