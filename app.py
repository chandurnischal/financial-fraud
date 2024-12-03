from flask import Flask, render_template, request
from graphs import (
    stacked_bar_chart,
    boxplot_tweets_per_day,
    average_length_of_url,
    average_length_of_domain,
)
import requests
import json

app = Flask(__name__)

with open("routes.json") as file:
    routes = json.load(file)


@app.route("/")
def index():
    return render_template("landing_page.html")


@app.route("/twitter_bots", methods=["GET", "POST"])
def twitter_bots():
    data = dict()

    data["prediction"] = None
    data["graphs"] = [stacked_bar_chart(), boxplot_tweets_per_day()]

    if request.method == "POST":

        payload = {
            "verified": request.form["verified"],
            "geo_enabled": request.form["geo_enabled"],
            "average_tweets_per_day": request.form["average_tweets_per_day"],
            "account_age_days": request.form["account_age_days"],
        }

        headers = {"Content-Type": "application/json"}

        try:
            base = routes["twitter"]
            response = requests.post(url=base, headers=headers, json=payload)
            data["prediction"] = response.json()["prediction"].title()
            data["confidence"] = response.json()["probability"]

        except:
            data["prediction"] = "Unable to predict"

        return render_template("twitter_bots.html", data=data)

    return render_template("twitter_bots.html", data=data)


@app.route("/malicious_url", methods=["GET", "POST"])
def malicious_url():
    res = dict()

    res["graphs"] = [average_length_of_url(), average_length_of_domain()]
    res["prediction"] = None


    if request.method == "POST":

        payload = {"url": request.form["url"]}

        headers = {"Content-Type": "application/json"}

        try:
            base = routes["urls"]

            response = requests.post(url=base, headers=headers, json=payload)

            res["prediction"] = response.json()["prediction"].title()
            res["confidence"] = response.json()["confidence"]

        except:
            res["prediction"] = "Benign"
            res["confidence"] = 1.00

        return render_template("malicious_url.html", data=res)

    return render_template("malicious_url.html", data=res)

