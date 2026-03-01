import pandas as pd

df = pd.read_csv("scored_data.csv")

# =============================
# Baseline Ranking
# =============================
baseline = df.sort_values(
    ["order_id", "predicted_prob"],
    ascending=[True, False]
)

baseline_top = baseline.groupby("order_id").head(1)

baseline_revenue = (
    baseline_top["predicted_prob"]
    * baseline_top["item_price"]
    * baseline_top["item_margin"]
).sum()

# =============================
# Revenue Optimized Ranking
# =============================
df["expected_revenue"] = (
    df["predicted_prob"]
    * df["item_price"]
    * df["item_margin"]
)

optimized = df.sort_values(
    ["order_id", "expected_revenue"],
    ascending=[True, False]
)

optimized_top = optimized.groupby("order_id").head(1)

optimized_revenue = optimized_top["expected_revenue"].sum()

uplift = (
    (optimized_revenue - baseline_revenue)
    / baseline_revenue
) * 100

print("\n===== Revenue Comparison =====")
print("Baseline Revenue:", round(baseline_revenue, 2))
print("Optimized Revenue:", round(optimized_revenue, 2))
print("Revenue Uplift (%):", round(uplift, 2))

print("\nAverage Revenue per Order (Baseline):",
      round(baseline_revenue / baseline_top.shape[0], 2))

print("Average Revenue per Order (Optimized):",
      round(optimized_revenue / optimized_top.shape[0], 2))

# =============================
# Cold Start Simulation
# =============================
print("\n===== Cold Start Fallback (New User) =====")

df["cold_start_score"] = (
    0.4 * df["popularity_score"]
    + 0.3 * df["category_match_flag"]
    + 0.2 * df["item_margin"]
)

cold_start = df.sort_values(
    ["order_id", "cold_start_score"],
    ascending=[True, False]
)

cold_top = cold_start.groupby("order_id").head(1)

cold_revenue = (
    cold_top["cold_start_score"]
    * cold_top["item_price"]
    * cold_top["item_margin"]
).sum()

print("Cold Start Revenue (Fallback):", round(cold_revenue, 2))