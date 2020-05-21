import pandas as pd
import numpy as np
from requests import get
from bs4 import BeautifulSoup

def get_all_urls():
    '''
    This function scrapes all of the Codeup blog urls from
    the main Codeup blog page and returns a list of urls.
    '''
    # The main Codeup blog page with all the urls
    url = 'https://codeup.com/resources/#blog'
    
    headers = {'User-Agent': 'Codeup Bayes Data Science'} 
    
    # Send request to main page and get response
    response = get(url, headers=headers)
    
    # Create soup object using response
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Create empty list to hold the urls for all blogs
    urls = []
    
    # Create a list of the element tags that hold the href/links
    link_list = soup.find_all(class_="jet-listing-dynamic-link__link")
    
    # get the href/link from each element tag in my list
    for link in link_list:
        
        # Add the link to my urls list
        urls.append(link.get('href'))
        
    return urls


def get_blog_articles(urls):
    '''
    This function takes in a list of Codeup Blog urls and a dictionary headers 
    and scrapes the title and text for each url returning a list of dictionaries
    with the title and text for each blog.
    '''
    headers = {'User-Agent': 'Codeup Bayes Data Science'} 
    
    # Create an empty list to hold dictionaries
    articles = []
    
    # Loop through each url in our list of urls
    for url in urls:
        
        # get request to each url saved in response
        response = get(url, headers=headers)
        
        # Create soup object from response text and parse
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Save the title of each blog in variable title
        title = soup.find('h1', itemprop='headline' ).get_text()
        
        # Save the text in each blog to variable text
        text = soup.find('div', itemprop='text').get_text()
        
        # Create a dictionary holding the title and text for each blog
        article = {'title': title, 'content': text}
        
        # Add each dictionary to the articles list of dictionaries
        articles.append(article)
        
    return articles