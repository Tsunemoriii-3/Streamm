import sys
from traceback import format_exc

from pymongo import MongoClient

from Powers import config
from Powers.logger import LOGGER

try:
    DB_CLIENT = MongoClient(config.DB_URI)
    DB_BASE = DB_CLIENT["Anime-Flix-V2-test"]
except Exception as e:
    LOGGER.info("Got an error while initiation the Mongo client")
    LOGGER.error(e)
    LOGGER.error(format_exc())
    sys.exit(1)
