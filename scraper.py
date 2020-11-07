from abc import ABC, abstractmethod
from house import House

class Scraper(ABC):
    @abstractmethod
    def getHouses(self) -> list[House]:
        pass

    def getName(self):
        return self.__class__.__name__
