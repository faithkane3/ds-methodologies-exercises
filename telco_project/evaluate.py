import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
from statsmodels.formula.api import ols
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score
from sklearn.feature_selection import f_regression 
from math import sqrt
import matplotlib.pyplot as plt

def plot_residuals(x, y):
    """
    Takes: 
           x, vector or string
           y, vector or string
    Returns: 
           a residual plot of lin regression
           of y on x
    """
    return sns.residplot(x, y)


def regression_errors(y, yhat):
    """
    Takes: 
          target variable y, Pandas Series
          yhat, calculated regression Pandas Series
    Returns:
          SSE, ESS, TSS, MSE, RMSE
    """
    from math import sqrt
    SSE = ((yhat - y) ** 2).sum()
    MSE = SSE / len(y)
    ESS = sum((yhat - y.mean())**2)
    TSS = SSE + ESS
    RMSE = sqrt(MSE)
    return SSE, ESS, TSS, MSE, RMSE


def baseline_mean_errors(y):
    """
    Takes: 
          target variable y, Pandas Series
    Returns:
          SSE, MSE, RMSE for baseline values
    """
    from math import sqrt
    bSSE = ((y.mean() - y) ** 2).sum()
    bMSE = bSSE / len(y)
    bRMSE = sqrt(bMSE)
    return bSSE, bMSE, bRMSE


def better_than_baseline(y, yhat):
    """
    Takes: 
          y variable, Pandas Series
          yhat variable, Pandas Series
    Returns:
          boolean value evaluating statement
              - model performs better
              than baseline
    """
    SSE = ((yhat - y) ** 2).sum()
    bSSE = ((y.mean() - y) ** 2).sum()
    return SSE < bSSE


def model_significance(ols_model):
    """Takes:
             ols model
       Returns:
             R2
             p_value
    """
    p_value = ols_model.f_pvalue
    R2 = ols_model.rsquared
    return R2, p_value