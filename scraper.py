from abc import ABC, abstractmethod
from house import House

class Scraper(ABC):
    @abstractmethod
    def getHouses(self) -> dict[House]:
        pass
