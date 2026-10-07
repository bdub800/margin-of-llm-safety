"""
Second-engine cross-check of work_products/valuation.xlsx (verifier r1 objection 2).

verify_valuation_xlsx.py recalculates the workbook with the `formulas` package. This script recalculates the SAME
file with a different, independently written engine (`pycel`) and compares key outputs with the python model.
It does not import `formulas` and does not rebuild the workbook.

    uv run --with pycel python work_products/crosscheck_valuation_xlsx_pycel.py
"""
from __future__ import annotations

import contextlib
import io
import os
import sys

from pycel import ExcelCompiler

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_valuation_xlsx as bx  # noqa: E402  (used only for row maps; workbook is NOT rewritten)
import forecast_earnings as fe  # noqa: E402
import terminal_value as tv  # noqa: E402
import valuation as val  # noqa: E402

with contextlib.redirect_stdout(io.StringIO()):
    import owners_earnings_roic as oer  # noqa: E402
    from openpyxl import Workbook  # noqa: E402
    # Rebuild row maps in memory only (same deterministic layout as the saved file)
    wb = Workbook(); wb.remove(wb.active)
    earn, start = bx.build_earnings(wb)
    earn.r = start + 3 + len(bx.CASES) * 22 + 3
    for c in bx.CASES:
        bx.build_workings(earn, c)
    bx.build_summary(earn, start)
    tvs = bx.build_terminal(wb, earn)
    vs = bx.build_valuation(wb, earn, tvs)

xl = ExcelCompiler(filename=bx.OUT_PATH)


def get(sb, name, col):
    return float(xl.evaluate(f"{sb.title}!{col}{sb.rows[name]}"))


rows, fails = [], 0


def check(label, got, exp, tol):
    global fails
    ok = abs(got - exp) <= tol
    fails += not ok
    rows.append((label, got, exp, "ok" if ok else "FAIL"))


r = val.SETTINGS.discount_rate
ex = val.scenario_values(r, "exit")
pp = val.scenario_values(r, "perpetuity")
for p, col in zip(oer.PERIODS, bx.HIST_COLS):
    check(f"historical OE {p}", get(earn, "h_oe", col), oer.rows_oe[p]["Owners' Earnings"] / 1000, 0.05)
for case in bx.CASES:
    y = fe.forecast(bx.SCEN_DEF[case])
    for i, col in enumerate(bx.YEAR_COLS):
        check(f"{case} OE {y[i].year}", get(earn, case + "_oe", col), y[i].owners_earnings, 0.3)
        check(f"{case} distributable {y[i].year}", get(earn, case + "_dist", col), y[i].distributable, 0.3)
for case in bx.VAL_CASES:
    col, name = bx.VAL_COL[case], bx.TV_KEY[case]
    check(f"TV {case}", get(tvs, "tv", col), tv.terminal_value(name)["total"], 1.0)
    check(f"implied r {case}", get(tvs, "vd_implied_r", col),
          tv.implied_discount_rate(tv.terminal_value(name)["total"] / tv.TERMINAL[name].owners_earnings,
                                   tv.STEADY[name]), 1e-4)
    check(f"US$/share {case}", get(vs, "v_ps", col), ex[name]["per_share"], 0.02)
    check(f"perpetuity US$/share {case}", get(vs, "p_ps", col), pp[name]["per_share"], 0.02)
check("HEADLINE weighted US$/share", get(vs, "v_ps", bx.WTD_COL),
      val.weighted({n: ex[n]["per_share"] for n in val.WEIGHTS}), 0.02)
check("weighted perpetuity US$/share", get(vs, "p_ps", bx.WTD_COL),
      val.weighted({n: pp[n]["per_share"] for n in val.WEIGHTS}), 0.02)
check("JH tax shield own-formula PV", get(vs, "jt_pv", "B"), val.pv_jh_tax_shield(r), 0.05)
for i, rate in enumerate((0.08, 0.09, 0.10, 0.11, 0.12)):
    e2 = val.scenario_values(rate, "exit")
    check(f"sensitivity exit @ {rate:.0%}", get(vs, f"sr_exit{i}", "G"),
          val.weighted({n: e2[n]["per_share"] for n in val.WEIGHTS}), 0.02)

for lab, g, e, s in rows:
    if s != "ok" or lab.startswith(("HEADLINE", "implied", "weighted", "TV ")):
        print(f"{lab:36} pycel {g:10.4f}  python {e:10.4f}  {s}")
print(f"\npycel engine: {len(rows)} checks, {fails} failures")
sys.exit(1 if fails else 0)
