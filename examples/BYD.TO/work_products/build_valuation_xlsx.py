"""
Build work_products/valuation.xlsx - a live, formula-linked Excel version of the Boyd Group (BYD.TO) model.

    uv run python work_products/build_valuation_xlsx.py        # writes valuation.xlsx
    uv run python work_products/verify_valuation_xlsx.py       # recalculates it and checks against the python

Three sheets, each starting with its inputs:
    1 Earnings          historical Owners' Earnings (FY2023-TTM Jun-2026, adjustments shown) side by side with the
                        FY2026E-FY2031E forecast for four cases (Bear / Base / Bull / No growth)
                        -> owners_earnings_roic.py (ROIC section skipped) + forecast_earnings.py
    2 Terminal Value    end-2031 exit-multiple terminal value + cross-checks          -> terminal_value.py
    3 SOTP Valuation    PV of cash flows + PV of terminal value + standalone assets - debt -> per share
                                                                                           -> valuation.py
Cell colours:  yellow fill + blue font = input;  green font = linked to an input/result elsewhere;  black = formula.

Inputs are taken from the python dataclasses where they exist (so the workbook and the scripts cannot drift);
historical figures are typed from owners_earnings_roic.py (thousands there, US$ millions here). Nothing in the
workbook uses Boyd's share price.
"""
from __future__ import annotations

import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.properties import PageSetupProperties

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import forecast_earnings as fe  # noqa: E402
import terminal_value as tv  # noqa: E402
import valuation as val  # noqa: E402

OUT_PATH = os.path.join(HERE, "valuation.xlsx")

# ------------------------------------------------------------------------------------------------ styles
INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
INPUT_FONT = Font(color="0000FF")
LINK_FONT = Font(color="008000")
BOLD = Font(bold=True)
SECTION_FILL = PatternFill("solid", fgColor="D9E1F2")
HEADER_FILL = PatternFill("solid", fgColor="EDEDED")

FMT_M = '#,##0.0;(#,##0.0);"-"'        # US$ millions
FMT_M3 = '#,##0.000;(#,##0.000);"-"'   # US$ millions, 3dp (raw filing figures in thousands)
FMT_PCT = '0.0%;(0.0%);"-"'
FMT_PCT2 = '0.00%;(0.00%);"-"'
FMT_X = '0.0"x"'
FMT_X2 = '0.00"x"'
FMT_N = '#,##0;(#,##0);"-"'
FMT_N2 = '0.00'
FMT_PP = '0.0;(0.0);"0.0"'             # percentage points
FMT_PS = '"$"#,##0.00'
FMT_YEAR = '0'
FMT_F = '0.000'

YEAR_COLS = ["F", "G", "H", "I", "J", "K"]            # sheet 1: FY2026E..FY2031E
PREV_COL = {"F": "D", "G": "F", "H": "G", "I": "H", "J": "I", "K": "J"}   # FY2026E looks back to FY2025 (col D)
HIST_COLS = ["B", "C", "D", "E"]                       # sheet 1: FY2023, FY2024, FY2025, TTM Jun-2026
NOTE_COL = "L"

CASES = ["Bear", "Base", "Bull", "NoGrowth"]           # sheet 1 order (forecast_earnings.py)
CASE_LABEL = {"Bear": "Bear", "Base": "Base", "Bull": "Bull", "NoGrowth": "No growth (existing business only)"}
VAL_CASES = ["Bear", "Base", "NoGrowth", "Bull"]      # sheets 2-3 order (valuation.md)
VAL_COL = {"Bear": "B", "Base": "C", "NoGrowth": "D", "Bull": "E"}
WTD_COL = "F"
SCEN_DEF = {"Bear": fe.BEAR, "Base": fe.BASE, "Bull": fe.BULL, "NoGrowth": fe.EXISTING_ONLY}
TV_KEY = {"Bear": "Bear", "Base": "Base", "Bull": "Bull", "NoGrowth": tv.NO_GROWTH}


class Inp:
    """An input value (highlighted)."""
    def __init__(self, v):
        self.v = v


class Lnk:
    """A formula that just links to an input or result elsewhere (green, not highlighted)."""
    def __init__(self, f):
        self.f = f


class SheetBuilder:
    """Writes rows top to bottom and remembers the row number of every named line item."""

    def __init__(self, wb: Workbook, title: str):
        self.ws = wb.create_sheet(title)
        self.title = title
        self.r = 1
        self.rows: dict[str, int] = {}
        self.ws.column_dimensions["A"].width = 58
        for c in "BCDEFGHIJK":
            self.ws.column_dimensions[c].width = 11.5
        self.ws.column_dimensions[NOTE_COL].width = 90
        self.ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
        self.ws.page_setup.orientation = "landscape"
        self.ws.page_setup.fitToWidth = 1
        self.ws.page_setup.fitToHeight = 0

    # ---- references
    def ref(self, name: str, col: str, from_sheet: "SheetBuilder | None" = None, absolute: bool = False) -> str:
        row = self.rows[name]
        cell = f"${col}${row}" if absolute else f"{col}{row}"
        if from_sheet is not None and from_sheet is not self:
            return f"'{self.title}'!{cell}"
        return cell

    def rng(self, name: str, c1: str, c2: str, from_sheet: "SheetBuilder | None" = None) -> str:
        row = self.rows[name]
        cell = f"${c1}${row}:${c2}${row}"
        if from_sheet is not None and from_sheet is not self:
            return f"'{self.title}'!{cell}"
        return cell

    # ---- writing
    @staticmethod
    def _safe_label(text: str) -> str:
        if text and text[0] in "=+-@":
            raise ValueError(f"label would be parsed as a formula: {text!r}")
        return text

    def blank(self, n: int = 1):
        self.r += n

    def section(self, text: str):
        c = self.ws[f"A{self.r}"]
        c.value = self._safe_label(text)
        c.font = Font(bold=True, size=12)
        for col in "ABCDEFGHIJKL":
            self.ws[f"{col}{self.r}"].fill = SECTION_FILL
        self.r += 1

    def text(self, text: str, italic: bool = True):
        c = self.ws[f"A{self.r}"]
        c.value = self._safe_label(text)
        c.font = Font(italic=italic)
        self.r += 1

    def header(self, label: str, cols: dict[str, str], note: str = "Source / explanation"):
        self.ws[f"A{self.r}"] = self._safe_label(label)
        for col, t in cols.items():
            self.ws[f"{col}{self.r}"] = self._safe_label(str(t))
            self.ws[f"{col}{self.r}"].alignment = Alignment(horizontal="right")
        if note:
            self.ws[f"{NOTE_COL}{self.r}"] = note
        for col in "ABCDEFGHIJKL":
            self.ws[f"{col}{self.r}"].font = BOLD
            self.ws[f"{col}{self.r}"].fill = HEADER_FILL
        self.r += 1

    def line(self, name: str | None, label: str, cells: dict, fmt: str = FMT_M, note: str = "",
             bold: bool = False) -> int:
        """cells: col -> number (input) | Inp | Lnk | '=formula' (calc)."""
        r = self.r
        self.ws[f"A{r}"] = self._safe_label(label)
        if bold:
            self.ws[f"A{r}"].font = BOLD
        for col, v in cells.items():
            c = self.ws[f"{col}{r}"]
            if isinstance(v, Inp) or isinstance(v, (int, float)):
                c.value = v.v if isinstance(v, Inp) else v
                c.fill, c.font = INPUT_FILL, INPUT_FONT
            elif isinstance(v, Lnk):
                assert v.f.startswith("="), v.f
                c.value = v.f
                c.font = LINK_FONT
            elif isinstance(v, str):
                assert v.startswith("="), f"formula must start with '=': {v!r}"
                c.value = v
                if bold:
                    c.font = BOLD
            elif v is None:
                continue
            else:
                raise TypeError(v)
            c.number_format = fmt
        if note:
            self.ws[f"{NOTE_COL}{r}"] = note
            self.ws[f"{NOTE_COL}{r}"].alignment = Alignment(wrap_text=False)
        if name:
            assert name not in self.rows, f"duplicate row name {name}"
            self.rows[name] = r
        self.r += 1
        return r


def legend(sb: SheetBuilder, title: str, subtitle: str):
    sb.ws["A1"] = title
    sb.ws["A1"].font = Font(bold=True, size=14)
    sb.ws["A2"] = subtitle
    sb.ws["A2"].font = Font(italic=True)
    sb.ws["A3"] = "Input (change me)"
    sb.ws["A3"].fill, sb.ws["A3"].font = INPUT_FILL, INPUT_FONT
    sb.ws["B3"] = "Linked from elsewhere (do not overwrite)"
    sb.ws["B3"].font = LINK_FONT
    sb.ws["F3"] = "Black = formula"
    sb.r = 5


# =====================================================================================================
# SHEET 1 - HISTORICAL AND FORECAST OWNERS' EARNINGS
# =====================================================================================================

