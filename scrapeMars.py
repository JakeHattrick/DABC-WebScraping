from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd


#!which chromedriver

def latestNews(browser,url):
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    firstSlide = soup.find("li",class_="slide")
    text = firstSlide.find("div",class_="list_text")
    newsTitle = text.find("div",class_='content_title').get_text()
    newsP = text.find("div",class_='article_teaser_body').get_text()
    return {"Title":newsTitle,"Content":newsP}

#url = 'https://mars.nasa.gov/news/'
#news = latestNews(url)
#print (news)

def featuredImg(browser,url):
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    featured = soup.find("article",class_='carousel_item')
    link = featured["style"].split("'")[1]
    featuredImgUrl = 'https://www.jpl.nasa.gov'+link
    return featuredImgUrl

#url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
#feat = featuredImg(url)
#print (feat)

def marsWeather(browser,url):
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    timeline = soup.find('div',class_='stream')
    latest = timeline.find('li')
    content = latest.find('div',class_='content')
    tweet = content.find('p','tweet-text').get_text()
    return tweet

#url = 'https://twitter.com/marswxreport?lang=en'
#tweet = marsWeather(url)
#print (tweet)

def marsFacts(browser,url):
    table = pd.read_html(url)[1]
    tableString = table.to_html()
    return tableString

#url = 'https://space-facts.com/mars/'
#facts = marsFacts(url)
#print(facts)

def hemisphere(browser,url):
    urlSearch = 'search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url+urlSearch)
    html = browser.html
    soup = bs(html,'html.parser')
    hemisphereImageUrls = []
    
    for result in soup.find_all('div',class_='item'):
        title = result.find('h3').get_text()
        #hemisphereImageUrls.append(title)\n",
        link = result.find('a')['href']
        #hemisphereImageUrls.append(link)\n",
        browser.visit(url+link)
        soup2 = bs(browser.html,'html.parser')
        downloads = soup2.find('div',class_='downloads')
        img = downloads.find('a')['href']
        browser.back()
        hemisphereImageUrls.append({'Title':title,"URL":img})

    return hemisphereImageUrls

#url = 'https://astrogeology.usgs.gov/'
#hemi = hemisphere(url)
#print(hemi)

def scrape():
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path)
    news = latestNews(browser,'https://mars.nasa.gov/news/')
    feat = featuredImg(browser,'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    tweet = marsWeather(browser,'https://twitter.com/marswxreport?lang=en')
    facts = marsFacts(browser,'https://space-facts.com/mars/')
    hemi = hemisphere(browser,'https://astrogeology.usgs.gov/')
    results = {
        "news_title": news[0],
        "news_paragraph": news[1],
        "featured_image": feat,
        "hemispheres": hemi,
        "weather": tweet,
        "facts": facts
    }
    browser.quit()
    return results

if __name__ == "__main__":
    print(scrape())
#print(scrape())