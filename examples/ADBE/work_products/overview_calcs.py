"""
Adobe (ADBE) overview - supporting calculations.
Sources: primary_sources/FY2025/md_and_a.md, primary_sources/2Q2026/md_and_a.md,
primary_sources/FY2025/cover_page.md, primary_sources/2Q2026/cover_page.md,
Knowledge Store IDs 7, 9 (web search, stock price / market cap, Aug 2026).
"""

# --- FY2025 vs FY2024 P&L growth (FY2025/md_and_a.md) ---
rev_fy25, rev_fy24 = 23_769, 21_505
net_income_fy25, net_income_fy24 = 7_130, 5_560  # 7.13B increased by $1.57B (28%) per MD&A -> FY24 implied
digital_media_rev_fy25, digital_experience_rev_fy25, pub_adv_rev_fy25 = 17_649, 5_864, 256

print("FY2025 total revenue growth: {:.1f}%".format((rev_fy25 - rev_fy24) / rev_fy24 * 100))
print("FY2025 net income growth: {:.1f}%".format((net_income_fy25 - net_income_fy24) / net_income_fy24 * 100))
print("FY2025 net margin: {:.1f}%".format(net_income_fy25 / rev_fy25 * 100))
print("Digital Media % of FY2025 revenue: {:.1f}%".format(digital_media_rev_fy25 / rev_fy25 * 100))
print("Digital Experience % of FY2025 revenue: {:.1f}%".format(digital_experience_rev_fy25 / rev_fy25 * 100))
print("Publishing & Advertising % of FY2025 revenue: {:.1f}%".format(pub_adv_rev_fy25 / rev_fy25 * 100))

# --- Total Adobe ARR growth (FY2025 10-K MD&A + Q2 FY2026 10-Q MD&A) ---
arr_fy24_end_revalued, arr_fy25_end = 22_610, 25_200  # $M, both FY2025-currency-basis
arr_fy25_end_revalued_fy26_basis = 25_660
arr_q2fy26_end = 27_100
print("\nFY2025 Total Adobe ARR growth (constant FX basis): {:.1f}%".format(
    (arr_fy25_end - arr_fy24_end_revalued) / arr_fy24_end_revalued * 100))
print("Q2 FY2026 ARR growth vs FY26-opening book ({:.0f}M): {:.1f}%".format(
    arr_fy25_end_revalued_fy26_basis,
    (arr_q2fy26_end - arr_fy25_end_revalued_fy26_basis) / arr_fy25_end_revalued_fy26_basis * 100))
semrush_arr_contribution = 480
organic_arr_q2fy26 = arr_q2fy26_end - semrush_arr_contribution
print("Q2 FY2026 ARR ex-Semrush: {}M, implying organic growth of {:.1f}%".format(
    organic_arr_q2fy26,
    (organic_arr_q2fy26 - arr_fy25_end_revalued_fy26_basis) / arr_fy25_end_revalued_fy26_basis * 100))

# --- 1H FY2026 vs 1H FY2025 (Q2 FY2026 10-Q) ---
rev_1h_fy26, rev_1h_fy25 = 13_016, 11_587
print("\n1H FY2026 revenue growth: {:.1f}%".format((rev_1h_fy26 - rev_1h_fy25) / rev_1h_fy25 * 100))

# --- Buybacks & share count (10-K cover page, 10-Q cover page, MD&A) ---
shares_jan2026, shares_jun2026 = 410.5, 397.5  # millions, per cover pages
buyback_fy2025, buyback_1h_fy26 = 11.28, 4.59  # $B, per MD&A
print("\nShare count decline, Jan 2026 cover page to Jun 2026 cover page: {:.1f}%".format(
    (shares_jan2026 - shares_jun2026) / shares_jan2026 * 100))
print("Combined FY2025 + 1H FY2026 buybacks: ${:.2f}B".format(buyback_fy2025 + buyback_1h_fy26))

# --- Rough market context (Knowledge Store IDs 7 & 9, web search - Aug 2026, approximate) ---
price_aug27_2026 = 290.00  # KS ID 7
shares_out_approx = 395  # millions, rough approximation post further buybacks since June 2026 (397.5M)
market_cap_approx = price_aug27_2026 * shares_out_approx / 1000  # $B
non_gaap_eps_fy26_low, non_gaap_eps_fy26_high = 24.35, 24.45  # FY2026 guidance, Q2 FY2026 transcript
pe_low = price_aug27_2026 / non_gaap_eps_fy26_high
pe_high = price_aug27_2026 / non_gaap_eps_fy26_low
print("\nApprox. market cap at ${:.2f}/sh (~{:.0f}M shares, rough estimate): ${:.1f}B".format(
    price_aug27_2026, shares_out_approx, market_cap_approx))
print("Implied forward P/E on FY2026 non-GAAP EPS guidance ({:.2f}-{:.2f}): {:.1f}x-{:.1f}x".format(
    non_gaap_eps_fy26_low, non_gaap_eps_fy26_high, pe_low, pe_high))
