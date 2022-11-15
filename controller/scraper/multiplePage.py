import requests
from bs4 import BeautifulSoup

# https://www.etsy.com/uk/search?q=bohimian+bracelet&page=1&ref=pagination
# url = 'https://www.amazon.co.uk/s?k=dslr+camera&i=black-friday&ref=nb_sb_noss'


def getdata(url):
    productData = []
    try:
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        hasData = soup.find('li', class_='wt-list-unstyled')
        if hasData:
            for data in soup.find_all('li', class_='wt-list-unstyled'):
                name = data.find('h3', class_='v2-listing-card__title').text
                price = data.find('span', class_='currency-value').text
                # star = data.find('div', class_='sprite-img')['aria-label']
                # print(star)
                productData.append({'name': name, 'price': price})
    except:
        None
    return productData


def getProductData(keyword: str):
    counter = 1
    while True:
        url = f'https://www.etsy.com/uk/search?q={keyword}&page={counter}&ref=pagination'
        data = getdata(url)
        print(f'-----------------------{counter}-----------------------------')
        # print(data)
        print(f'-----------------------{counter}-----------------------------')

        # url = getnextpage(data)

        if not data:
            break
        else:
            counter += 1
        # print(url)


def getProductByPage(soup):
    try:
        data = []
        for data in soup.find_all('li', class_='wt-list-unstyled'):
            name = data.find('h3', class_='v2-listing-card__title').text
            price = data.find('span', class_='currency-value').text
            # star = data.find('div', class_='sprite-img')['aria-label']
            print(name)
            print(price)
            # print(star)
            data.append({'name': name, 'price': price})

        return data
    except:
        return None
