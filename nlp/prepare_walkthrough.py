import pandas as pd
import numpy as np

import os
import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

from acquire_walkthrough import get_news_articles



def basic_clean(df, col):
    '''
    This function takes in a df and a string for a column and
    returns the df with a new column named 'basic_clean' with the
    passed column text normalized.
    '''
    df['basic_clean'] = df[col].str.lower()\
                    .str.replace(r"[^A-z0-9'\s]", '', regex=True)\
                    .str.normalize('NFKC')\
                    .str.encode('ascii', 'ignore')\
                    .str.decode('utf-8', 'ignore')
    return df


def tokenize(df, col):
    '''
    This function takes in a df and a string for a column and
    returns a df with a new column named 'clean_tokes' with the
    passed column text tokenized and in a list.
    '''
    tokenizer = nltk.tokenize.ToktokTokenizer()
    df['clean_tokes'] = df[col].apply(tokenizer.tokenize)
    return df


def stem(df, col):
    '''
    This function takes in a df and a string for a column name and
    returns a df with a new column named 'stemmed'.
    '''
    # Create porter stemmer
    ps = nltk.porter.PorterStemmer()
    
    # Create a Series of lists of stemmed words using our cleaned tokens
    stems = df[col].apply(lambda row: [ps.stem(word) for word in row])
    
    # Join our cleaned, stemmed lists of words back into strings of words/tokens
    df['stemmed'] = stems.str.join(' ')
    
    return df


def lemmatize(df, col):
    '''
    This function takes in a df and a string for column name and
    returns a the original df with a new column called 'lemmatized'.
    '''
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = df[col].apply(lambda row: [wnl.lemmatize(word) for word in row])
    df['lemmatized'] = lemmas.str.join(' ')
    return df


def remove_stopwords(df, col):
    '''
    This function takes in a df and a string for column name and 
    returns the df with a new column named 'clean' with stopwords removed.
    '''
    # Create stopword_list
    stopword_list = stopwords.words('english')
    
    # Split words in column
    words = df[col].str.split()
    
    # Check each words in each row of the column against stopword_list and return only those that are not
    filtered_words = words.apply(lambda row: [word for word in row if word not in stopword_list])
    
    # Create new column of words that have stopwords removed
    df['clean_' + col] = filtered_words.str.join(' ')
    
    return df


