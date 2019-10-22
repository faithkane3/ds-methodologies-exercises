import pandas as pd 
import numpy as np 
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler



def prep_iris(df):
    df.drop(columns=["species_id","measurement_id"], inplace=True)
    df.rename(columns={"species_name": "species"}, inplace=True)
    encoder = LabelEncoder()
    encoder.fit(df.species)
    encoder.transform(df.species)
    return df


def prep_titanic(df):
    df.fillna(np.nan, inplace=True)
    df = df[~df.embarked.isnull()]
    encoder = LabelEncoder()
    encoder.fit(df.embarked)
    df.embarked = encoder.transform(df.embarked)
    scaler = MinMaxScaler()
    scaler.fit(df[["age"]])
    df.age = scaler.transform(df[["age"]])
    scaler.fit(df[["fare"]])
    df.fare = scaler.transform(df[["fare"]])
    return df