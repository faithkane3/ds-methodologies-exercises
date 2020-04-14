import pandas as pd
import numpy as np
import scipy as sp 

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler

def prep_iris(df):
    train, test = train_test_split(df, train_size=.75, random_state=123)
    le = LabelEncoder()
    train['species'] = le.fit_transform(train[['species']])
    test['species'] = le.transform(test[['species']])
    return train, test

def inverse_encode(train_encoded, test_encoded):
    train['species'] = le.inverse_transform(train.species)
    test['species'] = le.inverse_transform(test.species)
    return train, test

