import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pydataset import data
import wrangle
import util

def split_my_data(x, y, train_size=.80, random_state=123):
    train_x, test_x, train_y, test_y = train_test_split(x, y, train_size, random_state)
    return pd.DataFrame(train_X), pd.DataFrame(test_x), pd.DataFrame(train_y), pd.DataFrame(test_y)

def split_my_data_whole(df, train_size=.80, random_state=123):
    train, test = train_test_split(df, train_size, random_state)
    return train, test

def standard_scaler(df):
    scaler_obj = StandardScaler(copy=True, with_mean=True, with_std=True).fit(df)
    return scaler_obj

def uniform_scaler(df):
    """Quantile transformer, non_linear transformation
    """
    scaler_obj = QuantileTransformer(n_quantiles=100, output_distribution='uniform', random_state=123, copy=True).fit(df)
    return scaler_obj

def apply_scaler(df, scaler_obj):
    scaled_df = pd.DataFrame(scaler_obj.transform(df))
    return scaled_df

def scale_inverse(scaled_df, scaler_obj):
    unscaled_df = pd.DataFrame(scaler_obj.inverse_transform(scaled_df), columns=scaled_df.columns.values).set_index([scaled_df.index.values])
    return unscaled_df

def gaussian_scaler(df):
    """Transforms and then normalizes data
    """
    scaler = PowerTransformer(method='yeo-johnson', standardize=False, copy=True).fit(df)
    return scaler_obj

def min_max_scaler(df):
    scaler = MinMaxScaler(copy=True, feature_range=(0,1)).fit(df)
    return scaler_obj

def iqr_robust_scaler(df):
    scaler = RobustScaler(quantile_range=(25.0,75.0), copy=True, with_centering=True, with_scaling=True).fit(df)
    return scaler_obj

