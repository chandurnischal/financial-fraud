from sqlalchemy import create_engine
import json
import pandas as pd

with open("config.json") as file:
    config = json.load(file)

DB_URL = "mysql+pymysql://{}:{}@{}:{}/{}".format(config["user"], config["password"], config["host"], config["port"], config["database"])

engine = create_engine(DB_URL)

query = "SHOW TABLES"

def retrieveFromDB(query:str):
    data = pd.read_sql(query, engine)
    return data

engine.dispose()