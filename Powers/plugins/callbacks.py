import os
import re
import time
from platform import python_version

from pyrogram import __version__
from pyrogram.types import CallbackQuery

from Powers import LOGGER
from Powers.config import NO_RES_PIC, SEARCH_PIC
from Powers.database.auto_del_mess import auto_del_insert
from Powers.functions import *
from Powers.streamer import DENDENMUSHI
from Powers.utils import *

from . import *


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
        await q.answer("Choose the quality given below this button", True)
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
        await q.edit_message_caption("Ping...")
        kb = await help_menu_kb()
        owner = await c.get_users(OWNER_ID)
        peers = PEERS().count_peers()
        speed = time.time() - start_time

        txt = f"""
Bot Status:
My Owner: {('@'+owner.username) if owner.username else owner.mention}
Total number of peers: {sum(peers)}
   ╚ Total number of users: {peers[0]}
   ╚ Total number of chats: {peers[1]}
Ping: {speed * 1000:.3f}
Pyrogram version: {__version__}
Python version: {python_version()}
"""
        await q.edit_message_caption(txt, reply_markup=kb)
        return

    elif data == "get_sudo_help":
        is_auth = await is_authorized(None, None, q)
        if not is_auth:
            await q.answer("You are not in my authorized users")
            return
        kb = await help_menu_kb()
        txt = dev_msg
        await q.edit_message_caption(txt, reply_markup=kb)
        return

    
    elif bool(re.match(r"^(prev|next|PREV|NEXT):.*_-?\d+$", data)):
        splited = data.split(":", 1)
        query, page = splited[1].split("_", 1)
        query = await encode_decode(query, "decode")
        page = int(page)
        if bool(re.match(r"^(prev|next)", splited[0])):
            query = int(query)
            anime_found = get_anime_results(query, page)
            txt = anime_res_txt.format(q=query, p=page, tp=anime_found[1]["totalPage"])
            await q.answer("Genrating kb it might take few minutes...", True)
            kb = await get_search_res_kb(anime_found, page)
            await q.edit_message_caption(txt, reply_markup=kb)
            return
        else:
            ani_id = query
            last_EP = int(q.message.caption.split("\n")[-2].split(":")[-1].strip())
            kb = await genrate_ep_kb(ani_id, last_EP, page)
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
        to_del = True
        _id = anime
        name = _id 
        anime_info, picture = get_anime_info(name)

        if not anime_info:
            anime_info = "404: No information found"
            picture = NO_RES_PIC
            kb = None
        else:
            kb = await ani_info_kb(name)

        await q.message.delete()
        await c.send_photo(chat.id, picture, anime_info, reply_markup=kb)
        if to_del:
            os.remove(picture)
        return

    elif bool(re.search(r"^(sub|dub):.*", data)):
        to_do, page, epnumber = data.split("_")
        to_do, _id = to_do.split(":")
        if to_do == "sub":
            dub = False
        else:
            dub = True

        name = _id
        _id = get_anime_results(name, top=True)
        Name = _id.replace('-', ' ').capitalize()
        txt = f"Here is the download and streamable link of {Name} episode {epnumber}"
        links = get_download_stream_links(_id, epnumber, dub)
        kb = await genrate_stream_kb(name, page, links)

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
            txt = f"Here is the download and streamable link of {Name} episode {ep.rsplit('-',1)[1]}"
            page = int(q.message.caption.split("\n")
                       [-1].split(":")[-1].strip().split("/")[0].strip())
            is_dub = is_dub_available(_id, epnumber)
            if is_dub:
                kb = await sub_or_dub_kb(name, page, epnumber)
                txt = f"You want to get the download and streamable link of {Name} episode {ep.rsplit('-',1)[1]} in sub or dub?"
                await q.edit_message_caption(txt, reply_markup=kb)
                return
            links = get_download_stream_links(_id, epnumber)
            kb = await genrate_stream_kb(name, page, links)

            msg = await q.edit_message_caption(txt, reply_markup=kb)
            tim = str(get_del_time())
            auto_del_insert(tim, user.id, msg.id)
            return
        else:
            _id, page = ep.split("_", 1)
            name = get_anime_results(_id, top=True)
            total_ep = get_last_ep(name)
            await q.answer(f"Genrating ep kb it may take a while...", True)
            kb = await genrate_ep_kb(_id, total_ep, int(page))
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
            anime_info = "404: No information found"
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
        await q.message.reply_text(f"Here is your deep link you can share it to your friend\n`{link}`")
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
                await q.answer("No description found")
                return
            kb = await desc_back(_id)

            await q.edit_message_caption(f"{anime_description}...", reply_markup=kb)
            return

        elif _ == "char":
            characters = get_char_anime(name)
            if not characters:
                await q.answer("No characters found")
                return
            kb = await desc_back(_id, True)
            char = f"Here are the list of the characters in the anime {characters['anime_name']}:\n"
            char += "╭────────────────•\n"
            for i in range(1, len(characters)):
                char += f"╰➢{characters[i]['name']} `{characters[i]['role']}`\n"
            char += "╰────────────────•"

            await q.edit_message_caption(char, reply_markup=kb)
            return

        else:
            _id = get_anime_results(name, top = True)
            last_EP = get_last_ep(_id)
            kb = await genrate_ep_kb(name, last_EP)
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
        await q.answer("No callback data found for this query 🤔")
        return