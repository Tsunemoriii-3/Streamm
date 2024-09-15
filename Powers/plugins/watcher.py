from pyrogram import filters
from pyrogram.types import ChatJoinRequest, ChatMemberUpdated

from Powers.database.pending_req_db import REQUESTED_USERS
from Powers.streamer import DENDENMUSHI


@DENDENMUSHI.on_chat_join_request(filters.channel | filters.group)
async def load_joinerr(_, cj: ChatJoinRequest):
    user = cj.from_user.id
    chat = cj.chat.id

    REQUESTED_USERS(chat).insert_pending_user(user)
    return


@DENDENMUSHI.on_chat_member_updated(filters.channel | filters.group)
async def remove_joinerr(_, u: ChatMemberUpdated):
    if not u.new_chat_member:
        return

    user = u.new_chat_member.user if u.new_chat_member else u.from_user
    chat = u.chat.id

    REQUESTED_USERS(chat).remove_pending_user(user.id)
    return
