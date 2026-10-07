"""
NamSys Inc. (TSXV: CTZ) - Five-year Owners' Earnings forecast, FY2026E-FY2030E.

Every input below carries a source tag. Source tags:
  FS23  primary_sources/FY2023/Namsys_-_Annual_FS_-_Feb262024.md
  FS24  primary_sources/FY2024/NamSys_AFS_021925.md
  FS25  primary_sources/FY2025/NamSys_AFS_022426.md
  MDA25 primary_sources/FY2025/NamSys_MDA_022426.md
  FSQ2  primary_sources/2Q2026/FS_Q2_NamSys_Apr_30_26_FINAL.md
  MDQ2  primary_sources/2Q2026/MDA_Q2_NamSys_Apr_30_26_FINAL.md
  AM25  fetched_docs/namsys_2025_annual_meeting_transcript.md
  AM26  fetched_docs/namsys_2026_annual_meeting_transcript.md
  OE    work_products/owners_earnings_and_roic.md
  CM    work_products/causal_model.md
  KS11  Knowledge Store ID 11 (Bank of Canada FXMUSDCAD fiscal-year averages)
  KS12  Knowledge Store ID 12 (Fed 2026 Diary of Consumer Payment Choice)

Run:  uv run python work_products/forecast_earnings_calcs.py
"""

from textwrap import dedent

def h(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)

def pct(x):
    return f"{100*x:+.1f}%"

def m(x):
    return f"{x:,.0f}"

# ---------------------------------------------------------------------------
# SECTION 0. HISTORICAL INPUTS (all sourced)
# ---------------------------------------------------------------------------
h("SECTION 0. Historical inputs")

# Reported revenue, CAD  [FS23, FS25, FSQ2]
REV = {"FY2022": 5_394_781, "FY2023": 6_093_020, "FY2024": 6_840_146,
       "FY2025": 7_891_605, "H1FY25": 3_951_863, "H1FY26": 4_267_406}

