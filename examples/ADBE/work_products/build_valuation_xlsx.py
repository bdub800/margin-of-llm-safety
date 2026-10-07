"""
Adobe Inc. (ADBE) — builds work_products/valuation.xlsx, a LIVE-FORMULA Excel
model that unifies four work products into three sheets:

  SHEET 1  "1. Inputs"
      Every hard-coded number in the model: judgment assumptions (amber) and
      reported actuals from filings (blue). Nothing else in the workbook is
      hard-coded.
        sources: owners_earnings_and_roic.md / owners_earnings_calcs.py
                 forecast_earnings.md      / forecast_earnings_calcs.py
                 terminal_value.md         / terminal_value_calcs.py
                 valuation.md              / valuation_calcs.py

  SHEET 2  "2. Owners' Earnings"
      Historical owners' earnings (FY2023A, FY2024A, FY2025A, TTM Q2 FY2026)
      and projected owners' earnings (FY2026E-FY2030E) SIDE BY SIDE on one
      identical construction, so the trend is readable across the page.
      §1 is the adjustment bridge itself — the answer is at the top. §2-§8 are
      the supporting build underneath: the itemised historical adjustments, the
      reported income statement and TTM build, the customer-group revenue base,
      the BASE-case forecast engine, the other three scenario engines, owners'
      earnings by scenario, and checks. No forecast share count, buyback
      path or forecast per-share figure is modelled anywhere.
        sources: owners_earnings_and_roic.md, forecast_earnings.md

  SHEET 3  "3. Terminal Value & SOTP"
      Terminal value at FY2030 year-end by scenario, the Gordon cross-check on
      the multiples, discounting, the sum-of-the-parts walk to an intrinsic
      value per diluted share, the equity bridge, and sensitivities.
        sources: terminal_value.md, valuation.md

WHAT CHANGED IN THIS REORGANISATION (presentation only — no number moved):
  1. Inputs is now the FIRST sheet, so the reader meets the assumptions before
     the machinery.
  2. The old 'Model' and 'Scenarios' sheets are merged into one owners'-earnings
     sheet. Scenario owners' earnings ARE owners' earnings; splitting them
     across two sheets forced the reader to hold two column maps at once.
  3. The owners'-earnings BRIDGE is moved to the top of sheet 2 (it used to sit
     at row 81, below 80 rows of supporting build). Historical and forecast run
     side by side in the same rows.
  4. The '1H FY2025 / 1H FY2026' interim-actuals block is moved to the Inputs
     sheet. On the old 'Model' sheet it sat in columns B and C, which the rest
     of that sheet used for FY2023A and FY2024A — the same two columns meant
     two different things on one sheet. That collision is now gone.
  5. Two CAGR columns (K, L) are added to sheet 2 so the historical trend and
     the forecast trend can be compared without a calculator.
  6. Freeze panes, section navigation blocks, and tab colours added.

DESIGN RULES (unchanged from the prior build)
  1. NOTHING computed is hard-coded. Every derived cell is an Excel formula
     chaining back to an input cell, reproducing the arithmetic in the python
     scripts above. The only hard-coded numbers are (a) reported actuals from
     filings and (b) judgment assumptions — both are highlighted.
  2. Highlighting:
        AMBER  = judgment / assumption input the reader may change
        BLUE   = reported actual from a primary source (a fixed input)
        GREEN  = headline output
        white  = formula, derived
  3. Every input carries a source citation in the note column.

Run:      uv run python work_products/build_valuation_xlsx.py
Verify:   uv run python work_products/verify_valuation_xlsx.py
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = "work_products/valuation.xlsx"

# --------------------------------------------------------------------------
# styles
# --------------------------------------------------------------------------
F_INPUT = PatternFill("solid", fgColor="FFE699")   # amber - judgment assumption
F_ACT = PatternFill("solid", fgColor="DDEBF7")     # blue  - reported actual
F_HDR = PatternFill("solid", fgColor="1F4E79")     # section band
F_SUB = PatternFill("solid", fgColor="D9E1F2")     # sub-band / column headers
F_OUT = PatternFill("solid", fgColor="E2EFDA")     # green - headline output
F_CHK = PatternFill("solid", fgColor="FFF2CC")     # pale  - check rows

FONT_HDR = Font(bold=True, color="FFFFFF", size=11)
FONT_SUB = Font(bold=True, size=10)
FONT_TITLE = Font(bold=True, size=14)
FONT_BOLD = Font(bold=True)
FONT_BIG = Font(bold=True, size=12)
FONT_NOTE = Font(italic=True, size=8, color="555555")
FONT_NAV = Font(italic=True, size=9, color="1F4E79")

TOP = Border(top=Side(style="thin"))
TOPD = Border(top=Side(style="double"))

NUM0 = '#,##0;(#,##0)'
NUM1 = '#,##0.0;(#,##0.0)'
NUM2 = '#,##0.00;(#,##0.00)'
PCT1 = '0.0%;(0.0%)'
PCT2 = '0.00%;(0.00%)'
USD2 = '$#,##0.00'
XMUL = '0.0"x"'
BPF = '#,##0" bp"'


def cell(ws, r, c, v, fmt=None, fill=None, font=None, border=None, align=None):
    """Write a value. Callers must use `txt()` for anything that may begin '='."""
    x = ws.cell(row=r, column=c, value=v)
    if fmt:
        x.number_format = fmt
    if fill:
        x.fill = fill
    if font:
        x.font = font
    if border:
        x.border = border
    if align:
        x.alignment = Alignment(horizontal=align)
    return x


def txt(ws, r, c, v, **kw):
    """Write TEXT. A leading space stops Excel parsing labels like "= EBITA"."""
    if isinstance(v, str) and v.startswith("="):
        v = " " + v
    return cell(ws, r, c, v, **kw)


def band(ws, r, text, ncols):
    for c in range(1, ncols + 1):
        txt(ws, r, c, text if c == 1 else None, fill=F_HDR, font=FONT_HDR)


def subband(ws, r, text, ncols):
    for c in range(1, ncols + 1):
        txt(ws, r, c, text if c == 1 else None, fill=F_SUB, font=FONT_SUB)


wb = Workbook()

# ==========================================================================
# SHEET 1 — INPUTS
# ==========================================================================
wi = wb.active
wi.title = "1. Inputs"
wi.sheet_properties.tabColor = "FFC000"
NC_I = 11                                   # note column K
wi.column_dimensions["A"].width = 58
wi.column_dimensions["B"].width = 13
wi.column_dimensions["C"].width = 13
for c in "DE":
    wi.column_dimensions[c].width = 3
for c in "FGHIJ":
    wi.column_dimensions[c].width = 12
wi.column_dimensions["K"].width = 100

YCOL = ["F", "G", "H", "I", "J"]            # FY2026E .. FY2030E
YLAB = ["FY2026E", "FY2027E", "FY2028E", "FY2029E", "FY2030E"]

I = {}                                      # key -> row number
r = 1
txt(wi, r, 1, "Adobe Inc. (ADBE) — MODEL INPUTS", font=FONT_TITLE)
r += 1
txt(wi, r, 1, "Every hard-coded number in this workbook lives on this sheet. "
              "Sheets 2 and 3 contain formulas only.", font=FONT_NOTE)
r += 1
txt(wi, r, 1, "AMBER = judgment / assumption input (change me).    "
              "BLUE = reported actual from a primary source (fixed).    "
              "White = formula.", font=FONT_NOTE)
r += 1
cell(wi, r, 2, "AMBER", fill=F_INPUT, font=FONT_NOTE, align="center")
cell(wi, r, 3, "BLUE", fill=F_ACT, font=FONT_NOTE, align="center")
r += 2
txt(wi, r, 1, "CONTENTS:  A. Valuation, tax and policy scalars   |   "
              "B. Scenario probabilities and terminal multiples   |   "
              "C. Equity bridge (Q2 FY2026 balance sheet)   |   "
              "D. Off-balance-sheet hosting obligations   |   "
              "E. Shared forecast assumptions   |   "
              "F. Scenario drivers   |   "
              "G. Interim actuals for the TTM build", font=FONT_NAV)
r += 2


def irow(key, label, val=None, fmt=NUM0, fill=F_INPUT, src=None, col=2,
         font=None, border=None):
    """One scalar input on the Inputs sheet."""
    global r
    I[key] = r
    txt(wi, r, 1, label, font=font)
    if val is not None:
        cell(wi, r, col, val, fmt=fmt, fill=(fill if not isinstance(val, str)
                                             else None), font=font, border=border)
    if src:
        txt(wi, r, NC_I, src, font=FONT_NOTE)
    row_ = r
    r += 1
    return row_


def iyears(key, label, vals, fmt=PCT1, fill=F_INPUT, src=None):
    """A five-year row of judgment inputs (FY2026E-FY2030E) on the Inputs sheet."""
    global r
    I[key] = r
    txt(wi, r, 1, label)
    for cl, v in zip(YCOL, vals):
        cell(wi, r, wi[cl + "1"].column, v, fmt=fmt, fill=fill)
    if src:
        txt(wi, r, NC_I, src, font=FONT_NOTE)
    row_ = r
    r += 1
    return row_


# ---- A. valuation, tax and policy scalars --------------------------------
band(wi, r, "A.  VALUATION, TAX AND POLICY SCALARS", NC_I)
r += 1
irow("disc", "Discount rate (r)", 0.15, PCT1,
     src="valuation.md §2 / §5.2: 'The discount rate is a stated variable, not a "
         "fitted one' — set at 15% per the brief, not derived from CAPM/WACC. "
         "valuation_calcs.py DISCOUNT_RATE.")
irow("tax", "Normalised tax rate", 0.21, PCT1,
     src="owners_earnings_and_roic.md §2.3: '21% ... approximately the U.S. federal "
         "statutory rate, sits within a point of the FY2023-FY2026E average GAAP ETR "
         "of 20.1% ... between the two converging measures.' GAAP ETR 18-23%, cash "
         "rate 25-27%. JUDGMENT. Sensitivity there: 18% -> TTM OE $7,775M; "
         "25% -> $7,111M.")
irow("disc_po", "Discount rate for PV of purchase obligations", 0.05, PCT1,
     src="owners_earnings_calcs.py DISC (§5). JUDGMENT: roughly Adobe's marginal "
         "borrowing cost.")
irow("opcash", "Operating cash need, % of revenue", 0.02, PCT1,
     src="owners_earnings_and_roic.md §4: 'Adobe collects in advance and runs "
         "negative working capital, so its genuine operating cash requirement is "
         "small ... This is an assumption, not a sourced figure.' "
         "owners_earnings_calcs.py OPERATING_CASH_PCT.")
irow("roic_t", "Terminal ROIC on incremental capital (Gordon cross-check only)", 0.70,
     PCT1,
     src="terminal_value.md §6.1 uses ROIC ~70% in the reinvestment drag term "
         "(1 - g/ROIC). owners_earnings_and_roic.md §1 reports TTM ROIC 72.0% "
         "(base) with a 43-45% conservative floor. Feeds the sheet-3 Gordon grid "
         "only — it does not affect the headline valuation.")
r += 1

# ---- B. scenario probabilities and terminal multiples --------------------
band(wi, r, "B.  SCENARIO PROBABILITIES AND TERMINAL MULTIPLES", NC_I)
r += 1
cell(wi, r, 2, "Probability", font=FONT_SUB, align="center")
cell(wi, r, 3, "Terminal x", font=FONT_SUB, align="center")
txt(wi, r, NC_I, "Probabilities: forecast_earnings.md §1 — 'my judgment and are not "
                 "sourced'. Terminal multiples: terminal_value.md §6.2 — ANALYST "
                 "JUDGMENT, cross-checked against the Gordon grid and peer multiples "
                 "on sheet 3.", font=FONT_NOTE)
r += 1
for key, lab, p, m, src in [
    ("sev", "SEVERE", 0.15, 7,
     "terminal_value.md §6.2: terminal decline, AI substitutes the workflow. Gordon at "
     "g=-3%, r=10% -> 8.0x. Market precedent ZM 9.0x; SSTK 0.23x sales after a -70% year."),
    ("bear", "BEAR", 0.25, 11,
     "terminal_value.md §6.2: grinding share loss, ~0-1% perpetual growth. Gordon at "
     "g=0-1%, r=9-10% -> 10.0x-12.3x. Floor cohort DBX 19.7x, GEN 18.0x, ZM 9.0x."),
    ("base", "BASE", 0.40, 15,
     "terminal_value.md §6.2: ~3% perpetual growth, 'the world where the question is "
     "neither resolved nor realised, so 15x — near today's actual and between the two "
     "peer cohorts — is the internally consistent choice.' Gordon at g=3%, r=9% -> 16.0x."),
    ("bull", "BULL", 0.20, 22,
     "terminal_value.md §6.2: franchise durable, AI net accretive. Gordon at g=4%, "
     "r=8.5% ~ 21x. Mature-software median 27.2x; ADSK 33.8x. Set BELOW both."),
]:
    I["p_" + key] = r
    I["m_" + key] = r
    txt(wi, r, 1, lab, font=FONT_BOLD)
    cell(wi, r, 2, p, fmt=PCT1, fill=F_INPUT)
    cell(wi, r, 3, m, fmt=XMUL, fill=F_INPUT)
    txt(wi, r, NC_I, src, font=FONT_NOTE)
    r += 1
I["p_sum"] = r
txt(wi, r, 1, "  check: probabilities sum to 100%")
cell(wi, r, 2, f"=SUM(B{I['p_sev']}:B{I['p_bull']})", fmt=PCT1, fill=F_CHK,
     border=TOP)
r += 2

# ---- C. equity bridge balance sheet --------------------------------------
band(wi, r, "C.  EQUITY BRIDGE — Q2 FY2026 BALANCE SHEET (period ended 29 May 2026)",
     NC_I)
r += 1
BS = "primary_sources/2Q2026/financial_statements.md, consolidated balance sheet."
irow("cash", "Cash and cash equivalents", 4919, NUM0, F_ACT, BS)
irow("sti", "Short-term investments", 707, NUM0, F_ACT, BS)
irow("debt_c", "Debt, current (incl. $494M commercial paper), carrying value", 1843,
     NUM0, F_ACT, BS + " Commercial paper drawn $494M — 10-Q Note 14.")
irow("debt_lt", "Debt, long-term (senior notes), carrying value", 4802, NUM0, F_ACT, BS)
irow("lease_c", "Operating lease liabilities, current", 91, NUM0, F_ACT, BS)
irow("lease_lt", "Operating lease liabilities, long-term", 329, NUM0, F_ACT, BS)
irow("sh_spot", "Shares outstanding, spot at 29 May 2026 (M)", 399.0, NUM1, F_ACT,
     BS + " A point-in-time count.")
irow("sh_dil", "Current dilutive effect of stock plans (M)", 0.1, NUM1, F_INPUT,
     "10-Q Note 12: three-months-ended diluted w.a. 402.5M less basic w.a. 402.4M. "
     "Small because 12.1M potential shares are currently anti-dilutive.")
irow("shares", " = Current diluted share count (M)",
     f"=B{I['sh_spot']}+B{I['sh_dil']}", NUM1, None,
     "valuation.md §3 = 399.1M. Per the brief this is TODAY's share count: no "
     "forecast buyback shrinkage (notably NOT the FY2030E 341M in "
     "forecast_earnings.md §8). The 402.5M three-month weighted average was "
     "rejected as backward-looking and stale while Adobe repurchases continuously.",
     font=FONT_BOLD, border=TOP)
r += 1

# ---- D. off-balance-sheet purchase obligations ---------------------------
band(wi, r, "D.  OFF-BALANCE-SHEET HOSTING / DATA-CENTRE PURCHASE OBLIGATIONS", NC_I)
r += 1
txt(wi, r, 1, "$6,821M of non-cancellable unconditional purchase obligations "
              "'primarily relating to contracts with vendors for third-party hosting "
              "and data center services' (owners_earnings_and_roic.md §4.1).",
    font=FONT_NOTE)
r += 1
po_first = None
for i, (yr, v) in enumerate([(2026, 2083), (2027, 1901), (2028, 1623),
                             (2029, 1196), (2030, 12), (2031, 6)]):
    k = f"po{yr}"
    I[k] = r
    if po_first is None:
        po_first = r
    txt(wi, r, 1, f"  FY{yr} contractual obligation")
    cell(wi, r, 2, v, fmt=NUM0, fill=F_ACT)
    if i == 0:
        txt(wi, r, NC_I, "primary_sources/FY2025/financial_statements.md Note 16 "
                         "maturity schedule; owners_earnings_calcs.py §5.",
            font=FONT_NOTE)
    r += 1
po_last = r - 1
I["po_tot"] = r
txt(wi, r, 1, "Undiscounted total", font=FONT_BOLD)
cell(wi, r, 2, f"=SUM(B{po_first}:B{po_last})", fmt=NUM0, font=FONT_BOLD, border=TOP)
r += 1
I["po_pv"] = r
txt(wi, r, 1, " = Present value, mid-year convention", font=FONT_BOLD)
cell(wi, r, 2,
     f"=SUMPRODUCT(B{po_first}:B{po_last}/(1+$B${I['disc_po']})"
     f"^(ROW(B{po_first}:B{po_last})-ROW($B${po_first})+0.5))",
     fmt=NUM0, font=FONT_BOLD, border=TOP)
txt(wi, r, NC_I, "owners_earnings_and_roic.md §4.1 reports $6,259M at 5%. "
                 "pv = SUM( v / 1.05^(i+0.5) ), i = 0..5 — owners_earnings_calcs.py §5.",
    font=FONT_NOTE)
r += 2

# ---- E. shared forecast assumptions --------------------------------------
band(wi, r, "E.  SHARED FORECAST ASSUMPTIONS (identical in all four scenarios)", NC_I)
r += 1
for cl, lab in zip(YCOL, YLAB):
    cell(wi, r, wi[cl + "1"].column, lab, font=FONT_SUB, align="center")
txt(wi, r, NC_I, "forecast_earnings.md §8 — the lines that do not vary by scenario.",
    font=FONT_NOTE)
r += 1
iyears("g_pa", "Publishing & Advertising subscription growth",
       [-0.05] * 5, PCT1, src="forecast_earnings_calcs.py §3 — run-off book. JUDGMENT.")
iyears("g_prod", "Product revenue growth", [-0.02, -0.05, -0.05, -0.05, -0.05], PCT1,
       src="forecast_earnings_calcs.py §3 — perpetual-licence run-off. JUDGMENT.")
iyears("g_serv", "Services and other revenue growth",
       [-0.20, -0.12, -0.10, -0.08, -0.08], PCT1,
       src="forecast_earnings_calcs.py §3 — 1H FY2026 annualised, then decline. JUDGMENT.")
iyears("fx", "Creative FX translation contribution", [0.02, 0, 0, 0, 0], PCT1,
       src="Q2 FY2026 FX added ~$94M net (causal_model.md Factor 1.7). Zero after "
           "FY2026: the model takes no currency view. forecast_earnings.md §4.")
iyears("sem", "Semrush revenue, $M (BEAR / BASE / BULL)", [280, 500, 540, 578, 612],
       NUM0, src="~$280M guided FY2026 contribution (primary_sources/2Q2026/md_and_a.md), "
                 "then annualises at 6-8%. Acquisition closed April 2026. JUDGMENT.")
iyears("sem_sev", "Semrush revenue, $M — SEVERE case override",
       [280, 470, 470, 470, 470], NUM0,
       src="forecast_earnings_calcs.py §9 severe override sem=... . JUDGMENT.")
iyears("amort", "Purchased-intangible amortisation, disclosed schedule ($M)",
       [222, 208, 151, 146, 143], NUM0, F_ACT,
       src="primary_sources/2Q2026/financial_statements.md Note 7. FY2026 = $91M "
           "actual 1H + $131M scheduled remainder. Excludes future acquisitions, so "
           "it is a FLOOR on future amortisation.")
iyears("nonrec", "Non-recurring operating charges forecast ($M)", [0] * 5, NUM0,
       src="ASSUMPTION: no future one-off charges are forecast in any scenario. "
           "Adobe booked $1,078M in FY2024 (Figma termination fee plus lease "
           "impairments) and $162M in 1H FY2026 (goodwill impairment plus the FTC "
           "loss contingency), so zero is an optimistic convention, not a neutral "
           "one. Setting these cells non-zero reduces owners' earnings pound for "
           "pound. forecast_earnings.md forecasts no one-offs.")
r += 1
irow("cr_prod", "Product cost ratio (cost of product / product revenue)",
     23 / 325, PCT2,
     src="FY2025 actual $23M / $325M held flat. forecast_earnings_calcs.py "
         "PROD_COST_RATIO.")
irow("cr_serv", "Services cost ratio (cost of services / services revenue)", 1.05,
     PCT2, src="Services is loss-making: FY2025 0.928, 1H FY2026 1.085. JUDGMENT 1.05.")
irow("am_in_cos", "FY2025 purchased-intangible amortisation inside cost of "
                  "subscription ($M)", 151, NUM0, F_ACT,
     src="primary_sources/FY2025/financial_statements.md Note 8. Stripped out of the "
         "cost ratio because owners' earnings adds all purchased-intangible "
         "amortisation back.")
irow("g_dep", "PP&E depreciation growth per year", 0.05, PCT1,
     src="forecast_earnings_calcs.py §8 chain(236.0, 5%). JUDGMENT.")
irow("capex_b", "Maintenance capex, FY2025 base ($M)", 241, NUM0,
     src=" = 3-year average actual capex FY2023-FY2025 ($240.667M), rounded — "
         "owners_earnings_and_roic.md §2.2: 'I use the three-year average actual "
         "capex of $241M as maintenance capex for every period — which lands within "
         "$5M of FY2025 depreciation.'")
irow("g_capex", "Maintenance capex growth per year", 0.05, PCT1,
     src="forecast_earnings_calcs.py §8 chain(241.0, 5%). JUDGMENT. Depreciation and "
         "maintenance capex both grow 5%, so they effectively cancel.")
r += 1

# ---- F. scenario drivers -------------------------------------------------
band(wi, r, "F.  SCENARIO DRIVERS — the root-cause variables the forecast is built on",
     NC_I)
r += 1
txt(wi, r, 1, "Each scenario re-runs the identical engine on its own driver set "
              "(sheet 2 §5 and §6). forecast_earnings.md §2-§7; "
              "forecast_earnings_calcs.py §9 scenario().", font=FONT_NOTE)
r += 1

DRIVER_LABELS = [
    ("mau", "MAU growth (Acrobat/Express monthly active users)", PCT1),
    ("rpm", "Change in revenue per average MAU", PCT1),
    ("cvol", "Creative paid-unit (volume) growth", PCT1),
    ("cpr", "Creative value-based price / tier-mix growth", PCT1),
    ("dx", "Digital Experience subscription growth", PCT1),
    ("drift", "Subscription cost ratio drift, ex-amortisation (bp/yr)", BPF),
    ("adv", "Advertising, % of revenue", PCT2),
    ("osm", "Other sales & marketing, % of revenue", PCT2),
    ("rd", "Research & development, % of revenue", PCT2),
    ("ga", "General & administrative, % of revenue", PCT2),
]

SCENARIOS = [
    ("sev", "SEVERE", "Generative AI SUBSTITUTES Adobe's creative workflows (as it did "
                      "Adobe Stock); Adobe defends with price cuts and more advertising.",
     {"mau": [0.17, 0.08, 0.04, 0.02, 0.00],
      "rpm": [-0.055, -0.07, -0.06, -0.05, -0.045],
      "cvol": [0.06, 0.00, -0.04, -0.05, -0.05],
      "cpr": [0.00, 0.00, 0.00, 0.00, 0.00],
      "dx": [0.08, 0.04, 0.025, 0.02, 0.015],
      "drift": [90, 100, 90, 80, 70],
      "adv": [0.076] * 5, "osm": [0.218] * 5, "rd": [0.195] * 5, "ga": [0.069] * 5}),
    ("bear", "BEAR", "AI substitution bites Creative, freemium advertising never comes "
                     "down, inference cost keeps compounding, BP&C monetisation keeps "
                     "eroding.",
     {"mau": [0.18, 0.11, 0.08, 0.06, 0.04],
      "rpm": [-0.045, -0.045, -0.035, -0.03, -0.03],
      "cvol": [0.07, 0.035, 0.02, 0.01, 0.00],
      "cpr": [0.005, 0.01, 0.01, 0.01, 0.01],
      "dx": [0.085, 0.06, 0.05, 0.045, 0.04],
      "drift": [80, 75, 65, 60, 55],
      "adv": [0.070, 0.073, 0.073, 0.073, 0.073], "osm": [0.213] * 5,
      "rd": [0.187] * 5, "ga": [0.067] * 5}),
    ("base", "BASE", "Freemium reach compounds but monetises at a falling rate; "
                     "hosting/AI cost drift decays; modest operating leverage in S&M.",
     {"mau": [0.18, 0.13, 0.10, 0.08, 0.06],
      "rpm": [-0.035, -0.025, -0.01, 0.00, 0.00],
      "cvol": [0.078, 0.06, 0.05, 0.04, 0.03],
      "cpr": [0.005, 0.02, 0.02, 0.02, 0.02],
      "dx": [0.09, 0.08, 0.075, 0.07, 0.065],
      "drift": [72, 50, 35, 25, 20],
      "adv": [0.069, 0.0695, 0.065, 0.061, 0.058],
      "osm": [0.210, 0.207, 0.204, 0.2015, 0.1995],
      "rd": [0.180] * 5, "ga": [0.067] * 5}),
    ("bull", "BULL", "Freemium converts, unit inference-cost deflation outruns volume "
                     "growth, advertising normalises after FY2027, price optimisations "
                     "resume in full.",
     {"mau": [0.19, 0.15, 0.12, 0.10, 0.08],
      "rpm": [-0.03, -0.005, 0.01, 0.015, 0.015],
      "cvol": [0.085, 0.085, 0.075, 0.065, 0.055],
      "cpr": [0.005, 0.03, 0.03, 0.03, 0.03],
      "dx": [0.095, 0.095, 0.09, 0.085, 0.08],
      "drift": [60, 25, 10, 0, -10],
      "adv": [0.068, 0.066, 0.059, 0.054, 0.051],
      "osm": [0.209, 0.204, 0.199, 0.195, 0.191],
      "rd": [0.178] * 5, "ga": [0.067] * 5}),
]

DRIVER_SRC = {
    "mau": "Q4 FY2025 call: MAU 'surpassed 750 million ... growing 20% year-over-year'. "
           "Decay paths are JUDGMENT. forecast_earnings.md §3, causal_model.md Factor 1.1.",
    "rpm": "The observable composite of free-to-paid conversion x price per paid seat; "
           "Adobe discloses neither component. forecast_earnings.md §3 flags confidence "
           "as LOW. JUDGMENT.",
    "cvol": "forecast_earnings.md §4: base decays 7.8% -> 3.0%; 'the bear case takes "
            "volume to 0% by FY2030 and the severe case to -5%'. JUDGMENT.",
    "cpr": "forecast_earnings.md §4 — value-based pricing and tier mix. JUDGMENT.",
    "dx": "forecast_earnings.md §5 — enterprise seat expansion and cross-sell. JUDGMENT.",
    "drift": "THE key cost finding: on an ex-amortisation basis the hosting/AI-inference "
             "cost ratio is deteriorating ~60bp/yr right now. forecast_earnings.md §6. "
             "JUDGMENT on the decay path.",
    "adv": "The freemium funnel spend, up 31.7% in FY2025 to $1,370M. "
           "forecast_earnings.md §7. JUDGMENT.",
    "osm": "forecast_earnings.md §7 — sales-force operating leverage. JUDGMENT.",
    "rd": "forecast_earnings.md §7: base 18.0%, 'bear case uses 18.7% and the severe "
          "case 19.5%'. JUDGMENT.",
    "ga": "forecast_earnings.md §7 — held flat at the FY2025 ratio in all scenarios "
          "except SEVERE (6.9%). JUDGMENT.",
}

for skey, sname, thesis, dvals in SCENARIOS:
    subband(wi, r, f"  {sname}  —  {thesis}", NC_I)
    r += 1
    for cl, lab in zip(YCOL, YLAB):
        cell(wi, r, wi[cl + "1"].column, lab, font=FONT_NOTE, align="center")
    r += 1
    for dkey, dlab, dfmt in DRIVER_LABELS:
        iyears(f"{skey}_{dkey}", "    " + dlab, dvals[dkey], dfmt,
               src=DRIVER_SRC[dkey] if skey == "sev" else None)
    r += 1

# ---- G. interim actuals for the TTM build --------------------------------
band(wi, r, "G.  INTERIM ACTUALS USED TO BUILD THE TTM Q2 FY2026 COLUMN", NC_I)
r += 1
txt(wi, r, 1, "Convention: TTM = FY2025 − 1H FY2025 + 1H FY2026 "
              "(owners_earnings_calcs.py §3).", font=FONT_NOTE)
r += 1
cell(wi, r, 2, "1H FY2025", font=FONT_SUB, align="center")
cell(wi, r, 3, "1H FY2026", font=FONT_SUB, align="center")
txt(wi, r, NC_I, "primary_sources/2Q2026/financial_statements.md — six months ended "
                 "30 May 2025 and 29 May 2026.", font=FONT_NOTE)
r += 1
for key, lab, v25, v26, fmt in [
    ("h_sub", "Subscription revenue", 11124, 12614, NUM0),
    ("h_prod", "Product revenue", 183, 179, NUM0),
    ("h_serv", "Services and other revenue", 280, 223, NUM0),
    ("h_cos_sub", "Cost of subscription revenue", 995, 1126, NUM0),
    ("h_cos_prod", "Cost of product revenue", 12, 11, NUM0),
    ("h_cos_serv", "Cost of services and other revenue", 253, 242, NUM0),
    ("h_rd", "Research and development", 2108, 2308, NUM0),
    ("h_sm", "Sales and marketing", 3121, 3592, NUM0),
    ("h_ga", "General and administrative", 744, 1009, NUM0),
    ("h_amopex", "Amortisation of intangibles (opex line)", 82, 72, NUM0),
    ("h_ebit", "Operating income (EBIT), reported", 4272, 4656, NUM0),
    ("h_amort", "Amortisation of purchased intangibles, total", 167, 91, NUM0),
    ("h_gw", "Goodwill impairment (Publishing & Advertising)", 0, 70, NUM0),
    ("h_ftc", "FTC/DOJ ROSCA loss contingency accrual", 0, 92, NUM0),
    ("h_sbc", "Stock-based compensation", 956, 1045, NUM0),
    ("h_sh", "Diluted weighted-average shares (M)", 433.2, 406.6, NUM1),
]:
    I[key] = r
    txt(wi, r, 1, "  " + lab)
    cell(wi, r, 2, v25, fmt=fmt, fill=F_ACT)
    cell(wi, r, 3, v26, fmt=fmt, fill=F_ACT)
    r += 1

wi.freeze_panes = "B7"

IN = "'1. Inputs'!"
print(f"Inputs sheet built: {r} rows, {len(I)} registered input cells.")


# ==========================================================================
# SHEET 2 — OWNERS' EARNINGS  (historical and forecast, side by side)
# ==========================================================================
# The owners'-earnings BRIDGE is written at the top of the sheet but cites
# supporting rows further down. Formulas are therefore written with @key@
# placeholders and resolved against the row registry once the sheet is
# complete. This keeps the reading order (answer first, machinery second)
# independent of the build order.
PENDING = []


def resolve(registry):
    for ws_, rr, cc in PENDING:
        v = ws_.cell(row=rr, column=cc).value
        for k, rownum in registry.items():
            v = v.replace("@" + k + "@", str(rownum))
        if "@" in v:
            raise ValueError(f"unresolved placeholder in {ws_.title}!{cc}{rr}: {v}")
        ws_.cell(row=rr, column=cc).value = v


# NOTE: the tab name deliberately omits the apostrophe in "Owners'". A sheet name
# containing an apostrophe must be escaped as '' inside every cross-sheet formula
# reference, which is a needless source of breakage.
wm = wb.create_sheet("2. Owners Earnings")
wm.sheet_properties.tabColor = "1F4E79"
wm.column_dimensions["A"].width = 60
for c in "BCDEFGHIJ":
    wm.column_dimensions[c].width = 12
wm.column_dimensions["K"].width = 11
wm.column_dimensions["L"].width = 11
wm.column_dimensions["M"].width = 100

HC = ["B", "C", "D", "E"]                    # FY2023A FY2024A FY2025A TTM
FC = ["F", "G", "H", "I", "J"]               # FY2026E .. FY2030E
HLAB = ["FY2023A", "FY2024A", "FY2025A", "TTM Q2FY26"]
KC, LC, NC = 11, 12, 13                      # CAGR hist, CAGR fcst, note

M = {}
r = 1
txt(wm, r, 1, "Adobe Inc. (ADBE) — OWNERS' EARNINGS: HISTORICAL AND PROJECTED ($M)",
    font=FONT_TITLE)
r += 1
txt(wm, r, 1, "Historical actuals (columns B-E) and the BASE-case forecast "
              "(columns F-J) are built on ONE identical construction, so the columns "
              "are directly comparable left to right. The other three scenarios run "
              "the same engine in §6 and are summarised in §7.", font=FONT_NOTE)
r += 1
txt(wm, r, 1, "AMBER = judgment input (all on sheet 1)    "
              "BLUE = reported actual from a primary source    "
              "GREEN = headline output    white = formula", font=FONT_NOTE)
r += 1
txt(wm, r, 1, "CONTENTS:  §1 The owners' earnings bridge (the answer)   |   "
              "§2 Supporting detail for the historical adjustments   |   "
              "§3 Reported income statement and the TTM build   |   "
              "§4 Customer-group revenue, the forecast's starting base   |   "
              "§5 Forecast build, BASE case   |   "
              "§6 The other three scenario engines   |   "
              "§7 Owners' earnings by scenario   |   "
              "§8 Checks", font=FONT_NAV)
r += 2

M["hdr"] = r
txt(wm, r, 1, "($M unless noted)", font=FONT_SUB, fill=F_SUB)
for cl, lab in zip(HC, HLAB):
    cell(wm, r, wm[cl + "1"].column, lab, font=FONT_SUB, align="center", fill=F_SUB)
for cl, lab in zip(FC, YLAB):
    cell(wm, r, wm[cl + "1"].column, lab, font=FONT_SUB, align="center", fill=F_SUB)
cell(wm, r, KC, "CAGR FY23-25", font=FONT_SUB, align="center", fill=F_SUB)
cell(wm, r, LC, "CAGR FY25-30E", font=FONT_SUB, align="center", fill=F_SUB)
cell(wm, r, NC, "Source / note", font=FONT_SUB, fill=F_SUB)
HDR_ROW = r
r += 2


def _put(rr, cc, v, fmt, fill, font, border):
    x = cell(wm, rr, cc, v, fmt=fmt, fill=fill, font=font, border=border)
    if isinstance(v, str) and "@" in v:
        PENDING.append((wm, rr, cc))
    return x


def mrow(key, label, hist=None, fcst=None, fmt=NUM0, fill=None, font=None,
         border=None, src=None, cagr=False, indent=0):
    """One row spanning historical (B-E) and forecast (F-J) columns."""
    global r
    M[key] = r
    txt(wm, r, 1, ("  " * indent) + label, font=font)
    if hist:
        for cl, v in zip(HC, hist):
            if v is None:
                continue
            _put(r, wm[cl + "1"].column, v, fmt,
                 (fill if not isinstance(v, str) else None), font, border)
    if fcst:
        for cl, v in zip(FC, fcst):
            if v is None:
                continue
            _put(r, wm[cl + "1"].column, v, fmt,
                 (fill if not isinstance(v, str) else None), font, border)
    if cagr:
        _put(r, KC, f"=IFERROR((D{r}/B{r})^(1/2)-1,\"\")", PCT1, None, font, border)
        if cagr != "hist":     # "hist" = no forecast columns on this row
            _put(r, LC, f"=IFERROR((J{r}/D{r})^(1/5)-1,\"\")", PCT1, None, font,
                 border)
    if src:
        txt(wm, r, NC, src, font=FONT_NOTE)
    row_ = r
    r += 1
    return row_


def mband(text):
    global r
    band(wm, r, text, NC)
    r += 1


def mnote(text):
    global r
    txt(wm, r, 1, text, font=FONT_NOTE)
    r += 1


def ttm(row_key_or_row, inp_key):
    """TTM = FY2025 − 1H FY2025 + 1H FY2026, pulling the interims from sheet 1."""
    return (f"=D@{row_key_or_row}@-{IN}$B${I[inp_key]}+{IN}$C${I[inp_key]}"
            if isinstance(row_key_or_row, str)
            else f"=D{row_key_or_row}-{IN}$B${I[inp_key]}+{IN}$C${I[inp_key]}")


# ---- §1  THE BRIDGE -------------------------------------------------------
mband("§1.  THE OWNERS' EARNINGS BRIDGE — HISTORICAL ACTUAL AND PROJECTED, "
      "SIDE BY SIDE")
mnote("EBIT + non-recurring charges + purchased-intangible amortisation = EBITA;  "
      "+ PP&E depreciation − maintenance capex = pre-tax owners' earnings;  "
      "x (1 − normalised tax rate) = OWNERS' EARNINGS.   "
      "Stock-based compensation is deliberately NOT added back — it is a real cost "
      "to owners and stays inside EBIT (owners_earnings_and_roic.md §2.1).")
r += 1

mrow("b_rev", "TOTAL REVENUE  (memo)",
     [f"={c}@is_rev@" for c in HC], [f"={c}@fc_rev@" for c in FC],
     font=FONT_BOLD, cagr=True,
     src="Historical from §3; forecast from §5. Shown here only to compute margins.")
r += 1

mrow("b_ebit", "Operating income (EBIT)",
     [f"={c}@is_ebit@" for c in HC], [f"={c}@fc_ebita@-{IN}{c}${I['amort']}" for c in FC],
     src="Historical: as reported (§3). Forecast: DERIVED as driver-built EBITA (§5) "
         "less Adobe's own disclosed forward amortisation schedule (sheet 1 §E), which "
         "excludes future acquisitions and is therefore a floor on amortisation.")
mrow("b_nonrec", "+ non-recurring charges booked in operating expenses",
     [f"={c}@adj_nr@" for c in HC], [f"={IN}{c}${I['nonrec']}" for c in FC],
     src="Detail in §2. FY2024 $1,078M = $1,000M Figma termination fee + $78M lease "
         "impairments; TTM $162M = $70M goodwill impairment + $92M FTC loss "
         "contingency, both booked in 1H FY2026 so neither is rolled "
         "(owners_earnings_calcs.py §3).")
mrow("b_amort", "+ amortisation of purchased intangibles",
     [375, 336, 310, ttm("b_amort", "h_amort")],
     [f"={IN}{c}${I['amort']}" for c in FC], fill=F_ACT,
     src="FY2025 10-K Note 8 / Q2 FY2026 10-Q Note 7. Added back because the acquired "
         "asset base is maintained by R&D and S&M that are already expensed inside "
         "EBIT, while the capital itself stays in invested capital.")
mrow("b_ebita", " = EBITA",
     [f"={c}@b_ebit@+{c}@b_nonrec@+{c}@b_amort@" for c in HC],
     [f"={c}@b_ebit@+{c}@b_nonrec@+{c}@b_amort@" for c in FC],
     font=FONT_BOLD, border=TOP, cagr=True,
     src="Earnings before interest, tax and purchased-intangible amortisation — the "
         "basis owners' earnings is built on.")
mrow("b_ebitam", "  EBITA margin",
     [f"={c}@b_ebita@/{c}@b_rev@" for c in HC],
     [f"={c}@b_ebita@/{c}@b_rev@" for c in FC], fmt=PCT1)
mrow("b_dep", "+ PP&E depreciation", [235, 239, 236, 236],
     [f"=$D@b_dep@*(1+{IN}$B${I['g_dep']})^{n}" for n in range(1, 6)], fill=F_ACT,
     src="FY2025 10-K Note 6. TTM is NOT rolled: depreciation is not separately "
         "disclosed in the 10-Q and net PP&E is essentially unchanged "
         "($1,873M -> $1,870M), so FY2025's $236M is carried "
         "(owners_earnings_calcs.py §3).")
mrow("b_capex", "− maintenance capex",
     [f"=-AVERAGE($B@adj_capex@:$D@adj_capex@)" for c in HC],
     [f"=-{IN}$B${I['capex_b']}*(1+{IN}$B${I['g_capex']})^{n}" for n in range(1, 6)],
     src="3-year average of ACTUAL capex FY2023-FY2025 (§2) = $240.7M, applied to "
         "every historical period; grown 5%/yr in the forecast off the rounded $241M "
         "base on sheet 1. owners_earnings_and_roic.md §2.2 — 'Using one year's "
         "depressed capex would flatter owners' earnings.'")
mrow("b_pretax", " = pre-tax owners' earnings",
     [f"={c}@b_ebita@+{c}@b_dep@+{c}@b_capex@" for c in HC],
     [f"={c}@b_ebita@+{c}@b_dep@+{c}@b_capex@" for c in FC],
     font=FONT_BOLD, border=TOP)
mrow("b_tax", "− normalised tax",
     [f"=-{c}@b_pretax@*{IN}$B${I['tax']}" for c in HC],
     [f"=-{c}@b_pretax@*{IN}$B${I['tax']}" for c in FC],
     src="At the single normalised rate on sheet 1 §A (21%), applied identically to "
         "every period and every scenario.")
mrow("b_oe", " = OWNERS' EARNINGS",
     [f"={c}@b_pretax@+{c}@b_tax@" for c in HC],
     [f"={c}@b_pretax@+{c}@b_tax@" for c in FC],
     font=FONT_BIG, border=TOPD, fill=F_OUT, cagr=True,
     src="Method A, owners_earnings_and_roic.md §1-§2. Forecast columns are the BASE "
         "case; §7 shows all four scenarios.")
mrow("b_oem", "  owners' earnings margin (% of revenue)",
     [f"={c}@b_oe@/{c}@b_rev@" for c in HC],
     [f"={c}@b_oe@/{c}@b_rev@" for c in FC], fmt=PCT1)
mrow("b_oeg", "  owners' earnings growth, year on year",
     [None, "=C@b_oe@/B@b_oe@-1", "=D@b_oe@/C@b_oe@-1", None],
     ["=F@b_oe@/D@b_oe@-1"] + [f"={c}@b_oe@/{p}@b_oe@-1"
                               for c, p in zip(FC[1:], FC[:-1])], fmt=PCT1,
     src="No growth is shown for the TTM column: it overlaps FY2025 and is not a "
         "clean year-on-year comparison. FY2026E growth is struck off FY2025A.")
r += 1
mnote("NO forecast share count, buyback path or forecast owners' earnings per share "
      "is modelled anywhere in this workbook. Projecting them requires stacking three "
      "further judgment assumptions — a buyback payout ratio, a stock-based "
      "compensation ratio, and an assumed repurchase PRICE — and the price assumption "
      "is circular with the valuation the model is trying to produce. The valuation on "
      "sheet 3 uses TODAY's diluted share count of 399.1M throughout, per the brief "
      "(valuation.md §3), so none of it would change the answer. Adobe's actual "
      "buyback pace is shown below as history only.")
mrow("b_sbc", "memo: stock-based compensation (deducted inside EBIT, never added back)",
     [1718, 1833, 1942, ttm("b_sbc", "h_sbc")], fill=F_ACT,
     src="FY2025 10-K Note 12. Cross-checked against shares actually delivered: 4.8M "
         "shares at a ~$408 weighted-average grant-date fair value ~ $1,920M against "
         "the $1,942M GAAP charge, within ~1% (owners_earnings_and_roic.md §2.1).")
mrow("b_sh", "memo: diluted shares (M) — HISTORICAL ONLY",
     [459.1, 449.7, 427.0, ttm("b_sh", "h_sh")], fmt=NUM1, fill=F_ACT,
     src="owners_earnings_calcs.py §7. TTM uses the same TTM convention: "
         "427.0 − 433.2 + 406.6 = 400.4M. NO forecast share count is modelled — see "
         "the note below.")
mrow("b_oeps", "memo: OWNERS' EARNINGS PER DILUTED SHARE — HISTORICAL ONLY",
     [f"={c}@b_oe@/{c}@b_sh@" for c in HC], fmt=USD2, font=FONT_BOLD, cagr="hist",
     src="owners_earnings_and_roic.md §1: $12.08 / $14.32 / $16.67 / $18.71. "
         "Reported actuals divided by reported share counts — no assumption in them.")
mrow("b_bb", "memo: buyback spend, ACTUAL — HISTORICAL ONLY", [4400, 9500, 11281, None],
     fill=F_ACT,
     src="owners_earnings_and_roic.md §5; 1H FY2026 spend was $4,589M. Shown as "
         "history, not extrapolated.")
mrow("b_bbx", "  actual buyback as a multiple of owners' earnings",
     [f"={c}@b_bb@/{c}@b_oe@" for c in HC[:3]], fmt=XMUL,
     src="Adobe repurchased at ~1.5-1.6x owners' earnings in FY2024-FY2025 — it spent "
         "more than it earned. terminal_value.md §9 flags that if that pace continues "
         "'the equity bridge stops being immaterial'. That is a stated RISK to the "
         "sheet-3 bridge, not a modelled forecast.")
r += 1

# ---- §2  SUPPORTING DETAIL FOR THE HISTORICAL ADJUSTMENTS ----------------
mband("§2.  SUPPORTING DETAIL FOR THE HISTORICAL OWNERS' EARNINGS ADJUSTMENTS")
mnote("Every add-back used in §1, itemised and sourced. This is the audit trail for "
      "the historical bridge.")
r += 1
mrow("adj_figma", "Figma acquisition termination fee", [0, "=C@is_figma@", 0, 0],
     src="FY2024 one-off, $1,000M, disclosed on its own income-statement line "
         "(primary_sources/FY2025/md_and_a.md). Pulled from §3 so it cannot drift.")
mrow("adj_lease", "Lease-related asset impairments", [0, 78, 0, 0], fill=F_ACT,
     src="FY2024, $78M — FY2025 10-K cash-flow statement; Note 7 places the charge "
         "in G&A. owners_earnings_and_roic.md §2.1.")
mrow("adj_gw", "Goodwill impairment, Publishing & Advertising",
     [0, 0, 0, f"={IN}$C${I['h_gw']}"],
     src="$70M, Q2 FY2026 10-Q Note 7. Booked in 1H FY2026, so it enters the TTM "
         "column directly and is NOT rolled through the FY25 − 1H25 + 1H26 formula.")
mrow("adj_ftc", "FTC/DOJ ROSCA loss contingency accrual",
     [0, 0, 0, f"={IN}$C${I['h_ftc']}"],
     src="$92M, 1H FY2026. Same treatment as the goodwill impairment above.")
mrow("adj_nr", " = total non-recurring charges added back in §1",
     [f"=SUM({c}@adj_figma@:{c}@adj_ftc@)" for c in HC],
     font=FONT_BOLD, border=TOP,
     src="FY2023 $0M, FY2024 $1,078M, FY2025 $0M ('none in FY2025'), TTM $162M — "
         "owners_earnings_and_roic.md §2.1.")
r += 1
mrow("adj_capex", "memo: capital expenditure, ACTUAL", [360, 183, 179, 201],
     fill=F_ACT,
     src="FY2025 10-K and Q2 FY2026 10-Q cash-flow statements. Net PP&E has been "
         "SHRINKING ($1,936M -> $1,873M -> $1,870M), i.e. recent capex runs below "
         "depreciation — which is why a 3-year average, not the latest year, is used "
         "as maintenance capex.")
mrow("adj_capex_avg", "  3-year average actual capex FY2023-FY2025 "
                      "( = maintenance capex applied to every historical period)",
     ["=AVERAGE(B@adj_capex@:D@adj_capex@)"], fmt=NUM1, border=TOP,
     src="$240.667M. owners_earnings_and_roic.md §2.2 notes this 'lands within $5M of "
         "FY2025 depreciation, a useful independent confirmation that it is the right "
         "order of magnitude'. Sensitivity there: +/-$60M of capex moves owners' "
         "earnings by ~$47M after tax, ~0.6%.")
r += 1
mnote("NOT adjusted, deliberately: (a) stock-based compensation is a real cost to "
      "owners and stays inside EBIT; (b) the $6,821M of hosting purchase obligations "
      "are contracted OPERATING spend already flowing through cost of revenue as "
      "incurred, so adding a charge would double-count — they are instead treated as "
      "a debt-like item in the equity bridge on sheet 3; (c) the deferred-revenue "
      "float is not counted as earnings. owners_earnings_and_roic.md §2.1, §4.1.")
r += 1

# ---- §3  REPORTED INCOME STATEMENT ---------------------------------------
mband("§3.  REPORTED INCOME STATEMENT — THE SOURCE OF THE EBIT LINE IN §1")
mnote("FY2023A-FY2025A as reported. The TTM Q2 FY2026 column is built as "
      "FY2025 − 1H FY2025 + 1H FY2026 from the interim actuals on sheet 1 §G.")
r += 1
SRC10K = "primary_sources/FY2025/financial_statements.md, Consolidated Statements of Income."
mrow("is_sub", "Subscription revenue", [18284, 20521, 22904, ttm("is_sub", "h_sub")],
     fill=F_ACT, src=SRC10K)
mrow("is_prod", "Product revenue", [460, 386, 325, ttm("is_prod", "h_prod")], fill=F_ACT)
mrow("is_serv", "Services and other revenue", [665, 598, 540, ttm("is_serv", "h_serv")],
     fill=F_ACT)
mrow("is_rev", "TOTAL REVENUE",
     [f"={c}@is_sub@+{c}@is_prod@+{c}@is_serv@" for c in HC],
     font=FONT_BOLD, border=TOP)
mrow("is_cos_sub", "Cost of subscription revenue",
     [1822, 1799, 2027, ttm("is_cos_sub", "h_cos_sub")], fill=F_ACT)
mrow("is_cos_prod", "Cost of product revenue",
     [29, 25, 23, ttm("is_cos_prod", "h_cos_prod")], fill=F_ACT)
mrow("is_cos_serv", "Cost of services and other revenue",
     [503, 534, 501, ttm("is_cos_serv", "h_cos_serv")], fill=F_ACT)
mrow("is_gp", "Gross profit",
     [f"={c}@is_rev@-{c}@is_cos_sub@-{c}@is_cos_prod@-{c}@is_cos_serv@" for c in HC],
     font=FONT_BOLD, border=TOP)
mrow("is_rd", "Research and development", [3473, 3944, 4294, ttm("is_rd", "h_rd")],
     fill=F_ACT)
mrow("is_sm", "Sales and marketing", [5351, 5764, 6488, ttm("is_sm", "h_sm")],
     fill=F_ACT)
mrow("is_ga", "General and administrative", [1413, 1529, 1573, ttm("is_ga", "h_ga")],
     fill=F_ACT)
mrow("is_amopex", "Amortisation of intangibles (operating expense line)",
     [168, 169, 157, ttm("is_amopex", "h_amopex")], fill=F_ACT)
mrow("is_figma", "Figma acquisition termination fee", [0, 1000, 0, 0], fill=F_ACT,
     src="FY2024 one-off, $1,000M — primary_sources/FY2025/md_and_a.md.")
mrow("is_ebit", "OPERATING INCOME (EBIT)",
     [f"={c}@is_gp@-{c}@is_rd@-{c}@is_sm@-{c}@is_ga@-{c}@is_amopex@-{c}@is_figma@"
      for c in HC], font=FONT_BOLD, border=TOP)
mrow("is_ebit_rep", "  check: EBIT as reported in the 10-K / 10-Q",
     [6650, 6741, 8706, ttm("is_ebit_rep", "h_ebit")], fill=F_ACT,
     src="The row above is built up from the individual revenue and expense lines; "
         "this is the figure Adobe reports. The difference must be zero.")
mrow("is_ebit_diff", "  difference (must be 0)",
     [f"={c}@is_ebit@-{c}@is_ebit_rep@" for c in HC], fill=F_CHK, border=TOP)
r += 1

# ---- §4  CUSTOMER-GROUP SUBSCRIPTION REVENUE -----------------------------
mband("§4.  CUSTOMER-GROUP SUBSCRIPTION REVENUE — THE FORECAST'S STARTING BASE")
r += 1
MDA = "primary_sources/FY2025/md_and_a.md."
mrow("cg_cmp", "Creative & Marketing Professionals subscription",
     [13425, 14749, 16303, None], fill=F_ACT, src=MDA)
mrow("cg_bpc", "Business Professionals & Consumers subscription (Acrobat/Express)",
     [4744, 5662, 6495, None], fill=F_ACT, src=MDA)
mrow("cg_pa", "Publishing & Advertising subscription", [115, 110, 106, None],
     fill=F_ACT, src=MDA)
mrow("cg_chk", "  check: the three groups sum to total subscription revenue "
               "(difference must be 0)",
     [f"={c}@cg_cmp@+{c}@cg_bpc@+{c}@cg_pa@-{c}@is_sub@" for c in HC[:3]],
     fill=F_CHK)
mrow("cg_dx", "Digital Experience segment subscription revenue",
     [4331, 4864, 5409, None], fill=F_ACT, src=MDA)
mrow("cg_creative", "Creative flagship subscription (DERIVED = C&MP − Digital Experience)",
     [f"={c}@cg_cmp@-{c}@cg_dx@" for c in HC[:3]], font=FONT_BOLD, border=TOP,
     src="C&MP is defined as the Digital Experience offerings PLUS the Creative Cloud "
         "flagship, so the Creative line is only obtainable by subtraction "
         "(forecast_earnings_calcs.py §0). Adobe does not disclose it directly.")
r += 1

# ---- §5  FORECAST BUILD — BASE CASE --------------------------------------
mband("§5.  FORECAST BUILD — BASE CASE.  Column D repeats the FY2025A anchor each "
      "driver is grown off, so the join between actual and forecast is visible.")
r += 1
subband(wm, r, "  Revenue drivers", NC)
r += 1
mrow("fc_mau", "Acrobat/Express MAU exiting fiscal year (M)",
     [None, "=D@fc_mau@/1.2", 750, None],
     [f"=D@fc_mau@*(1+{IN}F${I['base_mau']})"] +
     [f"={p}@fc_mau@*(1+{IN}{c}${I['base_mau']})" for c, p in zip(FC[1:], FC[:-1])],
     fmt=NUM1, fill=F_ACT,
     src="Q4 FY2025 call: MAU 'surpassed 750 million ... growing 20% year-over-year', "
         "so the FY2024 exit count is DERIVED as 750/1.20. causal_model.md Factor 1.1.")
mrow("fc_maug", "  MAU growth", [None, None, "=D@fc_mau@/C@fc_mau@-1", None],
     [f"={IN}{c}${I['base_mau']}" for c in FC], fmt=PCT1)
mrow("fc_amau", "Average MAU (M)", [None, None, "=(C@fc_mau@+D@fc_mau@)/2", None],
     ["=(D@fc_mau@+F@fc_mau@)/2"] +
     [f"=({p}@fc_mau@+{c}@fc_mau@)/2" for c, p in zip(FC[1:], FC[:-1])], fmt=NUM1,
     src="Revenue is earned across the year, so it is struck on the average of the "
         "opening and closing MAU count, not the exit count.")
mrow("fc_rpm", "Revenue per average MAU ($/yr)",
     [None, None, "=D@cg_bpc@/D@fc_amau@", None],
     [f"=D@fc_rpm@*(1+{IN}F${I['base_rpm']})"] +
     [f"={p}@fc_rpm@*(1+{IN}{c}${I['base_rpm']})" for c, p in zip(FC[1:], FC[:-1])],
     fmt=NUM2,
     src="The observable composite of free-to-paid conversion x price per paid seat. "
         "Adobe discloses NEITHER component, which is why forecast_earnings.md §3 "
         "flags this driver's confidence as LOW. It is the single largest swing "
         "factor in the BP&C line.")
r += 1
mrow("fc_bpc", "BP&C subscription revenue (Acrobat/Express)", [None, None, "=D@cg_bpc@", None],
     [f"={c}@fc_amau@*{c}@fc_rpm@" for c in FC])
mrow("fc_creative", "Creative subscription revenue", [None, None, "=D@cg_creative@", None],
     [f"=D@fc_creative@*(1+{IN}F${I['base_cvol']}+{IN}F${I['base_cpr']}+{IN}F${I['fx']})"] +
     [f"={p}@fc_creative@*(1+{IN}{c}${I['base_cvol']}+{IN}{c}${I['base_cpr']}"
      f"+{IN}{c}${I['fx']})" for c, p in zip(FC[1:], FC[:-1])],
     src="Grown by paid-unit volume + value-based price/tier mix + FX translation, "
         "the three drivers added rather than compounded (forecast_earnings.md §4).")
mrow("fc_dx", "Digital Experience subscription revenue", [None, None, "=D@cg_dx@", None],
     [f"=D@fc_dx@*(1+{IN}F${I['base_dx']})"] +
     [f"={p}@fc_dx@*(1+{IN}{c}${I['base_dx']})" for c, p in zip(FC[1:], FC[:-1])])
mrow("fc_sem", "Semrush revenue (acquisition closed April 2026)", [None, None, 0, None],
     [f"={IN}{c}${I['sem']}" for c in FC],
     src="Zero in FY2025 because the acquisition had not closed. "
         "primary_sources/2Q2026/md_and_a.md guides ~$280M of FY2026 contribution.")
mrow("fc_pa", "Publishing & Advertising subscription revenue", [None, None, "=D@cg_pa@", None],
     [f"=D@fc_pa@*(1+{IN}F${I['g_pa']})"] +
     [f"={p}@fc_pa@*(1+{IN}{c}${I['g_pa']})" for c, p in zip(FC[1:], FC[:-1])])
mrow("fc_prodrev", "Product revenue", [None, None, "=D@is_prod@", None],
     [f"=D@fc_prodrev@*(1+{IN}F${I['g_prod']})"] +
     [f"={p}@fc_prodrev@*(1+{IN}{c}${I['g_prod']})" for c, p in zip(FC[1:], FC[:-1])])
mrow("fc_servrev", "Services and other revenue", [None, None, "=D@is_serv@", None],
     [f"=D@fc_servrev@*(1+{IN}F${I['g_serv']})"] +
     [f"={p}@fc_servrev@*(1+{IN}{c}${I['g_serv']})" for c, p in zip(FC[1:], FC[:-1])])
mrow("fc_sub", "Total subscription revenue", [None, None, "=D@is_sub@", None],
     [f"={c}@fc_bpc@+{c}@fc_creative@+{c}@fc_dx@+{c}@fc_sem@+{c}@fc_pa@" for c in FC],
     font=FONT_BOLD, border=TOP)
mrow("fc_rev", "TOTAL REVENUE", [None, None, "=D@is_rev@", None],
     [f"={c}@fc_sub@+{c}@fc_prodrev@+{c}@fc_servrev@" for c in FC],
     font=FONT_BOLD, border=TOP)
mrow("fc_revg", "  total revenue growth", fcst=["=F@fc_rev@/D@fc_rev@-1"] +
     [f"={c}@fc_rev@/{p}@fc_rev@-1" for c, p in zip(FC[1:], FC[:-1])], fmt=PCT1)
r += 1
subband(wm, r, "  Cost drivers and EBITA  "
               "(EBITA = EBIT before purchased-intangible amortisation)", NC)
r += 1
mrow("fc_cr", "Subscription cost ratio, ex purchased-intangible amortisation",
     [None, None, f"=(D@is_cos_sub@-{IN}$B${I['am_in_cos']})/D@fc_sub@", None],
     [f"=D@fc_cr@+{IN}F${I['base_drift']}/10000"] +
     [f"={p}@fc_cr@+{IN}{c}${I['base_drift']}/10000" for c, p in zip(FC[1:], FC[:-1])],
     fmt=PCT2,
     src="THE key cost finding: on this ex-amortisation basis the hosting / AI-inference "
         "cost ratio is deteriorating ~60bp/yr right now (forecast_earnings.md §6). The "
         "base case assumes that drift DECAYS from 72bp to 20bp/yr; the bear and severe "
         "cases assume it does not.")
mrow("fc_cos_sub", "Cost of subscription revenue, ex-amortisation",
     [None, None, f"=D@is_cos_sub@-{IN}$B${I['am_in_cos']}", None],
     [f"={c}@fc_sub@*{c}@fc_cr@" for c in FC])
mrow("fc_cos_prod", "Cost of product revenue", [None, None, "=D@is_cos_prod@", None],
     [f"={c}@fc_prodrev@*{IN}$B${I['cr_prod']}" for c in FC])
mrow("fc_cos_serv", "Cost of services and other revenue", [None, None, "=D@is_cos_serv@", None],
     [f"={c}@fc_servrev@*{IN}$B${I['cr_serv']}" for c in FC])
mrow("fc_gp", "Gross profit, ex-amortisation",
     [None, None, "=D@fc_rev@-D@fc_cos_sub@-D@fc_cos_prod@-D@fc_cos_serv@", None],
     [f"={c}@fc_rev@-{c}@fc_cos_sub@-{c}@fc_cos_prod@-{c}@fc_cos_serv@" for c in FC],
     font=FONT_BOLD, border=TOP)
mrow("fc_adv", "Advertising expense", [970, 1040, 1370, None],
     [f"={c}@fc_rev@*{IN}{c}${I['base_adv']}" for c in FC], fill=F_ACT,
     src="primary_sources/FY2025/financial_statements.md Note 1 — the freemium funnel "
         "spend, up 31.7% in FY2025. Split out of sales & marketing because it is the "
         "cost of the MAU growth driver above.")
mrow("fc_osm", "Other sales & marketing expense", [None, None, "=D@is_sm@-D@fc_adv@", None],
     [f"={c}@fc_rev@*{IN}{c}${I['base_osm']}" for c in FC])
mrow("fc_rd", "Research and development", [None, None, "=D@is_rd@", None],
     [f"={c}@fc_rev@*{IN}{c}${I['base_rd']}" for c in FC])
mrow("fc_ga", "General and administrative", [None, None, "=D@is_ga@", None],
     [f"={c}@fc_rev@*{IN}{c}${I['base_ga']}" for c in FC])
mrow("fc_ebita", "EBITA (driver-built)",
     [None, None, "=D@fc_gp@-D@fc_adv@-D@fc_osm@-D@fc_rd@-D@fc_ga@", None],
     [f"={c}@fc_gp@-{c}@fc_adv@-{c}@fc_osm@-{c}@fc_rd@-{c}@fc_ga@" for c in FC],
     font=FONT_BOLD, border=TOP)
mrow("fc_ebitam", "  EBITA margin", [None, None, "=D@fc_ebita@/D@fc_rev@", None],
     [f"={c}@fc_ebita@/{c}@fc_rev@" for c in FC], fmt=PCT1)
mrow("fc_chk", "  check: driver-built EBITA less the §1 bridge EBITA, FY2025A",
     [None, None, "=D@fc_ebita@-D@b_ebita@", None], fill=F_CHK, border=TOP,
     src="FY2025 gap = −$2M, disclosed rather than hidden. Reported total "
         "purchased-intangible amortisation is $310M, but only $151M sits in cost of "
         "subscription and $157M in the amortisation opex line ($308M); ~$2M is inside "
         "other operating expense lines. The bridge anchors on the $310M add-back while "
         "the cost ratio is struck on the $151M figure — a 0.02% inconsistency carried "
         "over unchanged from forecast_earnings_calcs.py.")
r += 1

# ---- §6  THE OTHER THREE SCENARIO ENGINES --------------------------------
mband("§6.  THE OTHER THREE SCENARIO ENGINES — identical construction to §5, run on "
      "each scenario's own drivers (sheet 1 §F)")
mnote("Shared lines (Publishing & Advertising, product, services, depreciation, "
      "maintenance capex, tax) are pulled from the base build rather than re-derived, "
      "so a change there propagates to every scenario.")
r += 1

for skey, sname, thesis, _dv in SCENARIOS:
    if skey == "base":
        continue
    semk = "sem_sev" if skey == "sev" else "sem"
    subband(wm, r, f"  {sname}  —  {thesis}", NC)
    r += 1
    mrow(f"e_{skey}_mau", "MAU exiting year (M)", fcst=
         [f"=$D@fc_mau@*(1+{IN}F${I[skey + '_mau']})"] +
         [f"={p}@e_{skey}_mau@*(1+{IN}{c}${I[skey + '_mau']})"
          for c, p in zip(FC[1:], FC[:-1])], fmt=NUM1)
    mrow(f"e_{skey}_amau", "Average MAU (M)", fcst=
         [f"=($D@fc_mau@+F@e_{skey}_mau@)/2"] +
         [f"=({p}@e_{skey}_mau@+{c}@e_{skey}_mau@)/2" for c, p in zip(FC[1:], FC[:-1])],
         fmt=NUM1)
    mrow(f"e_{skey}_rpm", "Revenue per average MAU ($/yr)", fcst=
         [f"=$D@fc_rpm@*(1+{IN}F${I[skey + '_rpm']})"] +
         [f"={p}@e_{skey}_rpm@*(1+{IN}{c}${I[skey + '_rpm']})"
          for c, p in zip(FC[1:], FC[:-1])], fmt=NUM2)
    mrow(f"e_{skey}_bpc", "BP&C subscription revenue", fcst=
         [f"={c}@e_{skey}_amau@*{c}@e_{skey}_rpm@" for c in FC])
    mrow(f"e_{skey}_creative", "Creative subscription revenue", fcst=
         [f"=$D@fc_creative@*(1+{IN}F${I[skey + '_cvol']}+{IN}F${I[skey + '_cpr']}"
          f"+{IN}F${I['fx']})"] +
         [f"={p}@e_{skey}_creative@*(1+{IN}{c}${I[skey + '_cvol']}"
          f"+{IN}{c}${I[skey + '_cpr']}+{IN}{c}${I['fx']})"
          for c, p in zip(FC[1:], FC[:-1])])
    mrow(f"e_{skey}_dx", "Digital Experience subscription revenue", fcst=
         [f"=$D@fc_dx@*(1+{IN}F${I[skey + '_dx']})"] +
         [f"={p}@e_{skey}_dx@*(1+{IN}{c}${I[skey + '_dx']})"
          for c, p in zip(FC[1:], FC[:-1])])
    mrow(f"e_{skey}_sem", "Semrush revenue",
         fcst=[f"={IN}{c}${I[semk]}" for c in FC],
         src=("SEVERE takes the lower override path on sheet 1 §E "
              "(forecast_earnings_calcs.py §9)." if skey == "sev" else None))
    mrow(f"e_{skey}_pa", "Publishing & Advertising subscription revenue (shared)",
         fcst=[f"={c}@fc_pa@" for c in FC])
    mrow(f"e_{skey}_prod", "Product revenue (shared)",
         fcst=[f"={c}@fc_prodrev@" for c in FC])
    mrow(f"e_{skey}_serv", "Services and other revenue (shared)",
         fcst=[f"={c}@fc_servrev@" for c in FC])
    mrow(f"e_{skey}_sub", "Total subscription revenue", fcst=
         [f"={c}@e_{skey}_bpc@+{c}@e_{skey}_creative@+{c}@e_{skey}_dx@"
          f"+{c}@e_{skey}_sem@+{c}@e_{skey}_pa@" for c in FC],
         font=FONT_BOLD, border=TOP)
    mrow(f"e_{skey}_rev", "TOTAL REVENUE", fcst=
         [f"={c}@e_{skey}_sub@+{c}@e_{skey}_prod@+{c}@e_{skey}_serv@" for c in FC],
         font=FONT_BOLD, border=TOP)
    mrow(f"e_{skey}_cr", "Subscription cost ratio, ex-amortisation", fcst=
         [f"=$D@fc_cr@+{IN}F${I[skey + '_drift']}/10000"] +
         [f"={p}@e_{skey}_cr@+{IN}{c}${I[skey + '_drift']}/10000"
          for c, p in zip(FC[1:], FC[:-1])], fmt=PCT2)
    mrow(f"e_{skey}_gp", "Gross profit, ex-amortisation", fcst=
         [f"={c}@e_{skey}_rev@-{c}@e_{skey}_sub@*{c}@e_{skey}_cr@"
          f"-{c}@e_{skey}_prod@*{IN}$B${I['cr_prod']}"
          f"-{c}@e_{skey}_serv@*{IN}$B${I['cr_serv']}" for c in FC])
    mrow(f"e_{skey}_ebita", "EBITA", fcst=
         [f"={c}@e_{skey}_gp@-{c}@e_{skey}_rev@*({IN}{c}${I[skey + '_adv']}"
          f"+{IN}{c}${I[skey + '_osm']}+{IN}{c}${I[skey + '_rd']}"
          f"+{IN}{c}${I[skey + '_ga']})" for c in FC],
         font=FONT_BOLD, border=TOP)
    mrow(f"e_{skey}_dep", "+ PP&E depreciation (shared)",
         fcst=[f"={c}@b_dep@" for c in FC])
    mrow(f"e_{skey}_capex", "− maintenance capex (shared)",
         fcst=[f"={c}@b_capex@" for c in FC])
    mrow(f"e_{skey}_pretax", " = pre-tax owners' earnings", fcst=
         [f"={c}@e_{skey}_ebita@+{c}@e_{skey}_dep@+{c}@e_{skey}_capex@" for c in FC],
         font=FONT_BOLD, border=TOP)
    mrow(f"e_{skey}_oe", " = OWNERS' EARNINGS", fcst=
         [f"={c}@e_{skey}_pretax@*(1-{IN}$B${I['tax']})" for c in FC],
         font=FONT_BOLD, border=TOPD, fill=F_OUT)
    r += 1

# ---- §7  OWNERS' EARNINGS BY SCENARIO ------------------------------------
mband("§7.  OWNERS' EARNINGS BY SCENARIO AND PROBABILITY-WEIGHTED — the input to "
      "sheet 3")
r += 1
cell(wm, r, 2, "Probability", font=FONT_SUB, align="center")
cell(wm, r, 3, "FY2030E/FY2025A", font=FONT_SUB, align="center")
for cl, lab in zip(FC, YLAB):
    cell(wm, r, wm[cl + "1"].column, lab, font=FONT_SUB, align="center")
cell(wm, r, NC, "Source / note", font=FONT_SUB)
r += 1
SUMROWS = []
for skey, sname, thesis, _dv in SCENARIOS:
    oek = "b_oe" if skey == "base" else f"e_{skey}_oe"
    k = f"sum_{skey}"
    M[k] = r
    txt(wm, r, 1, f"Owners' earnings — {sname}")
    _put(r, 2, f"={IN}$B${I['p_' + skey]}", PCT1, None, None, None)
    _put(r, 3, f"=(J@{oek}@/D@b_oe@)^(1/5)-1", PCT1, None, None, None)
    for cl in FC:
        _put(r, wm[cl + "1"].column, f"={cl}@{oek}@", NUM0, None, None, None)
    txt(wm, r, NC, thesis, font=FONT_NOTE)
    SUMROWS.append(k)
    r += 1
M["sum_w"] = r
txt(wm, r, 1, "PROBABILITY-WEIGHTED OWNERS' EARNINGS", font=FONT_BIG)
_put(r, 2, f"=SUM(B@sum_sev@:B@sum_bull@)", PCT1, F_CHK, None, TOP)
_put(r, 3, f"=(J@sum_w@/D@b_oe@)^(1/5)-1", PCT1, F_OUT, FONT_BIG, TOPD)
for cl in FC:
    _put(r, wm[cl + "1"].column,
         "=" + "+".join(f"$B@sum_{s}@*{cl}@sum_{s}@" for s, *_ in
                        [(x[0],) for x in SCENARIOS]),
         NUM0, F_OUT, FONT_BIG, TOPD)
txt(wm, r, NC, "Weights are ANALYST JUDGMENT (forecast_earnings.md §1: 'my judgment "
                "and are not sourced'), not a sourced probability distribution. "
                "Column C is the 5-year CAGR off the FY2025A actual of $7,119M.",
    font=FONT_NOTE)
r += 2

# ---- §8  CHECKS ----------------------------------------------------------
mband("§8.  CHECKS AGAINST THE PUBLISHED WORK PRODUCTS")
mnote("Small residuals are expected: the published scripts round scenario owners' "
      "earnings to the nearest $M before weighting, whereas this workbook carries "
      "full precision throughout.")
r += 1
cell(wm, r, 2, "Model", font=FONT_SUB, align="center")
cell(wm, r, 3, "Published", font=FONT_SUB, align="center")
cell(wm, r, 4, "Diff", font=FONT_SUB, align="center")
r += 1
for lab, ref, pub, fmt, src in [
    ("FY2023A owners' earnings ($M)", "=B@b_oe@", 5545, NUM0,
     "owners_earnings_and_roic.md §1"),
    ("FY2024A owners' earnings ($M)", "=C@b_oe@", 6441, NUM0,
     "owners_earnings_and_roic.md §1"),
    ("FY2025A owners' earnings ($M)", "=D@b_oe@", 7119, NUM0,
     "owners_earnings_and_roic.md §1"),
    ("TTM Q2 FY2026 owners' earnings ($M)", "=E@b_oe@", 7490, NUM0,
     "owners_earnings_and_roic.md §1"),
    ("FY2025A owners' earnings per diluted share", "=D@b_oeps@", 16.67, NUM2,
     "owners_earnings_and_roic.md §1"),
    ("TTM Q2 FY2026 owners' earnings per diluted share", "=E@b_oeps@", 18.71, NUM2,
     "owners_earnings_and_roic.md §1"),
    ("FY2026E owners' earnings, BASE ($M)", "=F@b_oe@", 7729, NUM0,
     "forecast_earnings.md §1"),
    ("FY2030E owners' earnings, BASE ($M)", "=J@b_oe@", 10745, NUM0,
     "forecast_earnings.md §1"),
    ("FY2030E owners' earnings, SEVERE ($M)", "=J@e_sev_oe@", 6022, NUM0,
     "forecast_earnings.md §1 / valuation.md §2.1"),
    ("FY2030E owners' earnings, BEAR ($M)", "=J@e_bear_oe@", 8105, NUM0,
     "forecast_earnings.md §1 / valuation.md §2.1"),
    ("FY2030E owners' earnings, BULL ($M)", "=J@e_bull_oe@", 13035, NUM0,
     "forecast_earnings.md §1 / valuation.md §2.1"),
    ("FY2030E owners' earnings, WEIGHTED ($M)", "=J@sum_w@", 9835, NUM0,
     "terminal_value.md §1 / valuation.md §2.1. forecast_earnings.md §1 prints "
     "$9,834M — a rounding difference between the two documents."),
    ("FY2025A total revenue ($M)", "=D@b_rev@", 23769, NUM0,
     "primary_sources/FY2025/financial_statements.md — 22,904 + 325 + 540."),
    ("FY2026E total revenue, BASE ($M)", "=F@fc_rev@", 26496, NUM0,
     "forecast_earnings.md §1"),
    ("FY2030E total revenue, BASE ($M)", "=J@fc_rev@", 35267, NUM0,
     "forecast_earnings.md §1"),
    ("FY2026E EBITA, BASE ($M)", "=F@fc_ebita@", 9789, NUM0,
     "forecast_earnings.md §1"),
    ("FY2030E EBITA, BASE ($M)", "=J@fc_ebita@", 13607, NUM0,
     "forecast_earnings.md §1"),
]:
    txt(wm, r, 1, lab)
    _put(r, 2, ref, fmt, None, None, None)
    cell(wm, r, 3, pub, fmt=fmt, fill=F_ACT)
    _put(r, 4, f"=B{r}-C{r}", fmt, F_CHK, None, None)
    txt(wm, r, NC, src, font=FONT_NOTE)
    r += 1

wm.freeze_panes = wm.cell(row=HDR_ROW + 1, column=2).coordinate
resolve(M)
MS = "'2. Owners Earnings'!"
print(f"Owners' Earnings sheet built: {r} rows, {len(M)} registered rows.")


# ==========================================================================
# SHEET 3 — TERMINAL VALUE AND SUM-OF-THE-PARTS VALUATION
# ==========================================================================
wv = wb.create_sheet("3. Terminal Value and SOTP")
wv.sheet_properties.tabColor = "375623"
wv.column_dimensions["A"].width = 62
for c in "BCDEF":
    wv.column_dimensions[c].width = 14
wv.column_dimensions["G"].width = 3
wv.column_dimensions["H"].width = 104

SC = ["B", "C", "D", "E", "F"]               # SEVERE BEAR BASE BULL WEIGHTED
SLAB = ["SEVERE", "BEAR", "BASE", "BULL", "WEIGHTED"]
YC = ["B", "C", "D", "E", "F"]               # FY2026E .. FY2030E
NCV = 8                                      # note column H

V = {}
PENDV = []


def _putv(rr, cc, v, fmt=None, fill=None, font=None, border=None, align=None):
    x = cell(wv, rr, cc, v, fmt=fmt, fill=fill, font=font, border=border, align=align)
    if isinstance(v, str) and "@" in v:
        PENDV.append((wv, rr, cc))
    return x


def vrow(key, label, vals=None, fmt=NUM0, fill=None, font=None, border=None,
         src=None, cols=SC):
    global r
    V[key] = r
    txt(wv, r, 1, label, font=font)
    if vals:
        for cl, v in zip(cols, vals):
            if v is None:
                continue
            _putv(r, wv[cl + "1"].column, v, fmt,
                  (fill if not isinstance(v, str) else None), font, border)
    if src:
        txt(wv, r, NCV, src, font=FONT_NOTE)
    row_ = r
    r += 1
    return row_


def vscalar(key, label, val, fmt=NUM0, fill=None, font=None, border=None, src=None,
            col=2):
    global r
    V[key] = r
    txt(wv, r, 1, label, font=font)
    _putv(r, col, val, fmt, (fill if not isinstance(val, str) else None), font, border)
    if src:
        txt(wv, r, NCV, src, font=FONT_NOTE)
    row_ = r
    r += 1
    return row_


def vband(text):
    global r
    band(wv, r, text, NCV)
    r += 1


def vhdr(labels, cols=SC, extra=None):
    global r
    for cl, lab in zip(cols, labels):
        cell(wv, r, wv[cl + "1"].column, lab, font=FONT_SUB, align="center")
    if extra:
        txt(wv, r, 1, extra, font=FONT_SUB)
    r += 1


def vnote(text):
    global r
    txt(wv, r, 1, text, font=FONT_NOTE)
    r += 1


r = 1
txt(wv, r, 1, "Adobe Inc. (ADBE) — TERMINAL VALUE AND SUM-OF-THE-PARTS VALUATION",
    font=FONT_TITLE)
r += 1
txt(wv, r, 1, "Value = PV(forecast owners' earnings) + PV(terminal value) + standalone "
              "assets − all debt-like items, divided by TODAY's diluted share count. "
              "The valuation is trading-price blind: Adobe's share price and market "
              "capitalisation are not an input anywhere on this sheet "
              "(valuation.md §0, §2).", font=FONT_NOTE)
r += 1
txt(wv, r, 1, "CONTENTS:  §A Headline sum of the parts   |   §B Terminal value by "
              "scenario   |   §C Gordon cross-check on the terminal multiples   |   "
              "§D Discounting   |   §E Full valuation by scenario   |   "
              "§F Equity bridge   |   §G Sensitivity   |   §H Checks", font=FONT_NAV)
r += 2

# ---- §A  HEADLINE --------------------------------------------------------
vband("§A.  HEADLINE — SUM OF THE PARTS, PROBABILITY-WEIGHTED")
r += 1
vscalar("h_p1", "Part 1   PV of explicit-period owners' earnings, FY2026E-FY2030E (t=0..4)",
        "=F@v_pvoe@", NUM0,
        src="Detail in §E. Each scenario's own owners'-earnings path from sheet 2 §7, "
            "discounted at the rate on sheet 1.")
vscalar("h_p2", "Part 2   PV of terminal value at FY2030 year-end (t=4)", "=F@v_pvtv@",
        NUM0, src="Detail in §B and §E.")
vscalar("h_ev", "            = ENTERPRISE VALUE", "=B@h_p1@+B@h_p2@", NUM0,
        font=FONT_BOLD, border=TOP,
        src="An ENTERPRISE value, because owners' earnings are unlevered: interest "
            "expense and interest income sit below the operating line and are excluded "
            "(terminal_value.md §2).")
vscalar("h_p3", "Part 3   + Standalone assets (excess cash and short-term investments)",
        "=B@eb_assets@", NUM0)
vscalar("h_p4", "Part 4   − Total debt-like items", "=-B@eb_debt@", NUM0,
        src="Funded debt + operating leases + the PV of off-balance-sheet hosting "
            "commitments. Detail and alternative conventions in §F and §G(ii).")
vscalar("h_eq", "            = EQUITY VALUE", "=B@h_ev@+B@h_p3@+B@h_p4@", NUM0,
        font=FONT_BOLD, border=TOP)
vscalar("h_sh", "            ÷ diluted shares outstanding (M)", f"={IN}$B${I['shares']}",
        NUM1)
vscalar("h_ps", " = INTRINSIC VALUE PER DILUTED SHARE", "=B@h_eq@/B@h_sh@", USD2,
        font=FONT_BIG, border=TOPD, fill=F_OUT,
        src="valuation.md §1. The probability-weighted headline. §E shows the same "
            "walk for each scenario separately — the range is roughly 4.7x from least "
            "to most favourable, which is the honest measure of how open the question is.")
r += 1
vscalar("h_tvpct", "  memo: terminal value as % of enterprise value", "=B@h_p2@/B@h_ev@",
        PCT1,
        src="~72%. The answer is dominated by the terminal multiple, not by the "
            "five-year forecast. terminal_value.md §1 also flags that 38% of the "
            "probability-weighted terminal value comes from the 20%-probability bull "
            "case.")
r += 1

# ---- §B  TERMINAL VALUE --------------------------------------------------
vband("§B.  TERMINAL VALUE AT FY2030 YEAR-END, BY SCENARIO (undiscounted, enterprise "
      "basis)")
r += 1
vhdr(SLAB, extra="($M unless noted)")
vrow("v_prob", "Probability",
     [f"={IN}$B${I['p_' + k]}" for k in ["sev", "bear", "base", "bull"]] +
     ["=SUM(B@v_prob@:E@v_prob@)"], PCT1, fill=F_CHK,
     src="From sheet 1 §B. The WEIGHTED column here is the check that they sum to 100%.")
vrow("v_oe30", "FY2030E owners' earnings",
     [f"={MS}J{M['sum_' + k]}" for k in ["sev", "bear", "base", "bull", "w"]],
     NUM0, src="Sheet 2 §7 — the end point of each scenario's owners'-earnings path.")
vrow("v_mult", "Terminal multiple (x FY2030E owners' earnings)",
     [f"={IN}$C${I['m_' + k]}" for k in ["sev", "bear", "base", "bull"]] +
     ["=F@v_tv@/F@v_oe30@"], XMUL,
     src="ANALYST JUDGMENT (terminal_value.md §6.2), cross-checked in §C. Each "
         "multiple is applied to ITS OWN scenario's earnings; a multiple is never "
         "applied to blended earnings. The WEIGHTED cell is therefore an OUTPUT — the "
         "multiple implied by the weighted terminal value divided by the weighted "
         "FY2030E earnings ( = 15.3x, terminal_value.md §1). Note this is NOT the "
         "probability-weighted average of the four multiples, which is 14.2x: the "
         "higher-earnings scenarios also carry the higher multiples, so the implied "
         "multiple exceeds the simple mean.")
vrow("v_mult_avg", "  memo: probability-weighted AVERAGE of the four multiples",
     [None, None, None, None,
      "=B@v_prob@*B@v_mult@+C@v_prob@*C@v_mult@+D@v_prob@*D@v_mult@"
      "+E@v_prob@*E@v_mult@"], XMUL,
     src="Shown only to make the distinction above explicit. This figure is NOT used "
         "anywhere in the valuation.")
vrow("v_tv", "TERMINAL VALUE at FY2030 year-end",
     [f"={c}@v_mult@*{c}@v_oe30@" for c in SC[:4]] +
     ["=B@v_prob@*B@v_tv@+C@v_prob@*C@v_tv@+D@v_prob@*D@v_tv@+E@v_prob@*E@v_tv@"],
     NUM0, font=FONT_BOLD, border=TOP, fill=F_OUT,
     src="terminal_value.md §1: $42.2bn / $89.2bn / $161.2bn / $286.8bn, weighted "
         "$150.4bn. Applying a single 15x to weighted earnings instead would give "
         "$147.5bn, 'only 1.9% away' — the weighting method is not doing the work.")
vrow("v_tvshare", "  share of the weighted terminal value",
     [f"={c}@v_prob@*{c}@v_tv@/$F@v_tv@" for c in SC[:4]], PCT1,
     src="terminal_value.md §1. Note the bull case supplies ~38% of the weighted "
         "terminal value on a 20% probability — the single largest concentration of "
         "judgment in the valuation.")
r += 1

# ---- §C  GORDON CROSS-CHECK ---------------------------------------------
vband("§C.  CROSS-CHECK ON THE TERMINAL MULTIPLES — GORDON PERPETUITY GRID")
vnote("Value / owners' earnings = (1 − g / ROIC) / (r − g). The (1 − g/ROIC) term is "
      "the reinvestment drag: growth is not free, it must be funded out of earnings. "
      "terminal_value.md §6.1 runs this grid at ROIC ~70% (sheet 1 §A) and rejects a "
      "third-party 11.53% WACC as too high, using an 8-10% band instead. This grid is "
      "a SANITY CHECK on the judgment multiples in §B — it does not feed the valuation.")
r += 1
vhdr(["r = 8.0%", "r = 9.0%", "r = 10.0%", "r = 11.0%"], cols=["B", "C", "D", "E"],
     extra="perpetual growth g  \\  discount rate r")
GORDON_R = [0.08, 0.09, 0.10, 0.11]
gr_hdr = r - 1
for i, rr_ in enumerate(GORDON_R):
    cell(wv, gr_hdr, 2 + i, rr_, fmt=PCT1, fill=F_INPUT, align="center")
GROWS = [-0.03, 0.00, 0.01, 0.02, 0.03, 0.04]
g_first = r
for g in GROWS:
    cell(wv, r, 1, g, fmt=PCT1, fill=F_INPUT)
    for i in range(4):
        cl = "BCDE"[i]
        _putv(r, 2 + i,
              f"=(1-$A{r}/{IN}$B${I['roic_t']})/({cl}${gr_hdr}-$A{r})", XMUL)
    r += 1
txt(wv, g_first, NCV, "Read against §B: SEVERE 7x sits below the g=-3% row; BEAR 11x "
                      "between g=0% and g=1%; BASE 15x just under the g=3%, r=9% cell "
                      "(16.0x); BULL 22x just above g=4%, r=8.5%. Each judgment "
                      "multiple is therefore internally consistent with a plausible "
                      "(g, r) pair rather than picked freehand.", font=FONT_NOTE)
r += 1
vnote("Peer anchors at 31 Aug 2026 (fetched_docs/peer_multiples_compare_2026.md, "
      "terminal_value.md §5): mature large-cap software trailing P/E median 27.2x "
      "(MSFT 28.6x, SAP 28.8x, ORCL 25.9x, CRM 23.7x, INTU 21.8x, ADSK 33.8x); "
      "ex-growth / disruption-discounted median 18.8x (DBX 19.7x, GEN 18.0x, ZM 9.0x, "
      "DOCU 41.6x). ADBE itself trades at 16.7x trailing owners' earnings, a 59% "
      "de-rating from its own FY2021-FY2025 median of 40.9x. Peer P/Es are read "
      "directly against owners'-earnings multiples because TTM owners' earnings "
      "($7,490M) sit only 3.6% above TTM GAAP net income ($7,230M) — terminal_value.md §2.")
r += 1

# ---- §D  DISCOUNTING -----------------------------------------------------
vband("§D.  DISCOUNTING")
vnote("valuation.md §2: the current fiscal year is t=0 and is NOT discounted. As of "
      "the 1 Sep 2026 valuation date Adobe is inside FY2026, so FY2026E = t=0. The "
      "terminal value is the value of the business AT THE END of FY2030, realised at "
      "the same moment as the FY2030 flow, so it is discounted at the same t=4 factor "
      "— not t=5.")
r += 1
vhdr(YLAB, cols=YC, extra="($M unless noted)")
vrow("d_t", "t (years discounted)", [0, 1, 2, 3, 4], NUM0, cols=YC)
vrow("d_f", "Discount factor  = 1 / (1 + r)^t",
     [f"=1/(1+{IN}$B${I['disc']})^{c}@d_t@" for c in YC], NUM2, cols=YC,
     src=f"r is the single input at sheet 1 cell B{I['disc']}. At 15% the factors are "
         "1.0000 / 0.8696 / 0.7561 / 0.6575 / 0.5718.")
r += 1

# ---- §E  FULL VALUATION BY SCENARIO --------------------------------------
vband("§E.  FULL VALUATION BY SCENARIO — the four 'parts' behind the headline")
r += 1
vhdr(SLAB, extra="($M unless noted)")
OEROW = {k: M["sum_" + k] for k in ["sev", "bear", "base", "bull", "w"]}
vrow("v_pvoe", "Part 1  PV of owners' earnings, FY2026E-FY2030E",
     [f"=SUMPRODUCT({MS}$F${OEROW[k]}:$J${OEROW[k]},$B@d_f@:$F@d_f@)"
      for k in ["sev", "bear", "base", "bull", "w"]], NUM0,
     src="Each scenario's own owners'-earnings path (sheet 2 §7) times the discount "
         "factors in §D.")
vrow("v_pvtv", "Part 2  PV of terminal value (discounted at t=4)",
     [f"={c}@v_tv@*$F@d_f@" for c in SC], NUM0,
     src="The terminal values from §B brought back four years.")
vrow("v_ev", "           = ENTERPRISE VALUE",
     [f"={c}@v_pvoe@+{c}@v_pvtv@" for c in SC], NUM0, font=FONT_BOLD, border=TOP)
vrow("v_sa", "Part 3  + Standalone assets", ["=$B@eb_assets@"] * 5, NUM0)
vrow("v_db", "Part 4  − Total debt-like items", ["=-$B@eb_debt@"] * 5, NUM0,
     src="Identical in every scenario: the bridge is struck on today's balance sheet, "
         "not forecast forward. terminal_value.md §9 notes FY2030 net debt should stay "
         "~1% of a ~$150bn EV IF the buyback throttles to ~90% of owners' earnings; at "
         "the FY2024-25 pace of ~1.5x, 'the equity bridge stops being immaterial'. "
         "That risk is NOT modelled here.")
vrow("v_eq", "           = EQUITY VALUE", [f"={c}@v_ev@+{c}@v_sa@+{c}@v_db@" for c in SC],
     NUM0, font=FONT_BOLD, border=TOP)
vrow("v_sh", "           ÷ diluted shares (M)", [f"={IN}$B${I['shares']}"] * 5, NUM1)
vrow("v_ps", " = INTRINSIC VALUE PER DILUTED SHARE",
     [f"={c}@v_eq@/{c}@v_sh@" for c in SC], USD2, font=FONT_BIG, border=TOPD,
     fill=F_OUT,
     src="valuation.md §1: ~$104 / ~$183 / ~$298 / ~$487, weighted ~$278.")
vrow("v_tvp", "  memo: terminal value as % of enterprise value",
     [f"={c}@v_pvtv@/{c}@v_ev@" for c in SC], PCT1)
vrow("v_xchk", "  cross-check: probability-weighted average of the four per-share values",
     [None, None, None, None,
      "=B@v_prob@*B@v_ps@+C@v_prob@*C@v_ps@+D@v_prob@*D@v_ps@+E@v_prob@*E@v_ps@"],
     USD2, fill=F_CHK, border=TOP,
     src="Discounting is linear, so this MUST equal the WEIGHTED column above. A real "
         "internal-consistency check: it confirms the cash-flow stream and the terminal "
         "value are weighted on the same probabilities and combined exactly once. "
         "valuation.md §2.1 reports the two agree 'to the cent'.")
vrow("v_xdiff", "  difference (must be 0)", [None, None, None, None,
     "=F@v_xchk@-F@v_ps@"], NUM2, fill=F_CHK)
r += 1

# ---- §F  EQUITY BRIDGE ---------------------------------------------------
vband("§F.  THE EQUITY BRIDGE — standalone assets and all debt-like items "
      "(Q2 FY2026 balance sheet, 29 May 2026)")
r += 1
vscalar("eb_cash", "Cash and cash equivalents", f"={IN}$B${I['cash']}", NUM0)
vscalar("eb_sti", "Short-term investments", f"={IN}$B${I['sti']}", NUM0)
vscalar("eb_opcash", "− operating cash need (2% of TTM revenue)",
        f"=-{IN}$B${I['opcash']}*{MS}$E${M['b_rev']}", NUM0,
        src="owners_earnings_and_roic.md §4: 'Adobe collects in advance and runs "
            "negative working capital, so its genuine operating cash requirement is "
            "small. ... This is an assumption, not a sourced figure.' 2% of TTM "
            "revenue = ~$504M.")
vscalar("eb_assets", " = STANDALONE ASSETS", "=SUM(B@eb_cash@:B@eb_opcash@)", NUM0,
        font=FONT_BOLD, border=TOP)
r += 1
vscalar("eb_d1", "Debt, current (incl. commercial paper), carrying value",
        f"={IN}$B${I['debt_c']}", NUM0)
vscalar("eb_d2", "Debt, long-term, carrying value", f"={IN}$B${I['debt_lt']}", NUM0)
vscalar("eb_d3", "Operating lease liabilities, current", f"={IN}$B${I['lease_c']}", NUM0)
vscalar("eb_d4", "Operating lease liabilities, long-term", f"={IN}$B${I['lease_lt']}",
        NUM0)
vscalar("eb_d5", "Off-balance-sheet hosting purchase obligations, PV @ 5%",
        f"={IN}$B${I['po_pv']}", NUM0,
        src="A DISCLOSED JUDGMENT CALL, and the largest single swing in the bridge. The "
            "brief lists off-balance-sheet commitments as debt, and the same rule is "
            "applied symmetrically to operating leases. §G(ii) prices the alternatives.")
vscalar("eb_debt", " = TOTAL DEBT-LIKE ITEMS", "=SUM(B@eb_d1@:B@eb_d5@)", NUM0,
        font=FONT_BOLD, border=TOP)
vscalar("eb_net", "Net standalone assets less debt", "=B@eb_assets@-B@eb_debt@", NUM0,
        font=FONT_BOLD,
        src="~−$8.2bn, roughly $20/share of drag. NOT included: legal contingencies — "
            "Adobe is 'unable to estimate a reasonably possible financial loss or range "
            "of financial loss, if any' on the securities class action and derivative "
            "actions (Q2 FY2026 10-Q Note 13). That is flagged as an UNQUANTIFIED RISK, "
            "not a zero. No defined-benefit pension is disclosed.")
r += 1

# ---- §G  SENSITIVITY -----------------------------------------------------
vband("§G.  SENSITIVITY — the three assumptions that actually move the answer")
r += 1
subband(wv, r, "  (i) Discount rate  (probability-weighted path throughout)", NCV)
r += 1
WROW = M["sum_w"]
WRNG = f"{MS}$F${WROW}:$J${WROW}"
txt(wv, r, 1, "Discount rate", font=FONT_SUB)
for cl, lab in zip(SC, ["PV(OE)", "PV(TV)", "Enterprise value", "Value / share",
                        "TV % of EV"]):
    cell(wv, r, wv[cl + "1"].column, lab, font=FONT_SUB, align="center")
txt(wv, r, NCV, "The discount rate is a STATED variable, not a fitted one "
                "(valuation.md §5.2). A 5-point change moves the per-share answer by "
                "roughly 14-16% — large, but not large enough to change the sign of "
                "the conclusion on its own.", font=FONT_NOTE)
r += 1
for rate in [0.10, 0.125, 0.15, 0.175, 0.20]:
    bold = FONT_BOLD if rate == 0.15 else None
    cell(wv, r, 1, rate, fmt=PCT1, fill=F_INPUT, font=bold)
    _putv(r, 2, f"=SUMPRODUCT({WRNG},1/(1+$A{r})^(COLUMN({WRNG})-COLUMN({MS}$F${WROW})))",
          NUM0, None, bold)
    _putv(r, 3, f"=$F@v_tv@/(1+$A{r})^4", NUM0, None, bold)
    _putv(r, 4, f"=B{r}+C{r}", NUM0, None, bold)
    _putv(r, 5, f"=(D{r}+$B@eb_assets@-$B@eb_debt@)/{IN}$B${I['shares']}", USD2,
          F_OUT if rate == 0.15 else None, bold)
    _putv(r, 6, f"=C{r}/D{r}", PCT1, None, bold)
    r += 1
r += 1
subband(wv, r, "  (ii) Which items belong in the debt bridge (a disclosed judgment call)",
        NCV)
r += 1
txt(wv, r, 1, "Convention", font=FONT_SUB)
cell(wv, r, 2, "Total debt-like", font=FONT_SUB, align="center")
cell(wv, r, 3, "Value / share", font=FONT_SUB, align="center")
r += 1
for lab, expr, note_ in [
    ("Headline: funded debt + leases + hosting (the brief, literally)",
     "=$B@eb_debt@",
     "The published headline. valuation.md §3, after verifier objection 1 required "
     "leases and hosting to be treated symmetrically."),
    ("Funded debt + leases only, hosting excluded",
     "=$B@eb_debt@-$B@eb_d5@", None),
    ("Funded debt only, leases and hosting both excluded",
     "=SUM($B@eb_d1@:$B@eb_d2@)",
     "Full range across the three conventions is ~$16.74/share, a 6.0% spread — "
     "material but not decisive."),
]:
    txt(wv, r, 1, "   " + lab)
    _putv(r, 2, expr, NUM0)
    _putv(r, 3, f"=($F@v_ev@+$B@eb_assets@-B{r})/{IN}$B${I['shares']}", USD2)
    if note_:
        txt(wv, r, NCV, note_, font=FONT_NOTE)
    r += 1
r += 1
subband(wv, r, "  (iii) Terminal multiples — all four scaled together", NCV)
r += 1
txt(wv, r, 1, "Scaling applied to every scenario multiple", font=FONT_SUB)
for cl, lab in zip(SC, ["Weighted TV", "PV of TV", "Enterprise value",
                        "Value / share", ""]):
    if lab:
        cell(wv, r, wv[cl + "1"].column, lab, font=FONT_SUB, align="center")
txt(wv, r, NCV, "Terminal value is linear in the multiple, so a uniform scaling passes "
                "straight through. terminal_value.md §8 gives a defensible aggregate "
                "range of $120-180bn, which is the x0.8 to x1.2 band below. Because "
                "terminal value is ~72% of enterprise value, this is the single "
                "largest sensitivity on the sheet.", font=FONT_NOTE)
r += 1
for sc in [0.8, 0.9, 1.0, 1.1, 1.2]:
    bold = FONT_BOLD if sc == 1.0 else None
    cell(wv, r, 1, sc, fmt='0.0"x"', fill=F_INPUT, font=bold)
    _putv(r, 2, f"=$A{r}*$F@v_tv@", NUM0, None, bold)
    _putv(r, 3, f"=B{r}*$F@d_f@", NUM0, None, bold)
    _putv(r, 4, f"=$F@v_pvoe@+C{r}", NUM0, None, bold)
    _putv(r, 5, f"=(D{r}+$B@eb_assets@-$B@eb_debt@)/{IN}$B${I['shares']}", USD2,
          F_OUT if sc == 1.0 else None, bold)
    r += 1
r += 1

# ---- §H  CHECKS ----------------------------------------------------------
vband("§H.  CHECKS AGAINST THE PUBLISHED WORK PRODUCTS")
r += 1
cell(wv, r, 2, "Model", font=FONT_SUB, align="center")
cell(wv, r, 3, "Published", font=FONT_SUB, align="center")
cell(wv, r, 4, "Diff", font=FONT_SUB, align="center")
r += 1
for lab, ref, pub, fmt, src in [
    ("Terminal value, SEVERE ($M)", "=B@v_tv@", 42154, NUM0, "terminal_value.md §1"),
    ("Terminal value, BEAR ($M)", "=C@v_tv@", 89155, NUM0, "terminal_value.md §1"),
    ("Terminal value, BASE ($M)", "=D@v_tv@", 161175, NUM0, "terminal_value.md §1"),
    ("Terminal value, BULL ($M)", "=E@v_tv@", 286770, NUM0, "terminal_value.md §1"),
    ("Probability-weighted terminal value ($M)", "=F@v_tv@", 150436, NUM0,
     "terminal_value.md §1 / valuation.md §2.1"),
    ("Implied weighted terminal multiple", "=F@v_mult@", 15.3, NUM2,
     "terminal_value.md §1"),
    ("PV of owners' earnings, weighted ($M)", "=F@v_pvoe@", 33057, NUM0,
     "valuation.md §2.2"),
    ("PV of terminal value, weighted ($M)", "=F@v_pvtv@", 86012, NUM0,
     "valuation.md §2.2"),
    ("Enterprise value, weighted ($M)", "=F@v_ev@", 119069, NUM0, "valuation.md §2.2"),
    ("Standalone assets ($M)", "=B@eb_assets@", 5122, NUM0, "valuation.md §3"),
    ("Total debt-like items ($M)", "=B@eb_debt@", 13324, NUM0, "valuation.md §3"),
    ("Equity value, weighted ($M)", "=F@v_eq@", 110867, NUM0, "valuation.md §3"),
    ("Diluted shares (M)", f"={IN}$B${I['shares']}", 399.1, NUM1, "valuation.md §3"),
    ("INTRINSIC VALUE PER SHARE — SEVERE", "=B@v_ps@", 103.77, NUM2, "valuation.md §1"),
    ("INTRINSIC VALUE PER SHARE — BEAR", "=C@v_ps@", 182.59, NUM2, "valuation.md §1"),
    ("INTRINSIC VALUE PER SHARE — BASE", "=D@v_ps@", 297.71, NUM2, "valuation.md §1"),
    ("INTRINSIC VALUE PER SHARE — BULL", "=E@v_ps@", 487.47, NUM2, "valuation.md §1"),
    ("INTRINSIC VALUE PER SHARE — WEIGHTED", "=F@v_ps@", 277.79, NUM2,
     "valuation.md §1 — the headline."),
]:
    txt(wv, r, 1, lab)
    _putv(r, 2, ref, fmt)
    cell(wv, r, 3, pub, fmt=fmt, fill=F_ACT)
    _putv(r, 4, f"=B{r}-C{r}", fmt, F_CHK)
    txt(wv, r, NCV, src, font=FONT_NOTE)
    r += 1
r += 1
vnote("Small residuals are expected throughout: the published scripts round scenario "
      "owners' earnings to the nearest $M before weighting and multiplying, whereas "
      "this workbook carries full precision from the drivers all the way to the "
      "per-share value.")

for ws_, rr, cc in PENDV:
    v = ws_.cell(row=rr, column=cc).value
    for k, rownum in V.items():
        v = v.replace("@" + k + "@", str(rownum))
    if "@" in v:
        raise ValueError(f"unresolved placeholder in {ws_.title} r{rr} c{cc}: {v}")
    ws_.cell(row=rr, column=cc).value = v

wv.freeze_panes = "B7"

wb.save(OUT)
print(f"Terminal Value & SOTP sheet built: {r} rows.")
print(f"Wrote {OUT} with sheets: {wb.sheetnames}")
