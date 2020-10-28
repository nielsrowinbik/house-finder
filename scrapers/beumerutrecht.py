import requests
import json
import os
import re

from scraper import Scraper
from house import House

class BeumerUtrecht(Scraper):
    url = 'https://beumerutrecht.nl/woningen/'

    def getHouses(self) -> dict[House]:
        houses = {}

        response = requests.post(self.url, data=self.getPostData())

        data = json.loads(response.text)['maps']

        for entry in data:
            if entry['c'] == 'Beschikbaar':
                houses[entry['d']] = House(
                    city=entry['e'],
                    address=entry['d'],
                    link=self.url + entry['a'],
                    price=entry['g'],
                    image=None,
                    size='?'
                )

        return houses

    def getPostData(self):
        min = os.getenv('PRICE_MIN')
        max = os.getenv('PRICE_MAX')

        return {
            '__live': '1',
            '__templates[]': ['search', 'loop'],
            '__maps': 'all',
            'makelaar[]': ['beumermaarssen.nl', 'beumerutrecht.nl', 'beumervleutendemeern.nl', 'beumerwijkbijduurstede.nl'],
            'koophuur': 'koop',
            'plaats_postcode': 'Utrecht',
            'radiuscustom': '',
            'typewoning': '',
            'prijs': {
                'min': min, 
                'max': max,
            },
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