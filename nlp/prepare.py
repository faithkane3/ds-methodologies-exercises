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

def basic_clean(string):
    string = string.lower()
    string = string.strip()
    string = unicodedata.normalize('NFKD', string)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    string = re.sub(r"[^a-z0-9'\s]", '', string)
    return string

def tokenize(string):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    return tokenizer.tokenize(string, return_str=True)

def stem(string):
    ps = nltk.PorterStemmer()
    stems = [ps.stem(word) for word in string.split()]
    string_of_stems = ' '.join(stems)
    return string_of_stems

def lemmatize(string):
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    string_of_lemmas = ' '.join(lemmas)
    return string_of_lemmas

def remove_stopwords(string, extra_words=[], exclude_words=[]):
    string = tokenize(string)
    
    words = string.split()
    stopword_list = stopwords.words('english')
    
    stopword_list = set(stopword_list) - set(exclude_words)
    
    stopword_list = stopword_list.union(set(extra_words))
    
    filtered_words = [w for w in words if w not in stopword_list]
    final_string = ' '.join(filtered_words)
    return final_string

def prep_articles(df):
    df = df.assign(original = df.title)
    df = df.assign(normalized = df.original.apply(normalize))
    df = df.assign(stemmed = df.normalized.apply(stem))
    df = df.assign(lemmatized = df.normalized.apply(lemmatize))
    df = df.assign(cleaned = df.stemmed.apply(remove_stopwords))
    df.drop(columns=["title"], inplace=True)
    return df

# def prep_articles(df):
#     df['original'] = df.body
#     df['stemmed'] = df.body.apply(basic_clean).apply(stem)
#     df['lemmatized'] = df.body.apply(basic_clean).apply(lemmatize)
#     df['clean'] = df.body.apply(basic_clean).apply(remove_stopwords)
#     df.drop(columns=['body'], inplace=True)
#     return df

def prep_blog_posts():
    df = acquire.get_blog_posts()
    return prep_articles(df)

def prep_news_articles():
    df = acquire.get_news_articles()
    return prep_articles(df)

def prep_corpus():
    blog_df = prep_blog_posts()
    blog_df["source"] = "Codeup Blog"

    news_df = prep_news_articles()
    news_df["source"] = "InShorts News"

    return blog_df, news_df

