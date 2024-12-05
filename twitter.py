from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd
import boto3
import logging
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

app = Flask(__name__)

# Load the trained model and feature columns
MODEL_PATH = "/home/ec2-user/financial-fraud/random_forest_model.pkl"
FEATURE_COLUMNS_PATH = "/home/ec2-user/financial-fraud/feature_columns.pkl"

# Load the model
with open(MODEL_PATH, "rb") as model_file:
    model = pickle.load(model_file)

# Load the feature columns
with open(FEATURE_COLUMNS_PATH, "rb") as feature_file:
    feature_columns = pickle.load(feature_file)

# Initialize CloudWatch client
cloudwatch_client = boto3.client("cloudwatch", region_name="us-east-1")

def send_cloudwatch_metric(prediction, latency):
    """Send prediction metrics to CloudWatch."""
    try:
        cloudwatch_client.put_metric_data(
            Namespace="TwitterBotPrediction",
            MetricData=[
                {
                    "MetricName": "PredictionCount",
                    "Dimensions": [
                        {"Name": "PredictionType", "Value": prediction},
                    ],
                    "Value": 1,
                    "Unit": "Count"
                },
                {
                    "MetricName": "PredictionLatency",
                    "Value": latency,
                    "Unit": "Milliseconds"
                },
            ]
        )
    except (NoCredentialsError, PartialCredentialsError) as e:
        app.logger.error(f"CloudWatch error: {str(e)}")

@app.route("/twitter_bots", methods=["POST"])
def twitter_bots():
    import time
    start_time = time.time()

    try:
        if not request.is_json:
            return jsonify({"error": "Request data must be JSON"}), 400

        # Parse input data
        data = request.get_json()

        def parse_boolean(value):
            return str(value).strip().lower() == "true"

        # Parse boolean inputs
        verified = parse_boolean(data.get("verified", "false"))
        geo_enabled = parse_boolean(data.get("geo_enabled", "false"))

        # Parse numeric inputs
        try:
            average_tweets_per_day = float(data.get("average_tweets_per_day", 0))
            account_age_days = float(data.get("account_age_days", 0))
        except ValueError:
            return jsonify({"error": "average_tweets_per_day and account_age_days must be numeric"}), 400

        if average_tweets_per_day < 0 or account_age_days <= 0:
            return jsonify({"error": "average_tweets_per_day must be >= 0 and account_age_days must be > 0"}), 400

        # Prepare input as DataFrame
        input_data = pd.DataFrame([{
            "verified": int(verified),
            "geo_enabled": int(geo_enabled),
            "average_tweets_per_day": average_tweets_per_day,
            "account_age_days": account_age_days
        }])

        # Align features with the training set
        input_data = pd.get_dummies(input_data)
        input_data = input_data.reindex(columns=feature_columns, fill_value=0)

        # Predict using the model
        probabilities = model.predict_proba(input_data)[0]
        bot_probability = probabilities[1]
        human_probability = probabilities[0]


        # Simplified logic
        if verified and geo_enabled:
            if average_tweets_per_day < 50 and account_age_days > 30:
                prediction = "human"
            else:
                prediction = "bot"
        elif not verified and not geo_enabled:
            if bot_probability > 0.6 or average_tweets_per_day > 200 or account_age_days < 10:
                prediction = "bot"
            else:
                prediction = "human"
        else:
            prediction = "bot" if bot_probability > 0.5 else "human"

        # Scale probabilities for response
        if prediction == "bot":
            probability = max(0.9, bot_probability)  # Ensure at least 0.90 confidence for bot
        else:
            probability = max(0.8, human_probability)  # Ensure at least 0.80 confidence for human

        # Format the probability with two decimal places
        formatted_probability = f"{probability:.2f}"

        # Calculate latency
        latency = (time.time() - start_time) * 1000

        # Send CloudWatch metrics
        send_cloudwatch_metric(prediction, latency)

        # Return the result
        return jsonify({
            "prediction": prediction,
            "probability": formatted_probability
        }), 200

    except Exception as e:
        app.logger.error(f"Error during prediction: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
