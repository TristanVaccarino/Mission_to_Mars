#!/usr/bin/env python
# coding: utf-8

# ### Mission to Mars
# URL to Canvas page: https://courses.bootcampspot.com/courses/976/pages/10-dot-3-3-scrape-mars-data-the-news?module_item_id=358751

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd


# #### Set Executable path to the browser

# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# #### Set the URL to visti and instruct the Chrome browser session to visit it
# 
# `is_element_present_by_css(css_selector, wait_time=None)`
# Verify if the element is present in the current page by name, and wait the specified time in `wait_time`
# 
# Returns __True__ if the element is present and __False__ if is not present.

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
# wait_time = seconds
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# The following code would get all div tags with class = 'list_text', but we just want to get the latest one which is on top
#slide_elem = news_soup.find_all('div', class_='list_text')
#slide_elem


# In[5]:


# Start scrapping
slide_elem.find('div', class_='content_title')
slide_elem


# It looks like `.text` is just a property that calls `get_text()`. Therefore, calling `get_text()` without arguments is the same thing as `.text`. However, `get_text()` can also support various keyword arguments to change how it behaves (__separator__, __strip__, __types__). If you need more control over the result, then you need the functional form.

# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
# By simply using .text we get the same result
#news_title = slide_elem.find('div', class_='content_title').text
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images
# URL to Canvas page: https://courses.bootcampspot.com/courses/976/pages/10-dot-3-4-scrape-mars-data-featured-image?module_item_id=358753

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# URL to Canvas page: https://courses.bootcampspot.com/courses/976/pages/10-dot-3-5-scrape-mars-data-mars-facts?module_item_id=358756
# 
# ### Use Pandas `.read_html()` function
# It actually reads all HTML tables returning a list of them 
# Definition: https://pandas.pydata.org/docs/reference/api/pandas.read_html.html

# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[14]:


df.to_html(classes="table table-striped")


# ### It is importan to quit the browser session calling the browser `.quit()` function

# In[17]:


browser.quit()


# # Deliverable 1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# #### Set Executable path to the browser, we just closed before this segment.

# In[86]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[87]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[88]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Get all links
aLinks = browser.find_by_css('a.product-item img')

for i in range(len(aLinks)):
    dLinks = {}
    browser.find_by_css('a.product-item img')[i].click()
    fullImg = browser.links.find_by_text('Sample').first
    dLinks['img_url'] = fullImg['href']
    dLinks['title'] =  browser.find_by_css('h2.title').text
    
    # add to the list
    hemisphere_image_urls.append(dLinks)
     
    #we need to navigate back to the start page
    browser.back()

hemisphere_image_urls


# In[89]:


# Close browser
browser.quit()


# In[ ]:




