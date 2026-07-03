import pandas as pd
import plotly.express as px

# ==========================================================
# Load Dataset
# ==========================================================

def load_data():
    return pd.read_csv("hour.csv")


# ==========================================================
# Common Plotly Layout
# ==========================================================

def update_chart_layout(fig):

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#1b1b1b",
        plot_bgcolor="#1b1b1b",

        font=dict(
            family="Arial",
            color="white",
            size=14
        ),

        title_font=dict(
            size=20,
            color="#FFC107"
        ),

        margin=dict(
            l=30,
            r=30,
            t=60,
            b=30
        ),

        height=450,

        autosize=True,

        legend=dict(
            bgcolor="#1b1b1b"
        )

    )

    return fig


# ==========================================================
# Dashboard Statistics
# ==========================================================

def dashboard_stats():

    df = load_data()

    months = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    peak_month = int(df.groupby("mnth")["cnt"].mean().idxmax())

    return {

    "total_rentals": int(df["cnt"].sum()),

    "average_demand": round(df["cnt"].mean(), 2),

    "peak_hour": int(df.groupby("hr")["cnt"].mean().idxmax()),

    "peak_month": months[peak_month]

}



# ==========================================================
# Hourly Demand
# ==========================================================

def hourly_chart():

    df = load_data()

    hourly = (
        df.groupby("hr")["cnt"]
        .mean()
        .reset_index()
    )

    fig = px.line(

        hourly,

        x="hr",

        y="cnt",

        markers=True,

        title="Average Bike Rentals by Hour"

    )

    fig.update_traces(

        line=dict(
            color="#FFC107",
            width=4
        ),

        marker=dict(
            size=8
        )

    )

    fig = update_chart_layout(fig)

    return fig.to_html(

        full_html=False,

        include_plotlyjs="cdn",

        config={
            "responsive": True,
            "displayModeBar": False
        }

    )


# ==========================================================
# Monthly Demand
# ==========================================================

def monthly_chart():

    df = load_data()

    monthly = (
        df.groupby("mnth")["cnt"]
        .mean()
        .reset_index()
    )

    fig = px.bar(

        monthly,

        x="mnth",

        y="cnt",

        color="cnt",

        color_continuous_scale="YlOrBr",

        title="Average Monthly Bike Demand"

    )

    fig = update_chart_layout(fig)

    return fig.to_html(

        full_html=False,

        include_plotlyjs=False,

        config={
            "responsive": True,
            "displayModeBar": False
        }

    )

# ==========================================================
# Seasonal Demand
# ==========================================================

def seasonal_chart():

    df = load_data()

    season_map = {
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter"
    }

    seasonal = (
        df.groupby("season")["cnt"]
        .mean()
        .reset_index()
    )

    seasonal["season"] = seasonal["season"].map(season_map)

    fig = px.pie(

        seasonal,

        values="cnt",

        names="season",

        hole=0.45,

        color_discrete_sequence=px.colors.sequential.YlOrBr,

        title="Seasonal Demand Distribution"

    )

    fig.update_traces(

        textposition="inside",

        textinfo="percent+label"

    )

    fig = update_chart_layout(fig)

    return fig.to_html(

        full_html=False,

        include_plotlyjs=False,

        config={
            "responsive": True,
            "displayModeBar": False
        }

    )


# ==========================================================
# Weather Impact
# ==========================================================

def weather_chart():

    df = load_data()

    weather_map = {
        1: "Clear",
        2: "Mist",
        3: "Light Snow/Rain",
        4: "Heavy Rain"
    }

    weather = (
        df.groupby("weathersit")["cnt"]
        .mean()
        .reset_index()
    )

    weather["weathersit"] = weather["weathersit"].map(weather_map)

    fig = px.bar(

        weather,

        x="weathersit",

        y="cnt",

        color="cnt",

        color_continuous_scale="YlOrBr",

        title="Weather Impact on Rentals"

    )

    fig = update_chart_layout(fig)

    return fig.to_html(

        full_html=False,

        include_plotlyjs=False,

        config={
            "responsive": True,
            "displayModeBar": False
        }

    )


# ==========================================================
# Top Peak Hours
# ==========================================================

def top_peak_hours():

    df = load_data()

    peak_hours = (
        df.groupby("hr")["cnt"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    return peak_hours.to_dict()


# ==========================================================
# AI Insights
# ==========================================================

def ai_insights():

    stats = dashboard_stats()

    insights = [

        f"🚲 A total of {stats['total_rentals']:,} bike rentals have been recorded in the dataset.",

        f"📈 The average rental demand is {stats['average_demand']} bikes per hour.",

        f"⏰ Peak demand occurs around {stats['peak_hour']}:00, indicating the busiest rental period.",

        f"📅 {stats['peak_month']} experiences the highest average rental demand.",

        "💡 Increase bike availability during evening peak hours to reduce shortages.",

        "🔧 Schedule bike maintenance during low-demand periods to minimize service disruption.",

        "🌤 Weather conditions significantly influence bike rental demand.",

        "📊 Seasonal demand trends can help optimize inventory planning."

    ]

    return insights