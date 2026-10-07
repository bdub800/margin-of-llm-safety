"""Implied EV/Revenue paid by Constellation Software and Topicus.com for acquisitions.

Sources (all URLs):
- CSI FY2025 consolidated financial statements, Note 4 (Business acquisitions):
  Cipal Schaubroeck total consideration $258M + "additional acquisitions" total
  consideration $1,321M  => FY2025 total consideration $1,579M.
  https://www.csisoftware.com/wp-content/uploads/2026/04/Q4-2025-Shareholder-Report.pdf
- CSI FY2024 press release: "acquisitions completed for total consideration of
  $1,792 million including holdbacks and contingent consideration" (FY2024).
  https://www.csisoftware.com/constellation-software-inc-announces-results-for-the-fourth-quarter-and-year-ended-december-31-2024-and-declares-quarterly-dividend/
- CSI FY2025 MD&A organic-growth table, Note 2: "Estimated pre-acquisition revenues for
  the twelve months ended December 31, 2024 from companies acquired after December 31,
  2023" = $1,111M  (i.e. FY2024 standalone revenue of the 2024+2025 acquisition cohort).
  https://www.csisoftware.com/wp-content/uploads/2026/04/Q4-2025-Shareholder-Report.pdf
- Topicus FY2025 press release: total consideration EUR 390.4M.
  https://finance.yahoo.com/news/constellation-software-inc-topicus-com-220400881.html
- Topicus FY2025 MD&A organic-growth table, Note 2 proforma adj = EUR 198.0M.
  https://newsfile.futunn.com/public/NN-PersistNoticeAttachment/7781/20260226/SEDAR_PLUS/CSA_SEDAR_PLUS_NOTICE_RECORD_ID_2328375.pdf
"""

# --- Constellation Software: 2024 + 2025 acquisition cohort ---
csi_consideration_2025 = 258 + 1321          # $M, CSI FY2025 FS Note 4(a)+(b)
csi_consideration_2024 = 1792                # $M, CSI FY2024 press release
csi_cohort_consideration = csi_consideration_2024 + csi_consideration_2025
csi_cohort_revenue = 1111                    # $M, FY2024 standalone revenue of cohort
csi_multiple = csi_cohort_consideration / csi_cohort_revenue

print(f"CSI 2024+2025 consideration: ${csi_cohort_consideration:,.0f}M")
print(f"CSI cohort FY2024 revenue:   ${csi_cohort_revenue:,.0f}M")
print(f"CSI implied EV/Revenue:      {csi_multiple:.2f}x")

# Single-year sanity check: FY2025 spend vs the cohort revenue share attributable to
# 2025 deals is NOT separately disclosed, so the 2-year cohort is the cleanest cut.
# Upper/lower bracket using 2025-only and 2024-only spend against the same revenue base:
print(f"  bracket (2025 spend only / cohort rev): {csi_consideration_2025/csi_cohort_revenue:.2f}x (too low - denominator too big)")

# --- Topicus.com: 2024 + 2025 acquisition cohort (2024 consideration NOT FOUND) ---
top_consideration_2025 = 390.4               # EUR M
top_cohort_revenue = 198.0                   # EUR M, FY2024 standalone revenue of cohort
print(f"\nTopicus 2025 consideration alone / 2024+2025 cohort revenue: "
      f"{top_consideration_2025/top_cohort_revenue:.2f}x  "
      f"(LOWER BOUND - FY2024 consideration not sourced)")
