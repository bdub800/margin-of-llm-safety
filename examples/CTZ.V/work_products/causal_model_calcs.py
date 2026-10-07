"""
NamSys Inc. (TSXV: CTZ) -- calculations supporting work_products/causal_model.md

Every input below is tagged with the filing it came from. No figure is invented.

Sources (short tags used in comments):
  FS23  = primary_sources/FY2023/Namsys_-_Annual_FS_-_Feb262024.md
  MDA25 = primary_sources/FY2025/NamSys_MDA_022426.md
  FS25  = primary_sources/FY2025/NamSys_AFS_022426.md
  FS24  = primary_sources/FY2024/NamSys_AFS_021925.md
  FSQ2  = primary_sources/2Q2026/FS_Q2_NamSys_Apr_30_26_FINAL.md
  MDQ2  = primary_sources/2Q2026/MDA_Q2_NamSys_Apr_30_26_FINAL.md
  AM25  = fetched_docs/namsys_2025_annual_meeting_transcript.md
  AM26  = fetched_docs/namsys_2026_annual_meeting_transcript.md
"""

def pct(x):
    return f"{100*x:,.1f}%"


def money(x):
    return f"${x:,.0f}"


line = "-" * 78

# =============================================================================
# 1. INPUTS
# =============================================================================

# Revenue, total and split recurring / professional services
# FY2023, FY2024, FY2025: MDA25 "Revenue" tables + FS23 Note 7
# H1 FY2025 / H1 FY2026: MDQ2 six-month revenue table, FSQ2 Note 7
rev = {
    "FY2022": 5_394_781,   # FS23 statements of operations
    "FY2023": 6_093_020,   # MDA25 selected annual information
    "FY2024": 6_840_146,   # MDA25 selected annual information
    "FY2025": 7_891_605,   # MDA25 selected annual information
    "H1FY25": 3_951_863,   # MDQ2 six-month revenue table
    "H1FY26": 4_267_406,   # MDQ2 six-month revenue table
}
recurring = {
    "FY2024": 6_716_298,   # MDA25
    "FY2025": 7_811_909,   # MDA25
    "H1FY25": 3_929_927,   # MDQ2
    "H1FY26": 4_170_949,   # MDQ2
}
profsvcs = {
    "FY2024": 123_848,     # MDA25
    "FY2025": 79_696,      # MDA25
    "H1FY25": 21_936,      # MDQ2
    "H1FY26": 96_457,      # MDQ2
}

# Operating income (MDA25 selected annual info; MDQ2 quarterly table for H1)
op_inc = {
    "FY2022": 1_753_157,   # FS23
    "FY2023": 2_107_434,
    "FY2024": 2_572_018,
    "FY2025": 3_146_476,
}

# H1 operating income built from the MD&A expense lines (MDQ2 six-month sections)
h1 = {
    "H1FY25": dict(rev=3_951_863, cogs=1_364_558, gp=2_587_305,
                   selling=335_511, ga=574_253, dep=3_449, baddebt=50_746),
    "H1FY26": dict(rev=4_267_406, cogs=1_596_137, gp=2_671_269,
                   selling=309_302, ga=582_407, dep=3_623, baddebt=0),
}
for k, v in h1.items():
    v["op_inc"] = v["gp"] - v["selling"] - v["ga"] - v["dep"] - v["baddebt"]
    v["op_inc_exbd"] = v["op_inc"] + v["baddebt"]

# Geography (FS23 Note 7, FS25 Note 7, FSQ2 Note 7)
geo = {
    "FY2023": dict(US=4_815_496, Mexico=481_734, Canada=215_646,
                   DR=227_420, PR=264_191, Other=88_533),
    "FY2024": dict(US=5_281_952, Mexico=609_304, Canada=243_212,
                   DR=250_987, PR=258_115, Other=196_576),
    "FY2025": dict(US=5_979_328, Mexico=846_155, Canada=286_682,
                   DR=275_378, PR=262_573, Other=241_489),
    "H1FY25": dict(US=3_030_898, Mexico=381_617, Canada=151_395,
                   DR=135_687, PR=131_063, Other=121_203),
    "H1FY26": dict(US=3_137_260, Mexico=558_412, Canada=158_734,
                   DR=140_981, PR=133_714, Other=138_305),
}

# Employee compensation expense by function (Note 14 in each AFS / interim FS)
comp = {
    "FY2023": dict(cogs=1_686_897, selling=211_665, ga=518_151),   # FS24 Note 14
    "FY2024": dict(cogs=1_690_129, selling=259_294, ga=557_450),   # FS25/FS24 Note 14
    "FY2025": dict(cogs=1_739_266, selling=486_478, ga=555_762),   # FS25 Note 14
    "H1FY25": dict(cogs=844_523, selling=241_308, ga=275_568),     # FSQ2 Note 14
    "H1FY26": dict(cogs=1_016_795, selling=243_906, ga=278_705),   # FSQ2 Note 14
}

