from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd

def make_dictionary_from_article(url):
    headers = {'User-Agent': 'Codeup Bayes Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title
    body = soup.find('div', class_='mk-single-content').get_text()
    return {
        'title': title,
        'body': body
    }

def get_blog_articles():
    urls = ['https://codeup.com/codeups-data-science-career-accelerator-is-here/',
            'https://codeup.com/data-science-myths/',
            'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/',
            'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/',
            'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/']
    output = []
    
    for url in urls:
        output.append(make_dictionary_from_article(url))
        
    return output

