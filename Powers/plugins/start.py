from pyrogram import filters
from pyrogram.types import Message
import os
from Powers.database.auto_del_mess import auto_del_insert

from Powers.config import NO_RES_PIC
from Powers.streamer import DENDENMUSHI

from . import *


@DENDENMUSHI.on_message(filters.command("start"))
@is_joined
async def am_I_alive(c: DENDENMUSHI, m: Message):
    if len(m.text.strip().split()) > 1:
        data = m.text.split(None, 1)[1]
        if data.startswith("de:"):
            to_get = await encode_decode(data.split(":")[-1], "decode")
            splited = to_get.split(":", 1)
            if splited == "character":
                character_name = splited[1]
            else:
                anime_id = splited[1]
        elif data.startswith("a_"):
            anime_data = data.split("_")
            if len(anime_data) == 2:
                _id = anime_data[1]
                try:
                    _id = name = int(_id)
                except:
                    _id = await encode_decode(_id, "decode")
                    name = _id
                anime_info, picture = get_anime_info(name)
                to_del = True
                if not anime_info:
                    anime_info = "404: No information found"
                    to_del = False
                    picture = NO_RES_PIC
                    kb = None
                else:
                    kb = await ani_info_kb(_id)

                await m.reply_photo(picture, caption=anime_info, reply_markup=kb)
                if to_del:
                    os.remove(picture)
                return
            else:
                _id, page, ep = anime_data[1], anime_data[2], anime_data[3]
                name = get_anime_results(_id, top=True)
                Name = name.replace('-', ' ').capitalize()
                is_dub = is_dub_available(name, ep)
                txt = f"𝚂𝚝𝚛𝚎𝚊𝚖𝚊𝚋𝚕𝚎 𝙰𝚗𝚍 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝙻𝚒𝚗𝚔 𝙶𝚎𝚗𝚎𝚛𝚊𝚝𝚎𝚍 𝚂𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢!!!\n\n𝙰𝚗𝚒𝚖𝚎 - {Name}\n\n𝙴𝚙𝚒𝚜𝚘𝚍𝚎 - {ep}"
                if is_dub:
                    kb = await sub_or_dub_kb(_id, page, ep)
                    txt = f"𝙳𝚘 𝚈𝚘𝚞 𝚆𝚊𝚗𝚝 𝚃𝚘 𝚂𝚝𝚛𝚎𝚊𝚖 / 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 | {Name} - 𝙴𝚙𝚒𝚜𝚘𝚍𝚎 {ep} 𝙸𝚗 𝗦𝘂𝗯 𝚘𝚛 𝗗𝘂𝗯??"
                    await m.reply_text(txt, reply_markup=kb)
                    return
                links = get_download_stream_links(name, ep)
                kb = await genrate_stream_kb(_id, page, links)

                msg = m.reply_text(txt, reply_markup=kb)
                tim = str(get_del_time())
                auto_del_insert(tim, m.from_user.id, msg.id)
                return
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