# Headcount: AM25 "stable at 17 employees right now" (Apr 2025, i.e. FY2024 base);
#            AM26 "we are up to 21 employees today" (Apr 2026)
heads = {"FY2024": 17, "FY2025": 17, "H1FY26": 21}

# Customer concentration, by REVENUE RANK SLOT (not verified same customer)
# FS25 Note 7 and FSQ2 Note 7
conc = {
    "FY2024": (0.200, 0.089, 0.089),
    "FY2025": (0.159, 0.123, 0.107),
    "H1FY25": (0.175, 0.125, 0.097),
    "H1FY26": (0.131, 0.128, 0.114),
}

# Balance-sheet / cash items
cash_apr26 = 940_082          # FSQ2 SOFP
sti_apr26 = 6_425_965         # FSQ2 SOFP
gic_rate_lo, gic_rate_hi = 0.020, 0.0245   # FSQ2 Note 15 / MDQ2
tax_rate = 0.265              # MDA25 "The basic rate of 26.50% was applied"
usd_share = 0.96              # FSQ2 Note 11: "approximately 96% ... denominated in U.S. dollars"

# Trade receivables ONLY (ex sales-tax receivable), FS25 Note 3 / FSQ2 Note 3
ar = {"FY2024": 857_096, "FY2025": 1_164_580, "H1FY26": 1_330_766}
ar_90 = {"FY2024": 16_861, "FY2025": 126_998, "H1FY26": 237_066}     # FS25 / FSQ2 Note 3
defrev = {"FY2023": 287_783, "FY2024": 440_985, "FY2025": 301_975,
          "H1FY26": 707_554}                                          # FS25 / FSQ2
rev_ttm_apr26 = rev["FY2025"] + rev["H1FY26"] - rev["H1FY25"]

print(line)
print("1. THE OUTPUT BEING EXPLAINED: revenue growth, recurring vs total")
print(line)
for a, b in [("FY2023", "FY2024"), ("FY2024", "FY2025"), ("H1FY25", "H1FY26")]:
    g_tot = rev[b] / rev[a] - 1
    s = f"  {a} -> {b}:  total {pct(g_tot):>7}"
    if a in recurring and b in recurring:
        g_rec = recurring[b] / recurring[a] - 1
        ps_contrib = (profsvcs[b] - profsvcs[a]) / (rev[b] - rev[a])
        s += (f"   recurring {pct(g_rec):>7}"
              f"   prof-svcs share of $ growth {pct(ps_contrib):>7}")
    print(s)
print(f"\n  TTM to Apr-30-26 revenue = {money(rev_ttm_apr26)}"
      f"  (FY2025 + H1FY26 - H1FY25)")
print(f"  Recurring % of revenue: FY2024 {pct(recurring['FY2024']/rev['FY2024'])}, "
      f"FY2025 {pct(recurring['FY2025']/rev['FY2025'])}, "
      f"H1FY26 {pct(recurring['H1FY26']/rev['H1FY26'])}")

print()
print(line)
print("2. GEOGRAPHIC DECOMPOSITION OF GROWTH")
print("   (all regions except Canada are USD-billed, so REGION-vs-REGION")
print("    comparisons are FX-neutral; FSQ2 Note 11: ~96% of sales in USD)")
print(line)


def split(p):
    g = geo[p]
    us = g["US"]
    can = g["Canada"]
    intl = sum(g.values()) - us - can
    return us, can, intl


for a, b in [("FY2023", "FY2025"), ("FY2024", "FY2025"), ("H1FY25", "H1FY26")]:
    ua, ca, ia = split(a)
    ub, cb, ib = split(b)
    tot_g = rev[b] - rev[a]
    print(f"\n  {a} -> {b}   (total revenue change {money(tot_g)})")
    for name, xa, xb in [("US", ua, ub), ("Canada (CAD-billed)", ca, cb),
                         ("Intl ex-Canada", ia, ib)]:
        print(f"    {name:<22} {money(xa):>12} -> {money(xb):>12}  "
              f"growth {pct(xb/xa-1):>8}   "
              f"share of $ growth {pct((xb-xa)/tot_g):>8}")
    print(f"    Weight of US in {b} revenue: {pct(ub/rev[b])}; "
          f"Intl ex-Canada: {pct(ib/rev[b])}")

# What total growth is mechanically implied going forward at current regional rates
us_b, can_b, intl_b = split("H1FY26")
g_us = split("H1FY26")[0] / split("H1FY25")[0] - 1
g_intl = split("H1FY26")[2] / split("H1FY25")[2] - 1
w_us = us_b / rev["H1FY26"]
w_intl = intl_b / rev["H1FY26"]
w_can = can_b / rev["H1FY26"]
us_a, can_a, intl_a = split("H1FY25")
contrib_us = (us_b - us_a) / rev["H1FY25"]
contrib_can = (can_b - can_a) / rev["H1FY25"]
contrib_intl = (intl_b - intl_a) / rev["H1FY25"]
print(f"\n  Growth contribution (change / beginning total revenue):")
print(f"    US {100*contrib_us:+.2f} pts  Canada {100*contrib_can:+.2f} pts  "
      f"Intl ex-Canada {100*contrib_intl:+.2f} pts  "
      f"= {100*(contrib_us+contrib_can+contrib_intl):.2f} pts "
      f"vs reported {pct(rev['H1FY26']/rev['H1FY25']-1)}")
