import os

from flask import Flask, render_template, request

from utils.predictor import predict_bike

from utils.recommendation import get_recommendation

import utils.analytics as analytics

from flask import send_from_directory
from werkzeug.utils import secure_filename
from utils.batch_predictor import predict_dataset
app = Flask(__name__)


@app.route("/")
def home():
    return render_template(
    "index.html",
    active_page="home"
)

@app.route("/predict", methods=["GET", "POST"])
def predict():

    prediction = None
    demand = None
    recommendation = None

    if request.method == "POST":

        prediction = predict_bike(

            int(request.form["season"]),

            1,      # Fixed Year

            int(request.form["mnth"]),

            int(request.form["hr"]),

            int(request.form["weekday"]),

            int(request.form["weathersit"]),

            float(request.form["temp"]),

            float(request.form["hum"])

        )

        demand, recommendation = get_recommendation(prediction)

    return render_template(
    "predict.html",
    prediction=prediction,
    demand=demand,
    recommendation=recommendation,
    active_page="predict"
)


@app.route("/analytics")
def analytics_page():

    return render_template(
        "analytics.html",

        stats=analytics.dashboard_stats(),

        hourly=analytics.hourly_chart(),

        monthly=analytics.monthly_chart(),

        seasonal=analytics.seasonal_chart(),

        weather=analytics.weather_chart(),

        peaks=analytics.top_peak_hours(),

        insights=analytics.ai_insights()
    )


@app.route("/about")
def about():
   return render_template(
    "about.html",
    active_page="about"
)

@app.route("/batch_predict", methods=["GET", "POST"])
def batch_predict():

    if request.method == "POST":

        if "file" not in request.files:
            return render_template(
                "batch_predict.html",
                active_page="batch",
                error="Please upload a CSV file."
            )

        file = request.files["file"]

        if file.filename == "":
            return render_template(
                "batch_predict.html",
                active_page="batch",
                error="No file selected."
            )

        filename = secure_filename(file.filename)

        upload_path = os.path.join("uploads", filename)

        file.save(upload_path)

        result_df, missing = predict_dataset(upload_path)

        if missing:

            return render_template(
                "batch_predict.html",
                active_page="batch",
                error=f"Missing columns: {', '.join(missing)}"
            )

        output_filename = "predictions.csv"

        output_path = os.path.join(
            "outputs",
            output_filename
        )

        result_df.to_csv(output_path, index=False)

        return render_template(
            "batch_predict.html",
            active_page="batch",
            success=True,
            rows=len(result_df),
            filename=output_filename
        )

    return render_template(
        "batch_predict.html",
        active_page="batch"
    )


@app.route("/download_predictions/<filename>")
def download_predictions(filename):

    return send_from_directory(

        "outputs",

        filename,

        as_attachment=True

    )

@app.route("/sample_csv")
def sample_csv():

    return send_from_directory(
        "static/sample",
        "sample_bike_data.csv",
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)
