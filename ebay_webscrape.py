import re
from bs4 import BeautifulSoup
import requests
import unicodecsv as csv
import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess
#some more imports
from crochet import setup
      
#List of the video games to search on ebay
game_list=["Super Mario World 2 Yoshi's Island Super Nintendo"]

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
print(urls)

setup()

def run_spider(spiderName):
    module_name="first_scrapy.spiders.{}".format(spiderName)
    scrapy_var = import_module(module_name)   #do some dynamic import of selected spider   
    spiderObj=scrapy_var.mySpider()           #get mySpider-object from spider module
    crawler = CrawlerRunner(get_project_settings())   #from Scrapy docs
    crawler.crawl(spiderObj)    
# build a web crawler
# Create the Spider class
class Your_Spider(scrapy.Spider):
    name = "your_spider"
    # start_requests method
    def start_requests(self):
        urls = ['https://www.ebay.com/sch/i.html?_from=R40&_nkw=Super+Mario+World+2+Yoshi%27s+Island+Super+Nintendo&_in_kw=1&_ex_kw=&_sacat=0&LH_Sold=1&_udlo=&_udhi=&_samilow=&_samihi=&_sadis=15&_stpos=32308&_sargn=-1%26saslc%3D1&_salic=1&_sop=13&_dmd=1&_ipg=50&LH_Complete=1&_fosrp=1']
        for url in urls:
            yield scrapy.Request(url  = url,
                             callback = self.parse_1)
    # First parsing method
    def parse_1(self, response):
        # locate and extract a list of game links from the original url webpage 
        game_links = response.xpath('//h3[contains(@class,"lvtitle")]/a/@href')
        links_to_follow = game_links.extract()
        for url in links_to_follow:
            yield response.follow(url = url,
                                  callback = self.parse_2)
    # Second parsing method            
    def parse_2(self, response):
        product_title = response.xpath('//span[@id="vi-lkhdr-itmTitl"]/text()')
        product_title = product_title.extract_first().strip()
        return(product_title)
        
process = CrawlerProcess()
# Tell the process which spider to use
process.crawl(Your_Spider)
# Start the crawling process
process.start()

