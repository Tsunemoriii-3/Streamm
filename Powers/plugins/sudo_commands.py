from pyrogram import filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.enums import MessageEntityType as MET
from pyrogram.types import Message

from Powers import LOGFILE, LOGGER
from Powers.database.force_sub_db import FSUB_LINK, FSUBS
from Powers.streamer import DENDENMUSHI

from . import *


@DENDENMUSHI.on_message(filters.command("addsudo") & auth_users)
async def add_this_to_sudo(c: DENDENMUSHI, m: Message):
    if m.from_user.id != c.owner.id:
        await m.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ, ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ.")
        return
    elif m.reply_to_message and not m.reply_to_message.from_user:
        await m.reply_text("Reply to an user to add him in my sudo list.")
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
        await m.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ, ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ.")
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
    await m.reply_text(f"Removed {user} from sudo list")


@DENDENMUSHI.on_message(filters.command("addfsub") & auth_users)
async def add_this_to_fsub(c: DENDENMUSHI, m: Message):
    if len(m.command) == 1:
        await m.reply_text("Do /devcmd to see how to use this command")
        return

    elif len(m.command) == 2:
        try:
            chat_id = int(m.command[1])
            f_type = "auto"
            btn_name = None
        except ValueError:
            await m.reply_text("Channel id should be integer")
            return

    elif len(m.command) == 3:
        try:
            chat_id = int(m.command[1])
            f_type = "auto"
            btn_name = m.text.split(None, 2)[-1]
            if name := btn_name.lower() in ["auto", "direct", "request"]:
                f_type = name
                btn_name = False
        except ValueError:
            await m.reply_text("Channel id should be integer")
            return
    else:
        try:
            chat_id = int(m.command[1])
            
            if type_:=m.command[2] in ["auto", "direct", "request"]:
                f_type = type_.lower()
                split_ = 3
            else:
                f_type = "auto"
                split_ = 2

            btn_name = m.text.split(None, split_)[-1]
        except ValueError:
            await m.reply_text("Channel id should be integer")
            return

    chat = None

    if not btn_name:
        try:
            chat = await c.get_chat(chat_id, False)
            btn_name = chat.title
        except Exception as e:
            await m.reply_text(f"Make user I am admin in {chat_id}")
            LOGGER.error(e)
            return

    if f_type == "auto":
        try:
            if not chat:
                chat = await c.get_chat(chat_id, False)
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
    fsub.inser_fsub(chat_id, f_type, btn_name)

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
    return

@DENDENMUSHI.on_message(filters.command("ufname") & auth_users)
async def change_cur_fbtn_name(_, m: Message):
    if len(m.command) in [1, 2]:
        await m.reply_text("Useage\n/ufname [channel id] [new btn name]")
        return
    
    try:
        _id = int(m.command[1])
        btn_ = m.text.split(None, 1)[-1]
    except ValueError:
        await m.reply_text("Channel id should be integer")
        return

    old = FSUBS().update_fsub_btn(_id, btn_)

    if not old.get("btn_name", False):
        btn = None
    else:
        btn = old['btn_name']
    if not old:
        await m.reply_text("No matching entry found with given channel id")
    await m.reply_text(f"Channged button name for channel id: {_id} from {btn} to {btn_}")

@DENDENMUSHI.on_message(filters.command("getfsubs") & auth_users)
async def get_all_fsub_channels(c: DENDENMUSHI, m: Message):
    all_f_sub = FSUBS().get_fsubs()
    txt = "**All force subscribe channel are:**\n\n"
    for one in all_f_sub:
        chat_id = one["c_id"]
        try:
            chat = await c.get_chat(chat_id)
            txt += f"Chat name: {chat.title}:\n\tChat id: `{chat.id}`\n\tFsub type: {str(one['type']).capitalize()}\n\tButton name: {one['btn_name'] if one.get('btn_name', None) else 'Not set'}\n\n"
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

async def validate_link_return(m: Message):
    msg_entitites = m.entities

    if not msg_entitites:
        return
    else:
        for entity in msg_entitites:
            if entity.type == MET.URL:
                return m.text[entity.offset : (entity.offset +  entity.length)]

    return

@DENDENMUSHI.on_message(filters.command("addlink") & auth_users)
async def insert_this_link(_, m: Message):
    if len(m.command) == 1:
        await m.reply_text("Usage /addlink [link] [button name]")
        return
    
    elif len(m.command) == 2:
        
        link = await validate_link_return(m)

        if not link:
            await m.reply_text("No link found in the message try again")
            return

        if FSUB_LINK().insert_link(link):
            await m.reply_text("Looks like you forgot to give me button name setting it to none by default. You can update the button name later using `/ulname` command")
        else:
            await m.reply_text(f"An entity already exist with the given url. You can change the button name for it using `/ulname {link} [btn name]`")
            
    else:
        name = m.text.split(None, 2)[-1]
        link = await validate_link_return(m)

        if not link:
            await m.reply_text("No link found in the message try again")
            return

        if FSUB_LINK().insert_link(link, name):
            await m.reply_text(f"Successfully inserted the link ({link}) with name ({name}) in the database")

        return


@DENDENMUSHI.on_message(filters.command("ulname") & auth_users)
async def update_link_btn_name(_, m: Message):
    if len(m.command) in [1, 2]:
        await m.reply_text("Usage:\n`/ulname [link] [btn name]")
        return

    link = await validate_link_return(m)
    if not link:
        await m.reply_text("Give me a proper link\nThe given link is not valid")
        return
    
    name = m.text.split(None, 2)[-1]

    up = FSUB_LINK().update_btn(link, name)
    if not up:
        await m.reply_text("No matching entry found in database with given link")
        return
    
    await m.reply_text(f"Successfully updated values in database:\nLink used: {link}\nOld name: {up['btn_name']}\nNew name: {name}")
    return

@DENDENMUSHI.on_message(filters.command("rmlink") & auth_users)
async def remove_link_entity(_, m: Message):
    link = await validate_link_return(m)
    if not link:
        await m.reply_text("Give me a proper link\nThe given link is not valid")
        return
    
    was_ = FSUB_LINK().delete_link(link)
    if not was_:
        await m.reply_text("No entity found with given link")
        return
    
    await m.reply_text(f"Deleted the link from database\nButton name was: {was_['btn_name']}")
    return

@DENDENMUSHI.on_message(filters.command("getlinks") & auth_users)
async def get_all_linksss(_, m: Message):
    links = FSUB_LINK().get_all()

    if not links:
        return await m.reply_text("No link found")
    
    txt = "Here are all the links in my database:\n"
    for link in links:
        txt += f"Link: `{link['link']}\n\tButton name: {link['btn_name']}\n\n"
    
    await m.reply_text(txt)
    return