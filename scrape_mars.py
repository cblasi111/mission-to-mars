# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
from time import sleep
import time 


def scrape():
    
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    mars_info = {}

    #Scrape mars news
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    mars_news_soup = BeautifulSoup(html, 'html.parser')

    # Scrape the first article title and teaser paragraph text; return them
    first_title = mars_news_soup.find('div', class_='content_title').text
    first_paragraph = mars_news_soup.find('div', class_='article_teaser_body').text
    

    #Scrape featured image
    image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url_featured)

    html_image = browser.html

    featured_image_soup = BeautifulSoup(html_image, 'html.parser')
    featured_img_url  = featured_image_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    main_url = 'https://www.jpl.nasa.gov'

    featured_image_url = main_url + featured_img_url
    print("This is the URL: " + featured_image_url)

    #Scrape twitter
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    tweet_soup = BeautifulSoup(html, 'html.parser')
    
    # Scrape the tweet info and return
    first_tweet = tweet_soup.find('p', class_='TweetTextSize').text
    
    #Scrape Mars facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[1]
    df.columns = ['Property', 'Value']
    # Set index to property in preparation for import into MongoDB
    df.set_index('Property', inplace=True)
    
    # Convert to HTML table string and return
    df_html = df.to_html()

    #Scrape the hemisphere information
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title}) 
        mars_hemisphere.append({"img_url": image_url})

    mars_info = {
        'news_title': first_title,
        'news_paragraph': first_paragraph,
        'featured_image_url': featured_image_url,
        'weather_tweet': first_tweet,
        'mars_facts': df_html,
        'hemisphere_urls': mars_hemisphere
    }    
    
    return mars_info

    browser.quit()

