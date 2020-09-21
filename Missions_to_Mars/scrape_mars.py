# dependencies
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser

#  Mac Users - chromedriver path
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

### NASA Mars News ###

# URL of page to be scraped
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

browser.visit(url)

# retrieve article title
html = browser.html
soup = bs(html,'html.parser')

sections = soup.find('li', class_='slide')
container = sections.find('div', class_='image_and_description_container')
title_text = container.find('div', class_='list_text')
news_title = title_text.find('div', class_='content_title')
news_title =(news_title.text)
news_title

# retrieve description paragraph

html = browser.html
soup = bs(html,'html.parser')

sections = soup.find('li', class_='slide')
container = sections.find('div', class_='image_and_description_container')
title_text = container.find('div', class_='list_text')
news_p = title_text.find('div', class_='article_teaser_body')
news_p = news_p.text
news_p

### Image Scraping ###

# URL of featured image
jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(jpl_url)

# use splinter to click the button to bring up the full resolution image of the Featured Image
results = browser.find_by_id('full_image').first.click()

# scrape the new browser into soup and use soup to find the full resolution Featured Image
html = browser.html
soup = bs(html, "html.parser")
img_url = soup.find("img", class_="fancybox-image")["src"]
featured_image_url = 'http://jpl.nasa.gov' + img_url
featured_image_url

### Mars Facts ###

# visit facts page
facts_url = 'https://space-facts.com/mars/'
browser.visit(facts_url)

# scrape facts table using pandas
tables = pd.read_html(facts_url)
tables

facts_df = tables[0]

# convert table to html
html_table = facts_df.to_html()
html_table

# clean it up
html_table.replace('\n', '')

# save html string
facts_df.to_html('table.html')


### Mars Hemispheres ###

# visit USGS Astrogeology site
usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(usgs_url)
html = browser.html
soup = bs(html,'html.parser')

hemispheres = []
item = soup.find_all('div', class_='item')
for item in item:
    description = item.find('div', class_='description')
    image_title = (description.find('h3')).text
    partial_image_url = item.find('img', class_='thumb')['src']
    image_url = f'{usgs_url}{partial_image_url}'
    hemisphere_dict = {
        "title": image_title,
        "image_url": image_url
    }
    hemispheres.append(hemisphere_dict)
print(hemispheres)
