import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 
from util import get_db_url

def get_data_from_sql():
    query = """
        SELECT customer_id, monthly_charges, total_charges, tenure
        FROM customers
        WHERE contract_type_id = 3;
    """
    df = pd.read_sql(query, get_db_url("telco_churn"))
    return df


def clean_data(df):
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df["total_charges"] = df["total_charges"].astype('float')
    df = df.dropna()
    return df
       
def wrangle_telco():
    df = get_data_from_sql()
    df = clean_data(df)
    return df 
