start_msg = """
𝗛𝗲𝗹𝗹𝗼!! 𝗖𝗼𝗺𝗽𝗮𝗱𝗿𝗲 ꈍ◡ꈍ

<b><i>» Welcome To ⚡️⚡️Sonic Family⚡️⚡
» I'm Anime Flix - I Can Share Streaming And Download Links of Any Anime With You.
» Just Type Name of Any Anime, And Get Surprised By The Results.
» You Must Join My Channel @Sonic_Otakus And @Anime_Flix_Pro To Use Me.
» Enjoy Your Anime Watching Experience.</i></b>"""

# [Sonic Otakus](https://t.me/Sonic_Otakus)! I can give streamable link as well as download link of all anime and do much more see help to know what I can do.

help_msg = """
» Just Send Me The Name of Any Anime, And I Will Give You The Results.

**Available Commands**
• /ongoing: Top 10 Trending Ongoing Anime.
• /top: Top 10 All Time Popular Anime.
• /character [character name]: Search For The Given Character
• For Anime: Type A Name, And Send It.
"""

dev_msg = """
**OWNER COMMANDS**
• /addsudo [reply to user]: Will add sudoer
• /rmsudo [id of the user]: Will remove the sudoer

**SUDO COMMANDS**
• /addfsub [channel id] [type]: Add channel in force subscribe. Default to auto
• /rmfsub [channel id]: Remove channels from force subscribe
• /changetype [channel id] [newtype]: Replace the type of join 
• /getfsubs: Return all the fsubs channel with their types
• /logs: Return logs
• /stats: Current stats of the bot
• /gcast [tag] [reply to message]: Will broadcast replied message according to given tag
    Available tags:
        -u : Broadcast messages to all users.
        -c : Broadcast messages in all the chats
        -all : Broadcast messages to all chats and users
    In case you don't give tag or you give wrong the tag -all will be considered as default
"""

ani_info_string = """
<b>{name}</b>

<b><i>» <u>𝖲𝖼𝗈𝗋𝖾</u> ~ {score}
» <u>𝖲𝗈𝗎𝗋𝖼𝖾</u> ~ {source}
» <u>𝖳𝗒𝗉𝖾</u> ~ {mtype}
» <u>𝖤𝗉𝗂𝗌𝗈𝖽𝖾𝗌</u> ~ {episodes}
» <u>𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇</u> ~ {duration} minutes
» <u>𝖲𝗍𝖺𝗍𝗎𝗌</u> ~ {status}
» <u>𝖥𝗈𝗋𝗆𝖺𝗍</u> ~ {format}
» <u>𝖦𝖾𝗇𝗋𝖾</u> ~ {genre}
» <u>𝖳𝖺𝗀𝗌</u> ~ {tags}
» <u>𝖠𝖽𝗎𝗅𝗍 𝖱𝖺𝗍𝖾𝖽</u> ~ {isAdult}
» <u>𝖲𝗍𝗎𝖽𝗂𝗈</u> ~ {studio}
» <u>𝖳𝗋𝖺𝗂𝗅𝖾𝗋</u> ~ {trailer}
» <u>𝖶𝖾𝖻𝗌𝗂𝗍𝖾</u> ~ {siteurl}</i></b>
"""

ani_info_def_string = """
<b>{name}</b>

<b><i>» <u>𝖳𝗒𝗉𝖾</u> ~ {mtype}
» <u>𝖤𝗉𝗂𝗌𝗈𝖽𝖾𝗌</u> ~ {episodes}
» <u>𝖲𝗍𝖺𝗍𝗎𝗌</u> ~ {status}
» <u>𝖦𝖾𝗇𝗋𝖾</u> ~ {genre}
» <u>First Aired</u> ~ {aired} 
» <u>Other Name</u> ~ {oname}</i></b>
"""


char_info_string = """
<b><i>{name}

» <u>𝖦𝖾𝗇𝖽𝖾𝗋</u> ~ {gender}
» <u>𝖣𝖺𝗍𝖾 𝗈𝖿 𝖡𝗂𝗋𝗍𝗁</u> ~ {date_of_birth}
» <u>𝖠𝗀𝖾</u> ~ {age}
» <u>𝖡𝗅𝗈𝗈𝖽 𝖳𝗒𝗉𝖾</u> ~ {blood_type}
» <u>𝖥𝖺𝗏𝗈𝗎𝗋𝗂𝗍𝖾𝗌</u> ~ {favorites}
» <u>𝖶𝖾𝖻𝗌𝗂𝗍𝖾</u> ~ {siteurl}{role_in}</i></b>
"""

anime_res_txt = "<b><i>» Found Results For: {q}\n\n» Page: {p}/{tp}</i></b>"

ep_txt = "<b><i>» Choose The Episode You Want To Stream / Download From Below.\n\n» Total Episodes - {ep}\n\n» Page - {p}</i></b>"