print("  -> If US stays at this rate, intl must keep compounding >25% just to")
print("     hold total growth near 8%; each year intl weight rises, which")
print("     mechanically RAISES total growth if intl rate holds.")
for yrs in (1, 2, 3):
    u = us_b * (1 + g_us) ** yrs
    i = intl_b * (1 + g_intl) ** yrs
    c = can_b
    prev = (us_b * (1 + g_us) ** (yrs - 1) + intl_b * (1 + g_intl) ** (yrs - 1)
            + can_b)
    print(f"     year +{yrs}: implied total growth {pct((u+i+c)/prev - 1)}, "
          f"intl weight {pct(i/(u+i+c))}")

print()
print(line)
print("3. FX TRANSMISSION")
print(line)
fx_move = 0.05
rev_eff = usd_share * fx_move
print(f"  Revenue is ~{pct(usd_share)} USD-billed (FSQ2 Note 11); MDA25 risk factors:")
print("  \"the majority of our expenses, including employee wages, have been")
print("   denominated in Canadian dollars\" and the company does not hedge.")
print(f"\n  A {pct(fx_move)} move in USD/CAD moves FY2025 revenue by "
      f"{money(rev_eff*rev['FY2025'])} ({pct(rev_eff)})")
print(f"  If the CAD cost base is unchanged, that is {money(rev_eff*rev['FY2025'])} "
      f"straight to operating income")
elasticity = usd_share * rev["FY2025"] / op_inc["FY2025"]
print(f"  = {pct(rev_eff*rev['FY2025']/op_inc['FY2025'])} of FY2025 operating income")
print(f"  Operating-income elasticity to USD/CAD = {usd_share:.2f} x "
      f"Rev/OpInc = {usd_share:.2f} x {rev['FY2025']/op_inc['FY2025']:.2f} "
      f"= {elasticity:.2f}x")
print(f"  i.e. each 1% the CAD appreciates costs roughly {elasticity:.1f}% of "
      f"operating income.")

print("\n  Scoping the FX drag in H1FY26 (INFERENCE -- sign is known, magnitude is not):")
fx_loss_h1 = 102_941          # MDQ2 six-month "Gain (loss) on foreign exchange"
usd_billed_h1 = usd_share * rev["H1FY26"]
print(f"    Reported FX loss H1FY26 = {money(fx_loss_h1)} (H1FY25: $34,680 loss)")
print(f"    USD-billed revenue H1FY26 ~= {money(usd_billed_h1)}")
print(f"    Loss / USD-billed revenue = {pct(fx_loss_h1/usd_billed_h1)} of adverse")
print("    rate drift between invoice date and collection (~30-day terms, ~59-day DSO).")
print("    A LOSS means the CAD strengthened inside the invoice-to-cash window, so")
print("    the y/y translation effect on reported CAD revenue was also adverse.")
print("    It does NOT pin the y/y average-rate effect: that is a 12-month")
print("    comparison, not a 2-month one. Treat the y/y drag as 0-5 points and do")
print("    not let any conclusion depend on the point estimate.")
print("    The US-vs-international comparison above is immune to this, because")
print("    both are billed in the same currency.")

print()
print(line)
print("3b. QUARTERLY REVENUE PATH (MDA25 + MDQ2 quarterly tables, $000s)")
print(line)
q = [("Q1-24", 1_584), ("Q2-24", 1_661), ("Q3-24", 1_741), ("Q4-24", 1_854),
     ("Q1-25", 1_942), ("Q2-25", 2_010), ("Q3-25", 1_917), ("Q4-25", 2_023),
     ("Q1-26", 2_134), ("Q2-26", 2_134)]
for i, (lbl, v) in enumerate(q):
    seq = f"{100*(v/q[i-1][1]-1):+6.1f}%" if i else "     -"
    yoy = f"{100*(v/q[i-4][1]-1):+6.1f}%" if i >= 4 else "     -"
    print(f"  {lbl}  {v:>6}   seq {seq}   y/y {yoy}")
print("  -> y/y falls from +22.6% (Q1-25) to +6.2% (Q2-26), not monotonically but")
print("     unambiguously; the last two quarters are FLAT sequentially at $2,134k.")

print()
print(line)
print("4. COST SIDE: headcount is the driver, and it is lumpy")
print(line)
for p in ["FY2023", "FY2024", "FY2025", "H1FY25", "H1FY26"]:
    c = comp[p]
    tot = sum(c.values())
    r = rev[p]
    ann = 2 if p.startswith("H1") else 1
    print(f"  {p}: total comp {money(tot*ann):>12} (annualised)   "
          f"= {pct(tot/r)} of revenue   "
          f"COGS comp {money(c['cogs']*ann):>11} = {pct(c['cogs']/r)} of revenue")

