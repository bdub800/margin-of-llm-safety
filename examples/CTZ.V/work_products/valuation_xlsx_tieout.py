"""
Reconciles the ~$5 residual between work_products/valuation.xlsx and the equity
values published in work_products/valuation.md section 5.

The workbook links normalised share-based compensation as a live formula,
=AVERAGE(FY2023:FY2025 reported SBC) = 352,672 / 3 = 117,557.333..., whereas
forecast_earnings_calcs.py hard-codes the rounded constant NORM_SBC = 117,557.
It also carries the unrounded owners'-earnings path into the terminal value,
whereas terminal_value_calcs.py multiplies the rounded FY2030E figure of
2,859,320 published in forecast_earnings.md section 1.

This script runs the forecast + valuation engine both ways and attributes the
difference. Conclusion: the workbook is the more precise of the two, and the
entire residual is -$5.29 on a ~$40M equity value (0.000013%).

Run: uv run python work_products/valuation_xlsx_tieout.py
"""

# --- inputs, all as they appear on the workbook's Inputs sheet --------------
REV25 = 7_891_605                                   # FS25 statement of operations
FX25 = 1.4009                                       # Knowledge Store ID 11
GEO = dict(US=5_979_328, MX=846_155, CA=286_682,
           DR=275_378, PR=262_573, OT=241_489)      # FS25 Note 7
LEGACY_SHARE = 0.159                                # FS25 Note 7, largest customer
FX = [1.3860, 1.39, 1.39, 1.39, 1.39]               # FC FX_FLAT
CASH_COMP = 2_781_506 - 47_030                      # FS25 Note 14 less reported SBC
CPH = CASH_COMP / 17                                # AM25: 17 employees
COS_NC = 2_813_196 - 1_739_266                      # FS25 cost of sales less Note 14 comp
GA_NC = 1_165_985 - 555_762                         # FS25 G&A less Note 14 comp
TAX, PERM_DIFF = 0.265, 1_300                       # MDA25 / OE s2.2e
DEP_LESS_CAPEX = 7_465 - 9_661                      # FS25 Note 4 / cash-flow statement
H1_OVERLAP = 1_497_265                              # FSQ2 six months ended Apr 30 2026
STANDALONE = 940_082 + 6_425_965                    # FSQ2 balance sheet
DISC, MULT = 0.10, 12.0                             # VAL s1 / TV s6

D = dict(us=[.13, .11, .095, .08, .07], leg=[-.2] * 5, mex=[.48, .18, .10, .07, .05],
         oth=[.09, .13, .15, .15, .14], can=[.05] * 5,
         heads=[19.8, 22.5, 24., 25., 26.], wage=.035, elast=.85, ga=.035,
         sell=[150_000, 165_000, 181_500, 199_650, 219_615])

leg0 = LEGACY_SHARE * REV25 / FX25
START = dict(us=GEO["US"] / FX25 - leg0, leg=leg0, mex=GEO["MX"] / FX25,
             oth=(GEO["DR"] + GEO["PR"] + GEO["OT"]) / FX25, can=GEO["CA"])


def oe_path(norm_sbc, norm_bad_debt=19_220.0, round_each_year=False):
    lvl = dict(START)
    prev_cos, prev_ga, prev_rev = COS_NC, GA_NC, REV25
    out = []
    for i in range(5):
        for k in ("us", "leg", "mex", "oth", "can"):
            lvl[k] *= (1 + D[k][i])
        rev = (lvl["us"] + lvl["leg"] + lvl["mex"] + lvl["oth"]) * FX[i] + lvl["can"]
        comp = D["heads"][i] * CPH * (1 + D["wage"]) ** (i + 1)
        cos = prev_cos * (1 + D["elast"] * (rev / prev_rev - 1))
        ga = prev_ga * (1 + D["ga"])
        op = rev - (comp + norm_sbc + cos + ga + D["sell"][i] + norm_bad_debt)
        pretax = op + DEP_LESS_CAPEX
        oe = pretax - (TAX * (pretax + norm_sbc) + PERM_DIFF)
        out.append(round(oe) if round_each_year else oe)
        prev_cos, prev_ga, prev_rev = cos, ga, rev
    return out


def equity(path, round_terminal_year):
    flows = [path[0] - H1_OVERLAP] + path[1:]
    pv = sum(cf / (1 + DISC) ** t for t, cf in enumerate(flows))
    tv = MULT * (round(path[4]) if round_terminal_year else path[4])
    return pv + tv / (1 + DISC) ** 4 + STANDALONE


published = equity(oe_path(117_557, round_each_year=True), True)
step1 = equity(oe_path(352_672 / 3, round_each_year=True), True)
workbook = equity(oe_path(352_672 / 3), False)

print(f"Published in valuation.md s5 (rounded constants)     {published:>16,.4f}")
print(f"Workbook (live AVERAGE formula, unrounded OE path)   {workbook:>16,.4f}")
print(f"Total residual                                       {workbook - published:>16,.4f}")
print(f"  attributable to exact normalised SBC 117,557.33    {step1 - published:>16,.4f}")
print(f"  attributable to the unrounded OE path in the TV    {workbook - step1:>16,.4f}")
print(f"Residual as a share of equity value                  "
      f"{(workbook - published) / published:>16.8%}")
print(f"Per diluted share (27,459,593)                        "
      f"{(workbook - published) / 27_459_593:>16.8f}")
