# -*- coding: utf-8 -*-
"""App.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DSg6JJPFj89S05XodyxseIgqGNRqqFvd
"""

from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Root Route
@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Donor Prediction Chatbot API! Use the /chat endpoint to interact with the chatbot."

# Load the prediction and comparison data
donor_forecast = pd.read_csv("donor_forecast.csv")
comparison_data = pd.read_csv("actual_vs_predicted.csv")

@app.route("/chat", methods=["POST"])
def chatbot():
    user_message = request.json.get("message", "").lower()
    response = ""

    # Handle predicted visits query
    if "predicted visits" in user_message:
        try:
            requested_date = pd.to_datetime(user_message.split()[-1]).date()
            prediction = donor_forecast.loc[donor_forecast['ds'] == str(requested_date)]
            if not prediction.empty:
                yhat = round(prediction['yhat'].values[0])
                yhat_lower = round(prediction['yhat_lower'].values[0])
                yhat_upper = round(prediction['yhat_upper'].values[0])
                response = (f"The predicted donor visits for {requested_date} are {yhat}. "
                            f"The confidence interval is between {yhat_lower} and {yhat_upper}.")
            else:
                response = f"No prediction available for {requested_date}."
        except Exception:
            response = "Please provide a valid date in the format YYYY-MM-DD."

    # Handle actual vs predicted comparison query
    elif "comparison" in user_message or "actual vs predicted" in user_message:
        try:
            requested_date = pd.to_datetime(user_message.split()[-1]).date()
            comparison = comparison_data.loc[comparison_data['ds'] == str(requested_date)]
            if not comparison.empty:
                actual = round(comparison['Actual'].values[0])
                predicted = round(comparison['Predicted'].values[0])
                response = (f"On {requested_date}, the actual donor visits were {actual}, "
                            f"while the predicted visits were {predicted}.")
            else:
                response = f"No actual vs predicted data available for {requested_date}."
        except Exception:
            response = "Please provide a valid date in the format YYYY-MM-DD."

    # Fallback response for unrecognized queries
    else:
        response = "I can provide predictions or comparisons for donor visits. Please ask about a specific date."

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
