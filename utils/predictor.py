import joblib
import pandas as pd

model = joblib.load("bike_demand_model.joblib")


def predict_bike(
    season,
    yr,
    mnth,
    hr,
    weekday,
    weathersit,
    temp,
    hum
):

    input_df = pd.DataFrame({
    "season": [season],
    "yr": [yr],
    "mnth": [mnth],
    "hr": [hr],
    "holiday": [0],          # Hidden
    "weekday": [weekday],
    "workingday": [1],       # Hidden
    "weathersit": [weathersit],
    "temp": [temp],
    "atemp": [temp],         # Use temp
    "hum": [hum],
    "windspeed": [0.2]       # Hidden
})

    prediction = model.predict(input_df)

    return int(round(prediction[0]))