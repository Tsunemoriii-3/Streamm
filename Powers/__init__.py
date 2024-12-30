import shutil
from datetime import datetime
from logging import (INFO, WARNING, FileHandler, StreamHandler, basicConfig,
                     getLogger)
from os import mkdir, path
from sys import stdout

from pyrogram import Client, __version__

from Powers.config import FSUB_CHANNEL, OWNER_ID, REQ_FSUB, SUDO

LOG_DATETIME = datetime.now().strftime("%d_%m_%Y-%H_%M_%S")
LOGDIR = f"{__name__}/logs"

# Make Logs directory if it does not exixts
if not path.isdir(LOGDIR):
    mkdir(LOGDIR)
else:
    shutil.rmtree(LOGDIR)
    mkdir(LOGDIR)

LOGFILE = f"{LOGDIR}/{__name__}_{LOG_DATETIME}_log.txt"

file_handler = FileHandler(filename=LOGFILE)
stdout_handler = StreamHandler(stdout)

basicConfig(
    format="%(asctime)s - [STREAMER] - %(levelname)s - %(message)s",
    level=INFO,
    handlers=[file_handler, stdout_handler],
)

getLogger("pyrogram").setLevel(WARNING)
LOGGER = getLogger(__name__)


from Powers.database.force_sub_db import FSUBS
from Powers.database.sudo_db import SUPPORTS


async def load_channels(c: Client):
    fsubss = FSUBS()
    for i in FSUB_CHANNEL:
        x = await c.get_chat(int(i))
        fsubss.inser_fsub(int(i), "direct", x.title)
    for i in REQ_FSUB:
        x = await c.get_chat(int(i))
        fsubss.inser_fsub(int(i), "request", x.title)


async def load_support_users():
    LOGGER.info("ADDING SUPPORT USERS")
    support = SUPPORTS()
    if not SUDO:
        LOGGER.info("No sudo user found")
        return
    txt = ""
    for i in SUDO:
        support.insert_support_user(int(i))
        txt += f"Added {i} authorized users\n"
    support.insert_support_user(OWNER_ID)
    LOGGER.info("ADDED OWNER")

    LOGGER.info(
        f"{txt}\nAdded total of {len(SUDO)} authorized users + 1 Owner")

    return
