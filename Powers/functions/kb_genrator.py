import re
from typing import List

from pyrogram import Client
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM

from Powers import LOGGER, order_cache
from Powers.database.force_sub_db import FSUB_LINK, FSUBS
from Powers.functions.caching import CACHE
from Powers.utils.en_de_crypt import encode_decode
from Powers.utils.strings import dev_msg

from .anime_func import *

res_kb = CACHE.search_res_kb
ep_kb = CACHE.ep_kb

async def iterate_dev_caption(page: int = 1):
    caption = dev_msg
    if len(caption) <= 1024:
        return caption, None

    else:
        lines = caption.splitlines(True)
        total = len(lines) // 10
        start = 10 * (page - 1)
        end = 10 * page

        new = ""

        if not start:
            for line in lines[start : end]:
                new += line
            kb = [
                [
                    IKB("Next page ▶️", f"dev_{page+1}")
                ]
            ]
        
        elif page == total:
            for line in lines[start:]:
                new += line
            kb = [
                [
                    IKB("◀️ Previous page", f"dev_{page-1}")
                ]
            ]
        else:
            for line in lines[start : end]:
                new += line
            kb = [
                [
                    IKB("Next page ▶️", f"dev_{page+1}"),
                    IKB("◀️ Previous page", f"dev_{page-1}")
                ]
            ]
        
        kb.append(
            [
                IKB("sᴇᴄʀᴇᴛ", "get_sudo_help"),
                IKB("ʜᴏᴍᴇ", "start_menu")
            ]
        )
        return new, IKM(kb)
        
async def orgainzed_kb(kbs: List[IKB], rows: int = 2) -> List[List[IKB]]:
    """
    kbs: List of inlinekeyboardbutton
    rows: How many rows you want default to 2
    """
    new_kb = [kbs[i: i + rows] for i in range(0, len(kbs), rows)]
    return new_kb


async def get_fsub_kb(c: Client, data: str = "start") -> List[IKM]:
    """
    data: Either base 64 of the file you want to give after joining the channels or just start if the user is starting the bot for first time
    """
    try:
        all_fsubs = FSUBS().get_fsubs()

        fsub_join_links = []

        if order_cache:
            x = 1
            for key, val in order_cache.items():
                if re.match(r"-?\d+", key):
                    channel = int(key)
                    if val["type"] == "request":
                        invite_link = await c.create_chat_invite_link(
                            channel, creates_join_request=True
                        )
                    else:
                        invite_link = await c.create_chat_invite_link(channel)
                    
                    kb_name = f"⚡️𝗝𝗼𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 {x}⚡️"
                    x += 1
                    if name := val.get("btn_name", False):
                        kb_name = name
                        x -= 1

                    fsub_join_links.append(
                        IKB(kb_name, url=invite_link.invite_link)
                    )
                else:
                    if val:
                        btn_name = val
                    else:
                        btn_name = f"⚡️𝗝𝗼𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 {x}⚡️"
                        x += 1
                        
                    fsub_join_links.append(
                        IKB(btn_name, url=key)
                    )

        else:
            for i, j in enumerate(all_fsubs):
                channel = int(j["c_id"])
                if j["type"] == "request":
                    invite_link = await c.create_chat_invite_link(
                        channel, creates_join_request=True
                    )
                else:
                    invite_link = await c.create_chat_invite_link(channel)
                
                kb_name = f"⚡️𝗝𝗼𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 {i+1}⚡️"
                if name := j.get("btn_name", False):
                    kb_name = name

                fsub_join_links.append(
                    IKB(kb_name, url=invite_link.invite_link)
                )

            all_links = FSUB_LINK().get_all()

            for i in all_links:
                if name:=i.get("btn_name", None):
                    btn_name = name
                else:
                    btn_name = "⚡️𝗝𝗼𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹⚡️"
                    
                fsub_join_links.append(
                    IKB(btn_name, url=i["link"])
                )

        if not fsub_join_links:
            return None

        orgainzed = await orgainzed_kb(fsub_join_links)
        orgainzed.append(
            [IKB(f">>> 𝗧𝗿𝘆 𝗔𝗴𝗮𝗶𝗻 <<<", url=f"t.me/{c.me.username}?start={data}")])

        return IKM(orgainzed)

    except Exception as e:
        LOGGER.error(e)
        LOGGER.error(format_exc())


