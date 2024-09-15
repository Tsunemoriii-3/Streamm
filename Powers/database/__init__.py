import sys
from traceback import format_exc

from pymongo import MongoClient

from Powers import LOGGER, config

try:
    DB_CLIENT = MongoClient(config.DB_URI)
    DB_BASE = DB_CLIENT["ANIME-STREAMER"]
except Exception as e:
    LOGGER.info("Got an error while initiation the Mongo client")
    LOGGER.error(e)
    LOGGER.error(format_exc())
    sys.exit(1)
