from abc import ABC, abstractmethod

from item import Item


class Scraper(ABC):
    WEBSITE: str = NotImplemented
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'application/json',
        'Accept-Language': 'pl,en;q=0.5',
        'Referer': 'https://dictionary.cambridge.org/pl/dictionary/english/test',
        'AMP-Same-Origin': 'true',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    @abstractmethod
    def scrape(self, word: str) -> Item:
        return NotImplemented
