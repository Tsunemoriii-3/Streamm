from os import getenv

API_ID = int(getenv("20628383"))
API_HASH = getenv("API_HASH", "65a242463b8af9ba7b3c41d8de9738d1")
BOT_TOKEN = getenv("BOT_TOKEN", "7066626001:AAHEUmbfZpVYceXZGQJ8QYJ9JR5l01ijOsY")
SUDO = [int(i.strip()) for i in getenv("SUDO", "962802323 1315219809 1355116689 7283633166 1432756163 1344569458 1446111611 682111519").strip().split()]
OWNER_ID = int(getenv("1446111611"))
FSUB_CHANNEL = [int(i.strip())
                for i in getenv("FSUB_CHANNEL", "-1002402726494").strip().split()]
REQ_FSUB = [int(i.strip()) for i in getenv("REQ_FSUB", "-1002467950579").strip().split()]
AUTO_DEL = int(getenv("AUTO_DEL_TIME", 1))
AUTO_DEL_IN = getenv("AUTO_DEL_IN", "minute").lower()
START_PIC = getenv(
    "START_PIC", "https://telegra.ph/file/a79055783ce7582d2cf3d.jpg")
DB_URI = "mongodb+srv://Gojo:gojoisdead@test.m08k4kx.mongodb.net/?retryWrites=true&w=majority"
SEARCH_PIC = "https://graph.org/file/860e085d839419cde11c3.jpg"
NO_RES_PIC = "https://graph.org/file/d9f1b036aee08147856f7.jpg"
TRENDING = "https://graph.org/file/e561785a117dbff500281.jpg"
