from datetime import datetime
from traceback import format_exc

from pyrogram import Client
from pyrogram.errors.exceptions import MessageDeleteForbidden

from Powers.database.auto_del_mess import auto_del_delete, auto_del_get
from Powers.logger import LOGGER

# from info import AUTO_DEL

# from bot import app importing app gives err have to find alt

def till_date(date):
    try:
        form = "%Y-%m-%d %H:%M:%S.%f"
        z = datetime.strptime(date,form)
    except ValueError:
        date = date.rsplit(".",1)[0]
        form = "%Y-%m-%d %H:%M:%S"
        z = datetime.strptime(date,form)
    return z

"""
async def is_media_post(app: Client, chat, message_id, date):
    mess = message_id
    while True:
        try:
            UwU = await app.get_messages(chat, mess)
        except Exception:
            print("Exception in is_media_post line 22")
            break
        if UwU.empty:
            break
        if UwU.text and UwU.text.lower() != "No such file exist":
            break
        else:
            try:
                auto_del_delete(chat, mess)
                await app.delete_messages(chat, mess)
                mess += 1
            except Exception:
                mess += 1
                pass"""
            

async def auto_ddel_postss(app: Client):
    z = auto_del_get()
    for i in z:
        tim = till_date(i["datee"])
        if tim <= datetime.now():
            try:
                try:
                    await app.delete_messages(int(i["chat_id"]),int(i["mess_id"]))
                except MessageDeleteForbidden:
                    msg = await app.get_messages(int(i["chat_id"]), int(i["mess_id"]))
                    await msg.delete()
                LOGGER.info(f"Deleted message id {i['mess_id']} from chat {i['chat_id']}")
            except Exception as e:
                LOGGER.error(e)
                LOGGER.error(format_exc())
                pass
            
            # remove from db anyway
            LOGGER.info(f"Removed the entry from the db {i['mess_id']}, {i['chat_id']}")
            auto_del_delete(i["chat_id"], i["mess_id"])
