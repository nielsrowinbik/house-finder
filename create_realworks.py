import requests

from dotenv import load_dotenv
from bs4 import BeautifulSoup

from scrapers.realworks import createRealworksInstances

if __name__ == "__main__":
    load_dotenv()

    usr_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36'}

    def fetch_results():
        google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(
            'allinurl:aanbod/woningaanbod/UTRECHT',
            100,
            'nl'
        )
        response = requests.get(google_url, headers=usr_agent)
        response.raise_for_status()

        return response.text

    def parse_results(raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        result_block = soup.find_all('div', attrs={'class': 'g'})
        for result in result_block:
            link = result.find('a', href=True)
            title = result.find('h3')
            if link and title:
                yield link['href']

    existing = createRealworksInstances()
    existing = set(map(lambda instance: instance.url, existing))

    for result in parse_results(fetch_results()):
        split = None

        if '.nl' in result:
            split = '.nl'
        elif '.com' in result:
            split = '.com'

        if split is not None:
            url_part = result.split(split, 1)[0]
            url = url_part + split
            name = url_part.split('.')[-1]

            if url not in existing:
                with open('realworks_sites', 'a') as file:
                    file.write(name + ' ' + url)

    