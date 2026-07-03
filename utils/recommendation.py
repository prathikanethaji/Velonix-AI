def get_recommendation(prediction):

    if prediction < 100:

        return (
            "🟢 Low Demand",
            "Demand is low. Current fleet is sufficient. This is a good time to schedule maintenance or redistribute bikes to busier locations."
        )

    elif prediction < 300:

        return (
            "🟡 Moderate Demand",
            "Demand is moderate. Maintain the current fleet and monitor demand during peak hours."
        )

    else:

        return (
            "🔴 High Demand",
            "High demand expected. Deploy additional bikes, assign extra staff, and ensure docking stations are adequately stocked."
        )