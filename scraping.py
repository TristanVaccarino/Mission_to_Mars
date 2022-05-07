# ### Mission to Mars
# URL to Canvas page: https://courses.bootcampspot.com/courses/976/pages/10-dot-3-3-scrape-mars-data-the-news?module_item_id=358751


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# Main function
def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)
    
    #Create data dictionary to return
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres_data(browser),        
        "last_modified": dt.datetime.now()
    }

    # Close the browser
    browser.quit()
    return data

def mars_news(browser):   
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    # wait_time = seconds
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Error handling
    try:
        # Start scrapping
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):   
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Error Handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    # Error Handling
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        # df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
        
    except BaseException:
        return None

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html(classes="table table-striped table-dark")

# Deliverable 3: 
def hemispheres_data(browser):
     # Visit URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []

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

    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())