print(f"\n  Total operating cost FY2025 = {money(rev['FY2025']-op_inc['FY2025'])}; "
      f"compensation = {pct(sum(comp['FY2025'].values())/(rev['FY2025']-op_inc['FY2025']))}"
      f" of it.")
print("\n  The two-phase pattern that produces the margin cycle:")
print_rows = [
    ("FY2024->FY2025", rev["FY2025"]/rev["FY2024"]-1,
     comp["FY2025"]["cogs"]/comp["FY2024"]["cogs"]-1,
     0.644 - 0.624),
    ("H1FY25->H1FY26", rev["H1FY26"]/rev["H1FY25"]-1,
     comp["H1FY26"]["cogs"]/comp["H1FY25"]["cogs"]-1,
     0.626 - 0.655),
]
for lbl, gr, gc, dgm in print_rows:
    print(f"    {lbl}: revenue {pct(gr):>7}  COGS-comp {pct(gc):>7}  "
          f"gross margin {100*dgm:+.1f} pts")

print("\n  Revenue per employee (management's own metric, AM25: '400,000 per employee'):")
print(f"    FY2024, 17 staff: {money(rev['FY2024']/17)}  "
      f"<- cross-checks AM25's ~$400k claim")
print(f"    FY2025, 17 staff: {money(rev['FY2025']/17)}")
print(f"    H1FY26 annualised, 21 staff: {money(2*rev['H1FY26']/21)}")
print(f"    Revenue needed at 21 staff to restore FY2025 productivity: "
      f"{money(21*rev['FY2025']/17)} "
      f"(= {pct(21*rev['FY2025']/17/rev['FY2025']-1)} above FY2025)")

# Revenue required to restore FY2025 gross margin at the current COGS run-rate
cogs_run = 2 * h1["H1FY26"]["cogs"]
gm_fy25 = 1 - 2_813_196 / rev["FY2025"]       # MDA25: COGS FY2025 = 2,813,196
rev_needed = cogs_run / (1 - gm_fy25)
print(f"\n  Annualised H1FY26 COGS run-rate = {money(cogs_run)}")
print(f"  Revenue needed to reproduce the FY2025 gross margin of {pct(gm_fy25)}"
      f" = {money(rev_needed)}")
print(f"  = {pct(rev_needed/rev['FY2025']-1)} above FY2025 revenue, versus "
      f"H1FY26 annualised revenue of {money(2*rev['H1FY26'])}")

print()
print(line)
print("4b. OPERATING MARGIN BRIDGE: compensation ratio vs everything else")
print("    (total operating cost = revenue - operating income; split into the")
print("     Note 14 compensation figure and a non-compensation residual)")
print(line)
rows = []
for p in ["FY2023", "FY2024", "FY2025"]:
    oc = rev[p] - op_inc[p]
    cp = sum(comp[p].values())
    rows.append((p, rev[p], op_inc[p]/rev[p], cp/rev[p], (oc-cp)/rev[p]))
for p in ["H1FY25", "H1FY26"]:
    oi = h1[p]["op_inc_exbd"]           # ex bad debt, so the two halves compare
    oc = rev[p] - oi
    cp = sum(comp[p].values())
    rows.append((p + " (ex-bd)", rev[p], oi/rev[p], cp/rev[p], (oc-cp)/rev[p]))
print(f"  {'period':<16}{'revenue':>12}{'op margin':>12}{'comp/rev':>11}"
      f"{'non-comp/rev':>14}")
for p, r, om, cr, nr in rows:
    print(f"  {p:<16}{money(r):>12}{pct(om):>12}{pct(cr):>11}{pct(nr):>14}")
d_om = rows[2][2] - rows[0][2]
d_cr = rows[2][3] - rows[0][3]
print(f"\n  FY2023 -> FY2025: operating margin {100*d_om:+.1f} pts, of which the")
print(f"  compensation ratio explains {100*(-d_cr):+.1f} pts "
      f"({pct(-d_cr/d_om)} of the move).")
d_om2 = rows[4][2] - rows[3][2]
d_cr2 = rows[4][3] - rows[3][3]
d_nr2 = rows[4][4] - rows[3][4]
print(f"  H1FY25 -> H1FY26 (both ex-bad-debt): operating margin {100*d_om2:+.1f} pts")
print(f"    compensation ratio {100*d_cr2:+.1f} pts (a drag)")
print(f"    non-compensation ratio {100*d_nr2:+.1f} pts (an offset -- MDQ2: travel and")
print("      trade-show costs down $26,751 in selling expenses)")
print("  -> the FY2026 margin story is ENTIRELY a compensation-vs-revenue story,")
print("     partly masked by cutting discretionary non-comp spend.")