async def start_kb_genrator():
    kb = [
        [
            IKB("Sonic Otakus", url="https://t.me/Sonic_Otakus")
        ],
        [
            IKB("Anime Flix", url="https://t.me/Anime_Flix_Pro")
        ],
        [
            IKB("ʙᴏᴛ sᴛᴀᴛᴜs", "bot_status"),
            IKB("ʜᴇʟᴘ", "get_help")

        ]
    ]
    return IKM(kb)


async def help_menu_kb(help: str = "user"):
    """
    help: `dev` or `user`
    """

    if help.lower() == "user":
        kb = [
            [
                IKB("ʜᴇʟᴘ", "get_help"),
                IKB("ʜᴏᴍᴇ", "start_menu")
            ]
        ]
    else:
        kb = [
            [
                IKB("sᴇᴄʀᴇᴛ", "get_sudo_help"),
                IKB("ʜᴏᴍᴇ", "start_menu")
            ]
        ]
    return IKM(kb)


async def char_description_back(character, back: bool = False):
    character = await encode_decode(character)
    if len(f"cinfo:{character}".encode("utf-8")) > 64:
        character = character
    if back:
        kb = [
            [
                IKB("ᴅᴇsᴄʀɪᴘᴛɪᴏɴ", f"cinfo:{character}")
            ],
            [
                IKB("ᴄʟᴏsᴇ", "close")
            ]
        ]
    else:
        kb = [
            [
                IKB("ʙᴀᴄᴋ", f"cdes:{character}")
            ],
            [
                IKB("ᴄʟᴏsᴇ", "close")
            ]
        ]

    return IKM(kb)


async def get_search_res_kb(kwargs, page: int = 1):
    kb = []
    total_page = kwargs[1]["totalPage"]

    query = kwargs[1].get("query")

    if query and res_kb.get(query) and res_kb[query].get(page):
        return res_kb[query][page]

    for i in range(1, len(kwargs)+1):
        anime_name = kwargs[i]["title"]
        if anime_name.endswith("(Dub)"):
            continue
        en_anime_id = get_anilist_id(anime_name)
        if not en_anime_id:
            continue
        kb.append([IKB(anime_name, f"aid:{en_anime_id}")])

    encoded_id = query
    if total_page == 1:
        kb.append(
            [
                IKB("❌ 𝗖𝗹𝗼𝘀𝗲 ❌", "close")
            ]
        )
    elif page == 1:
        kb.append(
            [
                IKB("❌ 𝗖𝗹𝗼𝘀𝗲 ❌", "close"),
                IKB("▶️ 𝗡𝗲𝘅𝘁 ▶️", f"next:{encoded_id}_{page+1}")
            ]
        )
    elif page == total_page:
        kb.append(
            [
                IKB("◀️ 𝗕𝗮𝗰𝗸 ◀️", f"prev:{encoded_id}_{page-1}"),
                IKB("❌ 𝗖𝗹𝗼𝘀𝗲 ❌", "close")
            ]
        )
    else:
        kb.append(
            [
                IKB("◀️ 𝗕𝗮𝗰𝗸 ◀️", f"prev:{encoded_id}_{page-1}"),
                IKB("❌ 𝗖𝗹𝗼𝘀𝗲 ❌", "close"),
                IKB("▶️ 𝗡𝗲𝘅𝘁 ▶️", f"next:{encoded_id}_{page+1}")
            ]
        )

    _kb = IKM(kb)

    if query and res_kb.get(query):
        res_kb[query][page] = _kb
    else:
        res_kb[query] = {page : _kb}

    return _kb


