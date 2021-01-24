import requests

from scraper import Scraper
from house import House
from bs4 import BeautifulSoup

class DeBree(Scraper):
    def __init__(self):
        self.url = 'https://www.debreemakelaars.nl'

    def getHouses(self) -> list[House]:
        houses = []

        html = requests.get(self.url + '/aanbod').text

        soup = BeautifulSoup(html, 'html.parser')

        house_divs = soup.find_all('div', class_='grid3column')

        for house_div in house_divs:
            status = house_div.find('div', class_='notification-listing')
            
            if status is not None:
                status = status.text.lower()

            if status is not None and ('verkocht' in status or 'onder bod' in status or 'te huur' in status):
                continue

            address_div = house_div.find('div', class_='property-information-address')
            price_div = house_div.find('div', class_='property-information-price').a

            price = int(price_div.text.replace('€', '').replace(' ', '').replace('.', ''))

            if not (int(os.getenv('PRICE_MIN')) <= price <= int(os.getenv('PRICE_MAX'))):
                continue

            link_a = house_div.find('a')

            houses.append(
                House(
                    address=address_div.text.split(',')[0],
                    link=link_a['href'],
                    price=price_div.text,
                )
            )

        return houses