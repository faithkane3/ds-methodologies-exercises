import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,r2_score,explained_variance_score
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.linear_model import LinearRegression
from math import sqrt
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std

#import our scripts that do data science workflow
import env 
import wrangle
import split_scale
import evaluate
import features
import util


def modeling_function(x_train,x_test,y_train,y_test):
    predictions_train=pd.DataFrame({'actual':y_train.total_charges}).reset_index(drop=True)
    predictions_test=pd.DataFrame({'actual':y_test.total_charges}).reset_index(drop=True)
    #model 1
    lm1=LinearRegression()
    lm1.fit(x_train,y_train)
    lm1_predictions=lm1.predict(x_train)
    predictions_train['lm1']=lm1_predictions

    #model 2
    lm2=LinearRegression()
    lm2.fit(x_test,y_test)
    lm2_predictions=lm2.predict(x_test)
    predictions_test['lm2']=lm2_predictions
    
    return predictions_train, predictions_test


def plot_residuals(x, y):
    '''
    Plots the residuals of a model that uses x to predict y. Note that we don't
    need to make any predictions ourselves here, seaborn will create the model
    and predictions for us under the hood with the `residplot` function.
    '''
    return sns.residplot(x, y)


def plot_regression(x,y):
    res = sm.OLS(y, x).fit()
    prstd, iv_l, iv_u = wls_prediction_std(res)

    fig, ax = plt.subplots(figsize=(8,6))

    ax.plot(x, y, 'o', label="data")
    #ax.plot(x, y, 'b-', label="True")
    ax.plot(x, res.fittedvalues, 'r--.', label="OLS")
    ax.plot(x, iv_u, 'g--',label='97.5% Confidence Level')
    ax.plot(x, iv_l, 'b--',label='2.5% Confidence Level')
    ax.legend(loc='best');
    plt.show()

