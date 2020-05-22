#commands and bot descriptions

bot_description = """Welcome to the QLASH Bot Help Center. I am QLASH Bot and I allow users to do a bunch of cool and interesting stuff 😎.
To navigate in this help menu, please type ^help <category name> to view all possible commands and ^help <category name> <command name> for a detailed description of a command.
To run a command type ^<category> <command> <parameters (if any)>, for example ^util qlash-clan QLASH Olympus
If you have any question or problem with my commands, please do not hesitate to contact our staff or the bot creators directly.
I hope you have a pleasant stay in the discord server! 🤩😁 """

desc_bs_playerinfo = """Moderator command \nSearch for information about a specific PLAYER from the Brawl Stars game,
 including: \n-- Name & Tag \n-- Highest & Current Trophies \n-- Player Victories \n-- Championship Qualification"""

desc_bs_claninfo = """Moderator command \nSearch for information about a specific CLAN from the Brawl Stars game,
 including: \n-- Name & Tag \n-- Current & Required Trophies \n-- Player Count \n-- President & Highest Member"""

desc_bs_memberinfo =  """Moderator command \n
Search for information about a specific MEMBER in a given clan from the Brawl Stars game.
The difference from the player information is that, while in the previous function the parameter <#gametag> is required, for this function it is necessary to give the parameters <PlayerName> and <#clantag>, allowing you to not know the player's ingame tag.
Informations about the member include:
\n-- Name & Tag \n-- Clan Role \n-- Player Trophies"""

desc_qlash_allclans = """Utility command \n
Print a list of all official QLASH Clans and the respective required trophies. No Parameters are needed for this function."""

desc_qlash_clan = """Utility command \n
Print information about a specific QLASH Clan.
The parameter can be the clan tag (for precise search) or the clan name. In the second case, the name must be exact, or the command will not work."""

desc_set = """Get the discord role for the QLASH clan you belong to in Brawl Stars.
If you already have the right role, it will give it again. If you do not belong to an official clan, it will tell you explicitly.
The parameter required is your INGAME tag that you can find in your profile."""

desc_clan_add = """Moderator command \n
Add a QLASH Clan to the database. The parameters are the clan's tag and the clan's name written correctly.
Moderator and Sub-Coordinator roles are required."""

desc_clann_remove = """Moderator command \n
Remove a QLASH Clan to the database. The parameter is the clan's name written correctly.
Moderator and Sub-Coordinator roles are required."""

desc_ip = """Moderator command \n
Locate an ip address with information such as country, city, postal code, longitude & latitude and much more.
Only the creators of the bot have access to this function. Please contact them."""

desc_memberinfo = """Moderator command \n
Show rich information about a discord member inside the server.
Information includes: \n-- Name, Tag & ID\n-- Member Status \n-- Server join date \n-- Top role and permissions."""

desc_serverinfo = """Moderator Command \n
Shows all information of the current server.
These include: \n-- Name & ID \n-- Region \n-- Member count \n--Owner \n-- Date of creation. \n-- Much more"""

desc_member_dm = """Moderator Command \n
The bot sends a private message to the specified member.
The member can be accessed by tagging or by name#discriminator, while the message is written after the member parameter."""

desc_announce = """Moderator Command \n
The bot sends a message to the a specified channel.
The channel can be accessed by name, while the message is written after the channel parameter"""

desc_refresh_banlist = """Moderator Command \n
Get a list of members who are currently banned from ingame QLASH clans, but that find themselves in one.
The information is gathered from the banlist channel, where the most relevant information is the player tag and the period of ban."""
