from prophet import Prophet
import pandas as pd
import json
from datetime import datetime

# Load data
df = pd.read_csv("data/historical_appointments_with_address.csv", parse_dates=["date"])

forecast_results = []
forecast_horizon = 1  # 1 week ahead

for activity_type in df["activity_type"].unique():
    activity_df = df[df["activity_type"] == activity_type][["date", "count"]].rename(columns={"date": "ds", "count": "y"})
    
    # Convert to numeric, drop NaNs
    activity_df["y"] = pd.to_numeric(activity_df["y"], errors="coerce")
    activity_df.dropna(inplace=True)

    if len(activity_df) < 2:
        print(f"Skipping {activity_type} — not enough data")
        continue

    model = Prophet(weekly_seasonality=True, yearly_seasonality=True)
    model.fit(activity_df)
    
    future = model.make_future_dataframe(periods=1, freq="W")
    forecast = model.predict(future)
    next_week = forecast.tail(1)

    for _, row in next_week.iterrows():
        forecast_results.append({
            "activity_type": activity_type,
            "week": row["ds"].strftime("%Y-%m-%d"),
            "forecasted_count": round(row["yhat"])
        })

# Save output
output = {
    "generated_on": datetime.utcnow().isoformat(),
    "forecast": forecast_results
}

with open("data/activity_forecast_llm_ready.json", "w") as f:
    json.dump(output, f, indent=2)


print("✅ Forecast saved to activity_forecast_llm_ready.json")
