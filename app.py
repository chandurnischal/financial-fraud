import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

with open("weights/twitter_bot_classifier.pkl", "rb") as file:
    tweet_model = pickle.load(file) 


@app.route("/")
def index():
    return render_template("landing_page.html")

@app.route("/twitter_bots", methods=["GET", "POST"])
def twitter_bots():
    pred = None
    if request.method == "POST":
        data = request.form

        test = pd.DataFrame([[data["verified"], data["geo_enabled"], data["average_tweets_per_day"], data["account_age_days"]]], columns=tweet_model.feature_names_in_)


        test["verified"] = test["verified"].map({"true": True, "false": False})
        test["geo_enabled"] = test["geo_enabled"].map({"true": True, "false": False})
        test["average_tweets_per_day"] = test["average_tweets_per_day"].astype(float)
        test["account_age_days"] = test["account_age_days"].astype(float)


        pred = tweet_model.predict(test)[0]

        return render_template("twitter_bots.html", prediction=pred)

    return render_template("twitter_bots.html", prediction=pred)



@app.route("/malicious_url", methods=["GET", "POST"])
def malicious_url():

    if request.method == "POST":

        data = dict(request.form)

        url = "https://{}".format(data["url"])

        r = requests.get(url=url)

        pred = r.status_code    

        return render_template("malicious_url.html", prediction=pred)

    return render_template("malicious_url.html", prediction=None)


if __name__ == '__main__':
    app.run(debug=True)