import requests

from scraper import Scraper
from house import House
from bs4 import BeautifulSoup

class Punt(Scraper):
    def __init__(self):
        self.url = 'https://puntmakelaars.nl'

    def getHouses(self) -> list[House]:
        houses = []

        html = requests.get(self.url + '/nl/aanbod/kantoor-utrecht/?q=&prijs=200000-250000&prijs=250000-300000&prijs=300000-350000').text

        soup = BeautifulSoup(html, 'html.parser')

        house_ul = soup.find('ul', class_='listHouses')
        house_lis = house_ul.find_all('li')

        for house_li in house_lis:
            if house_li.get('id') is not None:
                continue

            status_span = house_li.find('span', class_='houseOverviewStatus')
            if status_span is not None:
                status = house_li.find('span', class_='houseOverviewStatus').text.lower()

            if status_span is not None and ('verkocht' in status or 'onder bod' in status):
                continue

            address_span = house_li.find('span', {'class': 'houseOverviewStreet'})
            price_span = house_li.find('span', class_='houseOverviewPrice')

            link_a = house_li.find('a')

            houses.append(
                House(
                    address=address_span.string,
                    link=self.url + link_a['href'],
                    price=price_span.string.strip(),
                )
            )

        return houses