def build_earnings(wb: Workbook) -> SheetBuilder:
    s = SheetBuilder(wb, "1 Earnings")
    legend(s, "Boyd Group Services (BYD.TO) - Sheet 1: Owners' Earnings, historical and forecast",
           "US$ millions unless stated. Python sources: owners_earnings_roic.py (historical), forecast_earnings.py "
           "(forecast). Share price not used anywhere.")

    # ------------------------------------------------------------------ 1.1 reported historical figures
    s.section("INPUTS")
    s.header("1.1 Reported figures (US$M, from filings)",
             {"B": "FY2023", "C": "FY2024", "D": "FY2025", "E": "H1-2025", "F": "H1-2026"})
    s.line("in_sales", "Sales", {"B": 2945.988, "C": 3070.342, "D": 3142.794, "E": 1558.730, "F": 2010.328},
           FMT_M3, "FY2023 AFS / FY2025 AFS statements of earnings; H1 columns from Q2FY26 interim statements "
                   "(owners_earnings_roic.py l.30-37)")
    s.line("in_q3_25", "Adjusted EBITDA, Q3-2025", {"B": 98.366}, FMT_M3, "Q2FY26 MD&A quarterly table, line 350")
    s.line("in_q4_25", "Adjusted EBITDA, Q4-2025", {"B": 103.609}, FMT_M3, "Q2FY26 MD&A quarterly table, line 350")
    s.line("in_q1_26", "Adjusted EBITDA, Q1-2026", {"B": 122.385}, FMT_M3, "Q2FY26 MD&A quarterly table, line 350")
    s.line("in_q2_26", "Adjusted EBITDA, Q2-2026", {"B": 135.932}, FMT_M3, "Q2FY26 MD&A quarterly table, line 350")
    s.line("in_ebitda", "Adjusted EBITDA (company-reported)",
           {"B": 368.247, "C": 334.819, "D": 376.306,
            "E": f"=D{s.r}-{s.ref('in_q3_25', 'B')}-{s.ref('in_q4_25', 'B')}",
            "F": f"={s.ref('in_q1_26', 'B')}+{s.ref('in_q2_26', 'B')}"},
           FMT_M3, "FY2023 MD&A l.282; FY2024 MD&A l.198; FY2025 MD&A l.209. H1-2025 = FY2025 less Q3 and Q4; "
                   "H1-2026 = Q1 + Q2")
    s.line("in_lp_prop", "Lease principal repaid - property",
           {"B": 95.441, "C": 103.888, "D": 111.142, "E": 54.892, "F": 72.637}, FMT_M3,
           "Financing section of cash flow statement (FY2025 AFS l.298; Q2FY26 FS l.167)")
    s.line("in_lp_veh", "Lease principal repaid - vehicle & equipment",
           {"B": 3.863, "C": 5.283, "D": 5.594, "E": 2.815, "F": 2.901}, FMT_M3,
           "FY2025 AFS l.299; Q2FY26 FS l.168")
    s.line("in_li_prop", "Lease interest paid - property",
           {"B": 31.328, "C": 39.464, "D": 44.095, "E": 21.555, "F": 31.872}, FMT_M3,
           "FY2025 AFS l.301; Q2FY26 FS l.171")
    s.line("in_li_veh", "Lease interest paid - vehicle & equipment",
           {"B": 0.728, "C": 1.021, "D": 0.730, "E": 0.462, "F": 0.531}, FMT_M3,
           "FY2025 AFS cash flows; Q2FY26 FS l.172. FY2025 principal + interest ties to AFS Note 17 repayments 161,561")
    s.line("in_capex_equip", "Equipment purchases & facility improvements (actual)",
           {"B": 57.482, "C": 77.333, "D": 54.306, "E": 25.765, "F": 24.802}, FMT_M3,
           "Investing section of cash flow statement; memo only (maintenance capex is modelled at % of sales)")
    s.line("in_capex_sw", "Software purchases and licensing (actual)",
           {"B": 1.684, "C": 3.124, "D": 8.094, "E": 3.132, "F": 0.936}, FMT_M3,
           "Investing section of cash flow statement")
    s.line("in_cash_tax", "Income taxes paid (cash)",
           {"B": 27.909, "C": 12.295, "D": 3.669, "E": 2.555, "F": 3.260}, FMT_M3,
           "Supplemental CFS line: FY2023 AFS l.297, FY2024 AFS l.300, FY2025 AFS l.318, Q2FY26 l.190")
    s.line("in_acq_actual", "Acquisition & transformational cost initiatives (actual)",
           {"B": 4.346, "C": 9.879, "D": 30.488, "E": 13.773, "F": 31.264}, FMT_M3,
           "Statement of earnings line (FY2023 label: 'Acquisition and transaction costs')")
    s.line("in_cfo", "Cash flow from operations (reported)",
           {"B": 357.545, "C": 313.325, "D": 352.989, "E": 170.593, "F": 224.591}, FMT_M3,
           "Statements of cash flows. Boyd reports all interest and lease principal in financing (AFS Note 2u)")
    s.line("in_wc", "Changes in non-cash working capital (in CFO)",
           {"B": 19.072, "C": -5.909, "D": 5.752, "E": 18.791, "F": -6.375}, FMT_M3,
           "Statements of cash flows; used only in the CFO reconciliation")
    s.line("in_sbc", "Equity-settled share-based payment added back in CFO",
           {"B": 0.0, "C": 0.928, "D": 4.319, "E": 1.877, "F": 4.689}, FMT_M3,
           "Statements of cash flows (FY2023 not separately disclosed)")
    s.line("in_other", "Other non-cash items added back in CFO",
           {"B": 0.444, "C": 1.033, "D": 2.928, "E": 0.001, "F": 3.425}, FMT_M3,
           "Mainly losses on disposal, already inside Adjusted EBITDA")
    s.line("in_curtax", "Current income tax expense (statement of earnings)",
           {"B": 25.872, "C": 7.667, "D": 5.828, "E": 10.634, "F": 4.201}, FMT_M3,
           "Statement of earnings; used only in the CFO reconciliation")
    s.blank()

    # ------------------------------------------------------------------ 1.2 OE normalization assumptions
    s.header("1.2 Owners' Earnings normalization assumptions", {"B": "Value"})
    s.line("a_maint", "Maintenance capex, % of sales", {"B": 0.017}, FMT_PCT2,
           "Mgmt guidance 1.6-1.8% of sales ex network tech & new locations, midpoint (FY2025 MD&A l.526; Q2FY26 "
           "MD&A l.102). Largest single judgment in historical OE")
    s.line("a_acq", "Normalized recurring acquisition cost (US$M/yr)", {"B": 5.0}, FMT_M,
           "JUDGMENT: FY2022 actual 1.7, FY2023 actual 4.3 bracket the ordinary-course level "
           "(owners_earnings_and_roic.md sec 2.5)")
    s.line("a_tax", "Normalized tax rate", {"B": 0.265}, FMT_PCT,
           "Combined statutory rate 26.66% (2025) / 26.53% (2024), FY2025 AFS Note 10a")
    s.blank()

    # ------------------------------------------------------------------ 1.3 forecast inputs (all cases)
    B, SV, JH, OL, NL = fe.BASE_YEAR, fe.SAVINGS, fe.JOE_HUDSONS, fe.OP_LEVERAGE, fe.NEW_LOCATIONS
    CO, OO, FI = fe.CORPORATE, fe.ONE_OFFS, fe.FINANCING
    yhdr = {c: f"{y}E" for c, y in zip(YEAR_COLS, fe.YEARS)}
    s.header("1.3 Forecast inputs, common to all cases", {"B": "Value", **yhdr})
    s.line("f_pf_sales", "FY2025 pro-forma sales (2025 acquisitions annualized)", {"B": B.pro_forma_sales}, FMT_M3,
           "FY2025 AFS l.713: revenue if 2025 acquisitions owned from Jan-1-2025. Starting legacy-Boyd sales base")
    s.line("f_sav25", "Project 360 savings already inside FY2025 EBITDA", {"B": B.savings_in_ebitda}, FMT_M,
           "~$40M realized in 2025 (FY2025 MD&A l.111); stripped out of the base margin, added back as savings")
    s.line("f_cum_sav", "Cumulative cost-program savings vs 2024 base (gross)",
           {c: SV.cumulative_savings[y] for c, y in zip(YEAR_COLS, fe.YEARS)}, FMT_M,
           "$40M 2025, +$65M 2026, +$35M ratably 2027-29 (Q2FY26 MD&A l.70, l.221)")
    s.line("f_acq_rev25", "Revenue booked in 2025 by locations acquired in 2025", {"B": 31.508}, FMT_M3,
           "FY2025 AFS l.713")
    s.line("f_acq_n25", "Locations acquired in 2025 (number)", {"B": 43}, FMT_N, "FY2025 AFS l.663")
    s.line("f_jh_pre_sales", "Joe Hudson's pre-deal sales (TTM Jun-25)", {"B": JH.pre_deal_sales}, FMT_M,
           "JH release l.14")
    s.line("f_jh_pre_margin", "Joe Hudson's pre-synergy Adj. EBITDA margin (pre-rent)",
           {"B": JH.pre_synergy_margin}, FMT_PCT, "JH release l.14")
    s.line("f_jh_sales26", "Joe Hudson's FY2026E sales (conversion-disrupted)", {"B": JH.sales_2026}, FMT_M,
           "ASSUMPTION: H1'26 $342.6M x2 plus modest H2 recovery (Q2FY26 MD&A l.72, l.291)")
    s.line("f_jh_margin26", "Joe Hudson's FY2026E margin", {"B": JH.margin_2026}, FMT_PCT,
           "ASSUMPTION: ~$22M lost sales x ~46% gross margin = ~1.4pp below pre-deal")
    s.line("f_ol_sens", "Operating leverage: margin change per 1pp of SSS above breakeven", {"B": OL.sensitivity},
           FMT_N2, "CALIBRATED: mgmt 2-4% SSS -> ~+20bp/yr (FY2025 call l.281); FY2024 SSS -1.8% -> margin -1.6pp")
    s.line("f_ol_be", "Operating leverage: breakeven SSS", {"B": OL.breakeven_sss}, FMT_PCT, "CALIBRATED (as above)")
    s.line("f_ol_max", "Operating leverage: max margin gain per year", {"B": OL.max_gain_per_year}, FMT_PCT2,
           "ASSUMPTION: technician capacity limits the upside")
    s.line("f_ol_min", "Operating leverage: max margin loss per year", {"B": OL.max_loss_per_year}, FMT_PCT2,
           "ASSUMPTION: management cost response limits the downside")
    s.line("f_tuck_cost", "New location: tuck-in cost per location (2026 prices)", {"B": NL.tuck_in_cost}, FMT_M,
           "2025 consideration $120.8M / 43 = $2.81M (FY2025 AFS l.663); H1'26 $18.9M / 7 = $2.69M")
    s.line("f_tuck_sales", "New location: tuck-in mature sales (2025 prices)",
           {"B": f"=({s.ref('f_pf_sales', 'B')}-{s.ref('in_sales', 'D')}+{s.ref('f_acq_rev25', 'B')})"
                 f"/{s.ref('f_acq_n25', 'B')}"}, FMT_M3,
           "Formula: 2025 acquired revenue annualized / 43 locations (forecast_earnings.py NewLocationInputs)")
    s.line("f_start_cost", "New location: start-up cost per location (2026 prices)", {"B": NL.startup_cost}, FMT_M,
           "Pooled 2022-25 leaseholds + equipment $133.7M / 79; mgmt $1.2-1.4M (Q2FY25 call l.146)")
    s.line("f_start_sales", "New location: start-up mature sales (2025 prices)", {"B": NL.startup_sales}, FMT_M,
           "Avg revenue per location (network $3.10M, JH $2.80M)")
    s.line("f_ramp", "Ramp: share of mature earnings at age 0 / 1 / 2 / 3+ (columns B-E)",
           {"B": NL.ramp[0], "C": NL.ramp[1], "D": NL.ramp[2], "E": NL.ramp[3]}, FMT_F,
           "Age 0 = year the capex is spent. Mgmt: locations 'reach maturity by the end of their third year' "
           "(Q2FY26 MD&A l.480)")
    s.line("f_infl", "New location build / purchase cost inflation per year", {"B": NL.cost_inflation}, FMT_PCT,
           "ASSUMPTION")
    s.line("f_sw_pct", "Software capex, % of sales", {"B": CO.software_capex_pct_sales}, FMT_PCT2,
           "~0.16-0.26% of sales historically (owners_earnings_and_roic.md l.103)")
    s.line("f_deal", "Normalized recurring acquisition cost (US$M/yr)", {"B": Lnk(f"={s.ref('a_acq', 'B')}")},
           FMT_M, "Linked to 1.2")
    s.line("f_tax", "Tax rate", {"B": Lnk(f"={s.ref('a_tax', 'B')}")}, FMT_PCT, "Linked to 1.2")
    s.line("f_oo_opex_tot", "One-offs: total transformation opex budget", {"B": 51.5}, FMT_M, "Q2FY26 MD&A l.223")
    s.line("f_oo_opex_spent", "One-offs: transformation opex spent to Jun-2026", {"B": 35.6}, FMT_M,
           "Q2FY26 MD&A l.223")
    s.line("f_oo_capex_tot", "One-offs: total JH integration capex budget", {"B": 30.0}, FMT_M, "Q2FY26 MD&A l.223")
    s.line("f_oo_capex_spent", "One-offs: JH integration capex spent to Jun-2026", {"B": 9.8}, FMT_M,
           "Q2FY26 MD&A l.223")
    s.line("f_oo_share", "One-offs: share of remaining spend by year",
           {c: OO.share_by_year.get(y, 0.0) for c, y in zip(YEAR_COLS, fe.YEARS)}, FMT_PCT, "ASSUMPTION")
    s.line("f_netdebt", "Net debt ex-leases at Jun-30-2026", {"B": FI.net_debt_jun_2026}, FMT_M,
           "Q2FY26 MD&A l.361 (debt net of cash, before leases). Leverage tracking only; not used in valuation")
    s.line("f_interest", "Cash interest on debt (pre-tax, per year)", {"B": FI.cash_interest}, FMT_M,
           "Q2'26 run-rate x2 (Q2FY26 MD&A l.390)")
    s.line("f_div", "Dividends (per year)", {"B": FI.dividends}, FMT_M, "H1'26 $6.3M x2 (Q2FY26 MD&A l.390)")
    s.line("f_share26", "Share of FY2026 cash flow still to come after Jun-2026", {"B": FI.share_of_2026_remaining},
           FMT_PCT, "Only H2-2026 changes net debt after the Jun-2026 starting point")
    s.line("f_w_bear", "Forecast probability weight - Bear", {"B": fe.SCENARIO_WEIGHTS["Bear"]}, FMT_PCT,
           "forecast_earnings.py SCENARIO_WEIGHTS (used for the weighted OE line and on sheet 2)")
    s.line("f_w_base", "Forecast probability weight - Base", {"B": fe.SCENARIO_WEIGHTS["Base"]}, FMT_PCT, "")
    s.line("f_w_bull", "Forecast probability weight - Bull", {"B": fe.SCENARIO_WEIGHTS["Bull"]}, FMT_PCT, "")
    s.blank()

    # ------------------------------------------------------------------ 1.4 scenario drivers
    s.header("1.4 Scenario drivers", {"B": "Value", **yhdr})
    for case in CASES:
        sc = SCEN_DEF[case]
        s.line(None, CASE_LABEL[case], {}, bold=True)
        is_ng = case == "NoGrowth"

        def base_link(name, col):
            return Lnk(f"={s.ref('Base_' + name, col)}")

        def yearly(values, name):
            if is_ng:
                return {c: base_link(name, c) for c in YEAR_COLS}
            return {c: v for c, v in zip(YEAR_COLS, values)}

        s.line(f"{case}_claims", "  Industry repairable claims volume (pp)", yearly(sc.claims_volume_pp, "claims"),
               FMT_PP, "Components of same-store sales growth (forecast_earnings.md sec 2)" if case == "Bear" else "")
        s.line(f"{case}_tcor", "  Average total cost of repair (pp)", yearly(sc.repair_cost_pp, "tcor"), FMT_PP, "")
        s.line(f"{case}_share", "  Boyd share gain (pp)", yearly(sc.share_gain_pp, "share"), FMT_PP, "")
        units_t = [u[0] for u in sc.new_units]
        units_s = [u[1] for u in sc.new_units]
        if is_ng:
            s.line(f"{case}_tuck", "  Tuck-in acquisitions opened (number)",
                   {c: v for c, v in zip(YEAR_COLS, units_t)}, FMT_N, "No locations opened from 2026")
            s.line(f"{case}_start", "  Start-ups opened (number)", {c: v for c, v in zip(YEAR_COLS, units_s)}, FMT_N,
                   "")
        else:
            s.line(f"{case}_tuck", "  Tuck-in acquisitions opened (number)", {c: v for c, v in zip(YEAR_COLS, units_t)},
                   FMT_N, "Base 2027+: 8 start-ups/qtr pipeline plus a similar number of tuck-ins "
                          "(unit_growth_capital_check.py)" if case == "Base" else "")
            s.line(f"{case}_start", "  Start-ups opened (number)", {c: v for c, v in zip(YEAR_COLS, units_s)}, FMT_N, "")

        def scalar(name, value, fmt, note=""):
            cell = base_link(name, "B") if is_ng else value
            s.line(f"{case}_{name}", f"  {LABELS[name]}", {"B": cell}, fmt, note)

        scalar("ret", sc.savings_retention, FMT_PCT, "Share of cost-program savings kept (rest absorbed by inflation)")
        if case == "Base":
            s.line("Base_maint", f"  {LABELS['maint']}", {"B": Lnk(f"={s.ref('a_maint', 'B')}")}, FMT_PCT2,
                   "Linked to 1.2 (same management guidance midpoint)")
        else:
            scalar("maint", sc.maintenance_capex_pct_sales, FMT_PCT2)
        scalar("rentesc", sc.rent_escalator, FMT_PCT, "ASSUMPTION: annual growth of existing-business cash rent")
        scalar("roic", sc.new_location_roic, FMT_PCT,
               "Mature EBITDA after rent / location cost (pre-maintenance capex, pre-tax)")
    s.blank()

    # ------------------------------------------------------------------ 2. historical OE
    hist_hdr = {"B": "FY2023", "C": "FY2024", "D": "FY2025", "E": "TTM Jun-26"}
    s.section("CALCULATIONS")
    s.header("2. Historical Owners' Earnings - adjustments from Adjusted EBITDA", hist_hdr)
    s.text("TTM Jun-2026 = FY2025 - H1-2025 + H1-2026 for every line. Deductions shown as negatives.")

    def hist(in_name, sign=1):
        pre = "-" if sign < 0 else ""
        cells = {c: f"={pre}{s.ref(in_name, c)}" for c in ("B", "C", "D")}
        cells["E"] = f"={pre}({s.ref(in_name, 'D')}-{s.ref(in_name, 'E')}+{s.ref(in_name, 'F')})"
        return cells

    s.line("h_sales", "Sales", hist("in_sales"), FMT_M)
    s.line("h_ebitda", "Adjusted EBITDA (company-reported)", hist("in_ebitda"), FMT_M, "Already after SBC", bold=True)
    s.line("h_margin", "  Adjusted EBITDA margin",
           {c: f"={s.ref('h_ebitda', c)}/{s.ref('h_sales', c)}" for c in HIST_COLS}, FMT_PCT)
    s.line("h_lp_prop", "  Lease principal - property", hist("in_lp_prop", -1), FMT_M)
    s.line("h_lp_veh", "  Lease principal - vehicle & equipment", hist("in_lp_veh", -1), FMT_M)
    s.line("h_li_prop", "  Lease interest - property", hist("in_li_prop", -1), FMT_M)
    s.line("h_li_veh", "  Lease interest - vehicle & equipment", hist("in_li_veh", -1), FMT_M)
    s.line("h_lease", "(less) Cash lease payments (rent)",
           {c: f"=SUM({c}{s.rows['h_lp_prop']}:{c}{s.rows['h_li_veh']})" for c in HIST_COLS}, FMT_M,
           "Replaces IFRS 16 ROU depreciation + lease interest: rent is an operating cost for a leased shop network")
    s.line("h_ear", "EBITDA after rent",
           {c: f"={s.ref('h_ebitda', c)}+{s.ref('h_lease', c)}" for c in HIST_COLS}, FMT_M, bold=True)
    s.line("h_maint", "(less) Maintenance capex at assumed % of sales",
           {c: f"=-{s.ref('a_maint', 'B', absolute=True)}*{s.ref('h_sales', c)}" for c in HIST_COLS}, FMT_M,
           "Replaces PP&E depreciation")
    s.line("h_sw", "(less) Software & licensing capex (actual)", hist("in_capex_sw", -1), FMT_M,
           "Replaces software amortization")
    s.line("h_acq", "(less) Normalized recurring acquisition cost",
           {c: f"=-{s.ref('a_acq', 'B', absolute=True)}" for c in HIST_COLS}, FMT_M,
           "Adj. EBITDA excludes all deal costs; a tuck-in acquirer incurs some every year")
    s.line("h_pretax", "Pre-tax Owners' Earnings",
           {c: f"={s.ref('h_ear', c)}+{s.ref('h_maint', c)}+{s.ref('h_sw', c)}+{s.ref('h_acq', c)}"
            for c in HIST_COLS}, FMT_M, bold=True)
    s.line("h_tax", "(less) Normalized tax",
           {c: f"=-{s.ref('h_pretax', c)}*{s.ref('a_tax', 'B', absolute=True)}" for c in HIST_COLS}, FMT_M,
           "Statutory, not cash: the cash-tax shield comes from acquisition spending that OE excludes")
    s.line("h_oe", "Owners' Earnings", {c: f"={s.ref('h_pretax', c)}+{s.ref('h_tax', c)}" for c in HIST_COLS},
           FMT_M, "Amortization of acquired intangibles excluded: no capex needed to maintain them", bold=True)
    s.line("h_oe_margin", "  Owners' Earnings margin",
           {c: f"={s.ref('h_oe', c)}/{s.ref('h_sales', c)}" for c in HIST_COLS}, FMT_PCT)
    s.line("h_oe_pct", "  Owners' Earnings as % of Adjusted EBITDA",
           {c: f"={s.ref('h_oe', c)}/{s.ref('h_ebitda', c)}" for c in HIST_COLS}, FMT_PCT)
    s.line("h_equip", "Memo: actual equipment & facility capex", hist("in_capex_equip"), FMT_M)
    s.line("h_equip_pct", "Memo: actual equipment capex, % of sales",
           {c: f"={s.ref('h_equip', c)}/{s.ref('h_sales', c)}" for c in HIST_COLS}, FMT_PCT2,
           "Compare with the maintenance-capex assumption in 1.2")
    s.line("h_acq_act", "Memo: actual acquisition & transformational costs", hist("in_acq_actual"), FMT_M)
    s.line("h_cash_tax", "Memo: income taxes actually paid", hist("in_cash_tax"), FMT_M)
    s.line("h_oe_cashtax", "Memo: OE if actual cash tax replaced normalized tax",
           {c: f"={s.ref('h_pretax', c)}-{s.ref('h_cash_tax', c)}" for c in HIST_COLS}, FMT_M,
           "Sensitivity only (owners_earnings_roic.py sec 12)")
    s.blank()

    s.header("2b. Cross-check: reported cash flow from operations to normalized Owners' Earnings", hist_hdr)
    s.line("r_cfo", "Cash flow from operations (reported)", hist("in_cfo"), FMT_M)
    s.line("r_lease", "(less) Cash lease payments (actual)", {c: f"={s.ref('h_lease', c)}" for c in HIST_COLS}, FMT_M)
    s.line("r_equip", "(less) Equipment purchases & facility improvements (actual)", hist("in_capex_equip", -1), FMT_M)
    s.line("r_sw", "(less) Software purchases and licensing (actual)", hist("in_capex_sw", -1), FMT_M)
    s.line("r_after", "Cash flow after rent and actual capex",
           {c: f"=SUM({c}{s.rows['r_cfo']}:{c}{s.rows['r_sw']})" for c in HIST_COLS}, FMT_M, bold=True)
    s.line("r_wc", "(less) Working capital swing (OE normalizes to nil)", hist("in_wc", -1), FMT_M)
    s.line("r_sbc", "(less) Equity-settled SBC added back in CFO", hist("in_sbc", -1), FMT_M)
    s.line("r_other", "(less) Other non-cash items added back in CFO", hist("in_other", -1), FMT_M)
    s.line("r_acq_act", "(plus) Actual acquisition & transformational costs", hist("in_acq_actual"), FMT_M)
    s.line("r_acq_norm", "(less) Normalized recurring acquisition cost", {c: f"={s.ref('h_acq', c)}" for c in HIST_COLS},
           FMT_M)
    s.line("r_capex_diff", "(plus) Capex: actual less assumed maintenance",
           {c: f"={s.ref('h_equip', c)}+{s.ref('h_maint', c)}" for c in HIST_COLS}, FMT_M)
    s.line("r_curtax", "(plus) Current income tax expense added back", hist("in_curtax"), FMT_M,
           "Current expense, not cash paid: the WC line already carries the taxes-payable movement")
    s.line("r_normtax", "(less) Normalized income tax", {c: f"={s.ref('h_tax', c)}" for c in HIST_COLS}, FMT_M)
    s.line("r_oe", "Owners' Earnings (via cash flow)",
           {c: f"={s.ref('r_after', c)}+SUM({c}{s.rows['r_wc']}:{c}{s.rows['r_normtax']})" for c in HIST_COLS},
           FMT_M, bold=True)
    s.line("r_check", "Check: difference vs section 2 (must be nil)",
           {c: f"={s.ref('r_oe', c)}-{s.ref('h_oe', c)}" for c in HIST_COLS}, FMT_M)
    s.blank()

    # placeholder for summary: needs workings rows, which come after. Reserve rows by building workings in a
    # second builder pass: we first lay out the summary skeleton with row numbers computed after workings.
    summary_start = s.r
    return s, summary_start


