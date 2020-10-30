import requests

from scraper import Scraper
from house import House
from bs4 import BeautifulSoup

class RVL(Scraper):
    def getHouses(self) -> dict[House]:
        houses = {}

        html = requests.get('https://www.rvlmakelaars.nl/koopwoningen-utrecht?a=Utrecht&m=158000&e=329000&sb=latest').text

        soup = BeautifulSoup(html, 'html.parser')

        container = soup.find('div', {'class': 'homeBox'}).div

        for house_div in container.findChildren('div'):
            if not house_div.has_attr('data-object'):
                continue

            price = house_div.find('cite').string
            if '€' not in price:
                continue

            address_span = house_div.find('span', {'class': 'p-name'})

            house = House(
                address=address_span.string,
                link=house_div.a['href'],
                price=price
            )
            
            houses[house.address] = house

        return houses
