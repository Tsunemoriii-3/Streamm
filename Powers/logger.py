import shutil
from datetime import datetime
from logging import (INFO, WARNING, FileHandler, StreamHandler, basicConfig,
                     getLogger, root)
from os import mkdir, path
from sys import stdout

name = __name__.split(".")[0] # name will be Powers.logger if we don't use split
LOGDIR = f"{name}/logs"

if not path.isdir(LOGDIR):
    mkdir(LOGDIR)
else:
    for handler in root.handlers[:]:
        if isinstance(handler, FileHandler):
            handler.close()
            root.removeHandler(handler)
    shutil.rmtree(LOGDIR)
    mkdir(LOGDIR)
    # pass

LOG_DATETIME = datetime.now().strftime("%d_%m_%Y-%H_%M_%S")
LOGFILE = f"{LOGDIR}/{name}_{LOG_DATETIME}_log.txt"

file_handler = FileHandler(filename=LOGFILE)
stdout_handler = StreamHandler(stdout)

basicConfig(
    format="%(asctime)s - [STREAMER] - %(levelname)s - %(message)s",
    level=INFO,
    handlers=[file_handler, stdout_handler],
)

getLogger("pyrogram").setLevel(WARNING)

LOGGER = getLogger(name)
