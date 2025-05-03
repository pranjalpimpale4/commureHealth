from prophet import Prophet
import pandas as pd
import json
from datetime import datetime
import os

def run_forecast():
    base_dir = os.path.dirname(os.path.dirname(__file__))  # from agents/ to backend/
    csv_path = os.path.join(base_dir, "data", "historical_appointments_with_address.csv")
    output_path = os.path.join(base_dir, "data", "activity_forecast_llm_ready.json")

    df = pd.read_csv(csv_path, parse_dates=["date"])

    forecast_results = []
    for activity_type in df["activity_type"].unique():
        activity_df = df[df["activity_type"] == activity_type][["date", "count"]].rename(columns={"date": "ds", "count": "y"})
        activity_df["y"] = pd.to_numeric(activity_df["y"], errors="coerce")
        activity_df.dropna(inplace=True)

        if len(activity_df) < 2:
            continue

        model = Prophet(weekly_seasonality=True, yearly_seasonality=True)
        model.fit(activity_df)

        future = model.make_future_dataframe(periods=1, freq="W")
        forecast = model.predict(future)
        next_week = forecast.tail(1)

        for _, row in next_week.iterrows():
            forecast_results.append({
                "category": activity_type,
                "event_date": row["ds"].strftime("%Y-%m-%d"),
                "count": round(row["yhat"])
            })

    output = {
        "generated_on": datetime.utcnow().isoformat(),
        "forecast": forecast_results
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(json.dumps(output, indent=2))  # ✅ This will print

    return output


# if __name__ == "__main__":
#     run_forecast()
