"""
Independent verification of work_products/valuation.xlsx.

The workbook contains only formulas, so this script RECALCULATES it with the
`formulas` engine (no Excel involved) and compares the recalculated cells against
the figures published in the four source work products:

  owners_earnings_and_roic.md  historical owners' earnings, FY2022A-FY2025A and TTM
  forecast_earnings.md         FY2026E-FY2030E owners' earnings, all four scenarios
  terminal_value.md            terminal value at 31-Oct-2030
  valuation.md                 equity value and value per diluted share

Run: uv run python work_products/verify_valuation_xlsx.py
"""

import openpyxl
import formulas

XL = "work_products/valuation.xlsx"
BOOK = "'[valuation.xlsx]{}'!{}"

# ---------------------------------------------------------------------------
# expected values, transcribed from the four work products
# ---------------------------------------------------------------------------
EXP_HIST_OE = {"C": 1_159_664, "D": 1_554_032, "E": 1_838_746, "F": 2_250_271,
               "M": 2_309_639}                                   # OE s2.1 + TTM
EXP_BASE_OE = {"G": 2_375_755, "H": 2_413_913, "I": 2_548_061,
               "J": 2_716_487, "K": 2_859_320}                    # FC s1
EXP_BASE_REV = {"G": 8_655_668, "H": 9_411_573, "I": 10_116_115,
                "J": 10_797_518, "K": 11_462_356}                 # FC s5
EXP_FY30_OE = {"Bull": 4_649_840, "Base": 2_859_320,
               "Bear - management right-sizes": 2_094_988,
               "Bear - no cost response": 1_505_664}              # FC s1 / s8 / s9b
EXP_TV = {"Bull": 69_747_600, "Base": 34_311_840,
          "Bear - management right-sizes": 16_759_904,
          "Bear - no cost response": 12_045_312}                  # TV s6 diagonal
EXP_EQUITY = {"Bull": 67_694_384, "Base": 39_974_178,
              "Bear - management right-sizes": 25_865_989,
              "Bear - no cost response": 21_364_839}              # VAL s5
EXP_PS = {"Bull": 2.47, "Base": 1.46,
          "Bear - management right-sizes": 0.94,
          "Bear - no cost response": 0.78}                        # VAL s5
EXP_SENS = {0.08: [1.31, 1.53, 1.76], 0.09: [1.27, 1.49, 1.72],
            0.10: [1.24, 1.46, 1.67], 0.11: [1.21, 1.42, 1.62],
            0.12: [1.18, 1.38, 1.58]}                             # VAL s6
EXP_COMP = [0.33, 0.85, 0.27]                                     # VAL s4

fails, checks = [], 0


def chk(label, got, want, tol):
    global checks
    checks += 1
    ok = got is not None and abs(float(got) - want) <= tol
    if not ok:
        fails.append(f"  FAIL {label}: workbook {got} vs expected {want}")
    print(f"  {'ok ' if ok else 'FAIL'} {label:<62} {got if got is None else float(got):>14,.2f}"
          f"   expected {want:>14,.2f}")


def structural_counts(wb):
    """Reproducible workbook-hygiene statistics.

    Added after verifier round 1 (pv/excel_model/r1_review.md, objection 1), which
    correctly noted that the descriptive counts quoted in the round summary were the
    one set of figures in this exercise not produced by a committed script.

    Note the distinction the raw "starts with =" count misses: 35 cells are
    accounting-style TEXT labels ("= EQUITY VALUE", "= Standalone assets") that
    build_valuation_xlsx.py deliberately forces back to strings, because openpyxl
    would otherwise infer a formula from the leading "=" and Excel would render
    #NAME?. Those are labels, not model logic.
    """
    out = dict(formulas=0, starts_eq=0, eq_labels=0, beige_nonempty=0,
               beige_numeric=0, col_q=0)
    for ws in wb:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if c.data_type == "f":
                    out["formulas"] += 1
                if isinstance(v, str) and v.startswith("="):
                    out["starts_eq"] += 1
                    if c.data_type == "s":
                        out["eq_labels"] += 1
                try:
                    beige = c.fill.fgColor.rgb == "00FFF2CC"
                except Exception:
                    beige = False
                if beige and v is not None:
                    out["beige_nonempty"] += 1
                    if isinstance(v, (int, float)):
                        out["beige_numeric"] += 1
                if c.column == 17 and v is not None:
                    out["col_q"] += 1
    return out


