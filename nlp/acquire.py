from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd

def get_blog_posts():
    filename = './codeup_blog_posts.csv'

    # check for presence of the file or make a new request
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return make_new_request()

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

def make_new_request():
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

# Function to get news articles

def get_news_articles():
    filename = 'inshorts_news_articles.csv'

    # check for presence of the file or make a new request
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return make_new_request()

def get_articles_from_topic(url):
    headers = {'user-agent': 'Codeup Bayes Instructor Example'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    output = []

    articles = soup.select(".news-card")

    for article in articles: 
        title = article.select("[itemprop='headline']")[0].get_text()
        body = article.select("[itemprop='articleBody']")[0].get_text()
        author = article.select(".author")[0].get_text()
        published_date = article.select(".time")[0]["content"]
        category = response.url.split("/")[-1]

        article_data = {
            'title': title,
            'body': body,
            'category': category,
            'author': author,
            'published_date': published_date,
        }
        output.append(article_data)


    return output


def make_new_request():
    urls = [
        "https://inshorts.com/en/read/business",
        "https://inshorts.com/en/read/sports",
        "https://inshorts.com/en/read/technology",
        "https://inshorts.com/en/read/entertainment"
    ]

    output = []
    
    for url in urls:
        # We use .extend in order to make a flat output list.
        output.extend(get_articles_from_topic(url))

    df = pd.DataFrame(output)
    df.to_csv('inshorts_news_articles.csv') 

    return df