LABELS = {"ret": "Savings retention", "maint": "Maintenance capex, % of sales",
          "rentesc": "Existing-business rent escalator", "roic": "New-location ROIC (mature)"}



def build_workings(s: SheetBuilder, case: str):
    """Section 4: one full forecast engine per case (forecast_earnings.py PARTS 3-5)."""
    Y = YEAR_COLS
    p = case + "_"
    s.header(f"4. Forecast workings - {CASE_LABEL[case]}",
             {"B": "", "C": "", "D": "FY2025", "E": "Jun-2026", **{c: f"{y}E" for c, y in zip(Y, fe.YEARS)}})
    s.line(p + "year", "Fiscal year", {"D": "=2025", **{c: f"={PREV_COL[c]}{s.r}+1" for c in Y}}, FMT_YEAR)
    yr = lambda c: s.ref(p + "year", c)  # noqa: E731

    # ---- same-store sales
    for key, label in (("claims", "Claims volume (pp)"), ("tcor", "Avg repair cost (pp)"), ("share", "Share gain (pp)")):
        s.line(p + "w_" + key, "  " + label, {c: Lnk(f"={s.ref(p + key, c)}") for c in Y}, FMT_PP)
    s.line(p + "sss", "Same-store sales growth",
           {c: f"=({s.ref(p + 'w_claims', c)}+{s.ref(p + 'w_tcor', c)}+{s.ref(p + 'w_share', c)})/100" for c in Y},
           FMT_PCT, "Claims volume + average repair cost + share gain")
    s.line(p + "pi", "Price / volume index vs FY2025 (cumulative SSS)",
           {"D": "=1", **{c: f"={PREV_COL[c]}{s.r}*(1+{s.ref(p + 'sss', c)})" for c in Y}}, FMT_F)
    # ---- existing business
    s.line(p + "legacy_sales", "Legacy Boyd sales (all locations open at Dec-2025)",
           {"D": Lnk(f"={s.ref('f_pf_sales', 'B', absolute=True)}"),
            **{c: f"={PREV_COL[c]}{s.r}*(1+{s.ref(p + 'sss', c)})" for c in Y}}, FMT_M,
           "FY2025 pro-forma sales grown with SSS")
    jh = {"F": Lnk(f"={s.ref('f_jh_sales26', 'B', absolute=True)}"),
          "G": f"={s.ref('f_jh_pre_sales', 'B', absolute=True)}*(1+{s.ref(p + 'sss', 'G')})"}
    jh.update({c: f"={PREV_COL[c]}{s.r}*(1+{s.ref(p + 'sss', c)})" for c in Y[2:]})
    s.line(p + "jh_sales", "Joe Hudson's sales", jh, FMT_M, "2026 disrupted; 2027 back to pre-deal run rate x (1+SSS)")
    s.line(p + "ex_sales", "Existing-business sales",
           {c: f"={s.ref(p + 'legacy_sales', c)}+{s.ref(p + 'jh_sales', c)}" for c in Y}, FMT_M, bold=True)
    ol = lambda n: s.ref(n, "B", absolute=True)  # noqa: E731
    s.line(p + "mchg", "Margin change from operating leverage",
           {c: f"=MIN(MAX({ol('f_ol_sens')}*({s.ref(p + 'sss', c)}-{ol('f_ol_be')}),{ol('f_ol_min')}),{ol('f_ol_max')})"
            for c in Y}, FMT_PCT2, "sensitivity x (SSS - breakeven), capped and floored")
    s.line(p + "legacy_margin", "Legacy Boyd margin, excluding cost-program savings",
           {"D": f"={s.ref('in_ebitda', 'D', absolute=True)}/{s.ref('in_sales', 'D', absolute=True)}"
                 f"-{s.ref(p + 'ret', 'B', absolute=True)}*{ol('f_sav25')}/{s.ref('in_sales', 'D', absolute=True)}",
            **{c: f"={PREV_COL[c]}{s.r}+{s.ref(p + 'mchg', c)}" for c in Y}}, FMT_PCT2,
           "FY2025: reported margin less the retained share of the $40M already in FY2025 EBITDA")
    jm = {"F": Lnk(f"={ol('f_jh_margin26')}"), "G": f"={ol('f_jh_pre_margin')}+{s.ref(p + 'mchg', 'G')}"}
    jm.update({c: f"={PREV_COL[c]}{s.r}+{s.ref(p + 'mchg', c)}" for c in Y[2:]})
    s.line(p + "jh_margin", "Joe Hudson's margin, excluding cost-program savings", jm, FMT_PCT2)
    s.line(p + "savings", "Retained cost-program savings",
           {c: f"={s.ref(p + 'ret', 'B', absolute=True)}*{s.ref('f_cum_sav', c)}" for c in Y}, FMT_M)
    s.line(p + "ex_ebitda", "Existing-business Adjusted EBITDA",
           {c: f"={s.ref(p + 'legacy_margin', c)}*{s.ref(p + 'legacy_sales', c)}"
               f"+{s.ref(p + 'jh_margin', c)}*{s.ref(p + 'jh_sales', c)}+{s.ref(p + 'savings', c)}" for c in Y},
           FMT_M, bold=True)
    s.line(p + "ex_margin", "  margin", {c: f"={s.ref(p + 'ex_ebitda', c)}/{s.ref(p + 'ex_sales', c)}" for c in Y},
           FMT_PCT)
    h1_rent = "+".join(s.ref(n, "F", absolute=True) for n in ("in_lp_prop", "in_lp_veh", "in_li_prop", "in_li_veh"))
    rent = {"F": f"=2*({h1_rent})"}
    rent.update({c: f"={PREV_COL[c]}{s.r}*(1+{s.ref(p + 'rentesc', 'B', absolute=True)})" for c in Y[1:]})
    s.line(p + "rent", "Existing-business cash rent", rent, FMT_M, "2026 = H1-2026 actual x2; then x (1 + escalator)")
    s.line(p + "rent_ratio", "  rent % of existing sales",
           {c: f"={s.ref(p + 'rent', c)}/{s.ref(p + 'ex_sales', c)}" for c in Y}, FMT_PCT2)

    # ---- new-location cohorts (column = opening year)
    s.text("New-location cohorts: each column below is the cohort OPENED in that year.")
    s.line(p + "c_tuck", "  Tuck-ins opened", {c: Lnk(f"={s.ref(p + 'tuck', c)}") for c in Y}, FMT_N)
    s.line(p + "c_start", "  Start-ups opened", {c: Lnk(f"={s.ref(p + 'start', c)}") for c in Y}, FMT_N)
    s.line(p + "c_infl", "  Cost inflation index",
           {c: f"=(1+{ol('f_infl')})^({yr(c)}-{s.ref(p + 'year', 'F', absolute=True)})" for c in Y}, FMT_F)
    s.line(p + "c_cost", "  Cohort cost = growth capex",
           {c: f"=({s.ref(p + 'c_tuck', c)}*{ol('f_tuck_cost')}+{s.ref(p + 'c_start', c)}*{ol('f_start_cost')})"
               f"*{s.ref(p + 'c_infl', c)}" for c in Y}, FMT_M)
    s.line(p + "c_msales", "  Cohort mature sales, 2025 prices",
           {c: f"={s.ref(p + 'c_tuck', c)}*{ol('f_tuck_sales')}+{s.ref(p + 'c_start', c)}*{ol('f_start_sales')}"
            for c in Y}, FMT_M)
    ramp = s.rng("f_ramp", "B", "E")
    s.line(p + "c_mat", "  Year cohort reaches maturity",
           {c: f"={yr(c)}+COUNT({ramp})-1" for c in Y}, FMT_YEAR)
    pi_rng = s.rng(p + "pi", "F", "K")
    roic = s.ref(p + "roic", "B", absolute=True)

    def matrix(key: str, label: str, fmt: str, formula):
        s.text(f"{label}: rows = cohort opened in year shown in column B; columns = calendar year.")
        for oc in Y:                                     # opening-year column of the cohort
            s.line(f"{p}{key}_{oc}", f"    cohort", {"B": Lnk(f"={yr(oc)}"),
                   **{c: formula(oc, c) for c in Y}}, fmt)
            s.ws[f"B{s.r - 1}"].number_format = FMT_YEAR
        return [f"{p}{key}_{oc}" for oc in Y]

    def age(oc, c):
        return f"({yr(c)}-B{s.r})"

    matrix("ramp", "  Ramp share", FMT_F,
           lambda oc, c: f"=IF({age(oc, c)}<0,0,INDEX({ramp},MIN({age(oc, c)},COUNT({ramp})-1)+1))")
    matrix("grow", "  Growth since maturity (joins same-store base)", FMT_F,
           lambda oc, c: f"=IF({yr(c)}>{s.ref(p + 'c_mat', oc, absolute=True)},{s.ref(p + 'pi', c)}"
                         f"/INDEX({pi_rng},MIN({s.ref(p + 'c_mat', oc, absolute=True)}"
                         f"-{s.ref(p + 'year', 'F', absolute=True)}+1,6)),1)")
    matrix("rrear", "  Run-rate EBITDA after rent (as if fully ramped)", FMT_M,
           lambda oc, c: f"=IF({yr(c)}>=B{s.r},{roic}*{s.ref(p + 'c_cost', oc, absolute=True)}"
                         f"*{s.ref(p + 'grow_' + oc, c)},0)")
    matrix("rrsales", "  Run-rate sales (as if fully ramped)", FMT_M,
           lambda oc, c: f"=IF({yr(c)}>=B{s.r},{s.ref(p + 'c_msales', oc, absolute=True)}*{s.ref(p + 'pi', c)},0)")
    matrix("ear", "  EBITDA after rent = run-rate x ramp share", FMT_M,
           lambda oc, c: f"={s.ref(p + 'rrear_' + oc, c)}*{s.ref(p + 'ramp_' + oc, c)}")
    matrix("nsales", "  Sales = run-rate x ramp share", FMT_M,
           lambda oc, c: f"={s.ref(p + 'rrsales_' + oc, c)}*{s.ref(p + 'ramp_' + oc, c)}")

    def col_sum(key, c):
        return f"=SUM({c}{s.rows[p + key + '_F']}:{c}{s.rows[p + key + '_K']})"

    s.line(p + "units", "New locations opened in year",
           {c: f"={s.ref(p + 'c_tuck', c)}+{s.ref(p + 'c_start', c)}" for c in Y}, FMT_N)
    s.line(p + "units_cum", "New locations open, cumulative",
           {"F": f"={s.ref(p + 'units', 'F')}", **{c: f"={PREV_COL[c]}{s.r}+{s.ref(p + 'units', c)}" for c in Y[1:]}},
           FMT_N)
    s.line(p + "gcapex", "Growth capex (this year's cohort cost)", {c: f"={s.ref(p + 'c_cost', c)}" for c in Y}, FMT_M)
    s.line(p + "new_ear", "New-location EBITDA after rent", {c: col_sum("ear", c) for c in Y}, FMT_M, bold=True)
    s.line(p + "new_sales", "New-location sales", {c: col_sum("nsales", c) for c in Y}, FMT_M)
    s.line(p + "new_rr_ear", "Memo: new-location run-rate EBITDA after rent", {c: col_sum("rrear", c) for c in Y}, FMT_M)
    s.line(p + "new_rr_sales", "Memo: new-location run-rate sales", {c: col_sum("rrsales", c) for c in Y}, FMT_M)
    s.line(p + "new_rent", "Memo: new-location rent (sales x network rent ratio)",
           {c: f"={s.ref(p + 'rent_ratio', c)}*{s.ref(p + 'new_sales', c)}" for c in Y}, FMT_M,
           "Presentation only: new-location earnings are modelled after rent")

    # ---- corporate
    s.line(p + "tot_sales", "Total sales", {c: f"={s.ref(p + 'ex_sales', c)}+{s.ref(p + 'new_sales', c)}" for c in Y},
           FMT_M, bold=True)
    s.line(p + "tot_ebitda", "Total Adjusted EBITDA (memo, pre-rent)",
           {c: f"={s.ref(p + 'ex_ebitda', c)}+{s.ref(p + 'new_ear', c)}+{s.ref(p + 'new_rent', c)}" for c in Y}, FMT_M)
    s.line(p + "ear", "EBITDA after rent", {c: f"={s.ref(p + 'ex_ebitda', c)}-{s.ref(p + 'rent', c)}"
                                            f"+{s.ref(p + 'new_ear', c)}" for c in Y}, FMT_M, bold=True)
    s.line(p + "maint_capex", "Maintenance capex",
           {c: f"={s.ref(p + 'maint', 'B', absolute=True)}*{s.ref(p + 'tot_sales', c)}" for c in Y}, FMT_M)
    s.line(p + "sw", "Software capex", {c: f"={ol('f_sw_pct')}*{s.ref(p + 'tot_sales', c)}" for c in Y}, FMT_M)
    s.line(p + "deal", "Normalized acquisition cost", {c: Lnk(f"={ol('f_deal')}") for c in Y}, FMT_M)
    s.line(p + "pretax", "Pre-tax Owners' Earnings",
           {c: f"={s.ref(p + 'ear', c)}-{s.ref(p + 'maint_capex', c)}-{s.ref(p + 'sw', c)}-{s.ref(p + 'deal', c)}" for c in Y},
           FMT_M)
    tax = ol("f_tax")
    s.line(p + "oe", "Owners' Earnings", {c: f"={s.ref(p + 'pretax', c)}*(1-{tax})" for c in Y}, FMT_M, bold=True)
    s.line(p + "capex_rate", "Maintenance + software capex rate", {"B": f"={s.ref(p + 'maint', 'B')}+{ol('f_sw_pct')}"},
           FMT_PCT2)
    rate = s.ref(p + "capex_rate", "B", absolute=True)
    s.line(p + "oe_ex", "  OE from existing business",
           {c: f"=({s.ref(p + 'ex_ebitda', c)}-{s.ref(p + 'rent', c)}-{rate}*{s.ref(p + 'ex_sales', c)}"
               f"-{s.ref(p + 'deal', c)})*(1-{tax})" for c in Y}, FMT_M)
    s.line(p + "oe_new", "  OE from new locations",
           {c: f"=({s.ref(p + 'new_ear', c)}-{rate}*{s.ref(p + 'new_sales', c)})*(1-{tax})" for c in Y}, FMT_M)
    s.line(p + "oe_new_rr", "  Memo: new-location OE if all cohorts were mature",
           {c: f"=({s.ref(p + 'new_rr_ear', c)}-{rate}*{s.ref(p + 'new_rr_sales', c)})*(1-{tax})" for c in Y}, FMT_M)
    s.line(p + "oe_ramp", "  Memo: OE still ramping",
           {c: f"={s.ref(p + 'oe_new_rr', c)}-{s.ref(p + 'oe_new', c)}" for c in Y}, FMT_M)
    s.line(p + "oneoffs", "One-off integration costs (after tax)",
           {c: f"={s.ref('f_oo_share', c, absolute=True)}*(({ol('f_oo_opex_tot')}-{ol('f_oo_opex_spent')})*(1-{tax})"
               f"+({ol('f_oo_capex_tot')}-{ol('f_oo_capex_spent')}))" for c in Y}, FMT_M)
    s.line(p + "dist", "Distributable cash = OE - growth capex - one-offs",
           {c: f"={s.ref(p + 'oe', c)}-{s.ref(p + 'gcapex', c)}-{s.ref(p + 'oneoffs', c)}" for c in Y}, FMT_M,
           bold=True)
    s.line(p + "cash_fin", "Cash after after-tax interest and dividends",
           {c: f"={s.ref(p + 'dist', c)}-{ol('f_interest')}*(1-{tax})-{ol('f_div')}" for c in Y}, FMT_M)
    nd = {"E": Lnk(f"={ol('f_netdebt')}"), "F": f"=E{s.r}-{s.ref(p + 'cash_fin', 'F')}*{ol('f_share26')}"}
    nd.update({c: f"={PREV_COL[c]}{s.r}-{s.ref(p + 'cash_fin', c)}" for c in Y[1:]})
    s.line(p + "netdebt", "Net debt ex-leases, period end", nd, FMT_M)
    s.line(p + "lev", "Net debt / EBITDA after rent",
           {c: f"={s.ref(p + 'netdebt', c)}/{s.ref(p + 'ear', c)}" for c in Y}, FMT_X2)
    s.blank()


