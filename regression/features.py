import pandas as pd
import statsmodels.api as sm 
import matplotlib.pyplot as plt
from sklearn.linear_model import LassoCV, LinearRegression
from sklearn.feature_selection import RFE, SelectKBest, f_regression

def select_kbest_freg(x, y, k):
    """Removes all but highest scoring features
    Takes:
          k - int: number of features
          x - df of features
          y - df of target
    Returns:
          list of column names of highest scoring features
    """
    f_selector = SelectKBest(f_regression, k).fit(x, y).get_support()
    f_feature = x.loc[:,f_selector].columns.tolist()
    return f_feature

def ols_backware_elimination(x, y):
    """Removes all but highest scoring features
    Takes:
          x - df of features
          y - df of target
    Returns:
          list of column names of highest scoring features
    """
    cols = list(x.columns)

    while (len(cols) > 0):
      # create a new dataframe that we will use to train the model...each time we loop through it will 
      # remove the feature with the highest p-value IF that p-value is greater than 0.05.
      # if there are no p-values > 0.05, then it will only go through the loop one time. 
      x_1 = x[cols]
      # fit the Ordinary Least Squares Model
      model = sm.OLS(y, x_1).fit()
      # create a series of the pvalues with index as the feature names
      p = model.pvalues
      # get the max p-value
      pmax = max(p)
      # get the feature that has the max p-value
      feature_with_p_max = p.idxmax()
      # if the max p-value is >0.05, the remove the feature and go back to the start of the loop
      # else break the loop with the column names of all features with a p-value <= 0.05
      if(pmax > 0.05):
            cols.remove(feature_with_p_max)
      else:
            break
    return cols 


def lasso_cs_coef(x, y):
    """
    Takes:
          df of features
          df of target
    Returns:
          coefficients for each feature
          plots the features with their weights
    """
    reg = LassoCV().fit(x, y)
    coef = pd.Series(reg.coef_, index = x.columns)
    imp_coef = coef.sort_values()
    plot = imp_coef.plot(kind = "barh")
    plt.show()
    return coef

    
def optimal_number_of_features(x, y):   
    """
    Takes:
          x_train: Pandas df
          y_train: Pandas df
    Returns:
          int: number of optimum features
          score
    """ 
    features_range = range(1, len(x.columns)+1)
    high_score = 0
    number_of_features = 0
    for n in features_range:
        model = LinearRegression()
        train_rfe = RFE(model, n).fit_transform(x, y)
        model.fit(train_rfe, y)
        score = model.score(train_rfe, y)
        if(score > high_score):
            high_score = score
            number_of_features = n
    return number_of_features, score


def optimal_features(x_train, x_test, y_train, n):
      """
      Takes: 
      x_train: Pandas df
      x_test: Pandas df
      y_train: Pandas df
      n: the output of optimal_number_of_features

      uses that value to run recursive feature elimination
      finds the n best features

      Returns:
      selected_features_rfe, x_train_rfe, x_test_rfe
      """
      cols = list(x_train.columns)
      model = LinearRegression()

      #Initializing RFE model
      rfe = RFE(model, n)

      #Transforming data using RFE
      train_rfe = rfe.fit_transform(x_train,y_train)
      test_rfe = rfe.transform(x_test)

      #Fitting the data to model
      model.fit(train_rfe, y_train)
      temp = pd.Series(rfe.support_,index = cols)
      selected_features_rfe = temp[temp==True].index

      x_train_rfe = pd.DataFrame(train_rfe, columns=selected_features_rfe)
      x_test_rfe = pd.DataFrame(test_rfe, columns=selected_features_rfe)

      return selected_features_rfe, x_train_rfe, x_test_rfe