print()
print(line)
print("5. OPERATING LEVERAGE: incremental margin, both directions")
print(line)
inc_fy = (op_inc["FY2025"]-op_inc["FY2023"])/(rev["FY2025"]-rev["FY2023"])
d_op = h1["H1FY26"]["op_inc"] - h1["H1FY25"]["op_inc"]
d_op_x = h1["H1FY26"]["op_inc_exbd"] - h1["H1FY25"]["op_inc_exbd"]
d_rev = rev["H1FY26"] - rev["H1FY25"]
print(f"  FY2023 -> FY2025: d(op inc) {money(op_inc['FY2025']-op_inc['FY2023'])} "
      f"/ d(rev) {money(rev['FY2025']-rev['FY2023'])} = {pct(inc_fy)} incremental margin")
print(f"  H1FY25 -> H1FY26 as reported:        {money(d_op)} / {money(d_rev)} "
      f"= {pct(d_op/d_rev)}")
print(f"  H1FY25 -> H1FY26 ex-bad-debt:        {money(d_op_x)} / {money(d_rev)} "
      f"= {pct(d_op_x/d_rev)}")
print(f"  (H1FY25 op income rebuilt from MD&A lines = {money(h1['H1FY25']['op_inc'])}; "
      f"MDQ2 quarterly table implies 822+805 = $1,627k -- ties)")
print(f"  (H1FY26 op income rebuilt = {money(h1['H1FY26']['op_inc'])}; "
      f"MDQ2 quarterly table implies 941+838 = $1,779k -- ties)")

print("\n  DOWNSIDE symmetry: because the cost base is headcount-driven and fixed")
print("  in the short run, lost revenue drops to operating income near 1:1.")
top3_h126 = sum(conc["H1FY26"])
# H1FY26 half-year dollars annualised -- NOT share x TTM revenue, which mismatches
# a 6-month share against a 12-month base (the share falls each period, so that
# splice understates by ~$47k).
one_cust = 2 * conc["H1FY26"][0] * rev["H1FY26"]
one_cust_ttm = (conc["FY2025"][0]*rev["FY2025"] + conc["H1FY26"][0]*rev["H1FY26"]
                - conc["H1FY25"][0]*rev["H1FY25"])
print(f"    Top-3 customers = {pct(top3_h126)} of H1FY26 revenue (FSQ2 Note 7)")
print(f"    Largest = {pct(conc['H1FY26'][0])} of H1FY26 revenue = "
      f"{money(conc['H1FY26'][0]*rev['H1FY26'])} in the half = {money(one_cust)} annualised")
print(f"    Cross-check, TTM slot build = {money(one_cust_ttm)} "
      f"({pct(one_cust_ttm/one_cust-1)} vs annualised)")
print(f"    (share x TTM revenue would give {money(conc['H1FY26'][0]*rev_ttm_apr26)}"
      f" -- WRONG: 6-month share on a 12-month base)")
print(f"    Losing it with costs unchanged = {pct(one_cust/op_inc['FY2025'])} of "
      f"FY2025 operating income")

print()
print(line)
print("6. CUSTOMER CONCENTRATION BY RANK SLOT (dollars)")
print("   CAVEAT: the filings do not say the rank slots are the same customers")
print(line)
for p in ["FY2024", "FY2025", "H1FY25", "H1FY26"]:
    base = rev[p]
    d = [s * base for s in conc[p]]
    ann = 2 if p.startswith("H1") else 1
    print(f"  {p}: #1 {money(d[0]*ann):>12}  #2 {money(d[1]*ann):>12}  "
          f"#3 {money(d[2]*ann):>12}   top-3 {pct(sum(conc[p]))} of revenue "
          f"(annualised $)")
print(f"\n  Slot #1, FY2024 -> FY2025: "
      f"{pct(conc['FY2025'][0]*rev['FY2025']/(conc['FY2024'][0]*rev['FY2024'])-1)}")
print(f"  Slot #1, H1FY25 -> H1FY26: "
      f"{pct(conc['H1FY26'][0]*rev['H1FY26']/(conc['H1FY25'][0]*rev['H1FY25'])-1)}")
print(f"  Slots #2+#3, H1FY25 -> H1FY26: "
      f"{pct(sum(conc['H1FY26'][1:])*rev['H1FY26']/(sum(conc['H1FY25'][1:])*rev['H1FY25'])-1)}")

print()
print(line)
print("7. EXPANSION-DRIVEN GROWTH: reconciling the two management statements")
print(line)
print("  AM25 (FY2024): net revenue retention 112%, zero churn, 12% growth.")
print("  AM26 (5-yr look-back): '~75% ... came from purely organic growth")
print("  amongst our customers. Almost none of it came from price increases.'")
g24 = rev["FY2024"] / rev["FY2023"] - 1
print(f"\n  FY2024 reported growth {pct(g24)}; NRR 112% implies the existing base")
print(f"  alone contributed ~12.0 pts, leaving ~{100*g24-12.0:+.1f} pts from net new")
print("  customers -> in FY2024, essentially ALL growth was expansion inside the")
print("  existing account base (consistent with AM25's disclosure that growth was")
print("  driven by 'one of our large customers rolling out our Cirreon CIT")
print("  application during the calendar year').")
print("\n  Implied expansion rate now, if churn is still ~zero and new-customer")
print("  contribution is still ~0: recurring revenue growth IS the NRR proxy.")
print(f"    FY2025 recurring growth  {pct(recurring['FY2025']/recurring['FY2024']-1)}"
      f"  -> implied NRR ~116%")