def build_summary(s: SheetBuilder, start_row: int):
    """Section 3: historical and forecast side by side, per case (links only)."""
    s.r = start_row
    s.header("3. Owners' Earnings - historical and forecast side by side",
             {"B": "FY2023", "C": "FY2024", "D": "FY2025", "E": "TTM Jun-26",
              **{c: f"{y}E" for c, y in zip(YEAR_COLS, fe.YEARS)}})
    s.text("Historical columns link to section 2; forecast columns link to the section 4 workings for each case.")
    for case in CASES:
        p = case + "_"
        S = "S_" + case + "_"
        s.line(None, CASE_LABEL[case], {}, bold=True)

        def both(hist_name, fc_formula, hist_sign=""):
            cells = {c: f"={hist_sign}{s.ref(hist_name, c)}" for c in HIST_COLS} if hist_name else {}
            cells.update({c: fc_formula(c) for c in YEAR_COLS})
            return cells

        s.line(S + "sales", "Sales", both("h_sales", lambda c: f"={s.ref(p + 'tot_sales', c)}"), FMT_M)
        growth = {"C": f"=C{s.r - 1}/B{s.r - 1}-1", "D": f"=D{s.r - 1}/C{s.r - 1}-1", "F": f"=F{s.r - 1}/D{s.r - 1}-1"}
        growth.update({c: f"={c}{s.r - 1}/{PREV_COL[c]}{s.r - 1}-1" for c in YEAR_COLS[1:]})
        s.line(S + "growth", "  growth (FY2026E vs FY2025)", growth, FMT_PCT)
        s.line(S + "ebitda", "Adjusted EBITDA", both("h_ebitda", lambda c: f"={s.ref(p + 'tot_ebitda', c)}"), FMT_M)
        s.line(S + "margin", "  margin", {c: f"={c}{s.r - 1}/{s.ref(S + 'sales', c)}" for c in HIST_COLS + YEAR_COLS},
               FMT_PCT)
        s.line(S + "rent", "(less) Cash rent",
               both("h_lease", lambda c: f"=-({s.ref(p + 'rent', c)}+{s.ref(p + 'new_rent', c)})"), FMT_M)
        s.line(S + "ear", "EBITDA after rent", both("h_ear", lambda c: f"={s.ref(p + 'ear', c)}"), FMT_M, bold=True)
        s.line(S + "maint", "(less) Maintenance capex", both("h_maint", lambda c: f"=-{s.ref(p + 'maint_capex', c)}"), FMT_M)
        s.line(S + "sw", "(less) Software capex", both("h_sw", lambda c: f"=-{s.ref(p + 'sw', c)}"), FMT_M)
        s.line(S + "acq", "(less) Normalized acquisition cost", both("h_acq", lambda c: f"=-{s.ref(p + 'deal', c)}"),
               FMT_M)
        s.line(S + "pretax", "Pre-tax Owners' Earnings", both("h_pretax", lambda c: f"={s.ref(p + 'pretax', c)}"),
               FMT_M)
        s.line(S + "tax", "(less) Tax at normalized rate",
               both("h_tax", lambda c: f"={s.ref(p + 'oe', c)}-{s.ref(p + 'pretax', c)}"), FMT_M)
        s.line(S + "oe", "Owners' Earnings", both("h_oe", lambda c: f"={s.ref(p + 'oe', c)}"), FMT_M, bold=True)
        s.line(S + "oe_margin", "  OE margin",
               {c: f"={s.ref(S + 'oe', c)}/{s.ref(S + 'sales', c)}" for c in HIST_COLS + YEAR_COLS}, FMT_PCT)
        g = {"C": f"=C{s.rows[S + 'oe']}/B{s.rows[S + 'oe']}-1", "D": f"=D{s.rows[S + 'oe']}/C{s.rows[S + 'oe']}-1",
             "F": f"=F{s.rows[S + 'oe']}/D{s.rows[S + 'oe']}-1"}
        g.update({c: f"={c}{s.rows[S + 'oe']}/{PREV_COL[c]}{s.rows[S + 'oe']}-1" for c in YEAR_COLS[1:]})
        s.line(S + "oe_growth", "  OE growth (FY2026E vs FY2025)", g, FMT_PCT)
        s.line(S + "oe_new", "  of which new locations (opened 2026+)",
               {c: f"={s.ref(p + 'oe_new', c)}" for c in YEAR_COLS}, FMT_M)
        s.line(S + "gcapex", "(less) Growth capex", {c: f"=-{s.ref(p + 'gcapex', c)}" for c in YEAR_COLS}, FMT_M)
        s.line(S + "oneoffs", "(less) One-off integration costs, after tax",
               {c: f"=-{s.ref(p + 'oneoffs', c)}" for c in YEAR_COLS}, FMT_M)
        s.line(S + "dist", "Distributable cash", {c: f"={s.ref(p + 'dist', c)}" for c in YEAR_COLS}, FMT_M, bold=True)
        s.line(S + "netdebt", "Net debt ex-leases, period end (Jun-2026 in TTM column)",
               {"E": f"={s.ref(p + 'netdebt', 'E')}", **{c: f"={s.ref(p + 'netdebt', c)}" for c in YEAR_COLS}}, FMT_M)
        s.blank()
    w = {k: s.ref("f_w_" + k.lower(), "B", absolute=True) for k in ("Bear", "Base", "Bull")}
    s.line("P_oe", "Probability-weighted OE (Bear/Base/Bull weights in 1.3)",
           {c: "=" + "+".join(f"{w[k]}*{s.ref('S_' + k + '_oe', c)}" for k in w) for c in YEAR_COLS},
           FMT_M, bold=True)
    s.line("P_dist", "Probability-weighted distributable cash",
           {c: "=" + "+".join(f"{w[k]}*{s.ref('S_' + k + '_dist', c)}" for k in w) for c in YEAR_COLS}, FMT_M)
    s.blank()


