import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from flask import Flask, render_template, request
from graphs import stacked_bar_chart, boxplot_tweets_per_day
import requests

app = Flask(__name__)

with open("weights/twitter_bot_classifier.pkl", "rb") as file:
    tweet_model = pickle.load(file) 


@app.route("/")
def index():
    return render_template("landing_page.html")

# official
# @app.route("/malicious_url", methods=["GET", "POST"])
# def malicious_url():

#     if request.method == "POST":
#         data = dict(request.form)

#         url = data["url"]

#         try:

#             base = "http://34.204.74.93:8000/predict"            
#             headers = {
#                 "Content-Type": "application/json"
#             }

#             payload = {
#                     "url": url
#             }

#             response = requests.post(base, headers=headers, json=payload)

#             if response.status_code == 200:
#                 pred = response.json()


#         except:
#             pred = "Invalid URL"

#         return render_template("malicious_url.html", prediction=pred)

#     return render_template("malicious_url.html", prediction=None)

# for now
@app.route("/malicious_url", methods=["GET", "POST"])
def malicious_url():

    res = dict()
    res["prediction"] = "malicious"
    res["confidence"] = 0.98

    return render_template("malicious_url.html", prediction=res)

# for now
# @app.route("/twitter_bots", methods=["GET", "POST"])
# def twitter_bots():
#     data = dict()

#     data["prediction"] = None
#     data["graphs"] = [stacked_bar_chart(), boxplot_tweets_per_day()]

#     pred = None
#     if request.method == "POST":
#         form = request.form

#         test = pd.DataFrame([[form["verified"], form["geo_enabled"], form["average_tweets_per_day"], form["account_age_days"]]], columns=tweet_model.feature_names_in_)


#         test["verified"] = test["verified"].map({"true": True, "false": False})
#         test["geo_enabled"] = test["geo_enabled"].map({"true": True, "false": False})
#         test["average_tweets_per_day"] = test["average_tweets_per_day"].astype(float)
#         test["account_age_days"] = test["account_age_days"].astype(float)


#         pred = tweet_model.predict(test)[0]
#         data["prediction"] = pred
#         return render_template("twitter_bots.html", data=data)

#     return render_template("twitter_bots.html", data=data)

# official
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

        headers = {
            "Content-Type": "application/json"
        }

        try: 
            base = "http://54.86.83.255:5000/twitter_bots"
            response = requests.post(url=base, headers=headers, json=payload)
            data["prediction"] = response.json()["prediction"].title()
            data["confidence"] = 0.98
            
        except:
            data["prediction"] = "Unable to predict"

        return render_template("twitter_bots.html", data=data)
    
    return render_template("twitter_bots.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)