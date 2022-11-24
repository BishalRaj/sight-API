from controller.dataHandler.etzy import saveItemData
import requests
from bs4 import BeautifulSoup
import logging
from schemas.item import itemsEntity
from config.db import conn
from controller.email import email
from schemas.tracking import trackingEntity, trackingsEntity


logger = logging.getLogger('ftpuploader')


def getdata(url):
    productData = []
    try:
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        hasData = soup.find('li', class_='wt-list-unstyled')
        if hasData:
            for data in soup.find_all('li', class_='wt-list-unstyled'):
                pid = data.find(
                    'div', class_='wt-height-full')['data-logger-id']
                name = data.find('h3', class_='v2-listing-card__title').text
                price = data.find('span', class_='currency-value').text
                productData.append(
                    {'pid': pid, 'name': name, 'price': price})
    except:
        None
    return productData

# Created data fetching for each product


def getProductData(keyword: str):
    counter = 1
    while True:
        url = f'https://www.etsy.com/uk/search?q={keyword}&page={counter}&ref=pagination'
        data = getdata(url)

        if not data:
            break
        else:
            counter += 1


def scrapeSingleProduct(url: str):
    singleProduct = []
    try:
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        hasData = soup.find('h1', class_='wt-break-word')
        if hasData:
            for data in soup.find_all('div', class_='body-wrap'):
                pid = data.find(
                    'div', class_='listing-page-image-carousel-component')['data-palette-listing-id']
                name = data.find('h1', class_='wt-break-word').text
                price = data.find('p', class_='wt-text-title-03').text
                review = data.find(
                    'h2', class_='wt-mr-xs-2 wt-text-body-03').text
                sales = ''
                for salesdata in data.find_all('span', class_='wt-text-caption'):
                    if "sales" in salesdata.text:
                        sales = salesdata.text
                        break
                rating = data.find("input", {"name": 'rating'}).get('value')
                img = data.find('img', class_='carousel-image')['src']
                singleProduct.append({'pid': pid, 'name': cleanData(name), 'price': cleanData(removeExtras(removeExtras(removeExtras(price, "+"), "Price:"), "£")), 'rating': cleanData(rating), 'sales': cleanData(removeChar(sales)),
                                      'review': cleanData(removeChar(review)), 'img': img, 'url': url})

    except Exception as e:
        logger.error(e)
    return singleProduct


def cleanData(data: str):
    data.replace("\n", "")
    data = data.strip()
    return data


def removeExtras(data: str, extra: str):
    data = data.replace(extra, "")
    return data


def removeChar(data: str):
    return ''.join(i for i in data if i.isdigit())


def automateTracking():
    # get all items
    # if fetched price is greater than saved price update item db and save in tracking
    itemDB = conn.sight.item

    ind = []
    items = itemsEntity(itemDB.find())
    counter = 1
    for item in items:
        print(f'fetching data number: {counter}')
        # ind.append(scrapeSingleProduct(item['url'])[0])
        newData = scrapeSingleProduct(item['url'])[0]

        # if scraped data == new data do nothing else alert user by sending email
        if (newData['price'] != item['price']):
            print('price changed')
            users = getUser(item['pid'])
            if users is not []:
                for user in users:
                    print(user)
                    subject = f"One of the product that you have been tracking has lowered the price. Please follow this link: {item['url']}"
                    email.sendEmail(user, "Price Update", subject)

                # save micro data such as price etc
                # scrapeSingleProduct(item['url'])[0]
        counter += 1
    return ind


def getUser(pid: str):
    trackingDB = conn.sight.tracker
    res = trackingsEntity(trackingDB.find({"pid": pid}))
    users = []
    for user in res:
        # print(user['username'])
        users.append(user['username'])
    return users
