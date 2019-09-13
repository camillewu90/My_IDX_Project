import re
from bs4 import BeautifulSoup
import requests
import unicodecsv as csv
import pandas as pd
from datetime import datetime
from pytz import timezone
      
#List of the video games to search on ebay
game_list=["Super Mario World 2 Yoshi's Island Super Nintendo","EarthBound Super Nintendo"]

# create the urls leading to the search page for each game in game_list
def make_urls(games):
    # List of urls created
    urls = []
    for game in games:
        # In order for it to work the spaces need to be replaced with a +
        game=game.replace(" ", "+")
        if "'" in game:
            game=game.replace("'",'%27')
        # create eBay url that can be modified to search for a specific sold game on eBay
        url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw={0}&_in_kw=1&_ex_kw=&_sacat=0&LH_Sold=1&_udlo=&_udhi=&_samilow=&_samihi=&_sadis=15&_stpos=32308&_sargn=-1%26saslc%3D1&_salic=1&_sop=13&_dmd=1&_ipg=50&LH_Complete=1&_fosrp=1".format(game)
        # url and appends it to the urls list
        urls.append(url)
    # Returns the list of completed urls
    return urls

url_list=make_urls(game_list)
print(url_list)
# get all the game links from the first original search page
def getLinks(url_list):
        product_links=[]
        for url in url_list:
            # Downloads the eBay page for processing
            res = requests.get(url)
            # Raises an exception error if there's an error downloading the website
            res.raise_for_status()
            # Creates a BeautifulSoup object for HTML parsing
            soup = BeautifulSoup(res.text, 'html.parser')
            h3s=soup.find_all('h3',{'class':'lvtitle'})
            for h3 in h3s:
                product_link=h3.a.get("href")
                product_links.append(product_link)
        return product_links
product_links=getLinks(url_list)
print(product_links)
#Scrapes and store the url, name, and price of the first item result listed on eBay   
def ebay_scrape(product_links): 
    product_title=[]
    price_usd=[]
    condition=[]
    time_sold=[]
    for product_link in product_links:
            # Downloads the product page for processing
            res = requests.get(product_link)
            # Raises an exception error if there's an error downloading the website
            res.raise_for_status()
            # Creates a BeautifulSoup object for HTML parsing
            soup = BeautifulSoup(res.text, 'html.parser')
            try:
                title = soup.find('span',{'id':'vi-lkhdr-itmTitl'}).get_text()
            except:
                title='None'
            product_title.append(title)
            try:
                price = soup.find('span',{'class':'notranslate'}).get_text().strip('\n\t\t\t\t\t\t\t\t\t\tUS $')
            except:
                title='None'
            price_usd.append(price)
            try:
                condition_ind=soup.find('div',{'class':'u-flL condText'}).get_text()
            except:
                title='None'
            condition.append(condition_ind)
            try:
                date=soup.find('span',{'id':'bb_tlft'}).get_text().replace('\r\n\t\t\t','').replace('\n\n',' ')
            except:
                title='None'
            time_sold.append(date)
    return (product_title,price_usd,condition,time_sold)

product_title,price_usd,condition,time_sold=ebay_scrape(product_links)           
print(product_title)
print(price_usd)
print(condition)
print(time_sold)

product_dict={}
product_dict['product_link']=product_links
product_dict['product_title']=product_title
product_dict['price_usd']=price_usd
product_dict['condition']=condition
product_dict['time_sold']=time_sold

print(product_dict)
         
product_df=pd.DataFrame.from_dict(product_dict,'columns')

print(product_df)