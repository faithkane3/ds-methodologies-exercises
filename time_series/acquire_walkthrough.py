import os
import pandas as pd
import numpy as np
import requests

def def get_df(name):
    """
    This function takes in the string
    '/items', '/stores', or '/sales' and
    returns a df containing all pages and
    creates a .csv file for future use.
    """
    base_url = 'https://python.zach.lol'
    api_url = base_url + '/api/v1/'
    response = requests.get(api_url + name)
    data = response.json()
    
    # create list from 1st page
    my_list = data['payload'][name]
    
    # loop through the pages and add to list
    while data['payload']['next_page'] != None:
        response = requests.get(base_url + data['payload']['next_page'])
        data = response.json()
        my_list.extend(data['payload'][name])
    
    # Create DataFrame from list
    df = pd.DataFrame(my_list)
    
    # Write DataFrame to csv file for future use
    df.to_csv(name + '.csv')
    return df

# Function that checks for a csv, and if one doesn't exist it creates one
# The function should also create one large df using all three df

def get_store_data():
    """
    This function checks for csv files
    for items, sales, and stores, and 
    if there are none, it creates them
    and merges them into one df
    """
    if os.path.isfile('items.csv'):
        items_df = pd.read_csv('items.csv', index_col=0)
    else:
        items_df = get_df('items')
    if os.path.isfile('stores.csv'):
        stores_df = pd.read_csv('stores.csv', index_col=0)
    else:
        stores_df = get_df('stores')
    if os.path.isfile('sales.csv'):
        sales_df = pd.read_csv('sales.csv', index_col=0)
    else:
        sales_df = get_df('sales')
    
    df = pd.merge(sales_df, stores_df, left_on='store', right_on='store_id').drop(columns={'store'})
    df = pd.merge(df, items_df, left_on='item', right_on='item_id').drop(columns={'item'})
    df['sale_date'] = pd.to_datetime(df.sale_date)
    df = df.set_index('sale_date').sort_index()
    return df

# Function that checks for a csv, and if it doesn't exist it reads url and creates one
# Function returns the df with a DateTime Index

def german_energy_csv():
    """
    This function takes in a string csv url
    and returns a df with a datetime index
    """
    if os.path.isfile('german_energy.csv'):
        df = pd.read_csv('german_energy.csv', parse_dates=True, index_col=0)
    else:
        url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
        df = pd.read_csv(url, parse_dates=True).set_index('Date').sort_index()
        df.to_csv('german_energy.csv')
    return df