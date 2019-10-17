import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.preprocessing import StandarScaler, MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_regresssion
import statsmodel.api as sm 

def select_kbest_freg(x, y, k):
    """Removes all but highest scoring features
    Takes:
          k - int: number of features
          x - df of features
          y - df of target
    Returns:
          list of column names of highest scoring features
    """
    f_selector = SelectKBest(f_regression, k).fit(x, y)
    f_support = f_selector.get_support()
    f_feature = x.loc[:,f_support].columns.tolist()
    return f_feature

def ols_backware_elimination(x, y):
    """Removes all but highest scoring features
    Takes:
          x - df of features
          y - df of target
    Returns:
          list of column names of highest scoring features
    """
    cols = list(x_train.columns)
    while (len(cols) > 0):
        p = []
        x_1 = x[cols]
        x_1 = sm.add_constant(x_1)
        model = sm.OLS(y, x_1).fit()
        p = model.pvalues
        pmax = max(p)
        feature_with_p_max = p.idxmax()
        if(pmax > 0.05):
            cols.remove(feature_with_p_max)
        else:
            break
    return cols 


def lasso_cs_coef(x, y):
    """
    
    """
    reg = LassoCV().fit(x, y)
    coef = pd.Series(reg.coef_, index = x.columns)
    imp_coef = coef.sort_values()
    plot = imp_coef.plot(kind = "barh")
    plt.show()
    return coef

    
def number_of_optimum_features(x_train, y_train, x_test, y_test):   
    """
    Takes:
          x_train: Pandas df
          y_train: Pandas df
          x_test: Pandas df
          y_test: Pandas df
    Returns:
          int: number of optimum features
    """ 
    number_of_features_list = np.arange(1, 3)
    high_score = 0
    number_of_features = 0
    score_list = []
    for n in range(len(number_of_features_list)):
        model = LinearRegression()
        rfe = RFE(model, number_of_features_list[n])
        x_train_rfe = rfe.fit_transform(x_train, y_train)
        x_test_rfe = rfe.transform(x_test)
        model.fit(x_train_rfe, y_train)
        score = model.score(x_test_rfe, y_test)
        score_list.append(score)
        if(score > high_score):
            high_Score = score
            number_of_features = number_of_features_list[n]
    return number_of_features