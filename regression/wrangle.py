import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 
from env import host, user, password


def get_db_url(username, hostname, password, db_name):
    return f"mysql+pymysql://{user}:{password}@{host}/{db_name}"

url = get_db_url(user, host, password, "telco_churn")

query = """
        SELECT customer_id, monthly_charges, total_charges, tenure
        FROM customers
        WHERE contract_type_id = 3;
"""
def wrangle_df(df, col):
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df[col] = df[col].astype('float')

def read_sql_query(query, url):
    df = pd.read_sql(query, url)
    return df

def wrangle_telco():
    df = pd.read_sql(query, url)
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df = pd.read_sql(query, url)
    return df



       