async def ani_info_kb(anime_id):
    anime_id = str(anime_id)
    if anime_id.strip().isnumeric():
        id_ = int(anime_id.strip())
    else:
        id_ = anime_id
        ts = f"episode:{id_}"
        size = len(ts.encode("utf-8"))
        if size > 64:
            id_ = anime_id
    kb = [
        [
            IKB("ᴄʜᴀʀᴀᴄᴛᴇʀs", f"char:{id_}"),
            IKB("ᴅᴇsᴄʀɪᴘᴛɪᴏɴ", f"des:{id_}")
        ],
        [
            IKB("𝗦𝘁𝗿𝗲𝗮𝗺 / 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 - 𝗘𝗽𝗶𝘀𝗼𝗱𝗲𝘀", f"episode:{id_}")
        ],
        [
            IKB("𝗦𝗵𝗮𝗿𝗲", f"deep:{id_}")
        ]
    ]

    return IKM(kb)


async def desc_back(anime, Des: bool = False):
    anime = str(anime)
    if anime.strip().isnumeric():
        en_query = int(anime.strip())
    else:
        en_query = await encode_decode(anime)
        size = len(f"ainfo:{en_query}".encode("utf-8"))
        if size > 64:
            en_query = anime
    
    if Des:
        return IKM([[IKB("ᴅᴇsᴄʀɪᴘᴛɪᴏɴ", f"des:{en_query}"), IKB("ʙᴀᴄᴋ", f"ainfo:{en_query}")]])
    else:
        return IKM([[IKB("ᴄʜᴀʀᴀᴄᴛᴇʀs", f"char:{en_query}"), IKB("ʙᴀᴄᴋ", f"ainfo:{en_query}")]])


async def genrate_ep_kb(anime_id, total_eps, curr_page=1):
    kb = []
    global ep_kb
    anime_id = str(anime_id)
    if ep_kb.get(anime_id, False) and ep_kb[anime_id].get(curr_page):
        return ep_kb[anime_id][curr_page]
    per_page = f"{int(total_eps) / 25}"
    int_part, float_part = str(per_page).split(".")
    total_page = int(int_part) + (1 if bool(float_part.strip("0")) else 0)
    if anime_id.strip().isnumeric():
        encoded_id = en_query = int(anime_id.strip())
    else:
        encoded_id = en_query = await encode_decode(anime_id)
        if len(f"PREV:{encoded_id}_{total_page}".encode("utf-8")) > 64:
            encoded_id = en_query = anime_id
    curr_page = max(1, min(curr_page, total_page))
    ep_start = (curr_page - 1) * 25 + 1
    offset = curr_page * 25
    if total_page <= curr_page:
        offset = total_eps

    for i in range(ep_start, offset + 1):
        ep_format = get_ep_fromat(anime_id, i)
        encoded = ep_format
        kb.append(IKB(f"{i}", f"ep:{encoded}"))
        
    rearranged = await orgainzed_kb(kb, 5)

    if total_page == 1:
        rearranged.extend(
            [
                [
                    IKB("ʙᴀᴄᴋ", f"ainfo:{en_query}"),
                    IKB("❌ 𝗖𝗹𝗼𝘀𝗲 ❌", "close"),
                ]
            ]
        )

    elif curr_page >= total_page:
        rearranged.extend(
            [

                [
                    IKB("◀️ 𝗕𝗮𝗰𝗸 ◀️", f"PREV:{encoded_id}_{curr_page-1}"),
                    IKB("▶️ 𝗡𝗲𝘅𝘁 ▶️", f"NEXT:{encoded_id}_{1}")
                ],
                [
                    IKB("◀️ 𝟱 𝗣𝗮𝗴𝗲", f"PREV:{encoded_id}_{curr_page-5}"),
                    IKB("𝟱 𝗣𝗮𝗴𝗲 ▶️", f"NEXT:{encoded_id}_{1}")
                ],
                [
                    IKB("◀️ 𝗙𝗶𝗿𝘀𝘁 𝗣𝗮𝗴𝗲", f"PREV:{encoded_id}_{1}"),
                ],
                [
                    IKB("ʙᴀᴄᴋ", f"ainfo:{en_query}"),
                    IKB("❌ 𝗖𝗹𝗼𝘀𝗲 ❌", "close"),
                ]
            ]
        )

    elif curr_page <= 1:
        rearranged.extend(
            [
                [
                    IKB("◀️ 𝗕𝗮𝗰𝗸 ◀️", f"PREV:{encoded_id}_{curr_page-1}"),
                    IKB("▶️ 𝗡𝗲𝘅𝘁 ▶️", f"NEXT:{encoded_id}_{2}")
                ],
                [
                    IKB("◀️ 𝟱 𝗣𝗮𝗴𝗲", f"PREV:{encoded_id}_{curr_page-5}"),
                    IKB("𝟱 𝗣𝗮𝗴𝗲 ▶️", f"NEXT:{encoded_id}_{curr_page+5}")
                ],
                [
                    IKB("𝗟𝗮𝘀𝘁 𝗣𝗮𝗴𝗲 ▶️", f"PREV:{encoded_id}_{total_page}"),
                ],
                [
                    IKB("ʙᴀᴄᴋ", f"ainfo:{en_query}"),
                    IKB("❌ 𝗖𝗹𝗼𝘀𝗲 ❌", "close"),
                ]
            ]
        )
        
    else:
        rearranged.extend(
            [
                [
                    IKB("◀️ 𝗕𝗮𝗰𝗸 ◀️", f"PREV:{encoded_id}_{curr_page-1}"),
                    IKB("▶️ 𝗡𝗲𝘅𝘁 ▶️", f"NEXT:{encoded_id}_{curr_page+1}")
                ],
                [
                    IKB("◀️ 𝟱 𝗣𝗮𝗴𝗲", f"PREV:{encoded_id}_{curr_page-5}"),
                    IKB("𝟱 𝗣𝗮𝗴𝗲 ▶️", f"NEXT:{encoded_id}_{curr_page+5}")
                ],
                [
                    IKB("◀️ 𝗙𝗶𝗿𝘀𝘁 𝗣𝗮𝗴𝗲", f"PREV:{encoded_id}_{1}"),
                    IKB("𝗟𝗮𝘀𝘁 𝗣𝗮𝗴𝗲 ▶️", f"NEXT:{encoded_id}_{total_page}"),
                ],
                [
                    IKB("ʙᴀᴄᴋ", f"ainfo:{en_query}"),
                    IKB("❌ 𝗖𝗹𝗼𝘀𝗲 ❌", "close"),
                ]
            ]
        )

    i_kb = IKM(rearranged)
    if ep_kb.get(anime_id):
        ep_kb[anime_id][curr_page] = i_kb
    else:
        ep_kb[anime_id] = {curr_page: i_kb}

    return i_kb


