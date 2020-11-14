#!/usr/bin/env python3
import argparse
import logging
import sys
from dataclasses import dataclass, field
from typing import List

from termcolor import colored

from database import Database
from scrapers.cambridge import CambridgeScraper
from settings import COLOR_CACHED, COLOR_NOT_FOUND, COLOR_SCRAPED, DATABASE_PATH


@dataclass
class PyphonArgs(argparse.Namespace):
    sentence: List[str] = field(default_factory=list)
    verbose: bool = False
    american: bool = False
    british: bool = False


def get_args() -> PyphonArgs:
    parser = argparse.ArgumentParser(description="Provide a sentence or just a word to get a transcription")
    parser.add_argument(
        "--sentence", "-s", type=str, nargs='+', help='A sentence to transcript',
    )
    parser.add_argument("--verbose", "-v", action='store_true', help='Vebose')
    parser.add_argument("--american", "-a", action='store_true', help='American pronunciation')
    parser.add_argument("--british", "-b", action='store_true', help='British pronunciation (default)')
    return parser.parse_args(namespace=PyphonArgs())


def main() -> int:
    args = get_args()

    if args.american and args.british:
        print('Flags -a and -b are mutually exclusive')
        return 1

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
    logging.debug("Instantiating a database in `%s`", DATABASE_PATH)
    db = Database(DATABASE_PATH)
    db.create(exists_ok=True)

    result = []
    logging.debug('Sentence: %s', args.sentence)
    for word in args.sentence:
        try:
            [candidate] = db.get_all(word)
            word_transcription = candidate.am if args.american else candidate.br
            result.append(colored(word_transcription, COLOR_CACHED))
        except ValueError:
            item = CambridgeScraper().scrape(word)
            if item is None:
                result.append(colored(word, COLOR_NOT_FOUND))
            else:
                db.insert(item)
                word_transcription = item.am if args.american else item.br
                result.append(colored(word_transcription, COLOR_SCRAPED))
    logging.debug('Result: %s', result)

    print(' '.join(result))
    return 0


if __name__ == '__main__':
    sys.exit(main())
