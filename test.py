from scrapers.domvast import Domvast
from scrapers.beumerutrecht import BeumerUtrecht
from scrapers.rvl import RVL
from scrapers.vandoorn import VanDoorn
from scrapers.molenbeek import Molenbeek

if __name__ == "__main__":
    sources = [
        Molenbeek()
    ]

    for source in sources:
        for house in source.getHouses():
            print(str(house))