print(f"    H1FY26 recurring growth  {pct(recurring['H1FY26']/recurring['H1FY25']-1)}"
      f"  -> implied NRR ~106%")

print()
print(line)
print("8. WORKING CAPITAL / COLLECTION SIGNALS")
print(line)
for p, r in [("FY2024", rev["FY2024"]), ("FY2025", rev["FY2025"]),
             ("H1FY26", rev_ttm_apr26)]:
    print(f"  {p}: receivables {money(ar[p]):>12}  DSO on "
          f"{'TTM ' if p=='H1FY26' else ''}revenue {ar[p]/r*365:5.1f} days   "
          f">90 days past due {money(ar_90[p]):>10} "
          f"= {pct(ar_90[p]/ar[p])} of receivables")
print(f"\n  Deferred revenue: " + "  ".join(
    f"{k} {money(v)}" for k, v in defrev.items()))
print(f"  Apr-30-26 balance is {defrev['H1FY26']/defrev['FY2025']:.2f}x the "
      f"Oct-31-25 balance.")
print("  Unearned revenue RECEIVED: $697,257 in all of FY2025 vs $842,173 in the")
print("  six months to Apr-30-26 (FS25 Note 7 / FSQ2 Note 7) -> annual legacy")
print("  product-support renewals are billed early in the calendar year.")
print("  NOTE: no Apr-30-2025 comparative deferred-revenue balance exists in")
print("  primary_sources, so seasonality here is an inference from the renewal")
print("  mechanic described in MDA25, not a confirmed year-on-year pattern.")

print()
print(line)
print("9. THE CAPITAL SINK: surplus cash earns less than it costs to hold")
print(line)
netcash = cash_apr26 + sti_apr26
print(f"  Cash + short-term investments at Apr-30-26 = {money(netcash)} "
      f"(FSQ2 SOFP), no debt")
print(f"  GIC yields {pct(gic_rate_lo)}-{pct(gic_rate_hi)} pre-tax (FSQ2 Note 15)")
print(f"  Pre-tax carry: {money(netcash*gic_rate_lo)} - {money(netcash*gic_rate_hi)}")
print(f"  After tax at {pct(tax_rate)}: {money(netcash*gic_rate_lo*(1-tax_rate))} - "
      f"{money(netcash*gic_rate_hi*(1-tax_rate))} "
      f"= {pct(gic_rate_lo*(1-tax_rate))}-{pct(gic_rate_hi*(1-tax_rate))} nominal")
print("  Interest income on short-term investments FELL even though the average")
print("  balance rose: $273,084 (FY2024) -> $235,681 (FY2025) [MDA25 'Interest")
print("  income'], and $115,058 (H1FY25) -> $95,212 (H1FY26) [MDQ2].")

print()
print(line)
print("10. ROUGH PENETRATION UNIT (order of magnitude only)")
print(line)
cit_share = 0.23          # AM26: "our CIT application is 23%"
cit_rev = cit_share * rev["FY2025"]
vehicle_share = 0.08      # AM26: software runs on ~8% of all US CIT vehicles
print(f"  AM26: CIT product ~{pct(cit_share)} of revenue -> ~{money(cit_rev)} in FY2025")
print(f"  AM26: that software runs on ~{pct(vehicle_share)} of US CIT vehicles")
print(f"  Naive unit: {money(cit_rev/ (100*vehicle_share))} of revenue per 1 pt of")
print("  US CIT vehicle share. OVERSTATED, because CIT revenue is not all US.")
print(f"  Read only as: doubling US CIT vehicle share would add revenue on the")
print(f"  order of {money(cit_rev)}, i.e. ~{pct(cit_rev/rev['FY2025'])} of FY2025")
print("  revenue -- a multi-year, not a quarterly, lever.")
print(line)

print()
print(line)
print("11. THE HIRING STEP, PRICED (17 -> 21 employees)")
print(line)
c25 = sum(comp["H1FY25"].values())
c26 = sum(comp["H1FY26"].values())
print(f"  Total compensation, H1FY25 {money(c25)} -> H1FY26 {money(c26)}  "
      f"({pct(c26/c25-1)})")
print(f"  Increase per half {money(c26-c25)}; annualised {money(2*(c26-c25))}")
print(f"  = {pct(2*(c26-c25)/op_inc['FY2025'])} of FY2025 operating income")
print(f"  Headcount {heads['FY2025']} -> {heads['H1FY26']} "
      f"({pct(heads['H1FY26']/heads['FY2025']-1)}); "
      f"compensation per head, annualised: "
      f"{money(2*c25/heads['FY2025'])} -> {money(2*c26/heads['H1FY26'])}")
print(line)

