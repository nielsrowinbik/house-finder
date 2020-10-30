import requests

from scraper import Scraper
from house import House
from bs4 import BeautifulSoup

class VanDoorn(Scraper):
    def getHouses(self) -> dict[House]:
        url = 'https://www.van-doorn.nl'
        houses = {}

        html = requests.get(url + '/aanbod/woningaanbod/UTRECHT/150000-325000/koop/aantal-80/').text

        soup = BeautifulSoup(html, 'html.parser')

        for house_li in soup.findAll('li', {'class': 'aanbodEntry'}):
            if 'Verkocht' in house_li.find('span', {'class': 'objectstatusbanner'}).string:
                continue

            price_span = house_li.find('span', {'class': 'koopprijs'})
            size_span = house_li.find('span', {'class': 'woonoppervlakte'})

            house = House(
                address=house_li.find('h3', {'class': 'street-address'}).string,
                link=url + house_li.find('a', {'class': 'aanbodEntryLink'})['href'],
                price=price_span.find('span', {'class': 'kenmerkValue'}).string.strip(),
                size=size_span.find('span', {'class': 'kenmerkValue'}).string.strip(),
            )

            houses[house.address] = house

        return houses
