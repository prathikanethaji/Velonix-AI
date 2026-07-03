import pandas as pd
import plotly.express as px

# Load dataset once
def load_data():
    return pd.read_csv("hour.csv")


def hourly_chart():

    df = load_data()

    hourly = df.groupby("hr")["cnt"].mean().reset_index()

    fig = px.line(
        hourly,
        x="hr",
        y="cnt",
        markers=True,
        title="Average Bike Demand by Hour"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    return fig.to_html(full_html=False)


def monthly_chart():
    df = load_data()
    monthly = df.groupby("mnth")["cnt"].mean().reset_index()

    fig = px.bar(
        monthly,
        x="mnth",
        y="cnt",
        color="cnt",
        title="Average Monthly Demand"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    return fig.to_html(full_html=False)


def seasonal_chart():

    df = load_data()

    season_names = {
        1:"Spring",
        2:"Summer",
        3:"Fall",
        4:"Winter"
    }

    season = df.groupby("season")["cnt"].mean().reset_index()

    season["season"] = season["season"].map(season_names)

    fig = px.pie(

        season,

        values="cnt",

        names="season",

        hole=.55,

        title="Seasonal Demand"

    )

    fig.update_layout(

        template="plotly_dark",

        height=450

    )

    return fig.to_html(full_html=False)


def weather_chart():

    df = load_data()

    weather_names={

        1:"Clear",

        2:"Mist",

        3:"Light Rain",

        4:"Heavy Rain"

    }

    weather=df.groupby("weathersit")["cnt"].mean().reset_index()

    weather["weathersit"]=weather["weathersit"].map(weather_names)

    fig=px.bar(

        weather,

        x="weathersit",

        y="cnt",

        color="cnt",

        title="Weather Impact"

    )

    fig.update_layout(

        template="plotly_dark",

        height=450

    )

    return fig.to_html(full_html=False)


def top_peak_hours():

    df = load_data()
    peak = df.groupby("hr")["cnt"].mean().sort_values(ascending=False).head(5)

    return peak

def dashboard_stats():

    df = load_data()
    stats = {

        "total_rentals": int(df["cnt"].sum()),

        "average_demand": int(df["cnt"].mean()),

        "peak_hour": int(df.groupby("hr")["cnt"].mean().idxmax()),

        "peak_month": int(df.groupby("mnth")["cnt"].mean().idxmax())

    }

    return stats

def ai_insights():

    df = load_data()

    peak_hour = df.groupby("hr")["cnt"].mean().idxmax()

    peak_season = (
        df.groupby("season")["cnt"]
        .mean()
        .idxmax()
    )

    peak_weather = (
        df.groupby("weathersit")["cnt"]
        .mean()
        .idxmax()
    )

    season_map = {
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter"
    }

    weather_map = {
        1: "Clear Weather",
        2: "Mist / Cloudy",
        3: "Light Rain",
        4: "Heavy Rain"
    }

    insights = [

        f"Peak bike demand occurs around {peak_hour}:00.",

        f"{season_map[peak_season]} records the highest average rentals.",

        f"{weather_map[peak_weather]} results in the highest demand.",

        "Demand increases during commuting hours, indicating strong work-related usage."

    ]

    return insights
