import requests
import json
import time

from scraper import Scraper
from house import House

class Molenbeek(Scraper):
    url = 'https://molenbeek.nl/api/properties/available.json?nocache=' + str(time.time())

    def getHouses(self) -> dict[House]:
        houses = {}

        response = requests.get(self.url)

        data = json.loads(response.text)['objects']

        for entry in data:
            if 'verkocht' in entry['availability_status'].lower():
                continue

            if entry['place'] != 'Utrecht':
                continue

            if (entry['buy_price'] == None) or not (150000 <= entry['buy_price'] < 325000):
                continue

            houses[entry['short_title']] = House(
                address=entry['short_title'],
                link=entry['url'],
                price='€ ' + str(entry['buy_price']),
                size=str(entry['usable_area_living_function']) + ' m²'
            )

        return houses