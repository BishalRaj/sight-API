import requests
from bs4 import BeautifulSoup


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


def getSingleProduct(url: str):

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
                sales = data.find('span', class_='wt-text-caption').text
                rating = data.find("input", {"name": 'rating'}).get('value')
                img = data.find('img', class_='carousel-image')['src']
                singleProduct.append({'pid': pid, 'name': cleanData(name), 'price': cleanData(removeExtras(removeExtras(removeExtras(price, "+"), "Price:"), "£")), 'rating': cleanData(rating), 'sales': cleanData(removeExtras(sales, 'sales')),
                                      'review': cleanData(removeExtras(review, "reviews")), 'img': img})

    except:
        None
    return singleProduct


def cleanData(data: str):
    data.replace("\n", "")
    data = data.strip()
    return data


def removeExtras(data: str, extra: str):
    data = data.replace(extra, "")
    return data
