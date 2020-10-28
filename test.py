from scrapers.domvast import Domvast
from scrapers.beumerutrecht import BeumerUtrecht

if __name__ == "__main__":
    sources = [
        Domvast(),
        BeumerUtrecht(),
    ]

    for source in sources:
        for house in source.getHouses():
            print(str(house))