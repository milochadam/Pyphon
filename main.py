#!/usr/bin/env python3
import argparse
import logging
import sys
from dataclasses import dataclass, field
from typing import List

from database import Database
from scrapers.cambridge import CambridgeScraper
from settings import DATABASE_PATH


@dataclass
class PyphonArgs(argparse.Namespace):
    sentence: List[str] = field(default_factory=list)
    verbose: bool = False


def get_args() -> PyphonArgs:
    parser = argparse.ArgumentParser(description="Provide a sentence or just a word to get a transcription")
    parser.add_argument(
        "--sentence", "-s", type=str, nargs='+', help='A sentence to transcript',
    )
    parser.add_argument("--verbose", "-v", action='store_true', help='Vebose')
    return parser.parse_args(namespace=PyphonArgs())


def main() -> int:
    args = get_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
    db = Database(DATABASE_PATH)
    db.create(exists_ok=True)

    result = []
    logging.debug('Sentence: %s', args.sentence)
    for word in args.sentence:
        try:
            [candidate] = db.get_all(word)
            result.append(candidate.br)
        except ValueError:
            item = CambridgeScraper().scrape(word)
            if item is None:
                result.append(word)
            else:
                db.insert(item)
                result.append(item.br)
    logging.debug('Result: %s', result)

    print(' '.join(result))
    return 0


if __name__ == '__main__':
    sys.exit(main())