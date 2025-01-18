import os

from pyrogram import filters
from pyrogram.types import Message

from Powers.config import NO_RES_PIC
from Powers.database.auto_del_mess import auto_del_insert
from Powers.functions.caching import CACHE
from Powers.streamer import DENDENMUSHI

from . import *

u_pref = CACHE.user_pref

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
        elif data.startswith("d_"):
            to_del = await m.reply_text("𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁 . . .")
            splited = data.split("_",1)[1]
            decod = (await encode_decode(splited, "decode")).split("-episode-")
            temp = decod[0]
            is_dub = bool(temp.rsplit("-", 1) == "dub") 
            if is_dub:
                _id = temp.rsplit("-",1)[0]
            else:
                _id = temp
            ep = decod[-1]
            to_del = await to_del.edit_text("𝙵𝚎𝚝𝚌𝚑𝚒𝚗𝚐 𝙻𝚒𝚗𝚔𝚜...")
            links = get_download_stream_links(_id, ep, is_dub)
            to_del = await to_del.edit_text("𝙶𝚎𝚗𝚎𝚛𝚊𝚝𝚒𝚗𝚐 Buttons...")
            sdata = f"d_{get_ep_fromat(_id, ep, is_dub)}"
            kb = await genrate_stream_kb(None, None, links, sdata)
            txt = f"<b><i>» Streamable And Download Link Generated Successfully. \n\n» Anime - {_id.replace('-', ' ').capitalize()}\n\n» Episode - {ep}</i></b>"
            await to_del.delete()
            msg = await m.reply_text(txt, reply_markup=kb)
            tim = str(get_del_time())
            auto_del_insert(tim, m.from_user.id, msg.id)
            return
        elif data.startswith("p_"):
            anime_data = data.split("_")
            name, page = anime_data[1], anime_data[2]
            _id, img = get_anime_results(name, top = True, with_img=True)
            to_del = await m.reply_text("» 𝙶𝚎𝚗𝚎𝚛𝚊𝚝𝚒𝚗𝚐 𝙻𝚒𝚗𝚔𝚜, 𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁 . . .")
            last_EP = get_last_ep(_id)
            sdata = f"p_{name}_{page}"
            page = int(page)
            kb = await genrate_ep_kb(name, last_EP, page, sdata)
            int_part, float_part = str(last_EP / 25).split(".")
            total_page = int(int_part) + (1 if bool(float_part.strip("0")) else 0)
            page = f"1/{total_page}"
            txt = ep_txt.format(ep=last_EP, p=page)
            await to_del.delete()
            msg = await m.reply_photo(img, caption=txt, reply_markup=kb)
            tim = str(get_del_time())
            auto_del_insert(tim, m.from_user.id, msg.id)
            return
        elif data.startswith("a_"):
            global u_pref
            u_pref[m.from_user.id] = "ask"
            anime_data = data.split("_")
            if len(anime_data) == 2:
                _id = anime_data[1]
                try:
                    _id = name = int(_id)
                except:
                    _id = name = await encode_decode(_id, "decode")
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
                txt = f"<b><i>» Streamable And Download Link Generated Successfully. \n\n» Anime - {Name}\n\n» Episode - {ep}</i></b>"
                if is_dub:
                    kb = await sub_or_dub_kb(_id, page, ep)
                    txt = f"<b>» Do You Want To ▶️ Stream / Download ⬇️ | {Name} ─ Episode ─ {ep} In <u>𝗦𝘂𝗯</u> or <u>𝗗𝘂𝗯</u>?</b>"
                    await m.reply_text(txt, reply_markup=kb)
                    return
                links = get_download_stream_links(name, ep)
                formated = f"d_{get_ep_fromat(name, ep, is_dub)}"
                kb = await genrate_stream_kb(_id, page, links, formated)

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
    txt, kb = await iterate_dev_caption()
    try:
        await m.reply_photo(START_PIC, caption=txt, reply_markup=kb)
    except Exception as e:
        LOGGER.error(e)
        LOGGER.error(format_exc())

    return