print()
print(line)
print("12. R1 REVIEW RESPONSE -- Obj 2: is the US 3.5% a single-account event?")
print(line)
c1_a = conc["H1FY25"][0] * rev["H1FY25"]
c1_b = conc["H1FY26"][0] * rev["H1FY26"]
us_d = split("H1FY26")[0] - split("H1FY25")[0]
print(f"  Rank-#1 half-year dollars: {money(c1_a)} -> {money(c1_b)} "
      f"= {money(c1_b-c1_a)}")
print(f"  Total US dollar growth: {money(us_d)}")
print(f"  (a) verifier's form -- add back to numerator only:")
print(f"      ({money(us_d)} + {money(c1_a-c1_b)}) / {money(split('H1FY25')[0])} "
      f"= {pct((us_d+(c1_a-c1_b))/split('H1FY25')[0])}")
print(f"  (b) correct like-for-like -- remove the account from BOTH periods:")
base = split("H1FY25")[0] - c1_a
print(f"      ({money(split('H1FY26')[0]-c1_b)}) / ({money(base)}) - 1 "
      f"= {pct((split('H1FY26')[0]-c1_b)/base - 1)}")
print("  Both assume rank-#1 is (i) the same customer in both periods and")
print("  (ii) domiciled in the US. Neither is disclosed. This is a LIVE")
print("  ALTERNATIVE to broad US saturation, not a refutation of it.")

print()
print(line)
print("13. R1 REVIEW RESPONSE -- Obj 3: FX elasticity vs USD-cost share")
print(line)
opc25 = rev["FY2025"] - op_inc["FY2025"]
print(f"  FY2025 operating cost base = {money(opc25)}")
print(f"  {'USD cost share':>16}{'net d(OpInc) on 5% move':>26}{'% of OpInc':>13}"
      f"{'elasticity':>13}")
for usd_cost in (0.0, 0.15, 0.30, 0.50):
    net = usd_share*fx_move*rev["FY2025"] - usd_cost*fx_move*opc25
    print(f"  {pct(usd_cost):>16}{money(net):>26}{pct(net/op_inc['FY2025']):>13}"
          f"{net/(fx_move*op_inc['FY2025']):>12.2f}x")
print("  MDA25 says only the 'majority' of expenses are CAD -- so 0% USD cost")
print("  is an UPPER BOUND, not a point estimate. Plausible range 1.9x-2.4x.")
print(line)

print()
print(line)
print("12. VERIFIER ROUND-1 RESPONSE CALCULATIONS")
print(line)

print("\n  (2) Is the US deceleration a broad-base effect or one account?")
# Rank-#1 customer dollars, HALF-YEAR (not annualised), FSQ2 Note 7
top1_h125 = conc["H1FY25"][0] * rev["H1FY25"]
top1_h126 = conc["H1FY26"][0] * rev["H1FY26"]
d_top1 = top1_h126 - top1_h125
us_a, us_b = geo["H1FY25"]["US"], geo["H1FY26"]["US"]
print(f"    Rank-#1 revenue: {money(top1_h125)} -> {money(top1_h126)}  "
      f"({pct(top1_h126/top1_h125-1)}), i.e. {money(d_top1)}")
print(f"    Total US revenue growth in the same window: {money(us_b-us_a)} "
      f"({pct(us_b/us_a-1)})")
print("    ASSUMING rank-#1 is the same US customer in both periods, strip it from")
print("    BOTH the numerator AND the base (the verifier divided by the unadjusted")
print("    base, which understates their own objection):")
ex_a, ex_b = us_a - top1_h125, us_b - top1_h126
print(f"      US ex-#1: {money(ex_a)} -> {money(ex_b)} = {pct(ex_b/ex_a-1)} growth")
print(f"      Verifier's arithmetic (unadjusted base): "
      f"{pct((us_b-us_a-d_top1)/us_a)}")
print(f"      Correct ex-account figure is {pct(ex_b/ex_a-1)}, NOT "
      f"{pct((us_b-us_a-d_top1)/us_a)} -- the objection is LARGER than claimed.")
print(f"    Rank-#1 decline as a share of the total revenue-growth shortfall:")
print(f"      FY2025 US growth rate {pct(geo['FY2025']['US']/geo['FY2024']['US']-1)}"
      f" applied to H1FY25 US base would have given "
      f"{money(us_a*(geo['FY2025']['US']/geo['FY2024']['US']-1))} of growth;")
print(f"      actual was {money(us_b-us_a)}; shortfall {money(us_a*(geo['FY2025']['US']/geo['FY2024']['US']-1)-(us_b-us_a))}")
print(f"      rank-#1 decline of {money(-d_top1)} covers "
      f"{pct(-d_top1/(us_a*(geo['FY2025']['US']/geo['FY2024']['US']-1)-(us_b-us_a)))}"
      f" of that shortfall.")

print("\n  (3) FX elasticity of operating income vs. USD share of the cost base")
oc25 = rev["FY2025"] - op_inc["FY2025"]
print(f"    FY2025 revenue {money(rev['FY2025'])}, operating cost {money(oc25)}, "
      f"operating income {money(op_inc['FY2025'])}")
