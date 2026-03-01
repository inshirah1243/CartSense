import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_auc_score

df = pd.read_csv("train_data.csv")

categorical_cols = ["user_segment", "hour_bucket"]

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])

X = df.drop(["accepted", "order_id", "user_id", "item_id"], axis=1)
y = df["accepted"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = xgb.XGBClassifier(eval_metric="logloss")
model.fit(X_train, y_train)

preds = model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, preds)

print("Model trained successfully.")
print("AUC Score:", round(auc, 4))

importance = model.feature_importances_
feature_importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": importance
}).sort_values("importance", ascending=False)

print("\nTop Features:")
print(feature_importance_df.head(10))

df["predicted_prob"] = model.predict_proba(X)[:, 1]
df.to_csv("scored_data.csv", index=False)

print("Scored data saved.")