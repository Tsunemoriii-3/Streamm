import os

from pyrogram import filters
from pyrogram.types import Message

from Powers.config import NO_RES_PIC, SEARCH_PIC, TRENDING
from Powers.functions import *
from Powers.streamer import DENDENMUSHI
from Powers.utils import *


@DENDENMUSHI.on_message(filters.command("character"))
@is_joined
async def retrieve_char_info(_, m: Message):
    if len(m.command) <= 1:
        await m.reply_text("**USAGE**\n/character [name]\n**EXAMPLE:**\n/character luffy")
        return

    to_del = await m.reply_text("Searching for the character")
    character = m.text.split(None, 1)[1]
    txt, picture = get_character_info(character)
    if not txt:
        await to_del.delete()
        await m.reply_photo(NO_RES_PIC, caption=f"No character found with name {character}")
        return

    kb = await char_description_back(character)
    await to_del.delete()
    await m.reply_photo(picture, caption=txt, reply_markup=kb)
    os.remove(picture)
    return


@DENDENMUSHI.on_message(filters.command("anime") & filters.private)
@is_joined
async def retrieve_anime(_, m: Message):
    if len(m.command) <= 1:
        await m.reply_text("**USAGE:**\n/anime [name]\n**EXAMPLE:**\n/anime One piece")
        return

    to_del = await m.reply_text("Searching for the anime")
    query = m.text.split(None, 1)[1]
    results = get_anime_results(query)

    if not results:
        await to_del.delete()
        await m.reply_photo(NO_RES_PIC, caption=f"No matching anime found for the given query {query}")
        return

    total_pages = results[1]["totalPage"]

    txt = anime_res_txt(q=query, p=1, tp=total_pages)
    kb = await get_search_res_kb(results)
    await to_del.delete()
    await m.reply_photo(SEARCH_PIC, caption=txt, reply_markup=kb)
    return

@DENDENMUSHI.on_message(filters.command(["ongoing", "top"]) & filters.private)
@is_joined
async def retrieve_totire_anime(_, m: Message):
    if m.command[0] == "ongoing":
        results = get_trending_anime()
        txt = "Here are the top 10 ongoing anime"
    else:
        txt = "Here are all time top 10 anime"
        results = get_alltime_popular()

    kb = await genrate_top_anime_kb(results)

    await m.reply_photo(TRENDING, caption=txt, reply_markup=kb)
    return

@DENDENMUSHI.on_message(filters.text & filters.private & no_cmd & ~filters.outgoing, group = 100)
@is_joined
async def search_anime_for_me(_, m: Message):
    query = m.text
    to_del = await m.reply_text("Searching for the anime")

    try:
        results = get_anime_results(query)
    except:
        results = False

    if not results:
        await to_del.delete()
        await m.reply_photo(NO_RES_PIC, caption=f"No matching anime found for the given query {query}")
        return

    total_pages = results[1]["totalPage"]

    txt = anime_res_txt.format(q=query, p=1, tp=total_pages)
    to_del = await to_del.edit_text("Query found building the keyboard....")
    kb = await get_search_res_kb(results)

    await to_del.delete()
    await m.reply_photo(SEARCH_PIC, caption=txt, reply_markup=kb)
