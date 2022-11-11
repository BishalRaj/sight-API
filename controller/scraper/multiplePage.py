import requests
from bs4 import BeautifulSoup
import time


def getdata(query):
    source = requests.get('https://www.amazon.co.uk/s?k={query}')

    time.sleep(2)

    # soup = BeautifulSoup(source.html.html, 'html.parser')
    soup = BeautifulSoup(source, 'html.parser')
    return soup


def getnextpage(soup):
    # this will return the next page URL
    pages = soup.find('ul', {'class': 'a-pagination'})
    if not pages.find('li', {'class': 'a-disabled a-last'}):
        url = 'https://www.amazon.co.uk' + \
            str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
        return url
    else:
        return


def getAllData(query):
    while True:
        data = getdata(query)
        url = getnextpage(data)
        if not url:
            break
        print(url)
    return True
