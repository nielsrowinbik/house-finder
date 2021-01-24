import requests
import re 

from scraper import Scraper
from house import House
from bs4 import BeautifulSoup

class Lauteslager(Scraper):
    def getHouses(self) -> list[House]:
        houses = []

        html = requests.get(self.getUrl(1)).text

        soup = BeautifulSoup(html, 'html.parser')

        page_select_div = soup.find('div', class_='pagination')

        last_page = 1

        if page_select_div is not None:
            for option in page_select_div.find_all('a'):
                if option.text != '':
                    last_page = option.text

        for page in range(1, int(last_page) + 1):
            html = requests.get(self.getUrl(page)).text

            soup = BeautifulSoup(html, 'html.parser')

            for house_div in soup.find_all('div', class_='offer-list-item'):
                status_div = house_div.find('div', class_='offer-status-flag')

                if status_div.text.strip() != 'Beschikbaar':
                    continue

                address_div = house_div.find('div', class_='item-data').h1
                link_div = house_div.find('div', class_='item-information')
                price_div = house_div.find('a', class_='primary-btn').span
                size_div = house_div.find('div', class_='specs').ul.li.span

                houses.append(
                    House(
                        address=address_div.text,
                        link=link_div.a['href'],
                        price=price_div.text,
                        size=size_div.text
                    )
                )

        return houses

    def getUrl(self, page):
        return 'https://www.lauteslager.nl/nl/aanbod/page/' + str(page) + '/?type=koop&plaats=utrecht&s&prijs_test[min]=150000&prijs_test[max]=350000&aantalKamers[0]&woonoppervlakte[0]' # TODO: Figure out a way to select correct range based on environment variables