"""
NamSys Inc. (CTZ.V) - overview support calculations.
Sources (all CAD $, IFRS, fiscal year end Oct 31):
  FY2023: primary_sources/FY2023/Namsys_-_Annual_FS_-_Feb262024.md
  FY2024: primary_sources/FY2024/NamSys_AFS_021925.md
  FY2025: primary_sources/FY2025/NamSys_AFS_022426.md
  H1 FY2026 (6 mo to Apr 30, 2026): primary_sources/2Q2026/FS_Q2_NamSys_Apr_30_26_FINAL.md
"""

# ---- Annual figures, $ CAD ----
revenue = {"FY2023": 6_093_020, "FY2024": 6_840_146, "FY2025": 7_891_605}
gross_profit = {"FY2023": 3_652_500, "FY2024": 4_269_368, "FY2025": 5_078_409}
operating_income = {"FY2023": 2_107_434, "FY2024": 2_572_018, "FY2025": 3_146_476}
net_income = {"FY2023": 1_614_875, "FY2024": 2_090_475, "FY2025": 2_486_109}
recurring_rev_pct = {"FY2023": None, "FY2024": 98.2, "FY2025": 99.0}  # from MD&A disclosures

# ---- Revenue CAGR FY2023 -> FY2025 (2-year) ----
rev_cagr_23_25 = (revenue["FY2025"] / revenue["FY2023"]) ** (1 / 2) - 1

# ---- Margins ----
gross_margin = {y: gross_profit[y] / revenue[y] for y in revenue}
operating_margin = {y: operating_income[y] / revenue[y] for y in revenue}
net_margin = {y: net_income[y] / revenue[y] for y in revenue}

# ---- H1 FY2026 vs H1 FY2025 ----
h1_revenue = {"H1FY2025": 3_951_863, "H1FY2026": 4_267_406}
h1_net_income = {"H1FY2025": 1_259_346, "H1FY2026": 1_312_064}
h1_rev_growth = h1_revenue["H1FY2026"] / h1_revenue["H1FY2025"] - 1
h1_ni_growth = h1_net_income["H1FY2026"] / h1_net_income["H1FY2025"] - 1

# ---- Balance sheet / cash build, per diluted share ----
diluted_shares_fy2025 = 27_601_426  # weighted avg diluted, FY2025 (Knowledge Store ID 8 corroborates $0.37/share net cash at FYE)
cash_and_st_invest_fy2025 = 846_423 + 9_329_249  # cash + short-term investments, Oct 31 2025
net_cash_per_diluted_share_fy2025 = cash_and_st_invest_fy2025 / diluted_shares_fy2025

# ---- Capital returned to shareholders, FY2024 - H1 FY2026 ----
special_dividend_2024 = 1_350_477  # $0.05/sh, paid June 2024
special_dividend_2026 = 4_027_790  # $0.15/sh, paid March 2026
buybacks_fy2024 = 339_924
buybacks_fy2025 = 46_492
buybacks_h1fy2026 = 240_996
total_capital_returned = (
    special_dividend_2024 + special_dividend_2026 + buybacks_fy2024 + buybacks_fy2025 + buybacks_h1fy2026
)

if __name__ == "__main__":
    print("Revenue CAGR FY2023-FY2025 (2yr):", round(rev_cagr_23_25 * 100, 1), "%")
    print("Gross margin by year:", {y: round(v * 100, 1) for y, v in gross_margin.items()})
    print("Operating margin by year:", {y: round(v * 100, 1) for y, v in operating_margin.items()})
    print("Net margin by year:", {y: round(v * 100, 1) for y, v in net_margin.items()})
    print("H1 FY2026 revenue growth vs H1 FY2025:", round(h1_rev_growth * 100, 1), "%")
    print("H1 FY2026 net income growth vs H1 FY2025:", round(h1_ni_growth * 100, 1), "%")
    print("Net cash per diluted share, FY2025 year-end:", round(net_cash_per_diluted_share_fy2025, 3))
    print("Total capital returned to shareholders (dividends+buybacks), FY2024-H1FY2026 ($):", total_capital_returned)
