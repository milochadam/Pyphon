from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

DATABASE_PATH = PROJECT_ROOT.joinpath('database.db')

COLOR_CACHED = 'green'
COLOR_SCRAPED = 'yellow'
COLOR_NOT_FOUND = 'red'
