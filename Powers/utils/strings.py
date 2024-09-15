start_msg = """
Hey {mention}!

Myself {bot_name}

I am developed to serve the channel [Sonic Otakus](https://t.me/Sonic_Otakus)! I can give streamable link as well as download link of all anime and do much more see help to know what I can do.
"""

help_msg = """
Just send me the name of any anime (or you can use /search [anime name]) I will search for it and give you the best matching results.

**Available Commands**
• /ongoing: Return the ongoing top 10 trending anime.
• /top: Return the top 10 all time popular anime.
• /search [anime name]: Search for the given anime
• /character [character name]: Search for the given character


NOTE: You can only search anime by name in my inbox
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
{name}

╭────────────────•
╰➢ **𝖲𝖼𝗈𝗋𝖾:** `{score}`
╰➢ **𝖲𝗈𝗎𝗋𝖼𝖾:** `{source}`
╰➢ **𝖳𝗒𝗉𝖾:** `{mtype}`
╰➢ **𝖤𝗉𝗂𝗌𝗈𝖽𝖾𝗌:** `{episodes}`
╰➢ **𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{duration} minutes`
╰➢ **𝖲𝗍𝖺𝗍𝗎𝗌:** `{status}`
╰➢ **𝖥𝗈𝗋𝗆𝖺𝗍:** `{format}`
╰➢ **𝖦𝖾𝗇𝗋𝖾:** `{genre}`
╰➢ **𝖳𝖺𝗀𝗌:** `{tags}`
╰➢ **𝖠𝖽𝗎𝗅𝗍 𝖱𝖺𝗍𝖾𝖽:** `{isAdult}`
╰➢ **𝖲𝗍𝗎𝖽𝗂𝗈:** `{studio}`
╰➢ **𝖳𝗋𝖺𝗂𝗅𝖾𝗋:** {trailer}
╰➢ **𝖶𝖾𝖻𝗌𝗂𝗍𝖾:** {siteurl}
╰────────────────•
"""

ani_info_def_string = """
{name}

╭────────────────•
╰➢ **𝖳𝗒𝗉𝖾:** `{mtype}`
╰➢ **𝖤𝗉𝗂𝗌𝗈𝖽𝖾𝗌:** `{episodes}`
╰➢ **𝖲𝗍𝖺𝗍𝗎𝗌:** `{status}`
╰➢ **𝖦𝖾𝗇𝗋𝖾:** `{genre}`
╰➢ **First aired:** `{aired}` 
╰➢ **Other name:** `{oname}`
╰────────────────•
"""


char_info_string = """
{name}

╭────────────────•
╰➢ **𝖦𝖾𝗇𝖽𝖾𝗋:** `{gender}`
╰➢ **𝖣𝖺𝗍𝖾 𝗈𝖿 𝖡𝗂𝗋𝗍𝗁:** `{date_of_birth}`
╰➢ **𝖠𝗀𝖾:** `{age}`
╰➢ **𝖡𝗅𝗈𝗈𝖽 𝖳𝗒𝗉𝖾:** `{blood_type}`
╰➢ **𝖥𝖺𝗏𝗈𝗎𝗋𝗂𝗍𝖾𝗌:** `{favorites}`
╰➢ **𝖶𝖾𝖻𝗌𝗂𝗍𝖾:** {siteurl}{role_in}
╰────────────────•
"""

anime_res_txt = "Found following results for the query: {q}\nPage: {p}/{tp}"

ep_txt = "Choose the episode you want to watch from below\nTotal episodes: {ep}\nPage:{p}"
