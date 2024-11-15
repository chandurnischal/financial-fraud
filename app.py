import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("landing_page.html")

@app.route("/twitter_bots", methods=['GET', 'POST'])
def twitter_bots():


    input_data = request.form["verified"]

    # return render_template("twitter_bots.html", prediction="Human" if prediction == "human" else "Bot")
    return render_template("twitter_bots.html", prediction=input_data)


@app.route("/malicious_url")
def malicious_url():
    return render_template("malicious_url.html")


if __name__ == '__main__':
    app.run(debug=True)