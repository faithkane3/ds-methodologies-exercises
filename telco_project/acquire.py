import pandas as pd 
from env import host, user, password

def get_db_url(db_name):
    return f"mysql+pymysql://{user}:{password}@{host}/{db_name}"


def get_titanic_data():
    query = "SELECT * FROM passengers"
    url = get_db_url("titanic_db")
    df = pd.read_sql(query, url)
    return df


def get_iris_data():
    query = """SELECT *
        FROM measurements
        JOIN species USING(species_id)"""
    url = get_db_url("iris_db")
    df = pd.read_sql(query, url)
    return df