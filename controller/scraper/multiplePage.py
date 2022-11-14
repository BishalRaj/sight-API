import requests
from bs4 import BeautifulSoup

# https://www.etsy.com/uk/search?q=bohimian+bracelet&page=1&ref=pagination
# url = 'https://www.amazon.co.uk/s?k=dslr+camera&i=black-friday&ref=nb_sb_noss'


def getdata(url):
    r = requests.get(url).text
    # r.html.render(sleep=1)
    soup = BeautifulSoup(r, 'html.parser')
    data = soup.find('li', class_='wt-list-unstyled')
    # print(data)
    if data:
        return data


def getProductData(keyword: str):
    counter = 1
    while True:
        url = f'https://www.etsy.com/uk/search?q={keyword}&page={counter}&ref=pagination'
        data = getdata(url)
        # url = getnextpage(data)
        counter += 1
        if not url:
            break
        print(url)


# counter = 245
# while True:
#     url = f'https://www.etsy.com/uk/search?q=hello&page={counter}&ref=pagination'
#     data = getdata(url)
#     if not data:
#         break
#     print(url)
#     counter = counter + 1
