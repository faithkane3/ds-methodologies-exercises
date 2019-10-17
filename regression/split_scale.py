import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pydataset import data
import wrangle
import util
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, QuantileTransformer, PowerTransformer, RobustScaler, MinMaxScaler


def split_my_data(df, train_ratio=.8, seed=123):
    """Takes in a df and returns a test
       and train set
    """
    train, test = train_test_split(df, train_size=train_ratio, random_state=seed)
    return train, test


def standard_scaler(train, test):
    """z-scores, removes mean and scales to unit variance.
       Takes in a train and test set of data,
       creates and fits a scaler to the train set,
       returns the scaler, train_scaled, test_scaled
    """
    scaler = StandardScaler(copy=True, with_mean=True, with_std=True).fit(train)
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled =  pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled


def uniform_scaler(train, test):
    """Quantile transformer, non_linear transformation - uniform.
       Reduces the impact of outliers, smooths out unusual distributions.
       Takes in a train and test set of data,
       creates and fits a scaler to the train set,
       returns the scaler, train_scaled, test_scalexsd
    """
    scaler = QuantileTransformer(n_quantiles=100, output_distribution='uniform', random_state=123, copy=True).fit(train)
    uniform_train = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values]) 
    uniform_test = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled


def normal_scaler(train, test, seed=123):
    """Quantile transformer, non_linear transformation - normal
       Takes in a train and test set of data,
       creates and fits a scaler to the train set,
       returns the scaler, train_scaled, test_scaled
    """
    scaler = QuantileTransformer(n_quantiles=100, output_distribution='normal', random_state=seed, copy=True).fit(train)
    normal_train = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values]) 
    normal_test = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled


def scale_inverse(scaler, train_scaled, test_scaled):
    """Takes in the scaler and scaled train and test sets
       and returns the scaler and the train and test sets
       in their original forms before scaling
    """
    train = pd.DataFrame(scaler.inverse_transform(train_scaled), columns=train_scaled.columns.values).set_index([train_scaled.index.values])
    test = pd.DataFrame(scaler.inverse_transform(test_scaled), columns=test_scaled.columns.values).set_index([test_scaled.index.values])
    return train, test


def gaussian_scaler(train, test, method='yeo-johnson'):
    """Transforms and then normalizes data.
       Takes in a train and test set, 
       yeo_johnson allows for negative data,
       box_cox allows positive data only.
       Zero_mean, unit variance normalized train and test.
    """
    scaler = PowerTransformer(method, standardize=False, copy=True).fit(train)
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled

def min_max_scaler(train, test):
    """Transforms features by scaling each feature to a given range.
       Takes in train and test data and returns
       the scaler and train and test scaled within range.
       Sensitive to outliers.
    """
    scaler = MinMaxScaler(copy=True, feature_range=(0,1)).fit(train)
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled

def iqr_robust_scaler(train, test):
    """Scales features using stats that are robust to outliers
       by removing the median and scaling data to the IQR.
       Takes in train and test sets and returns
       the scaler and scaled train and test sets
    """
    scaler = RobustScaler(quantile_range=(25.0,75.0), copy=True, with_centering=True, with_scaling=True).fit(train)
    train_scaled = pd.DataFrame(scaler.transform(train), columns=train.columns.values).set_index([train.index.values])
    test_scaled = pd.DataFrame(scaler.transform(test), columns=test.columns.values).set_index([test.index.values])
    return scaler, train_scaled, test_scaled