# Geographic revenue, CAD  [FS23 Note 7, FS24 Note 7, FS25 Note 7, FSQ2 Note 7]
GEO = {
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

# Top-3 customer revenue shares  [FS24 Note 7, FS25 Note 7, FSQ2 Note 7]
TOP = {"FY2023": (0.249,), "FY2024": (0.200, 0.089, 0.089),
       "FY2025": (0.159, 0.123, 0.107),
       "H1FY25": (0.175, 0.125, 0.097), "H1FY26": (0.131, 0.128, 0.114)}

# Bank of Canada monthly-average USD/CAD, fiscal-year averages  [KS11]
FX = {"FY2022": 1.2878, "FY2023": 1.3487, "FY2024": 1.3610, "FY2025": 1.4009,
      "H1FY25": 1.4209, "H1FY26": 1.3792}

# Income statement lines, CAD  [FS23, FS25, FSQ2]
COST_OF_SALES = {"FY2023": 2_440_520, "FY2024": 2_570_778, "FY2025": 2_813_196,
                 "H1FY25": 1_364_558, "H1FY26": 1_596_137}
SELLING = {"FY2023": 381_451, "FY2024": 442_187, "FY2025": 714_618,
           "H1FY25": 335_511, "H1FY26": 309_302}
GA = {"FY2023": 1_140_611, "FY2024": 1_255_163, "FY2025": 1_165_985,
      "H1FY25": 574_253, "H1FY26": 582_407}
BAD_DEBT = {"FY2023": 23_004, "FY2024": 0, "FY2025": 51_330,
            "H1FY25": 50_746, "H1FY26": 0}
OP_INC = {"FY2023": 2_107_434, "FY2024": 2_572_018, "FY2025": 3_146_476,
          "H1FY25": 1_626_795, "H1FY26": 1_779_560}

# Note 14 compensation, CAD  [FS23/FS24/FS25/FSQ2 Note 14]
COMP = {"FY2023": 1_686_897 + 211_665 + 518_151,
        "FY2024": 1_690_129 + 259_294 + 557_450,
        "FY2025": 1_739_266 + 486_478 + 555_762,
        "H1FY25": 844_523 + 241_308 + 275_568,
        "H1FY26": 1_016_795 + 243_906 + 278_705}
COMP_COS = {"FY2025": 1_739_266, "FY2024": 1_690_129,
            "H1FY25": 844_523, "H1FY26": 1_016_795}

# Reported share-based compensation (inside Note 14 comp)  [FS25 Note 6, FSQ2 Note 6]
SBC = {"FY2023": 191_468, "FY2024": 114_174, "FY2025": 47_030,
       "H1FY25": 27_020, "H1FY26": 4_894}

# Headcount  [AM25: "stable at 17 employees"; AM26: "up to 21 employees today"]
HEADS = {"FY2024": 17, "FY2025": 17, "Apr2026": 21}

# Normalisation constants carried over from the Owners' Earnings work product [OE Sec 2.1]
NORM_BAD_DEBT = 19_220        # 4-year average reported bad debt expense
NORM_SBC = 117_557            # FY2023-FY2025 average reported SBC
TAX_RATE = 0.265              # [MDA25 "The basic rate of 26.50% was applied"]
PERM_DIFF = 1_300             # Note 9 unexplained residual, FY2025 $1,385 / TTM $1,162 [OE Sec 2.2e]
DEP_MINUS_CAPEX = -2_196      # FY2025: depreciation 7,465 less capex 9,661 [OE Sec 2.1]

OE_ACTUAL = {"FY2022": 1_159_664, "FY2023": 1_554_032,
             "FY2024": 1_838_746, "FY2025": 2_250_271}   # [OE Sec 2.1]

print(f"FY2025 revenue {m(REV['FY2025'])}, operating income {m(OP_INC['FY2025'])}, "
      f"owners' earnings {m(OE_ACTUAL['FY2025'])}")
print(f"FY2025 Note 14 total compensation {m(COMP['FY2025'])} "
      f"= {COMP['FY2025']/REV['FY2025']:.1%} of revenue")

# ---------------------------------------------------------------------------
# SECTION 1. Does the Mexico country total equal one of the top-3 customers?
# ---------------------------------------------------------------------------
h("SECTION 1. Test: is Mexico's revenue a single customer?")
print("Mexico as a % of total revenue vs. the disclosed top-3 customer shares:\n")
print(f"{'Period':<9}{'Mexico %':>10}{'  top-3 disclosed shares':<34}{'closest':>9}{'gap (pp)':>10}")
for p in ["FY2023", "FY2024", "FY2025", "H1FY25", "H1FY26"]:
    mx = GEO[p]["Mexico"] / REV[p]
    best = min(TOP[p], key=lambda s: abs(s - mx))
    shares = ", ".join(f"{s:.1%}" for s in TOP[p])
    print(f"{p:<9}{mx:>9.2%}  [{shares:<30}]{best:>9.1%}{100*(mx-best):>10.2f}")
print(dedent("""
    Reading: in FY2024, FY2025, H1FY25 and H1FY26 the Mexico country total matches a
    disclosed top-3 customer share to within 0.06 percentage points. FY2023 is the only
    miss, and in that year only ONE customer share was disclosed (24.9%), so Mexico
    (7.9%) could not have appeared. INFERENCE (not disclosed): essentially all Mexican
    revenue is one customer. Consequence: the top-3 slot ranking is not stable, and in
    H1 FY2026 slot #1 (13.1%) is the Mexican account - which GREW 46% - not the legacy
    account that has been shrinking.
"""))

# ---------------------------------------------------------------------------
# SECTION 1b. Which geographic bucket can the legacy top account sit in?
# ---------------------------------------------------------------------------
# Added after verifier review round 1 (objection 2). The "US" label on the legacy
# account was previously asserted. It is in fact demonstrable by elimination: the
# Note 7 geographic table is by country (with "Other" a residual of several
# countries), so a single customer's revenue cannot exceed its own country bucket.
h("SECTION 1b. Elimination test: the legacy top account must sit in the US bucket")
LEGACY_SHARE = {"FY2023": 0.249, "FY2024": 0.200, "FY2025": 0.159,
                "H1FY25": 0.175, "H1FY26": 0.128}   # H1FY26: slot #2, see Section 3
print(f"{'Period':<9}{'legacy $CAD':>13}   buckets that are large enough to contain it")
for p, sh in LEGACY_SHARE.items():
    amt = sh * REV[p]
    big = [k for k, v in GEO[p].items() if v >= amt]
    # Mexico is already fully consumed by its own top-3 slot (Section 1), so it
    # cannot simultaneously host a second top-3 account.
    mex_slot = min(TOP[p], key=lambda s: abs(s - GEO[p]["Mexico"] / REV[p]))
    if "Mexico" in big and abs(mex_slot - GEO[p]["Mexico"] / REV[p]) < 0.001 and mex_slot != sh:
        big = [k for k in big if k != "Mexico"] + ["Mexico (excluded: already = its own top-3 slot)"]
    print(f"{p:<9}{m(amt):>13}   {', '.join(big)}")
print(dedent("""
    In every period the US is the only country bucket large enough. The label is
    therefore demonstrated, not inherited - the same standard applied to Mexico in
    Section 1. Caveat: this establishes the account is predominantly US-domiciled,
    not that 100% of its revenue is booked to the US line.
"""))

# ---------------------------------------------------------------------------
# SECTION 2. Constant-currency (USD) revenue by geography
# ---------------------------------------------------------------------------
h("SECTION 2. Constant-currency decomposition: how much of reported growth is FX?")

def usd(period, key):
    """Convert a CAD geographic line to USD at the period's average rate.
    ~96% of revenue is invoiced in USD [FSQ2 Note 11], so USD is the currency the
    commercial activity actually happens in. Canada is left in CAD."""
    return GEO[period][key] / FX[period]

INTL_OTHER = ("DR", "PR", "Other")

rows = []
for p in ["FY2023", "FY2024", "FY2025", "H1FY25", "H1FY26"]:
    us = usd(p, "US")
    mex = usd(p, "Mexico")
    oth = sum(usd(p, k) for k in INTL_OTHER)
    rows.append((p, us, mex, oth, us + mex + oth, GEO[p]["Canada"]))

print(f"{'Period':<9}{'US (USD)':>12}{'Mexico':>11}{'OthIntl':>11}{'USD total':>13}{'Canada CAD':>12}")
for r in rows:
    print(f"{r[0]:<9}{m(r[1]):>12}{m(r[2]):>11}{m(r[3]):>11}{m(r[4]):>13}{m(r[5]):>12}")

def growth(a, b):
    return b / a - 1

print("\nGrowth rates, reported CAD vs constant-currency USD:\n")
print(f"{'Bucket':<24}{'FY24->FY25 CAD':>16}{'FY24->FY25 USD':>16}"
      f"{'H1 y/y CAD':>13}{'H1 y/y USD':>13}")
pairs = [("US", "US"), ("Mexico", "Mexico")]
for label, key in pairs:
    cad_a = growth(GEO["FY2024"][key], GEO["FY2025"][key])
    usd_a = growth(usd("FY2024", key), usd("FY2025", key))
    cad_h = growth(GEO["H1FY25"][key], GEO["H1FY26"][key])
    usd_h = growth(usd("H1FY25", key), usd("H1FY26", key))
    print(f"{label:<24}{pct(cad_a):>16}{pct(usd_a):>16}{pct(cad_h):>13}{pct(usd_h):>13}")
oi_cad_a = growth(sum(GEO["FY2024"][k] for k in INTL_OTHER),
                  sum(GEO["FY2025"][k] for k in INTL_OTHER))
oi_usd_a = growth(sum(usd("FY2024", k) for k in INTL_OTHER),
                  sum(usd("FY2025", k) for k in INTL_OTHER))
oi_cad_h = growth(sum(GEO["H1FY25"][k] for k in INTL_OTHER),
                  sum(GEO["H1FY26"][k] for k in INTL_OTHER))
oi_usd_h = growth(sum(usd("H1FY25", k) for k in INTL_OTHER),
                  sum(usd("H1FY26", k) for k in INTL_OTHER))
print(f"{'Other intl (DR/PR/Oth)':<24}{pct(oi_cad_a):>16}{pct(oi_usd_a):>16}"
      f"{pct(oi_cad_h):>13}{pct(oi_usd_h):>13}")
tot_cad_a = growth(REV["FY2024"], REV["FY2025"])
tot_usd_a = growth(rows[1][4], rows[2][4])
tot_cad_h = growth(REV["H1FY25"], REV["H1FY26"])
tot_usd_h = growth(rows[3][4], rows[4][4])
print(f"{'TOTAL (ex-Canada)':<24}{pct(tot_cad_a):>16}{pct(tot_usd_a):>16}"
      f"{pct(tot_cad_h):>13}{pct(tot_usd_h):>13}")

print(dedent(f"""
    FX translation effect: FY2024 avg 1.3610 -> FY2025 avg 1.4009 = a {FX['FY2025']/FX['FY2024']-1:+.1%}
    TAILWIND to reported CAD revenue. H1 FY2025 avg 1.4209 -> H1 FY2026 avg 1.3792 =
    a {FX['H1FY26']/FX['H1FY25']-1:+.1%} HEADWIND. So reported growth flatters FY2025 and
    understates H1 FY2026. On a constant-currency basis the aggregate deceleration
    is {pct(tot_usd_a)} -> {pct(tot_usd_h)}, i.e. barely any, versus the reported
    {pct(tot_cad_a)} -> {pct(tot_cad_h)}.
"""))

# --- Recurring revenue only, constant currency -------------------------------
# Recurring = "Software subscriptions, hosted services, maintenance and product
# support" [FS25 Note 7, FSQ2 Note 7]. The geographic note does not split recurring
# from professional services, so the FX adjustment is applied at the total level,
# treating recurring as USD-billed in the same ~96% proportion as total revenue.
REC = {"FY2024": 6_716_298, "FY2025": 7_811_909,
       "H1FY25": 3_929_927, "H1FY26": 4_170_949}
rec_a_cad = REC["FY2025"] / REC["FY2024"] - 1
rec_a_cc = (1 + rec_a_cad) / (FX["FY2025"] / FX["FY2024"]) - 1
rec_h_cad = REC["H1FY26"] / REC["H1FY25"] - 1
rec_h_cc = (1 + rec_h_cad) / (FX["H1FY26"] / FX["H1FY25"]) - 1
print(f"Recurring revenue growth: FY2024->FY2025 {pct(rec_a_cad)} reported CAD -> "
      f"{pct(rec_a_cc)} constant currency")
print(f"Recurring revenue growth: H1 y/y        {pct(rec_h_cad)} reported CAD -> "
      f"{pct(rec_h_cc)} constant currency")
print("  (a genuine ~4-point deceleration in the durable line, versus the ~10-point")
print("   deceleration implied by the reported figures alone)")

# ---------------------------------------------------------------------------
# SECTION 3. Split the US bucket into the shrinking legacy account and the rest
# ---------------------------------------------------------------------------
h("SECTION 3. The legacy large US account vs. the rest of the US base")

# The historically-largest customer: 24.9% (FY23), 20.0% (FY24), 15.9% (FY25),
# 17.5% (H1FY25).  [FS24/FS25/FSQ2 Note 7]
legacy_cad = {"FY2023": 0.249 * REV["FY2023"], "FY2024": 0.200 * REV["FY2024"],
              "FY2025": 0.159 * REV["FY2025"], "H1FY25": 0.175 * REV["H1FY25"]}
for p, v in legacy_cad.items():
    print(f"  legacy account {p}: {m(v)} CAD = {m(v/FX[p])} USD")
print(f"  USD change FY2023->FY2024: {pct(growth(legacy_cad['FY2023']/FX['FY2023'], legacy_cad['FY2024']/FX['FY2024']))}")
print(f"  USD change FY2024->FY2025: {pct(growth(legacy_cad['FY2024']/FX['FY2024'], legacy_cad['FY2025']/FX['FY2025']))}")

# H1 FY2026 slot assignment is ambiguous once Mexico occupies slot #1. Two cases:
#   (a) legacy = slot #2 at 12.8%
#   (b) legacy = slot #3 at 11.4%  (or has dropped out of the top three entirely)
legacy_h126 = {"slot#2 @12.8%": 0.128 * REV["H1FY26"], "slot#3 @11.4%": 0.114 * REV["H1FY26"]}
base_h125_usd = legacy_cad["H1FY25"] / FX["H1FY25"]
print()
for lbl, v in legacy_h126.items():
    print(f"  legacy in H1FY26 if {lbl}: {m(v)} CAD = {m(v/FX['H1FY26'])} USD "
          f"-> y/y USD {pct(growth(base_h125_usd, v/FX['H1FY26']))}")

# Base case takes the LESS bad of the two (slot #2).
LEGACY_FY2025_USD = legacy_cad["FY2025"] / FX["FY2025"]
US_FY2025_USD = usd("FY2025", "US")
US_EX_LEGACY_FY2025_USD = US_FY2025_USD - LEGACY_FY2025_USD
US_FY2024_USD = usd("FY2024", "US")
US_EX_LEGACY_FY2024_USD = US_FY2024_USD - legacy_cad["FY2024"] / FX["FY2024"]
print(f"\n  US ex-legacy, USD: FY2024 {m(US_EX_LEGACY_FY2024_USD)} -> FY2025 "
      f"{m(US_EX_LEGACY_FY2025_USD)} = {pct(growth(US_EX_LEGACY_FY2024_USD, US_EX_LEGACY_FY2025_USD))}")

us_ex_h125 = usd("H1FY25", "US") - base_h125_usd
us_ex_h126 = usd("H1FY26", "US") - (0.128 * REV["H1FY26"]) / FX["H1FY26"]
print(f"  US ex-legacy, USD: H1FY25 {m(us_ex_h125)} -> H1FY26 {m(us_ex_h126)} = "
      f"{pct(growth(us_ex_h125, us_ex_h126))}")

# Strip the one-off professional-services spike out of that H1 figure.
ps_h125_usd = 21_936 / FX["H1FY25"]     # [MDQ2 revenue table]
ps_h126_usd = 96_457 / FX["H1FY26"]
ps_delta = ps_h126_usd - ps_h125_usd
print(f"  professional services USD: H1FY25 {m(ps_h125_usd)} -> H1FY26 {m(ps_h126_usd)}, "
      f"delta {m(ps_delta)}")
print(f"  US ex-legacy ex-PS-spike growth (worst case: all PS growth is US ex-legacy): "
      f"{pct(growth(us_ex_h125, us_ex_h126 - ps_delta))}")

# ---------------------------------------------------------------------------
# SECTION 4. Forecast drivers
# ---------------------------------------------------------------------------
h("SECTION 4. Driver assumptions")

YEARS = ["FY2026E", "FY2027E", "FY2028E", "FY2029E", "FY2030E"]

# Currency is exogenous and uncorrelated with operating performance, so it is held
# FLAT in every operating scenario and varied only in the Section 7 sensitivity.
# FY2026: the 10 realised months (Nov 25 - Aug 26) averaged 1.3852 [KS11]; Sep/Oct
# assumed at the August level of 1.3898 -> full-year 1.3860. FY2027+ held at 1.39,
# i.e. the most recent observable monthly average. This is a no-view assumption.
FX_FLAT = [1.3860, 1.39, 1.39, 1.39, 1.39]

SCENARIOS = {
    # Each tuple is the constant-currency (USD) growth rate for that bucket, by year.
    "Base": dict(
        us_ex_legacy=[0.13, 0.11, 0.095, 0.08, 0.07],
        legacy=[-0.20, -0.20, -0.20, -0.20, -0.20],
        mexico=[0.48, 0.18, 0.10, 0.07, 0.05],
        other_intl=[0.09, 0.13, 0.15, 0.15, 0.14],
        canada=[0.05, 0.05, 0.05, 0.05, 0.05],
        fx=FX_FLAT,
        heads=[19.8, 22.5, 24.0, 25.0, 26.0],
        wage_infl=0.035,
        cos_noncomp_elasticity=0.85,
        selling_noncomp_base=150_000, selling_noncomp_growth=0.10,
        ga_noncomp_growth=0.035,
    ),
    "Bear": dict(
        # Legacy account is lost outright in FY2028 (bank/CIT consolidation, the
        # winner-take-most mechanism in MDA25 Risk Factors). The rest of the US base
        # saturates. The Mexican rollout completes and plateaus. International never
        # lands a second large account. Headcount does not come back down - hiring
        # stops but nobody is cut (CM 4.4 revealed preference; FS25 Note 13 $1.1m
        # termination commitment).
        us_ex_legacy=[0.11, 0.08, 0.06, 0.05, 0.04],
        legacy=[-0.25, -0.30, -1.00, 0.0, 0.0],
        mexico=[0.40, 0.08, 0.00, 0.00, 0.00],
        other_intl=[0.08, 0.08, 0.08, 0.08, 0.08],
        canada=[0.03, 0.03, 0.03, 0.03, 0.03],
        fx=FX_FLAT,
        heads=[19.8, 22.5, 23.5, 24.0, 24.0],
        wage_infl=0.045,
        cos_noncomp_elasticity=1.00,
        selling_noncomp_base=150_000, selling_noncomp_growth=0.05,
        ga_noncomp_growth=0.045,
    ),
    "Bull": dict(
        # Legacy account stabilises. A second Mexico-sized international rollout
        # lands from FY2028 on the back of the UK/Australia hires and ISO 27001.
        # AI productivity holds headcount growth to ~1/yr.
        us_ex_legacy=[0.14, 0.13, 0.12, 0.11, 0.10],
        legacy=[-0.15, -0.08, -0.05, -0.05, -0.05],
        mexico=[0.50, 0.25, 0.15, 0.10, 0.08],
        other_intl=[0.12, 0.20, 0.30, 0.28, 0.24],
        canada=[0.06, 0.06, 0.06, 0.06, 0.06],
        fx=FX_FLAT,
        heads=[19.8, 22.0, 23.0, 24.0, 25.0],
        wage_infl=0.03,
        cos_noncomp_elasticity=0.75,
        selling_noncomp_base=150_000, selling_noncomp_growth=0.14,
        ga_noncomp_growth=0.03,
    ),
}

# FY2025 starting values
START = dict(
    us_ex_legacy=US_EX_LEGACY_FY2025_USD,
    legacy=LEGACY_FY2025_USD,
    mexico=usd("FY2025", "Mexico"),
    other_intl=sum(usd("FY2025", k) for k in INTL_OTHER),
    canada=GEO["FY2025"]["Canada"],
)
print("FY2025 starting buckets:")
for k, v in START.items():
    unit = "CAD" if k == "canada" else "USD"
    print(f"  {k:<14}{m(v):>12} {unit}")

# Cost base, FY2025
CASH_COMP_FY2025 = COMP["FY2025"] - SBC["FY2025"]
COMP_PER_HEAD_FY2025 = CASH_COMP_FY2025 / HEADS["FY2025"]
COS_NONCOMP_FY2025 = COST_OF_SALES["FY2025"] - COMP_COS["FY2025"]
SELL_NONCOMP_FY2025 = SELLING["FY2025"] - 486_478
GA_NONCOMP_FY2025 = GA["FY2025"] - 555_762
print(f"\nFY2025 cash compensation (Note 14 less reported SBC): {m(CASH_COMP_FY2025)}")
print(f"FY2025 cash compensation per head (17 staff): {m(COMP_PER_HEAD_FY2025)}")
print(f"FY2025 non-comp cost of sales (hosting etc.): {m(COS_NONCOMP_FY2025)}")
print(f"FY2025 non-comp selling: {m(SELL_NONCOMP_FY2025)}")
print(f"FY2025 non-comp G&A: {m(GA_NONCOMP_FY2025)}")

# Cross-check the implied H1 FY2026 average headcount
h1_cash_comp = COMP["H1FY26"] - SBC["H1FY26"]
implied_heads = h1_cash_comp / (COMP_PER_HEAD_FY2025 * 1.03 / 2)
print(f"\nCross-check: H1 FY2026 cash compensation {m(h1_cash_comp)} at a 3%-inflated "
      f"{m(COMP_PER_HEAD_FY2025*1.03)}/head implies an average of {implied_heads:.1f} staff "
      f"over the half (17 at the start of the year, 21 by 23 April 2026 [AM26]).")
fy26_heads_implied = (h1_cash_comp + 21 * COMP_PER_HEAD_FY2025 * 1.03 / 2) / (COMP_PER_HEAD_FY2025 * 1.03)
print(f"Holding 21 staff through H2 gives a FY2026 average of {fy26_heads_implied:.1f} "
      f"-> the model uses 19.8.")

# ---------------------------------------------------------------------------
# SECTION 4b. BACK-TEST: does the cost/OE engine reproduce FY2025 exactly?
# ---------------------------------------------------------------------------
h("SECTION 4b. Back-test of the cost -> owners' earnings engine on FY2025")
bt_cost = (CASH_COMP_FY2025 + SBC["FY2025"] + COS_NONCOMP_FY2025
           + GA_NONCOMP_FY2025 + SELL_NONCOMP_FY2025 + BAD_DEBT["FY2025"])
bt_op = REV["FY2025"] - bt_cost
print(f"  Rebuilt FY2025 operating income {m(bt_op)} vs reported {m(OP_INC['FY2025'])} "
      f"-> difference {m(bt_op - OP_INC['FY2025'])}")
bt_cost_norm = (CASH_COMP_FY2025 + NORM_SBC + COS_NONCOMP_FY2025
                + GA_NONCOMP_FY2025 + SELL_NONCOMP_FY2025 + NORM_BAD_DEBT)
bt_pretax_oe = REV["FY2025"] - bt_cost_norm + DEP_MINUS_CAPEX
bt_oe = bt_pretax_oe - (TAX_RATE * (bt_pretax_oe + NORM_SBC) + 1_385)
print(f"  Rebuilt FY2025 normalised pre-tax owners' earnings {m(bt_pretax_oe)} "
      f"vs {m(3_105_863)} in [OE Sec 2.1]")
print(f"  Rebuilt FY2025 owners' earnings {m(bt_oe)} vs {m(OE_ACTUAL['FY2025'])} in [OE Sec 2.1]")
print("  => the forward engine is the identical build, driven forward. No new method.")


# ---------------------------------------------------------------------------
# SECTION 5. Run the forecast
# ---------------------------------------------------------------------------

def run(name, a):
    h(f"SECTION 5. {name} case")
    lvl = dict(START)
    out = []
    prev_cos_nc = COS_NONCOMP_FY2025
    prev_ga_nc = GA_NONCOMP_FY2025
    prev_rev_cad = REV["FY2025"]
    for i, yr in enumerate(YEARS):
        for k in ("us_ex_legacy", "legacy", "mexico", "other_intl", "canada"):
            lvl[k] = lvl[k] * (1 + a[k][i])
        usd_total = lvl["us_ex_legacy"] + lvl["legacy"] + lvl["mexico"] + lvl["other_intl"]
        rev_cad = usd_total * a["fx"][i] + lvl["canada"]

        # --- costs
        comp = a["heads"][i] * COMP_PER_HEAD_FY2025 * (1 + a["wage_infl"]) ** (i + 1)
        cos_nc = prev_cos_nc * (1 + a["cos_noncomp_elasticity"] * (rev_cad / prev_rev_cad - 1))
        ga_nc = prev_ga_nc * (1 + a["ga_noncomp_growth"])
        sell_nc = a["selling_noncomp_base"] * (1 + a["selling_noncomp_growth"]) ** i
        total_cost = comp + NORM_SBC + cos_nc + ga_nc + sell_nc + NORM_BAD_DEBT
        op_inc = rev_cad - total_cost

        # --- operating income -> owners' earnings  [method per OE Sec 2]
        pretax_oe = op_inc + DEP_MINUS_CAPEX
        tax = TAX_RATE * (pretax_oe + NORM_SBC) + PERM_DIFF
        oe = pretax_oe - tax

        out.append(dict(year=yr, usd=usd_total, fx=a["fx"][i], rev=rev_cad, comp=comp,
                        cos_nc=cos_nc, ga_nc=ga_nc, sell_nc=sell_nc, op=op_inc,
                        oe=oe, heads=a["heads"][i],
                        us=lvl["us_ex_legacy"] + lvl["legacy"],
                        legacy=lvl["legacy"], mexico=lvl["mexico"],
                        other=lvl["other_intl"], canada=lvl["canada"],
                        rev_g=rev_cad / prev_rev_cad - 1))
        prev_cos_nc, prev_ga_nc, prev_rev_cad = cos_nc, ga_nc, rev_cad

    print(f"{'':<10}{'USDrev':>10}{'FX':>7}{'RevCAD':>11}{'g':>8}{'Comp':>10}"
          f"{'Heads':>7}{'OpInc':>10}{'OpMgn':>8}{'OE':>10}{'OEmgn':>8}")
    print(f"{'FY2025A':<10}{m(rows[2][4]):>10}{FX['FY2025']:>7.4f}{m(REV['FY2025']):>11}"
          f"{'+15.4%':>8}{m(CASH_COMP_FY2025):>10}{17:>7}{m(OP_INC['FY2025']):>10}"
          f"{OP_INC['FY2025']/REV['FY2025']:>7.1%}{m(OE_ACTUAL['FY2025']):>10}"
          f"{OE_ACTUAL['FY2025']/REV['FY2025']:>7.1%}")
    for r in out:
        print(f"{r['year']:<10}{m(r['usd']):>10}{r['fx']:>7.4f}{m(r['rev']):>11}"
              f"{pct(r['rev_g']):>8}{m(r['comp']):>10}{r['heads']:>7.1f}{m(r['op']):>10}"
              f"{r['op']/r['rev']:>7.1%}{m(r['oe']):>10}{r['oe']/r['rev']:>7.1%}")

    n = len(out)
    rev_cagr = (out[-1]["rev"] / REV["FY2025"]) ** (1 / n) - 1
    oe_cagr = (out[-1]["oe"] / OE_ACTUAL["FY2025"]) ** (1 / n) - 1
    print(f"\n  FY2025 -> FY2030E revenue CAGR {rev_cagr:.1%}; owners' earnings CAGR {oe_cagr:.1%}")
    print(f"  Cumulative owners' earnings FY2026E-FY2030E: {m(sum(r['oe'] for r in out))}")
    print(f"\n  Revenue bucket detail (USD, except Canada in CAD):")
    print(f"{'':<10}{'US total':>11}{'of which legacy':>17}{'Mexico':>10}{'OthIntl':>10}{'Canada':>10}")
    for r in out:
        print(f"{r['year']:<10}{m(r['us']):>11}{m(r['legacy']):>17}{m(r['mexico']):>10}"
              f"{m(r['other']):>10}{m(r['canada']):>10}")
    return out

results = {k: run(k, v) for k, v in SCENARIOS.items()}

# ---------------------------------------------------------------------------
# SECTION 6. Reconciliation of the FY2026E estimate to reported H1 FY2026
# ---------------------------------------------------------------------------
h("SECTION 6. FY2026E sanity check against reported H1 FY2026")
b = results["Base"][0]
h2_implied = b["rev"] - REV["H1FY26"]
print(f"  FY2026E revenue (model)          {m(b['rev'])}")
print(f"  H1 FY2026 actual [FSQ2]          {m(REV['H1FY26'])}")
print(f"  => implied H2 FY2026             {m(h2_implied)}  "
      f"({h2_implied/REV['H1FY26']-1:+.1%} vs H1)")
print(f"  Q3 FY2026 average USD/CAD was 1.3957 vs H1 FY2026 1.3792 [KS11], a +1.2%")
print(f"  translation tailwind, so the implied H2 needs only ~{(h2_implied/REV['H1FY26']-1)*100-1.2:.1f}% of")
print(f"  constant-currency sequential growth. H1 quarters grew +5.5% and 0.0%")
print(f"  sequentially in CAD [MDQ2]; the flat Q2 was itself an FX artefact -")
q1fx = (1.4055 + 1.3802 + 1.3778) / 3
q2fx = (1.3651 + 1.3717 + 1.3751) / 3
print(f"  Q1 FY2026 average rate {q1fx:.4f} vs Q2 {q2fx:.4f} = {q2fx/q1fx-1:+.2%}, so Q2")
print(f"  revenue grew {(1.0)/(q2fx/q1fx)-1:+.2%} sequentially in USD despite being flat in CAD.")

print(f"\n  FY2026E implied H2 compensation: {m(b['comp'] - h1_cash_comp)} vs 21 staff at "
      f"{m(COMP_PER_HEAD_FY2025*1.03/2)} each = {m(21*COMP_PER_HEAD_FY2025*1.03/2)}")

# ---------------------------------------------------------------------------
# SECTION 7. Sensitivities on the base case
# ---------------------------------------------------------------------------
h("SECTION 7. Sensitivity of FY2030E owners' earnings (base case)")
base_fy30 = results["Base"][-1]["oe"]
base_fy30_rev = results["Base"][-1]["rev"]
print(f"  Base case FY2030E owners' earnings: {m(base_fy30)}\n")

base_cum = sum(r["oe"] for r in results["Base"])

def variant(label, **over):
    a = dict(SCENARIOS["Base"])
    a.update(over)
    lvl = dict(START)
    prev_cos_nc, prev_ga_nc, prev_rev = COS_NONCOMP_FY2025, GA_NONCOMP_FY2025, REV["FY2025"]
    cum = 0.0
    for i in range(len(YEARS)):
        for k in ("us_ex_legacy", "legacy", "mexico", "other_intl", "canada"):
            lvl[k] = lvl[k] * (1 + a[k][i])
        usd_total = sum(lvl[k] for k in ("us_ex_legacy", "legacy", "mexico", "other_intl"))
        rev = usd_total * a["fx"][i] + lvl["canada"]
        comp = a["heads"][i] * COMP_PER_HEAD_FY2025 * (1 + a["wage_infl"]) ** (i + 1)
        cos_nc = prev_cos_nc * (1 + a["cos_noncomp_elasticity"] * (rev / prev_rev - 1))
        ga_nc = prev_ga_nc * (1 + a["ga_noncomp_growth"])
        sell_nc = a["selling_noncomp_base"] * (1 + a["selling_noncomp_growth"]) ** i
        op = rev - (comp + NORM_SBC + cos_nc + ga_nc + sell_nc + NORM_BAD_DEBT)
        prev_cos_nc, prev_ga_nc, prev_rev = cos_nc, ga_nc, rev
        pt = op + DEP_MINUS_CAPEX
        cum += pt - (TAX_RATE * (pt + NORM_SBC) + PERM_DIFF)
    pretax = op + DEP_MINUS_CAPEX
    oe = pretax - (TAX_RATE * (pretax + NORM_SBC) + PERM_DIFF)
    print(f"  {label:<52}{m(oe):>11}{(oe/base_fy30-1):>8.0%}{m(cum):>13}{(cum/base_cum-1):>8.0%}")

print(f"  {'Variant':<52}{'FY2030E OE':>11}{'vs base':>8}{'cum 5yr OE':>13}{'vs base':>8}")
variant("USD/CAD 1.25 from FY2027 (CAD +10%)", fx=[1.3860, 1.25, 1.25, 1.25, 1.25])
variant("USD/CAD 1.53 from FY2027 (CAD -10%)", fx=[1.3860, 1.53, 1.53, 1.53, 1.53])
variant("USD/CAD 1.32 from FY2027 (CAD +5%)", fx=[1.3860, 1.32, 1.32, 1.32, 1.32])
variant("USD/CAD 1.46 from FY2027 (CAD -5%)", fx=[1.3860, 1.46, 1.46, 1.46, 1.46])
variant("Legacy account lost outright in FY2027",
        legacy=[-0.20, -1.00, 0.0, 0.0, 0.0])
variant("Legacy account stops shrinking (0%/yr)", legacy=[0.0] * 5)
variant("US ex-legacy growth 3 pts lower every year",
        us_ex_legacy=[0.10, 0.08, 0.065, 0.05, 0.04])
variant("US ex-legacy growth 3 pts higher every year",
        us_ex_legacy=[0.16, 0.14, 0.125, 0.11, 0.10])
variant("Mexico account flat from FY2027", mexico=[0.48, 0.0, 0.0, 0.0, 0.0])
variant("Mexico account lost in FY2028", mexico=[0.48, 0.18, -1.0, 0.0, 0.0])
variant("Headcount +1/yr only (23 by FY2030)", heads=[19.8, 21.5, 22.0, 22.5, 23.0])
variant("Headcount +2.5/yr (31 by FY2030)", heads=[19.8, 23.5, 26.0, 28.5, 31.0])
variant("Wage inflation 5.0% not 3.5%", wage_infl=0.05)
variant("Non-comp cost of sales scales 1.0x with revenue", cos_noncomp_elasticity=1.0)

# ---------------------------------------------------------------------------
# SECTION 8. Summary table
# ---------------------------------------------------------------------------
h("SECTION 8. Owners' earnings summary, all scenarios (CAD)")
print(f"{'':<10}{'FY2025A':>11}" + "".join(f"{y:>11}" for y in YEARS) + f"{'5yr CAGR':>10}")
print(f"{'Actual':<10}{m(OE_ACTUAL['FY2025']):>11}")
for name in ["Bear", "Base", "Bull"]:
    r = results[name]
    cagr = (r[-1]["oe"] / OE_ACTUAL["FY2025"]) ** 0.2 - 1
    print(f"{name:<10}{'':>11}" + "".join(f"{m(x['oe']):>11}" for x in r) + f"{cagr:>9.1%}")
print()
print(f"{'':<10}{'FY2025A':>11}" + "".join(f"{y:>11}" for y in YEARS))
print(f"{'Revenue':<10}{m(REV['FY2025']):>11}")
for name in ["Bear", "Base", "Bull"]:
    print(f"{name:<10}{'':>11}" + "".join(f"{m(x['rev']):>11}" for x in results[name]))
print()
print("Owners' earnings margin:")
for name in ["Bear", "Base", "Bull"]:
    print(f"{name:<10}{OE_ACTUAL['FY2025']/REV['FY2025']:>11.1%}"
          + "".join(f"{x['oe']/x['rev']:>11.1%}" for x in results[name]))

# ---------------------------------------------------------------------------
# SECTION 9. Internal-consistency checks on the base case
# ---------------------------------------------------------------------------
h("SECTION 9. Internal-consistency checks, base case")
print("Revenue per employee (CAD) - the productivity claim implied by the forecast:")
print(f"  FY2024A {REV['FY2024']/17:>10,.0f}   [AM25 states '400,000 per employee' -> ties]")
print(f"  FY2025A {REV['FY2025']/17:>10,.0f}")
for r in results["Base"]:
    print(f"  {r['year']} {r['rev']/r['heads']:>10,.0f}")
print("  => the base case holds revenue per employee roughly FLAT at ~$435-440k from")
print("     FY2026 onward, i.e. it credits NO further productivity gain after the")
print("     FY2026 hiring reset. FY2025's $464k was achieved by under-hiring.\n")

print("Cash compensation as % of revenue:")
print(f"  FY2023A {(COMP['FY2023']-SBC['FY2023'])/REV['FY2023']:>7.1%}")
print(f"  FY2024A {(COMP['FY2024']-SBC['FY2024'])/REV['FY2024']:>7.1%}")
print(f"  FY2025A {CASH_COMP_FY2025/REV['FY2025']:>7.1%}")
for r in results["Base"]:
    print(f"  {r['year']} {r['comp']/r['rev']:>7.1%}")
print("  => rises to ~43%, well above the FY2023 level of 36.5%. The base case therefore")
print("     assumes the FY2023-FY2025 operating leverage REVERSES and does not return.\n")

# How much of the HISTORICAL earnings growth was currency rather than the business?
h("SECTION 9c. How much of FY2022->FY2025 earnings growth was just a weaker CAD?")
fy22_cost = REV["FY2022"] - 1_753_157   # FY2022 operating income [FS23]

fy22_geo_ex_canada = 4_348_529 + 319_726 + 267_540 + 195_635 + 54_118   # [FS23 Note 7]
fy22_canada = 209_233
rev22_restated = fy22_geo_ex_canada / FX["FY2022"] * FX["FY2025"] + fy22_canada
print(f"  FY2022 revenue restated at the FY2025 average rate: {m(rev22_restated)} "
      f"(reported {m(REV['FY2022'])})")
for usd_cost_share in (0.0, 0.20, 0.25):
    cost22_restated = fy22_cost * ((1 - usd_cost_share) + usd_cost_share * FX["FY2025"] / FX["FY2022"])
    op22_restated = rev22_restated - cost22_restated
    cc = (OP_INC["FY2025"] / op22_restated) ** (1 / 3) - 1
    print(f"    USD cost share {usd_cost_share:>4.0%}: restated FY2022 operating income "
          f"{m(op22_restated)} -> FY2022-FY2025 constant-currency CAGR {cc:>5.1%}")
# Same restatement carried all the way through to owners' earnings.
# FY2022 normalised pre-tax owners' earnings 1,621,643; Note 9 residual 1,091 [OE Sec 2.1]
for usd_cost_share in (0.0, 0.20):
    cost22_restated = fy22_cost * ((1 - usd_cost_share) + usd_cost_share * FX["FY2025"] / FX["FY2022"])
    uplift = (rev22_restated - cost22_restated) - 1_753_157
    pt22 = 1_621_643 + uplift
    oe22 = pt22 - (TAX_RATE * (pt22 + NORM_SBC) + 1_091)
    cc = (OE_ACTUAL["FY2025"] / oe22) ** (1 / 3) - 1
    print(f"    USD cost share {usd_cost_share:>4.0%}: restated FY2022 owners' earnings "
          f"{m(oe22)} -> FY2022-FY2025 constant-currency CAGR {cc:>5.1%}")
reported_cagr = (OP_INC["FY2025"] / 1_753_157) ** (1 / 3) - 1
print(f"  Reported FY2022->FY2025 operating income CAGR: {reported_cagr:.1%}")
print(f"  Reported FY2022->FY2025 owners' earnings CAGR: "
      f"{(OE_ACTUAL['FY2025']/OE_ACTUAL['FY2022'])**(1/3)-1:.1%}  [OE Sec 5]")
print(dedent("""
    => Roughly 8-9 percentage points of the ~21.5%/yr historical operating-income
    growth was CAD depreciation (1.2878 -> 1.4009), not the business. Because the
    forecast holds USD/CAD FLAT - a deliberate no-view assumption - that tailwind
    is set to zero. This is the single biggest reason the forecast owners'-earnings
    growth rate (~5%/yr base) is so much lower than the historical ~24.7%/yr, and
    it is a methodological choice, not a view that the business has deteriorated.
"""))

print("Implied FY2022 headcount (no SBC in FY2022, so Note 14 comp is all cash):")
for rate, lbl in [(130_897, "at the FY2023 per-head rate"),
                  (130_897 * 0.97, "at 3% below the FY2023 rate")]:
    print(f"  {2_075_797/rate:>5.1f} staff  ({lbl})")
print("  => headcount went ~16 (FY2022) to 21 (April 2026), i.e. ~+1.25/yr over four")
print("     years. The forecast adds ~+1.2/yr after FY2027. The FY2023-FY2025 flat-at-17")
print("     stretch is the anomaly, not the norm.\n")

print("Implied cash compensation per head, history vs forecast:")
for p, hd in [("FY2023", 17), ("FY2024", 17), ("FY2025", 17)]:
    print(f"  {p}A  {(COMP[p]-SBC[p])/hd:>10,.0f}  (at the disclosed point-in-time headcount)")
print("  NOTE: the implied +14.3% FY2024->FY2025 step at nominally flat headcount cannot")
print("  be pure wage inflation; it most likely reflects average-vs-point-in-time headcount")
print("  (the international business-development hire's first full year [MDA25, AM25]).")
print("  The forward 3.5% assumption is validated instead by the H1 FY2026 reconciliation")
print("  in Section 4 (predicted H2 compensation within 1.3% of 21 staff at the run-rate).\n")

# Bear case with a cost response
h("SECTION 9b. Bear case if management DOES right-size")
a = dict(SCENARIOS["Bear"]); a["heads"] = [19.8, 21.0, 21.0, 20.0, 20.0]
bear_rs = run("Bear + headcount frozen at 21 then trimmed to 20", a)
print("  The base bear case deliberately assumes NO cost response (CM 4.4 revealed")
print("  preference; FS25 Note 13 $1,100,000 termination commitment). Freezing and then")
print("  modestly trimming headcount recovers a large part of the damage - which is the")
print("  honest bound on how bad the downside really is over a five-year horizon.")
