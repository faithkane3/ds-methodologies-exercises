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


def plot_categorical_and_continuous_vars(df):
    """
    Takes:
          df
    Returns:
          three plots of categorical var with continuous var
    """
    plt.figure(figsize=(16,8))
    plt.subplot(1, 3, 1)
    plt.bar(df.tenure_years, df.total_charges)
    plt.xlabel("Tenure in years")
    plt.ylabel("Total charges in dollars")
    plt.subplot(1, 3, 2)
    sns.stripplot(df.tenure_years, df.total_charges)
    plt.subplot(1, 3, 3)
    plt.pie(df.groupby("tenure_years")["total_charges"].sum(), labels=list(df.tenure_years.unique()), autopct="%1.1f%%", shadow=True)
    plt.title("Percent of total charges by tenure")
    plt.show()