from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd

def make_dictionary_from_article(url):
    headers = {'User-Agent': 'Codeup Bayes Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text)
    title = soup.title.get_text()
    body = soup.find('div', class_='mk-single-content').get_text()
    
    output = {}
    output['title'] = title
    output['body'] = body
    
    return output

def get_blog_articles():
    urls = ['https://codeup.com/codeups-data-science-career-accelerator-is-here/',
            'https://codeup.com/data-science-myths/',
            'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/',
            'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/',
            'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/']
    
    output = []
    
    for url in urls:
        output.append(make_dictionary_from_article(url))
        
    df = pd.DataFrame(output)
    df.to_csv('codeup_blog_posts.csv')
    
    return df


def get_article_text():
    # if we already have the data, read it locally

    filename = 'codeup_blog_posts.csv'

    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return get_blog_articles()

