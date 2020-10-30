from scrapers.domvast import Domvast
from scrapers.beumerutrecht import BeumerUtrecht
from scrapers.rvl import RVL
from scrapers.vandoorn import VanDoorn

if __name__ == "__main__":
    sources = [
        VanDoorn()
    ]

    for source in sources:
        for house in source.getHouses():
            print(str(house))