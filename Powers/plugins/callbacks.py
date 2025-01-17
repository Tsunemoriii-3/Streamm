import asyncio
import os
import re
import time
from platform import python_version

from pyrogram import __version__
from pyrogram.types import CallbackQuery

from Powers.config import NO_RES_PIC, SEARCH_PIC
from Powers.database.auto_del_mess import auto_del_insert
from Powers.functions import *
from Powers.streamer import DENDENMUSHI
from Powers.utils import *

from . import *
from .start import u_pref


@DENDENMUSHI.on_callback_query()
async def callback_handlers(c: DENDENMUSHI, q: CallbackQuery):
    data = q.data
    user = q.from_user
    chat = q.message.chat
    # await q.answer("Please wait working on the data recieved from callback...")
    if data == "close":
        await q.message.delete()
        return

    elif data == "BELOW_DOWNLOAD":
        await q.answer("» 𝙲𝚑𝚘𝚘𝚜𝚎 𝚈𝚘𝚞𝚛 𝙳𝚎𝚜𝚒𝚛𝚎𝚍 𝚀𝚞𝚊𝚕𝚒𝚝𝚢 𝙵𝚛𝚘𝚖 𝙱𝚎𝚕𝚘𝚠.", True)
        return

    elif data == "get_help":
        kb = await help_menu_kb("dev")
        await q.edit_message_caption(help_msg, reply_markup=kb)
        return

    elif data == "start_menu":
        txt = start_msg.format(mention=user.mention, bot_name=c.me.full_name)
        kb = await start_kb_genrator()
        await q.edit_message_caption(txt, reply_markup=kb)
        return

    elif data == "bot_status":
        start_time = time.time()
        await q.edit_message_caption("» 𝙵𝚎𝚝𝚌𝚑𝚒𝚗𝚐 𝙸𝚗𝚏𝚘...")
        kb = await help_menu_kb()
        owner = await c.get_users(OWNER_ID)
        peers = PEERS().count_peers()
        speed = time.time() - start_time

        txt = f"""
» ᴍʏ ᴏᴡɴᴇʀ - {('@'+owner.username) if owner.username else owner.mention}
» ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀ ᴏғ ᴜsᴇʀs ɪɴ ʙᴏᴛ: {sum(peers)}
   ╚ ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀ ᴏғ ᴜsᴇʀs: {peers[0]}
   ╚ ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀ ᴏғ ᴄʜᴀᴛs: {peers[1]}
» ᴘɪɴɢ: {speed * 1000:.3f}
» ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ: {__version__}
» ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ: {python_version()}
"""
        await q.edit_message_caption(txt, reply_markup=kb)
        return

    elif data == "get_sudo_help":
        is_auth = await is_authorized(None, None, q)
        if not is_auth:
            await q.answer("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ, ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ.")
            return
        txt, kb = await iterate_dev_caption()
        await q.edit_message_caption(txt, reply_markup=kb)
        return

    elif bool(re.match(r"^dev_.*[0-9]$", data)):
        page = data.split("_")[-1]
        
        txt, kb = await iterate_dev_caption(int(page))

        await q.edit_message_caption(txt, reply_markup=kb)
    
    elif bool(re.match(r"^(prev|next|PREV|NEXT):.*_-?\d+$", data)):
        splited = data.split(":", 1)
        query, page = splited[1].split("_", 1)
        query = await encode_decode(query, "decode")
        page = int(page)
        if bool(re.match(r"^(prev|next)", splited[0])):
            query = int(query)
            anime_found = get_anime_results(query, page)
            if anime_found == 429:
                await q.answer("» 𝚃𝚘𝚘 𝙼𝚊𝚗𝚢 𝚄𝚜𝚎𝚛𝚜 𝙰𝚛𝚎 𝚄𝚜𝚒𝚗𝚐 𝙼𝚎, 𝙿𝚕𝚎𝚊𝚜𝚎 𝚃𝚛𝚢 𝙰𝚐𝚊𝚒𝚗 𝙸𝚗 𝟻 𝙼𝚒𝚗𝚞𝚝𝚎𝚜.", True)
                return
            query = (q.message.text or q.message.caption).split("\n")[0].split(":")[-1].strip()
            txt = anime_res_txt.format(q=query, p=page, tp=anime_found[1]["totalPage"])
            await q.answer("» 𝙶𝚎𝚗𝚎𝚛𝚊𝚝𝚒𝚗𝚐 𝙻𝚒𝚗𝚔𝚜, 𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁...", True)
            kb = await get_search_res_kb(anime_found, page)
            await q.edit_message_caption(txt, reply_markup=kb)
            return
        else:
            ani_id = query
            await q.answer("» 𝙶𝚎𝚗𝚎𝚛𝚊𝚝𝚒𝚗𝚐 𝙻𝚒𝚗𝚔𝚜, 𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁 . . .", True)
            last_EP = int(q.message.caption.split("\n")[2].split("-")[-1].strip())
            sdata = f"p_{ani_id}_{page}"
            kb = await genrate_ep_kb(ani_id, last_EP, page, sdata)
            int_part, float_part = str(last_EP / 25).split(".")
            total_page = int(int_part) + \
                (1 if bool(float_part.strip("0")) > 0 else 0)

            page = max(1, min(page, total_page))
            page = f"{page}/{total_page}"
            txt = ep_txt.format(ep=last_EP, p=page)
            await q.edit_message_caption(txt, reply_markup=kb)
            return

    elif data.startswith("aid:"):
        _, anime = data.split(":", 1)
        await q.answer("» 𝙵𝚎𝚝𝚌𝚑𝚒𝚗𝚐 𝙸𝚗𝚏𝚘 𝙰𝚗𝚍 𝙶𝚎𝚗𝚎𝚛𝚊𝚝𝚒𝚗𝚐 𝙻𝚒𝚗𝚔𝚜, 𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁 . . .", True)
        to_del = True
        _id = anime
        name = _id 
        anime_info, picture = get_anime_info(name)

        if not anime_info:
            anime_info = "» 𝚃𝚘𝚘 𝙼𝚊𝚗𝚢 𝚄𝚜𝚎𝚛𝚜 𝙰𝚛𝚎 𝚄𝚜𝚒𝚗𝚐 𝙼𝚎, 𝙿𝚕𝚎𝚊𝚜𝚎 𝚃𝚛𝚢 𝙰𝚐𝚊𝚒𝚗 𝙸𝚗 𝟻 𝙼𝚒𝚗𝚞𝚝𝚎𝚜."
            picture = NO_RES_PIC
            to_del = False
            kb = None
        elif anime_info == 429:
            try:
                to_sleep = int(picture.headers["Retry-After"])
            except:
                to_sleep = 30
            await q.answer(f"ᴛᴏᴏ ᴍᴀɴʏ ʀᴇǫᴜᴇsᴛs: ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ғᴏʀ {to_sleep} sᴇᴄᴏɴᴅs")
            LOGGER.info(f"Too many requests: Please wait for {to_sleep} seconds")
            await asyncio.sleep(to_sleep)
            return
        else:
            kb = await ani_info_kb(name)

        await q.message.delete()
        await c.send_photo(chat.id, picture, anime_info, reply_markup=kb)
        if to_del:
            os.remove(picture)
        return

    elif bool(re.search(r"^(sub|dub):.*", data)):
        global u_pref
        to_do, page, epnumber = data.split("_")
        to_do, _id = to_do.split(":")
        u_pref[q.from_user.id] = to_do
        if to_do == "sub":
            dub = False
        else:
            dub = True

        name = _id
        _id = get_anime_results(name, top=True)
        Name = _id.replace('-', ' ').capitalize()
        txt = f"<b><i>» Streamable And Download Link Generated Successfully. \n\n» Anime - {Name}\n\n» Episode - {epnumber}</i></b>"
        links = get_download_stream_links(_id, epnumber, dub)
        formated = f"d_{get_ep_fromat(_id, epnumber, dub)}"
        kb = await genrate_stream_kb(name, page, links, formated)

        msg = await q.edit_message_caption(txt, reply_markup=kb)
        tim = str(get_del_time())
        auto_del_insert(tim, user.id, msg.id)
        return

    elif data.startswith(("ep:", "bep:")):
        _, episode = data.split(":", 1)
        ep = episode
        if _ == "ep":
            _id = name = ep.rsplit('-', 2)[0]
            epnumber = episode.rsplit("-",1)[-1]
            _id = get_anime_results(name, top=True)
            Name = _id.replace('-', ' ').capitalize()
            txt = f"<b><i>» Streamable And Download Link Generated Successfully. \n\n» Anime - {Name}\n\n» Episode - {ep.rsplit('-',1)[1]}</i></b>"
            page = int(q.message.caption.split("\n")
                       [-1].split("-")[-1].strip().split("/")[0].strip())
            pref = u_pref.get(q.from_user.id)
            if pref and pref in ["ask", "sub"]:
                is_dub = is_dub_available(_id, epnumber)
            else:
                is_dub = False
            if is_dub and pref == "ask":
                kb = await sub_or_dub_kb(name, page, epnumber)
                txt = f"</b>» Do You Want To ▶︎ Stream / Download 🢃 | {Name} ─ Episode ─ {ep.rsplit('-',1)[1]} In <u>𝗦𝘂𝗯</u> or <u>𝗗𝘂𝗯</u>?</b>"
                await q.edit_message_caption(txt, reply_markup=kb)
                return
            elif is_dub and pref == "sub":
                links = get_download_stream_links(_id, epnumber, True)
                formated = f"d_{get_ep_fromat(_id, epnumber, True)}"
                kb = await genrate_stream_kb(name, page, links, formated)
            else:
                links = get_download_stream_links(_id, epnumber)
                formated = f"d_{get_ep_fromat(_id, epnumber)}"
                kb = await genrate_stream_kb(name, page, links, formated)

            msg = await q.edit_message_caption(txt, reply_markup=kb)
            tim = str(get_del_time())
            auto_del_insert(tim, user.id, msg.id)
            return
        else:
            _id, page = ep.split("_", 1)
            name = get_anime_results(_id, top=True)
            total_ep = get_last_ep(name)
            await q.answer(f"» 𝙶𝚎𝚗𝚎𝚛𝚊𝚝𝚒𝚗𝚐 𝙻𝚒𝚗𝚔𝚜, 𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁 . . .", True)
            sdata = f"a_{name}_{page}"
            kb = await genrate_ep_kb(_id, total_ep, int(page), sdata)
            txt = ep_txt.format(ep=total_ep, p=page)

            await q.edit_message_caption(txt, reply_markup=kb)

    elif data.startswith("ainfo:"):
        _, en_id = data.split(":", 1)
        try:
            _id = name = int(en_id)
        except:
            _id = await encode_decode(en_id, "decode")
            name = _id
        anime_info, picture = get_anime_info(name)
        to_del = True
        if not anime_info:
            anime_info = "» 𝚃𝚘𝚘 𝙼𝚊𝚗𝚢 𝚄𝚜𝚎𝚛𝚜 𝙰𝚛𝚎 𝚄𝚜𝚒𝚗𝚐 𝙼𝚎, 𝙿𝚕𝚎𝚊𝚜𝚎 𝚃𝚛𝚢 𝙰𝚐𝚊𝚒𝚗 𝙸𝚗 𝟻 𝙼𝚒𝚗𝚞𝚝𝚎𝚜."
            to_del = False
            picture = NO_RES_PIC
            kb = None
        else:
            kb = await ani_info_kb(_id)

        await q.message.delete()
        await c.send_photo(chat.id, picture, anime_info, reply_markup=kb)
        if to_del:
            os.remove(picture)
        return

    elif data.startswith("deep:"):
        link = await genrate_deep_link(c, data.split(":")[-1])
        await q.answer("» 𝙶𝚎𝚗𝚎𝚛𝚊𝚝𝚒𝚗𝚐 𝚂𝚑𝚊𝚛𝚎𝚋𝚕𝚎 𝙻𝚒𝚗𝚔 𝙵𝚘𝚛 𝚈𝚘𝚞𝚛 𝙵𝚛𝚒𝚎𝚗𝚍𝚜, 𝙸𝚏 𝚈𝚘𝚞 𝙷𝚊𝚟𝚎 𝙰𝚗𝚢 . . .", True)
        await q.message.reply_text(f"» 𝗦𝗵𝗮𝗿𝗲𝗮𝗯𝗹𝗲 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱! \n\n𝗧𝗮𝗽 𝗧𝗼 𝗖𝗼𝗽𝘆 ─ `{link}`")
        return

    elif data.startswith(("des:", "episode:", "char:")):
        _, anime = data.split(":", 1)
        try:
            _id = name = int(anime)
        except:
            _id = name = anime
            name = _id
        if _ == "des":
            anime_description = get_anime_info(name, only_description=True)
            if not anime_description:
                await q.answer("» ❌ 𝗡𝗼 𝗗𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 𝗙𝗼𝘂𝗻𝗱!")
                return
            kb = await desc_back(_id)

            await q.edit_message_caption(f"<b><i>{anime_description} | @Sonic_Otakus</i></b>", reply_markup=kb)
            return

        elif _ == "char":
            characters = get_char_anime(name)
            if not characters:
                await q.answer("<b>»</b> ❌ 𝗡𝗼 𝗖𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿𝘀 𝗙𝗼𝘂𝗻𝗱!")
                return
            kb = await desc_back(_id, True)
            char = f"<b>»</b> List of Characters In Anime ─ <b>{characters['anime_name']}:\n\n</b>"
            for i in range(1, len(characters)):
                char += f"<b>» {characters[i]['name']} ─</b> `{characters[i]['role']}`\n"
            
            await q.edit_message_caption(char, reply_markup=kb)
            return

        else:
            _id = get_anime_results(name, top = True)
            await q.answer("» 𝙶𝚎𝚗𝚎𝚛𝚊𝚝𝚒𝚗𝚐 𝙻𝚒𝚗𝚔𝚜, 𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁 . . .", True)
            last_EP = get_last_ep(_id)
            if type(last_EP) == str:
                last_EP = int(q.message.caption.split("\n")[6].split("~")[-1].strip())
            sdata = f"p_{name}_1"
            kb = await genrate_ep_kb(name, last_EP, sdata=sdata)
            int_part, float_part = str(last_EP / 25).split(".")
            total_page = int(int_part) + (1 if bool(float_part.strip("0")) else 0)
            page = f"1/{total_page}"
            txt = ep_txt.format(ep=last_EP, p=page)
            await q.edit_message_caption(txt, reply_markup=kb)

    elif data.startswith(("cinfo:", "cdes:")):
        to_do, char = data.split(":", 1)

        if to_do == "cinfo":
            char = await encode_decode(char, "decode")
            txt = get_character_info(char, pic_required=False)
            kb = await char_description_back(char)
        else:
            char = await encode_decode(char, "decode")
            txt = get_character_info(char, True)
            txt = f"{txt}..."
            kb = await char_description_back(char, True)

        await q.edit_message_caption(txt, reply_markup=kb)
        return

    else:
        await q.answer("ɴᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ!!!")
        return
