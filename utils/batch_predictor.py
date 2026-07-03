import pandas as pd
import joblib

# Load trained model
model = joblib.load("bike_demand_model.joblib")


def predict_dataset(file_path):

    # Read CSV
    df = pd.read_csv(file_path)

    # Columns the user must upload
    required_columns = [
        "season",
        "mnth",
        "hr",
        "weekday",
        "weathersit",
        "temp",
        "hum"
    ]

    # Check for missing columns
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        return None, missing

    # Add hidden/default columns
    df["yr"] = 1
    df["holiday"] = 0
    df["workingday"] = 1
    df["atemp"] = df["temp"]
    df["windspeed"] = 0.2

    # Arrange columns exactly as the model expects
    model_columns = [
        "season",
        "yr",
        "mnth",
        "hr",
        "holiday",
        "weekday",
        "workingday",
        "weathersit",
        "temp",
        "atemp",
        "hum",
        "windspeed"
    ]

    # Predict
    predictions = model.predict(df[model_columns])

    # Round predictions
    df["Predicted_Rentals"] = predictions.round().astype(int)

    # Demand Level
    def demand_level(value):
        if value < 100:
            return "Low"
        elif value < 300:
            return "Moderate"
        else:
            return "High"

    df["Demand_Level"] = df["Predicted_Rentals"].apply(demand_level)

    # AI Recommendation
    def recommendation(level):

        if level == "Low":
            return "Schedule maintenance or redistribute bikes."

        elif level == "Moderate":
            return "Maintain current fleet and monitor demand."

        else:
            return "Deploy additional bikes and staff."

    df["Recommendation"] = df["Demand_Level"].apply(recommendation)

    return df, None