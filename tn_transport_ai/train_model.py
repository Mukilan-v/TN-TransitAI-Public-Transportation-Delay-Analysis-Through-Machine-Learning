import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

BASE_DIR = Path(__file__).resolve().parent

data_path = BASE_DIR / "data" / "transport_dataset.csv"
df = pd.read_csv(data_path)

print(f"Training on {len(df)} records...")

# Encoders
le_weather = LabelEncoder()
le_day = LabelEncoder()

df["weather_enc"] = le_weather.fit_transform(df["weather"])
df["day_enc"] = le_day.fit_transform(df["day"])

feature_cols = [
    "distance_km",
    "hour",
    "day_enc",
    "is_weekend",
    "weather_enc",
    "traffic_score",
    "is_ghat",
    "base_time"
]

X = df[feature_cols]
y = df["delay_minutes"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

model = RandomForestRegressor(
    n_estimators=120,
    max_depth=14,
    min_samples_split=4,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("Model Evaluation Results:")
print(f"   R2 Accuracy Score: {r2 * 100:.2f}%")
print(f"   Mean Absolute Error (MAE): {mae:.2f} minutes")
print(f"   Root Mean Squared Error (RMSE): {rmse:.2f} minutes")

# Feature importances
importances = dict(zip(feature_cols, [round(float(v) * 100, 2) for v in model.feature_importances_]))
print("   Feature Importances:", importances)

model_payload = {
    "model": model,
    "le_weather": le_weather,
    "le_day": le_day,
    "feature_cols": feature_cols,
    "metrics": {
        "r2_pct": round(r2 * 100, 2),
        "mae": round(mae, 2),
        "rmse": round(rmse, 2)
    },
    "feature_importances": importances
}

models_dir = BASE_DIR / "models"
models_dir.mkdir(exist_ok=True)
model_path = models_dir / "transport_model.pkl"

with open(model_path, "wb") as f:
    pickle.dump(model_payload, f)

print(f"Advanced Model Saved Successfully at {model_path}!")