print(f"    Elasticity = (0.96*Rev - usd_cost_share*OpCost) / OpInc")
print(f"    {'USD cost share':>16}{'elasticity':>13}{'5% move -> op inc':>22}")
for s in (0.00, 0.10, 0.15, 0.20, 0.25, 0.30):
    e = (usd_share * rev["FY2025"] - s * oc25) / op_inc["FY2025"]
    print(f"    {pct(s):>16}{e:>12.2f}x{pct(0.05*e):>22}")
print("    Evidence bounding the USD cost share (FSQ2 Note 11): USD trade payables")
print(f"    of US$61,310 against total trade and other payables of $360,682 -> "
      f"17%-24%")
print("    of payables depending on the rate used (no rate series is in the sources).")
print("    Compensation is 58.6% of operating cost and the team is Canada-based with")
print("    UK/Australia hires (AM26) -- i.e. GBP/AUD, not USD. So the USD tail is")
print("    mainly cloud hosting. Plausible range 10%-25% -> elasticity 2.0x-2.3x.")
print(line)

print()
print(line)
print("13. LOSS OF THE LARGEST ACCOUNT: how much cost actually goes with it?")
print(line)
lost_rev = 2 * conc["H1FY26"][0] * rev["H1FY26"]       # FSQ2 Note 7, annualised
lost_share = lost_rev / rev_ttm_apr26
cogs25 = 2_813_196                                      # MDA25 / FS25 statements
cogs_comp25 = comp["FY2025"]["cogs"]                    # FS25 Note 14
cogs_noncomp = cogs25 - cogs_comp25
comp_per_head = 2 * sum(comp["H1FY26"].values()) / heads["H1FY26"]
print(f"  Revenue lost {money(lost_rev)} = {pct(lost_share)} of TTM revenue")
print(f"  FY2025 cost of sales {money(cogs25)}: compensation {money(cogs_comp25)} "
      f"({pct(cogs_comp25/cogs25)}), non-compensation residual {money(cogs_noncomp)}")
print("  The filings NEVER disaggregate the non-comp residual (Note 14 gives only")
print("  compensation). Cloud hosting is the presumed bulk -- that is an INFERENCE.")
print(f"  Annualised compensation per employee (H1FY26, 21 staff): "
      f"{money(comp_per_head)}")
print(f"\n  {'Scenario':<58}{'d(OpInc)':>13}{'% FY25 OpInc':>14}{'pass-thru':>11}")
scen = [
    ("A. Year 1, nothing cut (contractual salaries continue)", 0),
    ("B. + non-comp COGS falls pro-rata with revenue", lost_share * cogs_noncomp),
    ("C. B + one support FTE not replaced", lost_share * cogs_noncomp + comp_per_head),
    ("D. B + two support FTEs not replaced", lost_share * cogs_noncomp + 2 * comp_per_head),
    ("E. B + three support FTEs not replaced", lost_share * cogs_noncomp + 3 * comp_per_head),
]
for lbl, saved in scen:
    d = -(lost_rev - saved)
    print(f"  {lbl:<58}{money(d):>13}{pct(d/op_inc['FY2025']):>14}"
          f"{pct((lost_rev-saved)/lost_rev):>11}")
print(f"\n  Frictions that push toward scenario A in the near term:")
print(f"   - Employee termination commitment of $1,100,000 to three employees")
print(f"     (FS25 Note 13) -- cutting senior staff has a cash cost roughly equal")
print(f"     to a year of the lost revenue.")
print(f"   - Revealed preference: headcount went 17 -> 21 (AM25, AM26) WHILE growth")
print(f"     decelerated from 15.4% to 8.0%. Management does not cut into weakness.")
print(f"   - 21 people across 3 products and multiple time zones -- thin to start.")
print(f"  Frictions that push toward C-E over 2-3 years: support load genuinely")
print(f"  falls, and attrition can be used instead of termination (no payout).")
print(f"\n  Cross-check against observed incremental margin (script section 5):")
print(f"    FY2023->FY2025 upside incremental margin 57.8%; H1FY26 ex-bad-debt 32.3%.")
print(f"    Perfect symmetry would imply downside pass-through of 32%-58% -- close to")
print(f"    scenarios D-E. But the upside figure includes GROWTH spend (international")
print(f"    sales/support hires) that would NOT reverse on losing a customer, so true")
print(f"    steady-state pass-through should sit ABOVE that range.")
print(f"\n  HONEST RANGE: year 1 {pct(1.0)}-{pct((lost_rev-scen[1][1])/lost_rev)} "
      f"pass-through ({pct(lost_rev/op_inc['FY2025'])}-"
      f"{pct((lost_rev-scen[1][1])/op_inc['FY2025'])} of operating income);")
print(f"  steady state after right-sizing roughly "
      f"{pct((lost_rev-scen[3][1])/lost_rev)}-{pct((lost_rev-scen[2][1])/lost_rev)} "
      f"({pct((lost_rev-scen[3][1])/op_inc['FY2025'])}-"
      f"{pct((lost_rev-scen[2][1])/op_inc['FY2025'])} of operating income).")
print(line)
