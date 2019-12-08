import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

import acquire

def normalize(string):
    return unicodedata.normalize('NFKD', string)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')

def remove_special_characters(string):
    return re.sub(r"[^a-z0-9'\s]", '', string)

def basic_clean(s):
    s = s.lower()
    s = s.strip()
    s= unicodedata.normalize('NFKD', s)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    s = re.sub(r"[^a-z0-9'\s]", '', s)
    return s

def tokenize(s):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    return tokenizer.tokenize(s, return_str=True)

def stem(s):
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in s.split()]
    string_of_stems = ' '.join(stems)
    return string_of_stems

def lemmatize(s):
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in s.split()]
    string_of_lemmas = ' '.join(lemmas)
    return string_of_lemmas

def remove_stopwords(s, extra_words=[], exclude_words=[]):
    s = tokenize(s)
    
    words = s.split()
    stopword_list = stopwords.words('english')
    
    stopword_list = set(stopword_list) - set(exclude_words)
    
    stopword_list = stopword_list.union(set(extra_words))
    
    filtered_words = [w for w in words if w not in stopword_list]
    final_string = ' '.join(filtered_words)
    return final_string

def prep_articles(df):
    df['original'] = df.body
    df['stemmed'] = df.body.apply(basic_clean).apply(stem)
    df['lemmatized'] = df.body.apply(basic_clean).apply(lemmatize)
    df['clean'] = df.body.apply(basic_clean).apply(remove_stopwords)
    df.drop(columns=['body'], inplace=True)
    return df

