from pyrogram import filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.types import Message

from Powers import LOGFILE, LOGGER
from Powers.streamer import DENDENMUSHI

from . import *


@DENDENMUSHI.on_message(filters.command("addsudo") & auth_users)
async def add_this_to_sudo(c: DENDENMUSHI, m: Message):
    if m.from_user.id != c.owner.id:
        await m.reply_text("You are not owner, are you?")
        return
    elif m.reply_to_message and not m.reply_to_message.from_user:
        await m.reply_text("Reply to an user to add him in my suddoer list")
        return

    sup = SUPPORTS()
    user = m.reply_to_message.from_user
    u_id = user.id
    sup.insert_support_user(u_id)
    await m.reply_text(f"Added {user.mention} to suddoers list")
    return


@DENDENMUSHI.on_message(filters.command("rmsudo") & auth_users)
async def remove_this_from_sudo(c: DENDENMUSHI, m: Message):
    if m.from_user.id != c.owner.id:
        await m.reply_text("You are not owner, are you?")
        return
    elif len(m.command) == 1:
        await m.reply_text("Give me an user to remove")
        return

    try:
        user = int(m.command[1])
    except ValueError:
        await m.reply_text("Give me user id which should be in numbers")

    sup = SUPPORTS()
    sup.delete_support_user(user)
    await m.reply_text(f"Removed {user} from suddoer's list")


@DENDENMUSHI.on_message(filters.command("addfsub") & auth_users)
async def add_this_to_fsub(c: DENDENMUSHI, m: Message):
    if len(m.command) == 1:
        await m.reply_text("Do /devcmd to see how to use this command")
        return

    if len(m.command) == 2:
        try:
            chat_id = int(m.command[1])
            f_type = "auto"
        except ValueError:
            await m.reply_text("Channel id should be integer")
            return

    else:
        try:
            chat_id = int(m.command[1])
            f_type = (
                m.command[2].lower()
                if m.command[2] in ["audo", "direct", "request"]
                else "auto"
            )
        except ValueError:
            await m.reply_text("Channel id should be integer")
            return

    if f_type == "auto":
        try:
            chat = await c.get_chat(chat_id)
            if chat.username:
                f_type = "direct"
            else:
                f_type = "request"
        except Exception as e:
            await m.reply_text(f"Make user I am admin in {chat_id}")
            LOGGER.error(e)
            return

    try:
        bot_status = (await c.get_chat_member(chat_id, c.me.id)).status
        if bot_status != CMS.ADMINISTRATOR:
            await m.reply_text(f"Make user I am admin in {chat_id}")
            return
    except Exception as e:
        await m.reply_text(f"Make user I am admin in {chat_id}")
        LOGGER.error(e)
        return

    fsub = FSUBS()
    fsub.inser_fsub(chat_id, f_type)

    await m.reply_text(f"Added {chat_id} to force subscribe with {f_type} type")
    return


@DENDENMUSHI.on_message(filters.command("rmfsub") & auth_users)
async def remove_dis_fsub(c: DENDENMUSHI, m: Message):
    if len(m.command) == 1:
        await m.reply_text("Do /devcmd to see how to use this command")
        return

    try:
        chat_id = int(m.command[1])
    except ValueError:
        await m.reply_text("Channel id should be integer")
        return

    FSUBS().remove_fsub(chat_id)

    await m.reply_text(f"Removed {chat_id} from force sub")


@DENDENMUSHI.on_message(filters.command("changetype") & auth_users)
async def change_fsub_type(c: DENDENMUSHI, m: Message):
    if len(m.command) < 3:
        await m.reply_text("Do /devcmd to see how to use this command")
        return

    try:
        chat_id = int(m.command[1])
        f_type = m.command[2].lower()
        if f_type not in ["request", "direct"]:
            await m.reply_text("New force sub type should be request or direct")
            return
    except ValueError:
        await m.reply_text("Channel id should be integer")
        return

    type_ = FSUBS().inser_fsub(chat_id)
    if type(type_) == bool:
        await m.reply_text("This chat is not in my force subscribe list")
        return

    if type_ == f_type:
        await m.reply_text(f"Chat join type is already {f_type}")
        return

    FSUBS().update_fsub_type(chat_id, f_type)

    await m.reply_text(f"Changed force sub type from {type_} to {f_type}")


@DENDENMUSHI.on_message(filters.command("getfsubs") & auth_users)
async def get_all_fsub_channels(c: DENDENMUSHI, m: Message):
    all_f_sub = FSUBS().get_fsubs()
    txt = "**All force subscribe channel are:**\n\n"
    for one in all_f_sub:
        chat_id = one["c_id"]
        try:
            chat = await c.get_chat(chat_id)
            txt += f"Chat name: {chat.title}:\n\tChat id: `{chat.id}`\n\tFsub type: {str(one['type']).capitalize()}\n\n"
        except:
            txt += f"Chat id: `{chat.id}`\n\tFsub type: {str(one['type']).capitalize()}\n\n"
    await m.reply_text(txt)


@DENDENMUSHI.on_message(filters.command("logs") & auth_users)
async def give_me_logs(c: DENDENMUSHI, m: Message):
    to_del = await m.reply_text("Genrating logs...")
    with open(LOGFILE) as f:
        raw = ((f.read()))[1]
    await m.reply_document(
        document=LOGFILE,
        quote=True,
    )
    await to_del.delete()
    return


@DENDENMUSHI.on_message(filters.command("gcast") & auth_users)
async def broadcast_this_message(c: DENDENMUSHI, m: Message):
    repl_to = m.reply_to_message
    if not repl_to:
        await m.reply_text("Reply to a message to broadcast it.")

    if len(m.command) == 1:
        tag = "-all"
    elif len(m.command) > 1:
        tag = m.command[1].lower()
        if tag not in ["-u", "-c", "-all"]:
            tag = "-all"

    if tag == "-all":
        peers = PEERS().get_peers()
        peer_type = "chats and users"
    elif tag == "-u":
        peers = PEERS().get_peers("user")
        peer_type = "users"
    else:
        peers = PEERS().get_peers("chat")
        peer_type = "chats"

    total_peers = len(peers)
    to_del = await m.reply_text(
        f"Broadcasting messages to all {peer_type} which means total of {total_peers} peers"
    )
    failed = 0
    for i in peers:
        try:
            await repl_to.forward(int(i["peer"]))
        except:
            failed += 1

    txt = f"Successfully broadcasted message to {total_peers-failed} peers\n"
    if failed:
        txt += f"Failed to broadcast message to {failed} peers. Reasons can be either they have blocked me or they are vainshed in the darkness of this world ;) (No longer available on telegram)"

    await to_del.delete()
    await m.reply_text(txt)
    return


@DENDENMUSHI.on_message(filters.command("stats") & auth_users)
async def what_is_the_curr_stats(c: DENDENMUSHI, m: Message):
    users, chats = PEERS().count_peers()

    txt = f"**Current numbers of users and chats in my database are:**\nChats: {chats}\nUsers: {users}"
    await m.reply_text(txt)
    return
