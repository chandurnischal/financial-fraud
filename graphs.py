import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

twitter = pd.read_csv("../trial/raw.csv")

def convert_to_graph(fig):

    fig.update_layout(
        template='plotly',
        paper_bgcolor="#F7F7F7"
    )

    graph = pio.to_html(fig, full_html=False)

    return graph

def stacked_bar_chart():
    
    grouped = twitter.groupby(["account_type", "verified"]).size().unstack(fill_value=0)
    grouped = grouped.div(grouped.sum(axis=1), axis=0)

    fig = go.Figure()

    for v in grouped.columns:
        fig.add_trace(
            go.Bar(
                x=grouped.index,
                y=grouped[v],
                name=v
            )
        )
    
    fig.update_layout(
        barmode="stack",
        title="Account Type by Verification Status",
        xaxis_title="Account Type",
        yaxis_title="Proportion",
        legend_title="Status"
    )

    return convert_to_graph(fig)

def boxplot_tweets_per_day():
    fig = go.Figure()

    for type in twitter["account_type"].unique():
        fig.add_trace(
            go.Violin(
                y=twitter.loc[twitter["account_type"] == type, "average_tweets_per_day"],
                name=type,
                box_visible=True,
                meanline_visible=True,
            )
        )

    fig.update_layout(
        title="Average Tweets per Day by Account Type",
        xaxis_title="Account Type",
        yaxis_title="Average Tweets per Day",
        yaxis=dict(tickformat=".1f"),
    )

    return convert_to_graph(fig)