# =====================================================================================================
# SHEET 2 - TERMINAL VALUE
# =====================================================================================================

def build_terminal(wb: Workbook, e: SheetBuilder) -> SheetBuilder:
    s = SheetBuilder(wb, "2 Terminal Value")
    legend(s, "Boyd Group Services (BYD.TO) - Sheet 2: Terminal value at end-2031 (undiscounted)",
           "US$ millions. TV = EV/EBITDA-after-rent multiple x FY2031E EBITDA after rent + same multiple x ramp gap. "
           "Python source: terminal_value.py. Multiples from collision-repair deal evidence, not Boyd's share price.")
    cols = {VAL_COL[c]: CASE_LABEL[c].split(" (")[0] for c in VAL_CASES}
    s.section("INPUTS")
    s.header("2.1 Exit multiple (EV / EBITDA after rent)", cols)
    s.line("mult", "Chosen exit multiple", {VAL_COL[c]: tv.CHOSEN_MULTIPLE[TV_KEY[c]] for c in VAL_CASES}, FMT_X,
           "JUDGMENT within the deal evidence in 2.4 (terminal_value.md sec 6-7). No growth = base (same network)")
    s.blank()
    s.header("2.2 Steady-state assumptions (value-driver cross-check only)", cols)
    st = {c: tv.STEADY[TV_KEY[c]] for c in VAL_CASES}
    s.line("g_nc", "Growth without new capital (claims volume + repair cost)",
           {VAL_COL[c]: (Lnk(f"={VAL_COL['Base']}{s.r}") if c == "NoGrowth" else st[c].growth_no_capital)
            for c in VAL_CASES}, FMT_PCT, "Bear -1.5+2.0; Base -1.0+3.0; Bull capped so total g = 3% (impairment test)")
    s.line("g_share", "Growth from share gains needing new capacity",
           {VAL_COL[c]: st[c].growth_share for c in VAL_CASES}, FMT_PCT, "None in the no-growth-capex case")
    s.line("oe_yield", "After-tax OE yield on new capacity",
           {VAL_COL[c]: (Lnk(f"={VAL_COL['Base']}{s.r}") if c == "NoGrowth" else st[c].new_capacity_oe_yield)
            for c in VAL_CASES}, FMT_PCT, "Mature unit OE yield (forecast_earnings.md sec 6.4)")
    s.blank()
    it = tv.ImpairmentTest()
    s.header("2.3 Other cross-check inputs", {"B": "Value"})
    s.line("imp_g", "Boyd impairment test: terminal growth", {"B": it.terminal_growth}, FMT_PCT, "FY2025 AFS l.966")
    s.line("imp_lo", "Boyd impairment test: WACC low", {"B": it.wacc_low}, FMT_PCT, "FY2025 AFS l.966")
    s.line("imp_hi", "Boyd impairment test: WACC high", {"B": it.wacc_high}, FMT_PCT, "FY2025 AFS l.966")
    s.line("xr", "Cross-check discount rate (midpoint of impairment WACC)",
           {"B": f"=AVERAGE({s.ref('imp_lo', 'B')},{s.ref('imp_hi', 'B')})"}, FMT_PCT,
           "Formula. Used only for value-driver check and to compound 2026-31 cash in 3.4")
    s.line("margin_target", "Management Adj. EBITDA margin target", {"B": 0.14}, FMT_PCT,
           "Q2FY26 MD&A (14% target); used in the margin-normalization check")
    s.line("w_bear", "Forecast weight - Bear", {"B": Lnk(f"={e.ref('f_w_bear', 'B', s)}")}, FMT_PCT, "Linked to sheet 1")
    s.line("w_base", "Forecast weight - Base", {"B": Lnk(f"={e.ref('f_w_base', 'B', s)}")}, FMT_PCT, "Linked to sheet 1")
    s.line("w_bull", "Forecast weight - Bull", {"B": Lnk(f"={e.ref('f_w_bull', 'B', s)}")}, FMT_PCT, "Linked to sheet 1")
    s.blank()
    s.header("2.4 Collision-repair valuation evidence (EV / EBITDA after rent)", {"B": "Low", "C": "High", "D": "Mid"})
    for i, pe in enumerate(tv.PEER_EVIDENCE):
        s.line(f"peer{i}", pe.label, {"B": pe.low, "C": pe.high, "D": f"=AVERAGE(B{s.r},C{s.r})"}, FMT_X,
               f"Knowledge Store IDs {pe.source[3:]}" if pe.source.startswith("KS") else pe.source)
    s.blank()
    jd = tv.JoeHudsonsDeal()
    s.header("2.5 Joe Hudson's deal (fetched_docs/boyd_joe_hudsons_acquisition_announcement.md)", {"B": "Value"})
    s.line("jh_price", "Purchase price", {"B": jd.purchase_price}, FMT_M, "line 13")
    s.line("jh_taxben", "Expected tax benefits", {"B": jd.expected_tax_benefits}, FMT_M,
           "line 43 ('approximately $150 million'); also used as a standalone asset on sheet 3")
    s.line("jh_ear_ttm", "JHCC Adj. EBITDA, US GAAP (after rent), TTM", {"B": jd.ebitda_after_rent_ttm}, FMT_M, "line 37")
    s.line("jh_pre_ttm", "JHCC Adj. EBITDA, IFRS-like (pre-rent), TTM", {"B": jd.ebitda_pre_rent_ttm}, FMT_M, "line 37")
    s.line("jh_m_rr", "Disclosed multiple, run-rate pre-synergy", {"B": jd.disclosed_multiple_run_rate}, FMT_X, "line 43")
    s.line("jh_m_syn", "Disclosed multiple, run-rate + synergies", {"B": jd.disclosed_multiple_run_rate_synergies},
           FMT_X, "line 43")
    s.line("jh_syn_lo", "Disclosed synergies, low", {"B": jd.synergies_low}, FMT_M, "line 45")
    s.line("jh_syn_hi", "Disclosed synergies, high", {"B": jd.synergies_high}, FMT_M, "line 45")
    s.blank()
    ama = tv.AmaGroup()
    s.header("2.6 AMA Group (ASX: AMA), listed pure-play, A$M", {"B": "Value"})
    s.line("ama_cap", "Market capitalization (2026-09-25)", {"B": ama.market_cap}, FMT_M,
           "Knowledge Store ID 26 (moderate confidence)")
    s.line("ama_nd", "Net debt, FY26 (ex-leases)", {"B": ama.net_debt}, FMT_M, "Knowledge Store ID 26")
    s.line("ama_e26", "EBITDA FY26 (pre-AASB 16, i.e. after rent)", {"B": ama.ebitda_fy26}, FMT_M, "Knowledge Store ID 26")
    s.line("ama_e27lo", "EBITDA FY27 guidance low", {"B": ama.ebitda_fy27_guide_low}, FMT_M, "Knowledge Store ID 26")
    s.line("ama_e27hi", "EBITDA FY27 guidance high", {"B": ama.ebitda_fy27_guide_high}, FMT_M, "Knowledge Store ID 26")
    s.blank()
    s.header("2.7 Sensitivity axes", {"B": "", "C": "", "D": "", "E": "", "F": "", "G": "", "H": ""}, note="")
    s.line("sens_m", "Exit multiples to test", {c: m for c, m in zip("BCDEFGH", (7.0, 7.5, 8.0, 8.5, 9.0, 9.3, 10.0))},
           FMT_X)
    s.line("sens_r", "Discount rates to test (value-driver grid)", {c: r for c, r in zip("BCD", (0.08, 0.09, 0.10))},
           FMT_PCT)
    s.line("sens_g", "Total growth rates to test (value-driver grid)",
           {c: g for c, g in zip("BCDE", (0.015, 0.020, 0.025, 0.030))}, FMT_PCT)
    s.blank()

    # ------------------------------------------------------------------ calculations
    s.section("CALCULATIONS")
    hdr = {**cols, WTD_COL: "Weighted"}
    s.header("2.8 FY2031E terminal-year inputs (linked from sheet 1)", hdr)
    link31 = lambda key: {VAL_COL[c]: Lnk(f"={e.ref(c + '_' + key, 'K', s)}") for c in VAL_CASES}  # noqa: E731
    s.line("sales31", "FY2031E total sales", link31("tot_sales"), FMT_M)
    s.line("ear31", "FY2031E EBITDA after rent", link31("ear"), FMT_M)
    s.line("new31", "  of which new locations", link31("new_ear"), FMT_M)
    s.line("rr31", "New-location run-rate EBITDA after rent", link31("new_rr_ear"), FMT_M)
    s.line("oe31", "FY2031E Owners' Earnings", link31("oe"), FMT_M)
    s.line("exm31", "FY2031E existing-business margin", link31("ex_margin"), FMT_PCT)
    s.line("exs31", "FY2031E existing-business sales", link31("ex_sales"), FMT_M)
    s.blank()

    def wsum(name):
        """Bear/Base/Bull weighted sum of a row (the current row if `name` is not yet written)."""
        row = s.rows.get(name, s.r)
        return (f"={s.ref('w_bear', 'B', absolute=True)}*B{row}+{s.ref('w_base', 'B', absolute=True)}*C{row}"
                f"+{s.ref('w_bull', 'B', absolute=True)}*E{row}")
    s.header("2.9 Terminal value at end-2031 (undiscounted)", hdr)
    s.text("Weighted column = Bear/Base/Bull at the sheet 1 forecast weights (25/50/25); memo only. "
           "Sheet 3 applies its own case weights.")
    vc = [VAL_COL[c] for c in VAL_CASES]
    s.line("gap", "Ramp gap = run-rate less actual new-location EBITDA after rent",
           {c: f"={s.ref('rr31', c)}-{s.ref('new31', c)}" for c in vc}, FMT_M,
           "Earnings already paid for (capex spent) but not yet earned in 2031")
    s.line("tv_ear", "Multiple x FY2031E EBITDA after rent",
           {**{c: f"={s.ref('mult', c)}*{s.ref('ear31', c)}" for c in vc}, WTD_COL: wsum("tv_ear")}, FMT_M)
    s.line("tv_uplift", "Plus: ramp uplift = multiple x ramp gap",
           {**{c: f"={s.ref('mult', c)}*{s.ref('gap', c)}" for c in vc}, WTD_COL: wsum("tv_uplift")}, FMT_M,
           "No deduction for the 1-3 years before the gap is earned")
    s.line("tv", "Terminal value, end-2031",
           {**{c: f"={s.ref('tv_ear', c)}+{s.ref('tv_uplift', c)}" for c in vc}, WTD_COL: wsum("tv")}, FMT_M, bold=True)
    s.line("tv_oe", "  TV / FY2031E Owners' Earnings",
           {**{c: f"={s.ref('tv', c)}/{s.ref('oe31', c)}" for c in vc},
            WTD_COL: f"={s.ref('tv', WTD_COL)}/({wsum('oe31')[1:]})"}, FMT_X)
    s.line("tv_mult_w", "  Effective multiple on EBITDA after rent",
           {**{c: f"={s.ref('tv_ear', c)}/{s.ref('ear31', c)}" for c in vc},
            WTD_COL: f"={s.ref('tv_ear', WTD_COL)}/({wsum('ear31')[1:]})"}, FMT_X)
    s.blank()

    s.header("2.10 Base and no-growth TV sensitivity to the exit multiple", {"B": "Multiple", "C": "Base TV",
                                                                              "D": "No growth TV"})
    for i, col in enumerate("BCDEFGH"):
        m = s.ref("sens_m", col, absolute=True)
        s.line(f"sm{i}", "  TV at multiple", {
            "B": Lnk(f"={m}"),
            "C": f"={m}*({s.ref('ear31', 'C', absolute=True)}+{s.ref('gap', 'C', absolute=True)})",
            "D": f"={m}*({s.ref('ear31', 'D', absolute=True)}+{s.ref('gap', 'D', absolute=True)})"}, FMT_M)
        s.ws[f"B{s.r - 1}"].number_format = FMT_X
    s.blank()

    # growth programme: base vs no growth
    ycols = ["B", "C", "D", "E", "F", "G"]
    s.header("2.11 What the 2026-31 growth programme is worth at end-2031 (Base vs No growth)",
             {c: str(y) for c, y in zip(ycols, fe.YEARS)} | {"H": "Total"})
    s.line("gp_year", "Year", {c: Lnk(f"={e.ref('Base_year', yc, s)}") for c, yc in zip(ycols, YEAR_COLS)}, FMT_YEAR)
    s.line("gp_base", "Base distributable cash", {c: Lnk(f"={e.ref('Base_dist', yc, s)}") for c, yc in zip(ycols, YEAR_COLS)}
           | {"H": f"=SUM(B{s.r}:G{s.r})"}, FMT_M)
    s.line("gp_ng", "No-growth distributable cash",
           {c: Lnk(f"={e.ref('NoGrowth_dist', yc, s)}") for c, yc in zip(ycols, YEAR_COLS)}
           | {"H": f"=SUM(B{s.r}:G{s.r})"}, FMT_M)
    s.line("gp_diff", "Difference (Base less No growth)",
           {c: f"={s.ref('gp_base', c)}-{s.ref('gp_ng', c)}" for c in ycols} | {"H": f"=SUM(B{s.r}:G{s.r})"}, FMT_M)
    s.line("gp_fvf", "Compounding factor to end-2031 at cross-check rate",
           {c: f"=(1+{s.ref('xr', 'B', absolute=True)})^({s.ref('gp_year', 'G', absolute=True)}-{s.ref('gp_year', c)})"
            for c in ycols}, FMT_F)
    s.line("gp_fv", "Difference compounded to end-2031",
           {"H": f"=SUMPRODUCT(B{s.rows['gp_diff']}:G{s.rows['gp_diff']},B{s.rows['gp_fvf']}:G{s.rows['gp_fvf']})"},
           FMT_M)
    s.line("gp_dtv", "Extra terminal value from 2026-31 locations",
           {"H": f"={s.ref('tv', 'C')}-{s.ref('tv', 'D')}"}, FMT_M)
    s.line("gp_net", "Net value of the growth programme at end-2031",
           {"H": f"={s.ref('gp_dtv', 'H')}+{s.ref('gp_fv', 'H')}"}, FMT_M, "Close to nil: growth capex ~value-neutral",
           bold=True)
    s.blank()

    s.header("2.12 Cross-check: value-driver formula on Owners' Earnings", cols)
    s.line("vd_g", "Total steady-state growth g", {c: f"={s.ref('g_nc', c)}+{s.ref('g_share', c)}" for c in vc}, FMT_PCT)
    s.line("vd_reinv", "Reinvestment rate = share growth / OE yield",
           {c: f"={s.ref('g_share', c)}/{s.ref('oe_yield', c)}" for c in vc}, FMT_PCT)
    xr = s.ref("xr", "B", absolute=True)
    s.line("vd_mult", "Fundamental TV/OE at cross-check rate = (1+g)(1-reinv)/(r-g)",
           {c: f"=(1+{s.ref('vd_g', c)})*(1-{s.ref('vd_reinv', c)})/({xr}-{s.ref('vd_g', c)})" for c in vc}, FMT_X)
    s.line("vd_chosen", "Chosen TV / OE (from 2.9)", {c: f"={s.ref('tv_oe', c)}" for c in vc}, FMT_X)
    s.line("vd_implied_r", "Discount rate implied by the chosen TV",
           {c: f"={s.ref('vd_g', c)}+(1+{s.ref('vd_g', c)})*(1-{s.ref('vd_reinv', c)})/{s.ref('vd_chosen', c)}"
            for c in vc}, FMT_PCT2, "Chosen deal multiples imply ~8-9% returns")
    s.blank()
    s.header("2.13 Base value-driver TV/OE grid (rows = discount rate, columns = total growth)",
             {"B": "", "C": "", "D": "", "E": ""}, note="")
    s.line("grid_g", "Total growth g", {c: Lnk(f"={s.ref('sens_g', c)}") for c in "BCDE"}, FMT_PCT)
    for i, rc in enumerate("BCD"):
        r_ref = s.ref("sens_r", rc, absolute=True)
        gs = s.ref("g_share", "C", absolute=True)
        oy = s.ref("oe_yield", "C", absolute=True)
        s.line(f"grid{i}", "  TV/OE at discount rate (col A label) ->",
               {c: f"=(1+{s.ref('grid_g', c, absolute=True)})*(1-{gs}/{oy})/({r_ref}-{s.ref('grid_g', c, absolute=True)})"
                for c in "BCDE"}, FMT_X)
        s.ws[f"A{s.r - 1}"] = f"  TV/OE at discount rate {['8%', '9%', '10%'][i]} (row input 2.7 col {rc})"
    s.blank()
    s.header("2.14 Other cross-checks", {"B": "Value"})
    g_imp = s.ref("imp_g", "B")
    s.line("imp_mlo", "Impairment-test cash-flow multiple at WACC high", {"B": f"=(1+{g_imp})/({s.ref('imp_hi', 'B')}-{g_imp})"},
           FMT_X)
    s.line("imp_mhi", "Impairment-test cash-flow multiple at WACC low", {"B": f"=(1+{g_imp})/({s.ref('imp_lo', 'B')}-{g_imp})"},
           FMT_X)
    s.line("mn_lost", "Base: EBITDA lost if existing margin normalized to target",
           {"B": f"=({s.ref('exm31', 'C')}-{s.ref('margin_target', 'B')})*{s.ref('exs31', 'C')}"}, FMT_M)
    s.line("mn_tv", "Base: TV lower by", {"B": f"={s.ref('mult', 'C')}*{s.ref('mn_lost', 'B')}"}, FMT_M)
    s.line("jh_net", "Joe Hudson's: net price (price less tax benefits)",
           {"B": f"={s.ref('jh_price', 'B')}-{s.ref('jh_taxben', 'B')}"}, FMT_M)
    s.line("jh_rr", "Joe Hudson's: implied run-rate EBITDA after rent", {"B": f"={s.ref('jh_net', 'B')}/{s.ref('jh_m_rr', 'B')}"},
           FMT_M)
    s.line("jh_syn", "Joe Hudson's: implied synergies",
           {"B": f"={s.ref('jh_net', 'B')}/{s.ref('jh_m_syn', 'B')}-{s.ref('jh_rr', 'B')}"}, FMT_M,
           "Compare with disclosed 35-45")
    s.line("jh_raw", "Joe Hudson's: multiple on raw TTM EBITDA after rent",
           {"B": f"={s.ref('jh_net', 'B')}/{s.ref('jh_ear_ttm', 'B')}"}, FMT_X)
    s.line("jh_max", "Joe Hudson's: max multiple if disclosed basis were pre-rent",
           {"B": f"={s.ref('jh_net', 'B')}/{s.ref('jh_pre_ttm', 'B')}"}, FMT_X,
           "Below 13.3x, so the disclosed multiple must be on after-rent EBITDA")
    s.line("ama_ev", "AMA Group: EV (A$M)", {"B": f"={s.ref('ama_cap', 'B')}+{s.ref('ama_nd', 'B')}"}, FMT_M)
    s.line("ama_m26", "AMA Group: EV / FY26 EBITDA", {"B": f"={s.ref('ama_ev', 'B')}/{s.ref('ama_e26', 'B')}"}, FMT_X)
    s.line("ama_m27", "AMA Group: EV / FY27 guidance (high end of EBITDA)",
           {"B": f"={s.ref('ama_ev', 'B')}/{s.ref('ama_e27hi', 'B')}"}, FMT_X)
    return s


