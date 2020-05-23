#commands and bot descriptions

bot_description = """Welcome to the QLASH Bot Help Center. I am QLASH Bot and I allow users to do a bunch of cool and interesting stuff 😎.
To navigate in this help menu, please type ^help <category name> to view all possible commands under a category, and ^help <category name> <command name> for a detailed description of a command.
To run a command type ^<category> <command> <parameters (if any)>, for example ^util qlash-clan QLASH Olympus or ^fun roll
If you have any question or problem with my commands, please do not hesitate to contact our staff or the Bot creators directly.
I hope you have a pleasant stay in the discord server! 🤩😁 """

desc_bs_playerinfo = """Moderator command
No Cooldown \n
Search for information about a specific PLAYER from the Brawl Stars game, including: \n-- Name & Tag \n-- Highest & Current Trophies \n-- Player Victories \n-- Championship Qualification"""

desc_bs_claninfo = """Moderator command
No Cooldown \n
Search for information about a specific CLAN from the Brawl Stars game, including: \n-- Name & Tag \n-- Current & Required Trophies \n-- Player Count \n-- President & Highest Member"""

desc_bs_memberinfo =  """Moderator command
No Cooldown \n
Search for information about a specific MEMBER in a given clan from the Brawl Stars game.
The difference from the player information is that, while in the previous function the parameter <#gametag> is required, for this function it is necessary to give the parameters <PlayerName> and <#clantag>, allowing you to not know the player's ingame tag.
Informations about the member include:
\n-- Name & Tag \n-- Clan Role \n-- Player Trophies"""

desc_qlash_allclans = """Utility command
60 seconds cooldown per channel \n
Print a list of all official QLASH Clans and the respective required trophies. No Parameters are needed for this function."""

desc_qlash_clan = """Utility command
60 seconds cooldown per channel \n
Print information about a specific QLASH Clan.
The parameter can be the clan tag (for precise search) or the clan name. In the second case, the name must be exact, or the command will not work."""

desc_set = """Utility command
60 seconds cooldown per user (only usable in the roles_assignement channel) \n
Get the discord role for the QLASH clan you belong to in Brawl Stars.
If you already have the right role, it will give it again. If you do not belong to an official clan, it will tell you explicitly.
The parameter required is your INGAME tag that you can find in your profile."""

desc_clan_add = """Moderator command
No Cooldown \n
Add a QLASH Clan to the database. The parameters are the clan's tag and the clan's name written correctly.
Moderator and Sub-Coordinator roles are required."""

desc_clann_remove = """Moderator command
No Cooldown \n
Remove a QLASH Clan to the database. The parameter is the clan's name written correctly.
Moderator and Sub-Coordinator roles are required."""

desc_ip = """Moderator command
No Cooldown \n
Locate an ip address with information such as country, city, postal code, longitude & latitude and much more.
Only the creators of the bot have access to this function. Please contact them."""

desc_memberinfo = """Moderator command
No Cooldown \n
Show rich information about a discord member inside the server.
Information includes: \n-- Name, Tag & ID\n-- Member Status \n-- Server join date \n-- Top role and permissions."""

desc_serverinfo = """Moderator Command
No Cooldown \n
Shows all information of the current server.
These include: \n-- Name & ID \n-- Region \n-- Member count \n--Owner \n-- Date of creation. \n-- Much more"""

desc_member_dm = """Moderator Command
No Cooldown \n
The bot sends a private message to the specified member.
The member can be accessed by tagging or by name#discriminator, while the message is written after the member parameter."""

desc_announce = """Moderator Command
No Cooldown\n
The bot sends a message to the a specified channel.
The channel can be accessed by name, while the message is written after the channel parameter"""

desc_refresh_banlist = """Moderator Command
No Cooldown \n
Get a list of members who are currently banned from ingame QLASH clans, but that find themselves in one.
The information is gathered from the banlist channel, where the most relevant information is the player tag and the period of ban."""

#*****************************************************************************************************************
#**********************************************       FUN     ****************************************************
#*****************************************************************************************************************

desc_coinflip = """Fun command
30 seconds cooldown per user \n
Throw a coin to get a completely random outcome from either Heads or Tails."""

#*****************************************************************************************************************
#********************************************       VARIOUS     **************************************************
#*****************************************************************************************************************

channels_response = """
```
Here is a list of the main channels in this server:
- #welcome: here you can read our main rules in order to establish order in the server. We advise you to read them carefully
- #🔥announcements: we use this channel to announce changes, tournaments, competitions, applications and more things within the server
- #👑all-qlash-clans: here you can find all official QLASH clans in Brawl Stars, with the corresponding trophy limit.
- #roles-assignment: in this channel you can send a screenshot as a proof of your position in a qlash clan to unlock benefits such as tournaments, dedicated channels and more..
- there are various general chats for most of the languages worldwide. Please chat in the right channel based on the language you are speaking.
- #📗support: in this channel you can publicly ask for help at any time and our staff will contact you as soon as possible.
- #🤖bot-spam: in this channel you can interact with our bots. We do this to avoid confusion in channels for normal conversation.
- #📢tournament-announcements: here we give announcements on qlash tournaments

If you have more questions about channels, do not hesitate to contact our staff.
```
"""
