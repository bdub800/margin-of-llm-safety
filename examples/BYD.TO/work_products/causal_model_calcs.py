"""Calculations supporting work_products/causal_model.md (Boyd Group, US$M).
Inputs from primary_sources (Q2FY26 MD&A, FY2025/FY2024 MD&A) and work_products/owners_earnings_and_roic.md."""

# --- Stage 1: Q2 2026 sales bridge (Q2FY26 MD&A, Sales) ---
q2_sales, q2_growth = 1013.652, 233.2
new_loc, jh, sss, closures = 211.3, 174.8, 22.3, -0.4
prior = q2_sales - q2_growth
print("Q2'26 sales bridge (% of prior-year Q2 sales):")
for k, v in [("new locations", new_loc), ("  of which Joe Hudson's", jh), ("same-store", sss), ("closures", closures)]:
    print(f"  {k:24s} {v:7.1f}  {v/prior*100:5.1f}%")
print(f"  other/FX residual        {q2_growth-new_loc-sss-closures:7.1f}")
print(f"  JH annualized sales run-rate ~ {jh*4:.0f}")

# Same-store sales history (MD&As, ex-FX) vs industry repairable claims
sss_hist = {"FY2023": 15.8, "FY2024": -1.8, "FY2025": -0.2, "Q4'25": 2.2, "H1'26": 2.2, "Q2'26": 2.9}
claims = {"FY2024": -9.0, "FY2025": -6.0, "Q4'25": -3.0, "H1'26": -1.0, "Q2'26": -1.0}  # midpoints of ranges
print("\nSSS outperformance vs repairable-claims midpoint (pp):")
for k in claims:
    print(f"  {k:7s} SSS {sss_hist[k]:5.1f}%  claims {claims[k]:5.1f}%  spread {sss_hist[k]-claims[k]:4.1f}pp")

# Long-term algorithm (FY2025 MD&A / Q1FY26 call): TCOR 3-4% + miles 1% - claims(ADAS) 2% + share
# Q1FY26 call (official framework): miles +1%, ADAS -2%.  FY2025 call adds car park +1% (but states net "down 1%").
for tcor in (0.0, 1.0, 3.5):
    print(f"  implied industry repairable $ growth at TCOR {tcor}%: {tcor+1-2:.1f}% (2-term, Q1FY26) / {tcor+1+1-2:.1f}% (3-term, FY2025 call)")

# --- Stage 2/3: margin bridge (Results of Operations tables) ---
gm = {"FY2023": 45.5, "FY2024": 45.5, "FY2025": 46.4, "Q2'25": 46.8, "Q2'26": 47.4}
opex = {"FY2023": 33.0, "FY2024": 34.6, "FY2025": 34.4, "Q2'25": 34.8, "Q2'26": 33.9}
print("\nGross margin - opex ratio (= Adj. EBITDA margin approx):")
for k in gm:
    print(f"  {k:7s} GM {gm[k]:.1f}%  opex {opex[k]:.1f}%  diff {gm[k]-opex[k]:.1f}%")
# FY2024 operating deleverage: SSS -1.8% -> opex ratio +1.6pp, EBITDA margin 12.5%->10.9%
print(f"  FY2024: EBITDA margin change {10.9-12.5:.1f}pp on SSS -1.8% -> ~{(10.9-12.5)/-1.8:.1f}pp margin per 1% SSS (crude, includes new-store drag)")

# --- Stage 4: Owners' Earnings sensitivities (TTM Jun-26, owners_earnings_and_roic.md) ---
ttm_sales, ttm_ebitda, ttm_rent, ttm_oe, tax = 3594.4, 460.3, 189.8, 145.9, 0.265
print(f"\nTTM rent / Adj. EBITDA = {ttm_rent/ttm_ebitda*100:.1f}%;  OE / Adj. EBITDA = {ttm_oe/ttm_ebitda*100:.1f}%")
# EBITDA-to-OE bridge shares (owners_earnings_and_roic.md, TTM)
maint, sw, acq, taxamt = 61.1, 5.9, 5.0, 52.6
for k, v in [("rent", ttm_rent), ("maintenance capex", maint), ("rent + maint. capex", ttm_rent+maint), ("software capex", sw), ("normalized acq. cost", acq), ("normalized tax", taxamt), ("total consumed", ttm_rent+maint+sw+acq+taxamt)]:
    print(f"  {k:22s} {v:6.1f}  {v/ttm_ebitda*100:5.1f}% of Adj. EBITDA")
d_oe_100bp = ttm_sales*0.01*(1-tax)
print(f"+100bp Adj. EBITDA margin on TTM sales -> OE +{d_oe_100bp:.1f} ({d_oe_100bp/ttm_oe*100:.0f}% of TTM OE)")
d_oe_1pct_sss = ttm_sales*0.01*0.47*(1-tax)  # upper bound: flow-through at gross margin, no incremental opex
print(f"+1% SSS at ~47% GM flow-through (upper bound) -> OE +{d_oe_1pct_sss:.1f} ({d_oe_1pct_sss/ttm_oe*100:.0f}%)")
syn_remaining = 65.0  # $140M program less $35M realized H1'26 less $40M in 2025 (Q2FY26 MD&A)
print(f"Remaining ~$65M synergies after tax -> OE +{syn_remaining*(1-tax):.1f} ({syn_remaining*(1-tax)/ttm_oe*100:.0f}%)")
target_gap = (0.14-ttm_ebitda/ttm_sales)*ttm_sales*(1-tax)
print(f"Reaching 14% margin target on TTM sales -> OE +{target_gap:.1f}; TTM margin {ttm_ebitda/ttm_sales*100:.1f}%")
