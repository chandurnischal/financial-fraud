import pymysql as pm
import json
import pandas as pd

with open("config.json") as file:
    config = json.load(file)


def connectToDB(query: str) -> pd.DataFrame:
    with pm.connect(**config) as conn:
        data = pd.read_sql(query, conn)

    return data
