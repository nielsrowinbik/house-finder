import requests
import re

from scraper import Scraper
from house import House
from bs4 import BeautifulSoup

class Makelaar1(Scraper):
    url = 'https://www.makelaar1.nl/?minvraagprijs=150000&maxvraagprijs=325000&plaats=utrecht&keuze=zoeken&straalkm=10&typeobject=koop' # TODO: Figure out a way to select correct range based on environment variables

    def getHouses(self) -> list[House]:
        houses = []

        html = requests.get(self.url).text

        soup = BeautifulSoup(html, 'html.parser')

        page_select = soup.find('select', {'class': 'submitZoeken'})

        last_page = None
        for option in page_select.find_all('option'):
            last_page = option

        for page in range(1, int(last_page['value']) + 1):
            html = requests.get(self.url + '&page2=' + str(page)).text

            soup = BeautifulSoup(html, 'html.parser')

            for house_div in soup.find_all('div', class_='object'):
                status_div = house_div.find('div', class_='statusLabel')

                if status_div is not None: 
                    continue

                address_div = house_div.find('div', class_='objectKop')
                price_div = house_div.find('div', class_='objectPrice')
                link_div = house_div.find('div', class_='objectThumbs')
                size_div = house_div.find(text=re.compile('Woonopp.*'))

                houses.append(
                    House(
                        address=address_div.text,
                        link=link_div.a['href'],
                        price=price_div.text.strip(),
                        size=size_div[9:]
                    )
                )

        return houses
