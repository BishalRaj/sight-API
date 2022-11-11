from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook
import requests

wb = Workbook()


def fetch(state_name):
    try:
        headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,ne;q=0.8,hi;q=0.7",
        }
        source = requests.get(
            f'https://www.amazon.co.uk/{state_name}', headers).text
        soup = BeautifulSoup(source, 'html.parser')

        for state_data in soup.find_all('div', class_='map-list-item'):
            city = state_data.find('a', class_='ga-link')['data-city-item']
            city_link = state_data.find('a', class_='ga-link')['href']
            source_individual = requests.get(city_link, headers=headers).text
            soup_ind = BeautifulSoup(source_individual, 'html.parser')

            for city_data in soup_ind.find_all('div', class_='map-list-item'):
                title = city_data.find('span', class_='location-name').text
                address = city_data.find('div', class_='address').text
                title = title.split('®', 1)[0]
                address = address.split('Inside', 1)[0]
                address = address.replace('\n', "")
                splitted_address = address.rsplit(city.upper())
                address = address.replace(city.upper(), ', '+city.upper())
                street = splitted_address[0]
                state = state_name.upper()
                zip = splitted_address[-1].rsplit(state_name.upper())
                zip = zip[-1]
                zip = zip.replace(' ', "")

            # print(f'{counter} data fetched')

        return True
    except:
        return False
