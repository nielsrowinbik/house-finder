from scrapers.domvast import Domvast
from scrapers.beumerutrecht import BeumerUtrecht
from scrapers.rvl import RVL
from scrapers.molenbeek import Molenbeek
from scrapers.makelaar1 import Makelaar1
from scrapers.lauteslager import Lauteslager
from scrapers.punt import Punt
from scrapers.debree import DeBree

from scrapers.realworks import createRealworksInstances, Realworks

if __name__ == "__main__":
    pass
    # print(createRealworksInstances())
    sources = [
        # Realworks(name="brecheisen", url="https://www.brecheisen.nl")
        DeBree()
    ]

    for source in sources:
        for house in source.getHouses():
            print(house.toMarkdown())