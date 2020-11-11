import logging
import sqlite3
from pathlib import Path
from typing import List

from item import Item


class Database:
    def __init__(self, path: Path) -> None:
        self._path = path

    def create(self, exists_ok: bool = False) -> None:
        with sqlite3.connect(str(self._path)) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    'CREATE TABLE phonetic ('
                    '    id INTEGER PRIMARY KEY AUTOINCREMENT,'
                    '    word TEXT NOT NULL,'
                    '    br TEXT NOT NULL,'
                    '    am TEXT NOT NULL,'
                    '    source TEXT NOT NULL'
                    ');'
                )
            except sqlite3.OperationalError:
                if not exists_ok:
                    raise

    def insert(self, item: Item) -> None:
        with sqlite3.connect(str(self._path)) as connection:
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO phonetic VALUES (NULL, "{}", "{}", "{}", "{}")'.format(
                    item.word, item.br, item.am, item.source
                )
            )

    def get_all(self, word: str) -> List[Item]:
        logging.debug('Looking for word `%s` in the database', word)
        with sqlite3.connect(str(self._path)) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM phonetic WHERE word = "{}"'.format(word))
            ret = [Item(*it[1:]) for it in cursor.fetchall()]
            logging.debug('Found results: %s', ret)
            return ret
