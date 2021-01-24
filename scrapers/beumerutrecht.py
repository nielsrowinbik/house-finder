import requests
import json
import re

from scraper import Scraper
from house import House

class BeumerUtrecht(Scraper):
    url = 'https://beumerutrecht.nl/woningen/'

    def getHouses(self) -> list[House]:
        houses = []

        response = requests.post(self.url, data=self.getPostData())

        data = json.loads(response.text)['maps']

        for entry in data:
            if entry['c'] == 'Beschikbaar':

                houses.append(
                    House(
                        address=entry['d'],
                        link=self.url + entry['a'],
                        price=entry['g'].replace('&euro;', '€'),
                    )
                )

        return houses

    def getPostData(self):
        return {
            '__live': '1',
            '__templates[]': ['search', 'loop'],
            '__maps': 'all',
            'makelaar[]': ['beumermaarssen.nl', 'beumerutrecht.nl', 'beumervleutendemeern.nl', 'beumerwijkbijduurstede.nl'],
            'koophuur': 'koop',
            'plaats_postcode': 'Utrecht',
            'radiuscustom': '',
            'typewoning': '',
            'prijs[min]': '150000', # TODO: Figure out a way to select correct range based on environment variables
            'prijs[max]': '350000', # TODO: Figure out a way to select correct range based on environment variables
            'status[]': None,
            'woningsoort[]': None,
            'liggingen[]': None,
            'buitenruimtes[]': None,
            'bouwperiode[]': None,
            'energielabel[]': None,
            'voorzieningen[]': None,
            'openHuis[]': None,
            'nieuwAanbod[]': None,
            'woonOppervlakte': '',
            'perceelOppervlakte': '',
            'aantalKamers': '',
            'slaapkamers': '',
            'subscribe_email': '',
            'orderby': 'custom_order:asc,publicatiedatum:desc',
        }