def main():
    wb = openpyxl.load_workbook(XL)

    def find(sheet, text, start=1, exact=True):
        """row number of the first column-B label matching `text`."""
        ws = wb[sheet]
        for r in range(start, ws.max_row + 1):
            v = ws.cell(r, 2).value
            if isinstance(v, str):
                s = v.strip()
                if (s == text) if exact else (text in s):
                    return r
        raise KeyError(f"{sheet}: {text!r} not found after row {start}")

    model = formulas.ExcelModel().loads(XL).finish()
    sol = model.calculate()

    def val(sheet, coord):
        v = sol.get(BOOK.format(sheet.upper(), coord))
        if v is None:
            return None
        try:
            return v.value[0, 0]
        except Exception:
            return v.value

    print("\n1. INPUTS SHEET INTERNAL CHECKS (must be zero)")
    chk("geographic revenue total vs reported FY2025 revenue",
        val("Inputs", f"C{find('Inputs', 'Check: geographic total less reported FY2025 revenue')}"),
        0, 1)
    chk("rebuilt FY2025 operating income vs reported (FC s4b back-test)",
        val("Inputs", f"C{find('Inputs', 'Check: rebuilt FY2025 operating income less reported')}"),
        0, 1)

    print("\n2. HISTORICAL OWNERS' EARNINGS BRIDGE (OE s2.1)")
    r_oe = find("Owners Earnings", "= OWNERS' EARNINGS")
    for col, want in EXP_HIST_OE.items():
        chk(f"owners' earnings, column {col}",
            val("Owners Earnings", f"{col}{r_oe}"), want, 2)

    print("\n3. FORECAST, BASE CASE, SHOWN IN THE SAME BRIDGE (FC s1/s5)")
    r_rev = find("Owners Earnings", "Revenue")
    for col, want in EXP_BASE_REV.items():
        chk(f"revenue {col}", val("Owners Earnings", f"{col}{r_rev}"), want, 2)
    for col, want in EXP_BASE_OE.items():
        chk(f"owners' earnings {col}", val("Owners Earnings", f"{col}{r_oe}"), want, 2)

    print("\n4. BRIDGE vs SCENARIO ENGINE (must be zero in every column)")
    r_chk = find("Owners Earnings", "CHECK: bridge owners' earnings less scenario-engine owners' earnings")
    for col in ["F", "G", "H", "I", "J", "K"]:
        chk(f"bridge less engine, {col}", val("Owners Earnings", f"{col}{r_chk}"), 0, 2)

    print("\n5. FY2030E OWNERS' EARNINGS AND TERMINAL VALUE, ALL SCENARIOS (FC s1, TV s6)")
    for name in EXP_FY30_OE:
        r = find("Valuation", name)
        chk(f"FY2030E owners' earnings -- {name}", val("Valuation", f"C{r}"),
            EXP_FY30_OE[name], 2)
        chk(f"terminal value at 31-Oct-2030 -- {name}", val("Valuation", f"E{r}"),
            EXP_TV[name], 20)

    print("\n6. EQUITY VALUE AND VALUE PER DILUTED SHARE (VAL s5)")
    r_sum = find("Valuation", "Scenario  (each with its own scenario-consistent terminal multiple)")
    for name in EXP_EQUITY:
        r = find("Valuation", name, start=r_sum)
        chk(f"equity value -- {name}", val("Valuation", f"G{r}"), EXP_EQUITY[name], 40)
        chk(f"value per diluted share -- {name}", val("Valuation", f"H{r}"),
            EXP_PS[name], 0.005)

    print("\n7. BASE-CASE SUM OF THE PARTS (VAL s4)")
    for lab, want, tol in [
        ("PV of FY2026E-FY2030E owners' earnings", 9_172_683, 20),
        ("+ PV of terminal value (base multiple x FY2030E OE, discounted at t=4)",
         23_435_448, 20),
        ("= PV of the operating business", 32_608_131, 30),
        ("= EQUITY VALUE", 39_974_178, 40),
        ("= VALUE PER DILUTED SHARE", 1.4557, 0.002),
    ]:
        chk(lab[:60], val("Valuation", f"C{find('Valuation', lab)}"), want, tol)

    print("\n8. COMPOSITION OF THE BASE-CASE PER-SHARE VALUE (VAL s4)")
    r_c = find("Valuation", "PV of FY2026E-FY2030E owners' earnings",
               start=find("Valuation", "= VALUE PER DILUTED SHARE"))
    for i, want in enumerate(EXP_COMP):
        chk(f"per-share component {i + 1}", val("Valuation", f"C{r_c + i}"), want, 0.005)

    print("\n9. SENSITIVITY GRID: DISCOUNT RATE x TERMINAL MULTIPLE (VAL s6)")
    r_h = find("Valuation", "r  \\  terminal multiple")
    for i, (rate, wants) in enumerate(sorted(EXP_SENS.items()), start=1):
        for col, want in zip("CDE", wants):
            chk(f"per share at r={rate:.0%}, {col}", val("Valuation", f"{col}{r_h + i}"),
                want, 0.006)

    print("\n10. TIE-OUT ROWS vs valuation.md (differences must be zero)")
    r_t = find("Valuation", "Equity value -- Bull")
    for i, name in enumerate(["Bull", "Base", "Bear - management right-sizes",
                              "Bear - no cost response"]):
        chk(f"tie-out difference -- {name}", val("Valuation", f"E{r_t + i}"), 0, 40)

    print("\n11. STRUCTURAL COUNTS (added after verifier round 1, pv/excel_model/r1_review.md)")
    s = structural_counts(wb)
    for label, got, want in [
        ("live formula cells (openpyxl data_type == 'f')", s["formulas"], 1_117),
        ("cells whose VALUE starts with '=' (formulas + labels)", s["starts_eq"], 1_152),
        ("   of which accounting-style TEXT labels, not formulas", s["eq_labels"], 35),
        ("highlighted numeric input cells (beige FFF2CC)", s["beige_numeric"], 318),
        ("   plus the legend colour swatch at Inputs!C4 (not an input)",
         s["beige_nonempty"] - s["beige_numeric"], 1),
        ("inline source tags in column Q", s["col_q"], 96),
    ]:
        chk(label, got, want, 0)

    print("\n" + "=" * 78)
    if fails:
        print(f"{len(fails)} of {checks} checks FAILED:")
        print("\n".join(fails))
    else:
        print(f"ALL {checks} CHECKS PASSED -- the workbook reproduces every published "
              f"figure from the four work products.")
    print("=" * 78)


if __name__ == "__main__":
    main()
