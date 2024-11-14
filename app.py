import numpy as np
import plotly.graph_objs as go
import plotly.offline as pyo
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("landing_page.html")

@app.route("/twitter_bots")
def twitter_bots():
    return render_template("twitter_bots.html")

@app.route("/malicious_url")
def malicious_url():
    return render_template("malicious_url.html")


if __name__ == '__main__':
    app.run(debug=True)