async def genrate_stream_kb(anime_id, page, kwargs):
    en_query = f"{anime_id}_{page}"
    kb = [
        [
            IKB("𝗦𝘁𝗿𝗲𝗮𝗺 - 𝗢𝗻𝗹𝗶𝗻𝗲 --->", url=kwargs["stream"]),
        ]
    ]
    if type(kwargs["download"]) == list:
        kb.append([IKB("👇 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 👇", "BELOW_DOWNLOAD")])
        to_append = []

        for i in kwargs["download"]:
            to_append.append(IKB(i["quality"], url=i["link"]))
        kb.append(to_append)
    else:
        kb.append([IKB("Download", url=kwargs["download"])])
    kb.append(
        [
            IKB("ʙᴀᴄᴋ", f"bep:{en_query}"),
        ]
    )
    return IKM(kb)

async def sub_or_dub_kb(anime_id, page, episode):
    kb = [
        [
            IKB("𝗦𝘂𝗯", f"sub:{anime_id}_{page}_{episode}"),
            IKB("𝗗𝘂𝗯", f"dub:{anime_id}_{page}_{episode}")
        ],
        [
            IKB("𝗦𝗵𝗮𝗿𝗲", f"deep:{anime_id}_{page}_{episode}")
        ],
        [
            IKB("ʙᴀᴄᴋ", f"bep:{anime_id}_{page}"),
        ]
    ]

    return IKM(kb)

async def genrate_top_anime_kb(collection):
    kb = []
    for i in range(1, len(collection)+1):
        data = collection[i]
        cb = f"ainfo:{data['id']}"
        kb.append([IKB(data["name"], cb)])
    kb.append([IKB("❌ 𝗖𝗹𝗼𝘀𝗲 ❌", "close")])

    return IKM(kb)
