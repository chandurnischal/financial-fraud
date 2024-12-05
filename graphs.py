import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from connectDB import retrieveFromDB


# twitter = retrieveFromDB("SELECT account_type, verified, average_tweets_per_day FROM twitter_dataset")
# urls = retrieveFromDB("SELECT type, url_length, domain_length FROM malicious_urls")

twitter = pd.read_csv("data/raw.csv")
urls = pd.read_csv("data/url.csv")

colors = ["#F9DBBD", "#FCA17D", "#DA627D", "#9A348E"]

def convert_to_graph(fig):

    fig.update_layout(template="plotly", paper_bgcolor="#F7F7F7")

    graph = pio.to_html(fig, full_html=False)

    return graph


def stacked_bar_chart():

    grouped = twitter.groupby(["account_type", "verified"]).size().unstack(fill_value=0)
    grouped = grouped.div(grouped.sum(axis=1), axis=0)

    fig = go.Figure()

    for i, v in enumerate(grouped.columns):
        fig.add_trace(go.Bar(
            x=grouped.index, 
            y=grouped[v], 
            name=v, 
            marker=dict(color=colors[i % 2])
        ))

    fig.update_layout(
        barmode="stack",
        title="Account Type by Verification Status",
        xaxis_title="Account Type",
        yaxis_title="Proportion",
        legend_title="Status",
    )

    return convert_to_graph(fig)


def boxplot_tweets_per_day():
    fig = go.Figure()

    for i, type in enumerate(twitter["account_type"].unique()):
        fig.add_trace(
            go.Violin(
                y=twitter.loc[twitter["account_type"] == type, "average_tweets_per_day"],
                name=type,
                box_visible=True,
                meanline_visible=True,
                marker=dict(color=colors[i % 2]),
            )
        )

    fig.update_layout(
        title="Average Tweets per Day by Account Type",
        xaxis_title="Account Type",
        yaxis_title="Average Tweets per Day",
        yaxis=dict(tickformat=".1f"),
    )

    return convert_to_graph(fig)


def average_length_of_url():

    aggregate = urls.groupby("type")["url_length"].median().reset_index()
    

    fig = go.Figure(
        data=[
            go.Bar(
                x=aggregate["type"],
                y=aggregate["url_length"],
                marker=dict(color=colors)
            )
        ]
    )


    fig.update_layout(
        title="Average Length of URLs",
        xaxis_title="Type of Malignity",
        yaxis_title="Average Length of URL",
        template="plotly",
    )

    return convert_to_graph(fig)

def pie_chart_urls():
    aggregate = urls["type"].value_counts().reset_index()
    
    fig = go.Figure(
        data=[
            go.Pie(
                labels=aggregate["type"],
                values=aggregate["count"],
                marker=dict(colors=colors)
            )
        ]
    )


    fig.update_layout(title="Types of URLs")

    return convert_to_graph(fig)