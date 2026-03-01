import numpy as np
import pandas as pd
import random

np.random.seed(42)
random.seed(42)

# ==============================
# Generate Users
# ==============================
def generate_users(n_users=3000):
    segments = ["budget", "mid", "premium"]
    segment_probs = [0.6, 0.3, 0.1]

    users = []

    for user_id in range(n_users):
        segment = np.random.choice(segments, p=segment_probs)

        if segment == "budget":
            avg_order_value = np.random.normal(250, 50)
            order_freq = np.random.randint(2, 6)
        elif segment == "mid":
            avg_order_value = np.random.normal(400, 80)
            order_freq = np.random.randint(4, 10)
        else:
            avg_order_value = np.random.normal(700, 120)
            order_freq = np.random.randint(6, 15)

        users.append([
            user_id,
            segment,
            max(100, avg_order_value),
            order_freq,
            np.random.choice([0, 1], p=[0.4, 0.6]),
            np.random.choice(["tier1", "tier2"], p=[0.7, 0.3])
        ])

    return pd.DataFrame(users, columns=[
        "user_id",
        "segment",
        "avg_order_value",
        "order_frequency",
        "veg_preference",
        "city_tier"
    ])


# ==============================
# Generate Items
# ==============================
def generate_items(n_items=300):
    categories = ["main", "beverage", "dessert", "side"]
    cuisines = ["biryani", "chinese", "pizza", "north_indian", "fast_food"]

    items = []

    for item_id in range(n_items):
        category = np.random.choice(categories, p=[0.4, 0.25, 0.2, 0.15])
        cuisine = np.random.choice(cuisines)

        if category == "main":
            price = np.random.uniform(200, 500)
            margin = np.random.uniform(0.2, 0.35)
        elif category == "beverage":
            price = np.random.uniform(60, 180)
            margin = np.random.uniform(0.5, 0.7)
        elif category == "dessert":
            price = np.random.uniform(120, 300)
            margin = np.random.uniform(0.4, 0.55)
        else:
            price = np.random.uniform(80, 250)
            margin = np.random.uniform(0.35, 0.5)

        popularity = np.random.uniform(0, 1)

        items.append([
            item_id,
            category,
            cuisine,
            round(price, 2),
            round(margin, 2),
            round(popularity, 3)
        ])

    return pd.DataFrame(items, columns=[
        "item_id",
        "category",
        "cuisine",
        "price",
        "margin_percent",
        "popularity_score"
    ])


# ==============================
# Generate Orders
# ==============================
def generate_orders(users_df, items_df, n_orders=8000):

    orders = []
    main_items = items_df[items_df["category"] == "main"]

    for order_id in range(n_orders):
        user = users_df.sample(1).iloc[0]
        main_item = main_items.sample(1).iloc[0]

        cart_size = np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])
        cart_value = main_item["price"] + np.random.uniform(0, 200)

        hour_bucket = np.random.choice(
            ["lunch", "dinner", "late"],
            p=[0.35, 0.5, 0.15]
        )

        weekend_flag = np.random.choice([0, 1], p=[0.7, 0.3])

        if weekend_flag == 1:
            cart_value *= 1.1

        orders.append([
            order_id,
            user["user_id"],
            round(cart_value, 2),
            cart_size,
            hour_bucket,
            weekend_flag
        ])

    return pd.DataFrame(orders, columns=[
        "order_id",
        "user_id",
        "cart_value",
        "cart_size",
        "hour_bucket",
        "weekend_flag"
    ])


# ==============================
# Acceptance Logic
# ==============================
def simulate_acceptance(user_segment, item_category, cart_value,
                        hour_bucket, item_price, user_avg_spend):

    prob = 0.1

    if item_category in ["beverage", "dessert"]:
        prob += 0.25

    if hour_bucket == "dinner" and item_category == "dessert":
        prob += 0.15

    if 250 < cart_value < 320:
        prob += 0.10

    if user_segment == "budget" and item_price > user_avg_spend * 0.5:
        prob -= 0.20

    if user_segment == "premium" and item_category == "dessert":
        prob += 0.10

    prob = max(0, min(prob, 0.95))

    return np.random.rand() < prob


# ==============================
# Training Data
# ==============================
def generate_training_data(users_df, items_df, orders_df):

    rows = []

    for _, order in orders_df.iterrows():

        user = users_df.loc[
            users_df["user_id"] == order["user_id"]
        ].iloc[0]

        candidate_items = items_df.sample(3)

        for _, item in candidate_items.iterrows():

            accepted = simulate_acceptance(
                user["segment"],
                item["category"],
                order["cart_value"],
                order["hour_bucket"],
                item["price"],
                user["avg_order_value"]
            )

            rows.append([
                order["order_id"],
                user["user_id"],
                item["item_id"],
                user["segment"],
                order["cart_value"],
                order["cart_size"],
                order["hour_bucket"],
                order["weekend_flag"],
                item["price"],
                item["margin_percent"],
                item["popularity_score"],
                1 if item["category"] in ["beverage", "dessert"] else 0,
                int(accepted)
            ])

    return pd.DataFrame(rows, columns=[
        "order_id",
        "user_id",
        "item_id",
        "user_segment",
        "cart_value",
        "cart_size",
        "hour_bucket",
        "weekend_flag",
        "item_price",
        "item_margin",
        "popularity_score",
        "category_match_flag",
        "accepted"
    ])


# ==============================
# MAIN
# ==============================
if __name__ == "__main__":

    users_df = generate_users()
    items_df = generate_items()
    orders_df = generate_orders(users_df, items_df)
    train_df = generate_training_data(users_df, items_df, orders_df)

    users_df.to_csv("users.csv", index=False)
    items_df.to_csv("items.csv", index=False)
    orders_df.to_csv("orders.csv", index=False)
    train_df.to_csv("train_data.csv", index=False)

    print("Data generation complete.")