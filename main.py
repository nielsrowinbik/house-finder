
import time
import requests
import os
import json

from dotenv import load_dotenv
from tinydb import TinyDB, where

from scrapers.domvast import Domvast
from scrapers.beumerutrecht import BeumerUtrecht
from scrapers.rvl import RVL
from scrapers.vandoorn import VanDoorn
from scrapers.molenbeek import Molenbeek

def notify(message: str) -> bool:
    url = 'https://api.telegram.org/bot' + os.getenv('TELEGRAM_API_KEY') + '/sendMessage'
    data = {
        'chat_id': os.getenv('TELEGRAM_CHAT_ID'),
        'text': message,
        'parse_mode': 'MarkdownV2'
    }

    try:
        response = requests.post(url, data = data)
        result = json.loads(response.text)['ok']
    except Exception as e:
        print('Notify failed D:')
        print(e)

    if not result:
        print('Notify failed D:')
        print(response.text)

    return result

def loop():
    try:
        sources = [
            Domvast(),
            BeumerUtrecht(),
            RVL(),
            VanDoorn(),
            Molenbeek(),
        ]

        ip_response = requests.get('https://ifconfig.me')

        print('Searching the interwebs with IP: ' + ip_response.text)

        db = TinyDB('db.json')

        for source in sources:
            print('Searching in ' + source.__class__.__name__)

            new_houses = source.getHouses()

            if len(new_houses) == 0:
                print('No houses found :(')

            for address in new_houses:
                if db.contains(where('address') == address):
                    print('Found existing house: ' + address)
                else:
                    house = new_houses[address]

                    print('Found new house: ' + address)
                    db.insert({'address': address})
                    notify(house.toMarkdown())
    except Exception as e:
        print(e)

if __name__ == '__main__':
    load_dotenv()

    starttime = time.time()
    print('Started at: ', starttime)

    interval = 15.0 * 60.0
    print('Checking every ' + str(interval) + ' seconds')

    while True:
        loop()

        time.sleep(interval - ((time.time() - starttime) % interval))