# =====================================================================================================
# SHEET 3 - SUM OF THE PARTS VALUATION
# =====================================================================================================

def build_valuation(wb: Workbook, e: SheetBuilder, t: SheetBuilder) -> SheetBuilder:
    s = SheetBuilder(wb, "3 SOTP Valuation")
    legend(s, "Boyd Group Services (BYD.TO) - Sheet 3: Sum-of-the-parts valuation per share",
           "US$ millions unless stated. Value = PV(2026-31 distributable cash) + PV(terminal value) + standalone "
           "assets - debt. Python source: valuation.py. Trading price not used.")
    ST, H1, D, A, R, SH, FX, JT = (val.SETTINGS, val.H1, val.DEBT, val.ASSETS, val.RATIO, val.SHARES, val.FX,
                                     val.JH_TAX)
    cols = {VAL_COL[c]: CASE_LABEL[c].split(" (")[0] for c in VAL_CASES}
    vc = [VAL_COL[c] for c in VAL_CASES]
    s.section("INPUTS")
    s.header("3.1 Valuation settings and case weights", {"B": "Value"})
    s.line("r", "Discount rate", {"B": ST.discount_rate}, FMT_PCT, "Task requirement (valuation.py ValuationSettings)")
    s.line("vy", "Valuation year (t = 0, not discounted)", {"B": ST.valuation_year}, FMT_YEAR)
    s.line("ty", "Terminal year (TV sits at end of this year)", {"B": ST.terminal_year}, FMT_YEAR)
    s.header("Case weights", cols)
    s.line("w", "Weight in headline value", {VAL_COL[c]: val.WEIGHTS[TV_KEY[c]] for c in VAL_CASES}, FMT_PCT,
           "No growth shares the base drivers, so takes half the base's 50% (valuation.md sec 1)")
    s.blank()
    s.header("3.2 H1-2026 actuals (to strip realized cash out of FY2026E)", {"B": "Value"})
    s.line("h1_ebitda", "H1-2026 Adjusted EBITDA", {"B": Lnk(f"={e.ref('in_ebitda', 'F', s)}")}, FMT_M,
           "Linked to sheet 1")
    s.line("h1_rent", "H1-2026 cash rent",
           {"B": Lnk("=" + "+".join(e.ref(n, "F", s) for n in ("in_lp_prop", "in_lp_veh", "in_li_prop", "in_li_veh")))},
           FMT_M, "Linked to sheet 1")
    s.line("h1_growth", "H1-2026 net growth spend (acquisitions & development less sale-leasebacks, ex-JH)",
           {"B": H1.net_growth_spend}, FMT_M, "forecast_earnings.md sec 6.1a, H1-2026 row")
    s.blank()
    s.header("3.3 Balance sheet at Jun-30-2026 (Q2FY26 FS)", {"B": "Value"})
    s.line("cash", "Cash", {"B": A.cash}, FMT_M3, "Balance sheet")
    s.line("opcash", "Operating cash requirement", {"B": A.operating_cash_requirement}, FMT_M,
           "owners_earnings_and_roic.md sec 4: cash capped at $25M as operating")
    s.line("d_rev", "Revolver + swing line (net of financing costs)", {"B": D.revolver}, FMT_M3, "Note 11")
    s.line("d_tla", "Term Loan A (net of financing costs)", {"B": D.term_loan_a}, FMT_M3, "Note 11")
    s.line("d_seller", "Seller notes (deferred acquisition consideration)", {"B": D.seller_notes}, FMT_M3, "Note 11")
    s.line("d_n30", "Senior notes 2030, US$ (C$525M principal)", {"B": D.senior_notes_2030}, FMT_M3, "Note 12")
    s.line("d_n33", "Senior notes 2033, US$ (C$275M principal)", {"B": D.senior_notes_2033}, FMT_M3, "Note 12")
    s.line("d_div", "Dividends payable", {"B": D.dividends_payable}, FMT_M3, "Balance sheet")
    s.line("d_der_a", "Cross-currency swaps - asset", {"B": D.derivatives_asset}, FMT_M3, "Balance sheet")
    s.line("d_der_l", "Cross-currency swaps - liability", {"B": D.derivatives_liability}, FMT_M3, "Balance sheet")
    s.line("m_lease_c", "Memo: lease liabilities, current (NOT deducted)", {"B": 159.574}, FMT_M3,
           "Rent is charged in full inside Owners' Earnings; deducting would double count")
    s.line("m_lease_nc", "Memo: lease liabilities, non-current (NOT deducted)", {"B": 891.311}, FMT_M3, "")
    s.line("m_dtl", "Memo: deferred tax liability (NOT deducted)", {"B": D.deferred_tax_liability_memo}, FMT_M3, "")
    s.line("m_dta", "Memo: deferred tax asset", {"B": D.deferred_tax_asset_memo}, FMT_M3, "")
    s.blank()
    s.header("3.4 Goodwill & intangible tax shields (value outside OE, which is taxed at full rate)", {"B": "Value"})
    s.line("jh_est", "Joe Hudson's tax benefits, Boyd's estimate", {"B": Lnk(f"={t.ref('jh_taxben', 'B', s)}")}, FMT_M,
           "Linked to sheet 2 (JH release l.43)")
    s.line("jh_gw", "Joe Hudson's goodwill (book)", {"B": R.jh_goodwill}, FMT_M3, "Q2FY26 FS acquisition table l.249-258")
    s.line("jh_cr", "Joe Hudson's customer relationships", {"B": 700.0}, FMT_M3, "Same table")
    s.line("jh_br", "Joe Hudson's brand", {"B": 0.5}, FMT_M3, "Same table")
    s.line("jh_ip", "Joe Hudson's intellectual property", {"B": 0.3}, FMT_M3, "Same table")
    s.line("lg_gw", "Legacy goodwill, Dec-2025", {"B": R.legacy_goodwill}, FMT_M3, "Q2FY26 FS l.28, Dec-25 column")
    s.line("lg_int", "Legacy intangibles (net), Dec-2025", {"B": R.legacy_intangibles}, FMT_M3, "Same")
    s.line("o_gw", "Other 2026 acquisitions: goodwill", {"B": R.other_2026_goodwill}, FMT_M3,
           "Q2FY26 FS acquisition table, 'Other acquisitions'")
    s.line("o_cr", "Other 2026 acquisitions: customer relationships", {"B": 5.496}, FMT_M3, "Same")
    s.line("o_nc", "Other 2026 acquisitions: non-competes", {"B": 0.245}, FMT_M3, "Same")
    s.line("jt_gw", "Cross-check: JH tax-deductible goodwill", {"B": JT.deductible_goodwill}, FMT_M3, "Q2FY26 FS l.316")
    s.line("jt_int", "Cross-check: JH tax-deductible intangibles", {"B": JT.deductible_intangibles}, FMT_M3,
           "Q2FY26 FS l.318")
    s.line("jt_yrs", "Cross-check: US tax amortization life (years)", {"B": JT.amortization_years}, FMT_N,
           "From internal AI model knowledge: IRC s.197 15-year straight line")
    s.line("jt_first", "Cross-check: share of 2026 deduction still to come", {"B": JT.share_of_first_year_remaining},
           FMT_PCT, "H1-2026 benefit already inside Jun-26 cash")
    s.line("jt_tax", "Tax rate", {"B": Lnk(f"={e.ref('a_tax', 'B', s)}")}, FMT_PCT, "Linked to sheet 1")
    s.blank()
    s.header("3.5 Share count and FX", {"B": "Value"})
    s.line("sh_basic", "Basic shares outstanding, Jun-30-2026", {"B": SH.basic_shares_jun_2026}, FMT_N,
           "Q2FY26 FS statement of changes in equity")
    s.line("sh_dw", "Diluted weighted shares, Q2-2026", {"B": SH.diluted_weighted_q2_2026}, FMT_N, "Q2FY26 FS l.129")
    s.line("sh_bw", "Basic weighted shares, Q2-2026", {"B": SH.basic_weighted_q2_2026}, FMT_N, "Q2FY26 FS l.128")
    s.line("sh_opt", "Share option plan cap", {"B": SH.option_plan_cap}, FMT_N, "FY2025 AFS l.459")
    s.line("fx_cad", "C$ principal of senior notes (525 + 275)", {"B": FX.notes_principal_cad}, FMT_M,
           "FY2025 MD&A l.25, l.35")
    s.line("fx_usd", "US$ carrying principal of senior notes",
           {"B": Lnk(f"={s.ref('d_n30', 'B')}+{s.ref('d_n33', 'B')}")}, FMT_M3, "Linked to 3.3")
    s.blank()
    s.header("3.6 Sensitivity axes", {"B": "", "C": "", "D": "", "E": "", "F": "", "G": ""}, note="")
    s.line("sens_r", "Discount rates to test", {c: r for c, r in zip("BCDEF", (0.08, 0.09, 0.10, 0.11, 0.12))}, FMT_PCT)
    s.line("sens_m", "Exit multiple shifts to test (all cases)",
           {c: m for c, m in zip("BCDEFG", (-1.5, -1.0, -0.5, 0.0, 0.5, 1.0))}, '+0.0"x";-0.0"x";0.0"x"')
    s.blank()

    # ------------------------------------------------------------------ calculations
    s.section("CALCULATIONS")
    ycols = ["B", "C", "D", "E", "F", "G"]
    s.header("3.7 Timeline and discount factors", {c: str(y) for c, y in zip(ycols, fe.YEARS)})
    s.line("yr", "Year", {"B": f"={s.ref('vy', 'B')}", **{c: f"={p}{s.r}+1" for p, c in zip(ycols, ycols[1:])}},
           FMT_YEAR)
    s.line("t", "t (years from valuation year)", {c: f"={s.ref('yr', c)}-{s.ref('vy', 'B', absolute=True)}" for c in ycols},
           FMT_N)
    s.line("df", "Discount factor", {c: f"=1/(1+{s.ref('r', 'B', absolute=True)})^{s.ref('t', c)}" for c in ycols},
           '0.0000')
    s.line("df_t", "Discount factor at terminal year",
           {"B": f"=1/(1+{s.ref('r', 'B')})^({s.ref('ty', 'B')}-{s.ref('vy', 'B')})"}, '0.0000')
    s.blank()

    s.header("3.8 FY2026 stub: only H2-2026 cash counts (H1 is inside Jun-26 net debt)", cols)
    fy26 = lambda key: {VAL_COL[c]: Lnk(f"={e.ref(c + '_' + key, 'F', s)}") for c in VAL_CASES}  # noqa: E731
    s.line("oe26", "FY2026E Owners' Earnings", fy26("oe"), FMT_M, "Linked to sheet 1")
    s.line("ear26", "FY2026E EBITDA after rent", fy26("ear"), FMT_M)
    s.line("gc26", "FY2026E growth capex", fy26("gcapex"), FMT_M)
    s.line("oo26", "FY2026E one-offs (all Jul-2026 onward)", fy26("oneoffs"), FMT_M)
    h1_ear = f"({s.ref('h1_ebitda', 'B', absolute=True)}-{s.ref('h1_rent', 'B', absolute=True)})"
    s.line("h2share", "H2 share of FY2026E OE (proxy: H2 share of EBITDA after rent)",
           {c: f"=({s.ref('ear26', c)}-{h1_ear})/{s.ref('ear26', c)}" for c in vc}, FMT_PCT)
    s.line("h2oe", "H2-2026 Owners' Earnings", {c: f"={s.ref('oe26', c)}*{s.ref('h2share', c)}" for c in vc}, FMT_M)
    s.line("h2gc", "H2-2026 growth capex = FY less H1 actual (floor 0)",
           {c: f"=MAX({s.ref('gc26', c)}-{s.ref('h1_growth', 'B', absolute=True)},0)" for c in vc}, FMT_M)
    s.line("stub", "H2-2026 distributable cash",
           {c: f"={s.ref('h2oe', c)}-{s.ref('h2gc', c)}-{s.ref('oo26', c)}" for c in vc}, FMT_M, bold=True)
    s.blank()

    s.header("3.9 Distributable cash counted in the valuation", {c: str(y) for c, y in zip(ycols, fe.YEARS)} | {"H": "PV"})
    for case in VAL_CASES:
        cells = {"B": f"={s.ref('stub', VAL_COL[case])}"}
        cells.update({c: Lnk(f"={e.ref(case + '_dist', yc, s)}") for c, yc in zip(ycols[1:], YEAR_COLS[1:])})
        cells["H"] = f"=SUMPRODUCT(B{s.r}:G{s.r},{s.rng('df', 'B', 'G')})"
        s.line("cf_" + case, CASE_LABEL[case], cells, FMT_M, "2026 = H2 stub (3.8); 2027-31 linked to sheet 1")
    s.blank()

    # bridge items (computed once)
    s.header("3.10 Standalone assets and debt (computed once, same for every case)", {"B": "Value"})
    s.line("b_xcash", "Excess cash above operating requirement", {"B": f"=MAX({s.ref('cash', 'B')}-{s.ref('opcash', 'B')},0)"},
           FMT_M)
    s.line("b_jh_tot", "JH goodwill + intangibles (book)",
           {"B": f"={s.ref('jh_gw', 'B')}+{s.ref('jh_cr', 'B')}+{s.ref('jh_br', 'B')}+{s.ref('jh_ip', 'B')}"}, FMT_M)
    s.line("b_lg_tot", "Legacy goodwill + intangibles (book)", {"B": f"={s.ref('lg_gw', 'B')}+{s.ref('lg_int', 'B')}"}, FMT_M)
    s.line("b_o_tot", "Other 2026 goodwill + intangibles",
           {"B": f"={s.ref('o_gw', 'B')}+{s.ref('o_cr', 'B')}+{s.ref('o_nc', 'B')}"}, FMT_M)
    s.line("b_jh", "JH tax shield (Boyd's estimate)", {"B": f"={s.ref('jh_est', 'B')}"}, FMT_M)
    s.line("b_lg", "Legacy tax shield = JH estimate x legacy / JH book ratio",
           {"B": f"={s.ref('jh_est', 'B')}*{s.ref('b_lg_tot', 'B')}/{s.ref('b_jh_tot', 'B')}"}, FMT_M,
           "Inference: assumes pre-2023 goodwill is as deductible as 2023-25 goodwill (disclosed deductible)")
    s.line("b_o", "Other 2026 acquisitions tax shield (same ratio method)",
           {"B": f"={s.ref('jh_est', 'B')}*{s.ref('b_o_tot', 'B')}/{s.ref('b_jh_tot', 'B')}"}, FMT_M)
    s.line("b_sa", "Standalone assets, total",
           {"B": f"={s.ref('b_xcash', 'B')}+{s.ref('b_jh', 'B')}+{s.ref('b_lg', 'B')}+{s.ref('b_o', 'B')}"}, FMT_M,
           bold=True)
    s.line("b_derv", "Cross-currency swaps, net asset", {"B": f"={s.ref('d_der_a', 'B')}-{s.ref('d_der_l', 'B')}"}, FMT_M)
    s.line("b_debt", "Debt and debt-like items, total",
           {"B": "=" + "+".join(s.ref(n, "B") for n in ("d_rev", "d_tla", "d_seller", "d_n30", "d_n33", "d_div"))
                 + f"-{s.ref('b_derv', 'B')}"}, FMT_M, "Leases and deferred tax deliberately excluded (3.3 memo)",
           bold=True)
    s.line("b_shares", "Diluted shares (millions) = basic + dilutive RSU/PSU",
           {"B": f"=({s.ref('sh_basic', 'B')}+{s.ref('sh_dw', 'B')}-{s.ref('sh_bw', 'B')})/1000000"}, '#,##0.000',
           "Options anti-dilutive (Q2FY26 FS l.669)")
    s.line("b_fx", "C$ per US$ implied by Boyd's own note balances", {"B": f"={s.ref('fx_cad', 'B')}/{s.ref('fx_usd', 'B')}"},
           '0.0000', "No market FX used")
    s.blank()

    # SOTP table
    hdr = {**cols, WTD_COL: "Weighted"}
    def wsum(name):
        """Case-weighted sum of a row (the current row if `name` is not yet written)."""
        row = s.rows.get(name, s.r)
        return f"=SUMPRODUCT({s.rng('w', 'B', 'E')},B{row}:E{row})"
    b = lambda n: s.ref(n, "B", absolute=True)  # noqa: E731
    s.header("3.11 SUM OF THE PARTS - intrinsic value per share (headline, exit-multiple TV)", hdr)
    s.line("v_pvcf", "PV of 2026-31 distributable cash",
           {**{VAL_COL[c]: f"={s.ref('cf_' + c, 'H')}" for c in VAL_CASES}, WTD_COL: wsum("v_pvcf")}, FMT_M)
    s.line("v_tv", "Terminal value, end-2031 (sheet 2)",
           {**{VAL_COL[c]: Lnk(f"={t.ref('tv', VAL_COL[c], s)}") for c in VAL_CASES}, WTD_COL: wsum("v_tv")}, FMT_M)
    s.line("v_pvtv", "PV of terminal value", {**{c: f"={s.ref('v_tv', c)}*{b('df_t')}" for c in vc},
                                              WTD_COL: wsum("v_pvtv")}, FMT_M)
    s.line("v_ev", "Enterprise value (operating business)",
           {**{c: f"={s.ref('v_pvcf', c)}+{s.ref('v_pvtv', c)}" for c in vc}, WTD_COL: wsum("v_ev")}, FMT_M, bold=True)
    s.line("v_tvsh", "  terminal value share of EV", {c: f"={s.ref('v_pvtv', c)}/{s.ref('v_ev', c)}" for c in vc + [WTD_COL]},
           FMT_PCT)
    for n, lab in (("b_xcash", "Plus: excess cash"), ("b_jh", "Plus: JH tax shield"),
                   ("b_lg", "Plus: legacy goodwill & intangibles tax shield"), ("b_o", "Plus: other 2026 tax shield")):
        s.line("v_" + n, lab, {c: f"={b(n)}" for c in vc + [WTD_COL]}, FMT_M)
    debt_rows = (("d_rev", "Less: revolver + swing line"), ("d_tla", "Less: Term Loan A"), ("d_seller", "Less: seller notes"),
                 ("d_n30", "Less: senior notes 2030"), ("d_n33", "Less: senior notes 2033"),
                 ("d_div", "Less: dividends payable"))
    for n, lab in debt_rows:
        s.line("v_" + n, lab, {c: f"=-{b(n)}" for c in vc + [WTD_COL]}, FMT_M)
    s.line("v_derv", "Plus: cross-currency swaps, net asset", {c: f"={b('b_derv')}" for c in vc + [WTD_COL]}, FMT_M)
    first, last = s.rows["v_ev"], s.rows["v_derv"]
    s.line("v_eq", "Equity value",
           {c: f"={c}{first}+SUM({c}{s.rows['v_b_xcash']}:{c}{last})" for c in vc + [WTD_COL]}, FMT_M, bold=True)
    s.line("v_ps", "Intrinsic value per diluted share (US$)",
           {**{c: f"={s.ref('v_eq', c)}/{b('b_shares')}" for c in vc}, WTD_COL: wsum("v_ps")}, FMT_PS, bold=True)
    s.line("v_ps_cad", "Intrinsic value per diluted share (C$)",
           {c: f"={s.ref('v_ps', c)}*{b('b_fx')}" for c in vc + [WTD_COL]}, FMT_PS, bold=True)
    s.line("v_check", "Check: weighted equity / shares less weighted per share (must be nil)",
           {WTD_COL: f"={s.ref('v_eq', WTD_COL)}/{b('b_shares')}-{s.ref('v_ps', WTD_COL)}"}, FMT_N2)
    w1 = {k: e.ref("f_w_" + k.lower(), "B", s) for k in ("Bear", "Base", "Bull")}
    s.line("v_ps_r1", "Memo: per share at sheet 1 forecast weights (Bear/Base/Bull only)",
           {WTD_COL: "=" + "+".join(f"{w1[k]}*{s.ref('v_ps', VAL_COL[k])}" for k in w1)}, FMT_PS)
    s.blank()

    # perpetuity cross-check
    s.header("3.12 Cross-check: perpetuity terminal value at this sheet's discount rate", hdr)
    s.line("p_rroe", "FY2031E run-rate OE (OE + new-location OE still ramping)",
           {VAL_COL[c]: Lnk(f"={e.ref(c + '_oe', 'K', s)}+{e.ref(c + '_oe_ramp', 'K', s)}") for c in VAL_CASES}, FMT_M)
    s.line("p_g", "Steady-state growth (sheet 2)", {c: Lnk(f"={t.ref('vd_g', c, s)}") for c in vc}, FMT_PCT)
    s.line("p_reinv", "Reinvestment rate (sheet 2)", {c: Lnk(f"={t.ref('vd_reinv', c, s)}") for c in vc}, FMT_PCT)
    s.line("p_mult", "TV / OE = (1+g)(1-reinvestment)/(r-g)",
           {c: f"=(1+{s.ref('p_g', c)})*(1-{s.ref('p_reinv', c)})/({b('r')}-{s.ref('p_g', c)})" for c in vc}, FMT_X)
    s.line("p_tv", "Perpetuity terminal value, end-2031",
           {**{c: f"={s.ref('p_mult', c)}*{s.ref('p_rroe', c)}" for c in vc}, WTD_COL: wsum("p_tv")}, FMT_M)
    s.line("p_ev", "Enterprise value",
           {**{c: f"={s.ref('v_pvcf', c)}+{s.ref('p_tv', c)}*{b('df_t')}" for c in vc}, WTD_COL: wsum("p_ev")}, FMT_M)
    s.line("p_eq", "Equity value", {c: f"={s.ref('p_ev', c)}+{b('b_sa')}-{b('b_debt')}" for c in vc + [WTD_COL]}, FMT_M)
    s.line("p_ps", "Per diluted share (US$)",
           {**{c: f"={s.ref('p_eq', c)}/{b('b_shares')}" for c in vc}, WTD_COL: wsum("p_ps")}, FMT_PS, bold=True)
    s.line("p_impl", "Implied EV / FY2031E EBITDA after rent",
           {c: f"={s.ref('p_tv', c)}/{t.ref('ear31', c, s)}" for c in vc}, FMT_X, "Compare with chosen exit multiples")
    s.blank()

    # sensitivity: discount rate
    rcols = ["B", "C", "D", "E", "F"]
    s.header("3.13 Discount factors at each test rate (rows) by year", {c: str(y) for c, y in zip(ycols, fe.YEARS)}
             | {"H": "Terminal"})
    for i, rc in enumerate(rcols):
        rr = s.ref("sens_r", rc, absolute=True)
        s.line(f"sdf{i}", "  discount factors", {**{c: f"=1/(1+{rr})^{s.ref('t', c, absolute=True)}" for c in ycols},
                                                 "H": f"=1/(1+{rr})^({b('ty')}-{b('vy')})"}, '0.0000')
        s.ws[f"A{s.r - 1}"] = f"  discount factors at test rate in 3.6 column {rc}"
    s.blank()
    s.header("3.14 Sensitivity: US$ per share by discount rate", {"B": "Rate"} | {c: "" for c in "CDEFGHIJ"}, note="")
    s.line(None, "Exit-multiple TV:  Bear | Base | No growth | Bull | Weighted  (cols C-G)", {})
    for i, rc in enumerate(rcols):
        row = s.rows[f"sdf{i}"]
        cells = {"B": Lnk(f"={s.ref('sens_r', rc)}")}
        for c, cc in zip(VAL_CASES, "CDEF"):
            cells[cc] = (f"=(SUMPRODUCT({s.rng('cf_' + c, 'B', 'G')},$B${row}:$G${row})+{s.ref('v_tv', VAL_COL[c], absolute=True)}"
                         f"*$H${row}+{b('b_sa')}-{b('b_debt')})/{b('b_shares')}")
        cells["G"] = f"=SUMPRODUCT({s.rng('w', 'B', 'E')},C{s.r}:F{s.r})"
        s.line(f"sr_exit{i}", "  exit TV", cells, FMT_PS)
        s.ws[f"B{s.r - 1}"].number_format = FMT_PCT
    s.line(None, "Perpetuity TV at the test rate:  Bear | Base | No growth | Bull | Weighted  (cols C-G)", {})
    for i, rc in enumerate(rcols):
        row = s.rows[f"sdf{i}"]
        rr = s.ref("sens_r", rc, absolute=True)
        cells = {"B": Lnk(f"={s.ref('sens_r', rc)}")}
        for c, cc in zip(VAL_CASES, "CDEF"):
            vcol = VAL_COL[c]
            g, ri, oe = (s.ref(n, vcol, absolute=True) for n in ("p_g", "p_reinv", "p_rroe"))
            cells[cc] = (f"=(SUMPRODUCT({s.rng('cf_' + c, 'B', 'G')},$B${row}:$G${row})"
                         f"+(1+{g})*(1-{ri})/({rr}-{g})*{oe}*$H${row}+{b('b_sa')}-{b('b_debt')})/{b('b_shares')}")
        cells["G"] = f"=SUMPRODUCT({s.rng('w', 'B', 'E')},C{s.r}:F{s.r})"
        s.line(f"sr_perp{i}", "  perpetuity TV", cells, FMT_PS)
        s.ws[f"B{s.r - 1}"].number_format = FMT_PCT
    s.blank()
    s.header("3.15 Sensitivity: US$ per share by exit-multiple shift (at discount rate in 3.1)",
             {"B": "Shift", "C": "Bear", "D": "Base", "E": "No growth", "F": "Bull", "G": "Weighted"}, note="")
    for i, mc in enumerate(["B", "C", "D", "E", "F", "G"]):
        sh = s.ref("sens_m", mc, absolute=True)
        cells = {"B": Lnk(f"={sh}")}
        for c, cc in zip(VAL_CASES, "CDEF"):
            vcol = VAL_COL[c]
            cells[cc] = (f"=({s.ref('v_pvcf', vcol, absolute=True)}+({t.ref('mult', vcol, s)}+{sh})*"
                         f"({t.ref('ear31', vcol, s)}+{t.ref('gap', vcol, s)})*{b('df_t')}+{b('b_sa')}-{b('b_debt')})"
                         f"/{b('b_shares')}")
        cells["G"] = f"=SUMPRODUCT({s.rng('w', 'B', 'E')},C{s.r}:F{s.r})"
        s.line(f"sm{i}", "  multiple shift", cells, FMT_PS)
        s.ws[f"B{s.r - 1}"].number_format = '+0.0"x";-0.0"x";0.0"x"'
    s.blank()

    s.header("3.16 Bridge alternatives (weighted equity value, US$ per share)", {"B": "Adjust.", "C": "US$/sh"})
    weq = s.ref("v_eq", WTD_COL, absolute=True)
    r_, n_, f_ = b("r"), b("jt_yrs"), b("jt_first")
    s.line("jt_saving", "JH annual tax saving (deductible basis / life x tax rate)",
           {"B": f"=({b('jt_gw')}+{b('jt_int')})/{n_}*{b('jt_tax')}"}, FMT_M)
    s.line("jt_pv", "JH tax shield, own PV at discount rate (half-years at both ends)",
           {"B": f"={s.ref('jt_saving', 'B')}*({f_}+(1-(1+{r_})^-({n_}-1))/{r_}+(1-{f_})*(1+{r_})^-{n_})"}, FMT_M,
           "Cross-check of Boyd's ~$150M")
    alts = [
        ("Headline", "=0"),
        ("Also deduct net deferred tax liability", f"={b('m_dtl')}-{b('m_dta')}"),
        ("Drop all goodwill/intangible tax shields", f"={b('b_jh')}+{b('b_lg')}+{b('b_o')}"),
        ("Drop only the legacy + other 2026 shields", f"={b('b_lg')}+{b('b_o')}"),
        ("JH at own-formula PV instead of Boyd's estimate", f"={b('b_jh')}-{s.ref('jt_pv', 'B', absolute=True)}"),
        ("Count all Jun-26 cash as excess", f"=-({b('cash')}-{b('b_xcash')})"),
        ("Lease liabilities also deducted (WRONG: double count)", f"={b('m_lease_c')}+{b('m_lease_nc')}"),
    ]
    for i, (lab, f) in enumerate(alts):
        s.line(f"alt{i}", lab, {"B": f, "C": f"=({weq}-B{s.r})/{b('b_shares')}"}, FMT_M)
        s.ws[f"C{s.r - 1}"].number_format = FMT_PS
    s.line("alt_opt", "All plan options issued, no proceeds",
           {"B": "=0", "C": f"={weq}/({b('b_shares')}+{b('sh_opt')}/1000000)"}, FMT_M)
    s.ws[f"C{s.r - 1}"].number_format = FMT_PS
    s.blank()
    s.header("3.17 Sanity checks (Base case)", {"B": "Value"})
    s.line("sc1", "Base EV / FY2026E EBITDA after rent", {"B": f"={s.ref('v_ev', 'C')}/{e.ref('Base_ear', 'F', s)}"}, FMT_X)
    s.line("sc2", "Base EV / FY2027E EBITDA after rent", {"B": f"={s.ref('v_ev', 'C')}/{e.ref('Base_ear', 'G', s)}"}, FMT_X)
    s.line("sc3", "Base EV / FY2026E Owners' Earnings", {"B": f"={s.ref('v_ev', 'C')}/{e.ref('Base_oe', 'F', s)}"}, FMT_X)
    s.line("sc4", "Base EV / FY2027E Owners' Earnings", {"B": f"={s.ref('v_ev', 'C')}/{e.ref('Base_oe', 'G', s)}"}, FMT_X)
    return s


# =====================================================================================================
# MAIN
# =====================================================================================================

def main():
    wb = Workbook()
    wb.remove(wb.active)
    earn, summary_start = build_earnings(wb)
    # Section 3 (summary) sits above section 4 (workings) but links into it, so reserve its rows first.
    n_summary = 3 + len(CASES) * 22 + 3
    earn.r = summary_start + n_summary
    for case in CASES:
        build_workings(earn, case)
    end_r = earn.r
    build_summary(earn, summary_start)
    assert earn.r <= summary_start + n_summary, (earn.r, summary_start + n_summary)
    earn.r = end_r
    earn.ws.freeze_panes = "B5"
    tvs = build_terminal(wb, earn)
    tvs.ws.freeze_panes = "B5"
    vs = build_valuation(wb, earn, tvs)
    vs.ws.freeze_panes = "B5"
    wb.active = 2
    wb.save(OUT_PATH)
    print(f"wrote {OUT_PATH}")
    return earn, tvs, vs


if __name__ == "__main__":
    main()
