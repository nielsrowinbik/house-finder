import requests
import json
import os

from scraper import Scraper
from house import House
from bs4 import BeautifulSoup

class Domvast(Scraper):
    def getHouses(self) -> dict[House]:
        houses = {}

        soup = BeautifulSoup(self.getHTML(), 'html.parser')

        objects = soup.findAll('div', {'class': 'object'})

        for house_object in objects:
            address = house_object.find('span', {'class', 'adres'})
            city = house_object.find('span', {'class', 'plaatsnaam'})
            link = house_object.find('a', {'class', 'adreslink'})
            price = house_object.find('span', {'class', 'element_prijs2'})
            image = house_object.find('img', {'class', 'img-responsive'})
            
            size = house_object.find(text='Gebruiksoppervlak wonen')

            if size is not None:
                size = size.parent.findNext('div').string

            status = house_object.find('div', {'class', 'status'})

            # Only has status if has bid or is sold
            if status is not None:
                continue

            if city is None or city.string.strip() != 'Utrecht':
                continue

            if price is not None:
                price = price.string

            if image is not None:
                image = image['src']

            if link is not None:
                link = link['href']

            house = House(
                city=city.string,
                address=address.string,
                link=link,
                price=price,
                image=image,
                size=size
            )

            houses[house.address] = house

        return houses
    
    def getIDs(self) -> list[str]:
        min = os.getenv('PRICE_MIN')
        max = os.getenv('PRICE_MAX')

        url = 'https://www.domvast.nl/huizen/smartselect.aspx'
        data = {
            'sorteer': 'Desc~Datum,Asc~Prijs',
            'prijs': str(min) + ',' + str(max),
            'prefilter': 'Koopaanbod',
            'pagenum': '0',
            'pagerows': '1000',
        }

        response = requests.post(url, data = data)
        result = json.loads(response.text)

        return result['AllMatches']

    def getHTML(self) -> str:
        url = 'https://www.domvast.nl/huizen/smartelement.aspx'
        data = {
            'id': ','.join(self.getIDs())
        }

        response = requests.post(url, data = data)
        
        return response.text