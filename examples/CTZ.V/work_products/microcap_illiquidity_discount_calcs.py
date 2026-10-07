"""Illiquidity / size-discount -> implied terminal earnings multiple.

Inputs and their sources (all cited in the accompanying research note):
- CRSP/Kroll (Duff & Phelps) beta-adjusted size premia, as of 31-Dec-2018:
  decile 10a = 3.71%, decile 10b = 8.25% (mkt cap US$2.5M-184.8M).
  Source: quickreadbuzz.com summary of D&P Cost of Capital Navigator.
- Yardeni forward P/E by size index (see note for as-of dates).
- Stout Restricted Stock Study (data thru Mar-2025): median DLOM 15.7%,
  mean 20.4%; 5th (highest-risk) quintile median 42.9%.
"""

def cap_mult(r, g):
    return 1.0 / (r - g)

base_r = 0.095   # illustrative cost of equity for a liquid small/mid-cap
g = 0.03         # illustrative terminal growth

print("=== Size premium -> capitalisation multiple ===")
for label, sp in [("liquid small/mid-cap (no size prem.)", 0.0),
                  ("+ decile 10a size prem. 3.71%", 0.0371),
                  ("+ decile 10b size prem. 8.25%", 0.0825)]:
    r = base_r + sp
    m = cap_mult(r, g)
    print(f"{label:42s} r={r:6.2%}  1/(r-g)={m:5.1f}x")

base_m = cap_mult(base_r, g)
for label, sp in [("10a", 0.0371), ("10b", 0.0825)]:
    m = cap_mult(base_r + sp, g)
    print(f"  implied multiple discount vs liquid base ({label}): {m/base_m - 1:6.1%}")

print()
print("=== Observed index forward P/E gaps (multiple discount, not DCF) ===")
for asof, big, mid, small in [("30-Dec-2023 (Yardeni, daily)", 19.5, 14.7, 14.5),
                              ("04-May-2026 (Yardeni QuickTakes)", 20.9, 16.3, 15.9)]:
    print(f"{asof:36s} smallcap vs largecap: {small/big - 1:6.1%} | midcap vs largecap: {mid/big - 1:6.1%}")

print()
print("=== DLOM stacked on an observed small-cap multiple (illustrative) ===")
small_pe = 15.9
for label, dlom in [("Stout median 15.7%", 0.157),
                    ("Stout mean 20.4%", 0.204),
                    ("Stout top-risk-quintile median 42.9%", 0.429),
                    ("practitioner private-co rule of thumb 35%", 0.35)]:
    print(f"{label:44s} -> {small_pe * (1 - dlom):5.1f}x")
