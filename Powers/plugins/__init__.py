from datetime import datetime, timedelta
from traceback import format_exc

from Powers.config import AUTO_DEL, AUTO_DEL_IN, OWNER_ID, START_PIC
from Powers.functions import *
from Powers.utils import *


def get_del_time():
    now = datetime.now()
    if AUTO_DEL_IN.lower() == "minute":
        total = now + timedelta(minutes=AUTO_DEL)
    elif AUTO_DEL_IN.lower() == "second":
        total = now + timedelta(seconds=AUTO_DEL)
    else:
        total = now + timedelta(hours=AUTO_DEL)
    return total

def till_date(date):
    try:
        form = "%Y-%m-%d %H:%M:%S.%f"
        z = datetime.strptime(date,form)
    except ValueError:
        date = date.rsplit(".",1)[0]
        form = "%Y-%m-%d %H:%M:%S"
        z = datetime.strptime(date,form)
    return z