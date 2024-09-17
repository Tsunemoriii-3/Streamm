from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.enums import ChatType as CT
from pyrogram.types import CallbackQuery, Message

from Powers.config import OWNER_ID
from Powers.database.force_sub_db import FSUBS
from Powers.database.peer_db import PEERS
from Powers.database.pending_req_db import REQUESTED_USERS
from Powers.database.sudo_db import SUPPORTS
from Powers.functions.kb_genrator import *


async def is_authorized(_, __, data: Message or CallbackQuery):
    if data.from_user:
        authorized = SUPPORTS().is_support_user(data.from_user.id)
        is_owner = data.from_user.id == OWNER_ID
        return (authorized or is_owner)
    else:
        return False

async def not_commands(_, __, m: Message):
    if m.command:
        return False
    return True

def is_joined(func):
    async def force_subscriber(c: Client, m: Message):
        if not m.from_user:
            await m.reply_text("You are not user...")
            return
        is_auth = bool(SUPPORTS().is_support_user(m.from_user.id) or m.from_user.id == OWNER_ID)
        if is_auth:
            return await func(c, m)
        to_del = await m.reply_text("<b><i>» Checking User Profile - Please Wait...</i></b>")
        user_id = 0
        if m.from_user:
            user_id = m.from_user.id
            is_already = PEERS().insert_peer("user", user_id)
        chat_id = m.chat.id
        if chat_id != user_id:
            is_already = PEERS().insert_peer("chat", user_id)
        if m.chat.type == CT.PRIVATE:
            data = "start"
            if len(m.text.strip().split()) > 1:
                data = (m.text.split(None, 1)[1]).lower()
                if not data:
                    data = "start"
                else:
                    data = data

            user = m.from_user.id

            channels = FSUBS().get_fsubs()
            if not channels:
                await to_del.delete()
                return await func(c, m)
            f_join = False
            for i in channels:
                channel = int(i["c_id"])
                if i["type"] == "request":
                    try:
                        u_status = await c.get_chat_member(channel, user)
                        if u_status.status in [
                            CMS.ADMINISTRATOR,
                            CMS.MEMBER,
                            CMS.OWNER,
                        ]:
                            continue
                        else:
                            reqq = REQUESTED_USERS(
                                channel).get_pending_users(user)
                            if not reqq:
                                f_join = True
                                break
                    except Exception:
                        reqq = REQUESTED_USERS(channel).get_pending_users(user)
                        if not reqq:
                            f_join = True
                            break
                else:
                    try:
                        u_status = await c.get_chat_member(channel, user)
                        if u_status.status in [
                            CMS.ADMINISTRATOR,
                            CMS.MEMBER,
                            CMS.OWNER,
                        ]:
                            continue
                        else:
                            f_join = True
                            break
                    except Exception:
                        f_join = True
                        break

            if f_join:
                kb = await get_fsub_kb(c, data)
                await m.reply_text(
                    "<b><i>» You Must Join All The Channels First To Access Me.</i></b>",
                    reply_markup=kb,
                )
                await to_del.delete()
                return
            else:
                await to_del.delete()
                return await func(c, m)

        elif not is_already and m.chat.type != CT.PRIVATE:
            await m.reply_text(
                "<b><i>» Start Me In PM To Access My Features.</i></b>",
                reply_markup=IKM(
                    [
                        [
                            IKB(
                                "<b><i>» Start Me In PM To Access My Features.</i></b>",
                                url=f"t.me/{c.me.username}?start=start",
                            )
                        ]
                    ]
                ),
            )
            return

    return force_subscriber


no_cmd = filters.create(not_commands)
auth_users = filters.create(is_authorized)
