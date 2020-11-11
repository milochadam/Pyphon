import logging
from typing import Optional

import requests
from bs4 import BeautifulSoup
from item import Item

from scrapers.scraper import Scraper


class CambridgeScraper(Scraper):
    WEBSITE = "https://dictionary.cambridge.org/pl/dictionary/english/"

    def scrape(self, word: str) -> Optional[Item]:
        logging.debug("Scraping `%s` from cambridge dictionary", word)

        website = f'{self.WEBSITE}{word}'
        soup = BeautifulSoup(requests.get(website, headers=self.headers).text, 'lxml')

        try:
            br = soup.find('span', class_='uk dpron-i').find('span', class_='ipa dipa lpr-2 lpl-1').text
        except AttributeError:
            br = None

        try:
            am = soup.find('span', class_='us dpron-i').find('span', class_='ipa dipa lpr-2 lpl-1').text
        except AttributeError:
            am = None

        if br is None and am is None:
            return None

        am = am or br
        br = br = am

        return Item(word=word, br=br, am=am, source=website)
