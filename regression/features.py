import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.preprocessing import StandarScaler, MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_regresssion
import statsmodel.api as sm 

def select_kbest_freg(x_train, y_train, k):
    """Removes all but highest scoring features
    Takes:
          k - int: number of features
          x_train - df of features
          y_train - df of target
    Returns:
          list of column names of highest scoring features
    """
    f_selector = SelectKBest(f_regression, k).fit(x_train, y_train)
    f_support = f_selector.get_support()
    f_feature = x_train.loc[:,f_support].columns.tolist()
    return f_feature

def ols_backware_elimination(x_train, y_train):
    """

    """
    cols = list(x_train.columns)
    pmax = 1
    while (len(cols) > 0):
        p = []
        x_1 = x_train[cols]
        x_1 = sm.add_constant(x_1)
        model = sm.OLS(y_train, x_1).fit()
        p = pd.Series(model.pvalues.values[1:], index = cols)
        pmax = max(p)
        feature_with_p_max = p.idxmax()
        if(pmax > 0.05):
            cols.remove(feature_with_p_max)
        else:
            break
    return cols 


def lasso_cs_coef(x_train, y_train):
    """
    
    """
    reg = LassoCV().fit(x_train, y_train)
    coef = pd.Series(reg.coef_, index = x_train.columns)
    imp_coef = coef.sort_values()
    plot = imp_coef.plot(kind = "barh")
    return coef, plot

    
