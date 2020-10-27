
import time
import requests
import os
import json

from dotenv import load_dotenv

from scrapers.domvast import Domvast

def notify(message: str) -> bool:
    url = 'https://api.telegram.org/bot' + os.getenv('TELEGRAM_API_KEY') + '/sendMessage'
    data = {
        'chat_id': os.getenv('TELEGRAM_CHAT_ID'),
        'text': message,
        'parse_mode': 'MarkdownV2'
    }

    response = requests.post(url, data = data)
    result = json.loads(response.text)['ok']

    if not result:
        print('Notify failed D:')
        print(response.text)

    return result

if __name__ == '__main__':
    load_dotenv()

    houses = {}
    sources = [
        Domvast()
    ]

    starttime = time.time()
    print('Started at: ', starttime)

    interval = 15.0 * 60.0
    print('Checking every ' + str(interval) + ' seconds')

    while True:
        print('Checking now :D')

        for source in sources:
            new_houses = source.getHouses()

            for address in new_houses:
                if address not in houses:
                    print('Found new house: ' + address)
                    house = new_houses[address]
                    houses[address] = house
                    notify(house.toMarkdown())

        time.sleep(interval - ((time.time() - starttime) % interval))
