import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 
import numpy as np 


def plot_variable_pairs(df):
    """
    Takes:
          df
    Returns:
          PairGrid plot of all relationships
          with regression line
    """
    g=sns.PairGrid(df)
    g.map(sns.regplot)
    plt.show()


def months_to_years(df):
    """
    Takes:
          df
    Returns:
          df with new feature "tenure_years" as a category type
          calculating tenure in complete years
    """
    df["tenure_years"] = round(df.tenure // 12).astype("category")
    return df