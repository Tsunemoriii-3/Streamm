from pyrogram import filters
from pyrogram.types import Message

from Powers.streamer import DENDENMUSHI

from . import *


@DENDENMUSHI.on_message(filters.command("start"))
@is_joined
async def am_I_alive(c: DENDENMUSHI, m: Message):
    if len(m.text.strip().split()) > 1:
        data = (m.text.split(None, 1)[1]).lower()
        if data.startswith("de:"):
            to_get = await encode_decode(data.split(":")[-1], "decode")
            splited = to_get.split(":", 1)
            if splited == "character":
                character_name = splited[1]
            else:
                anime_id = splited[1]
    txt = start_msg.format(mention=m.from_user.mention,
                           bot_name=c.me.full_name)
    kb = await start_kb_genrator()
    try:
        await m.reply_photo(START_PIC, caption=txt, reply_markup=kb)
    except Exception as e:
        LOGGER.error(e)
        LOGGER.error(format_exc())
    
    return


@DENDENMUSHI.on_message(filters.command("help"))
@is_joined
async def get_normal_user_help(c: DENDENMUSHI, m: Message):
    kb = await help_menu_kb("user")
    txt = help_msg.format(username=c.me.username)
    try:
        await m.reply_photo(START_PIC, caption=txt, reply_markup=kb)
    except Exception as e:
        LOGGER.error(e)
        LOGGER.error(format_exc())
    
    return


@DENDENMUSHI.on_message(filters.command(["devcmd", "devhelp"]) & auth_users)
async def get_dev_user_help(_, m: Message):
    kb = await help_menu_kb()
    txt = dev_msg
    try:
        await m.reply_photo(START_PIC, caption=txt, reply_markup=kb)
    except Exception as e:
        LOGGER.error(e)
        LOGGER.error(format_exc())
    
    return