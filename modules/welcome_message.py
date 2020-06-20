import discord
from modules import constants


WELCOME_MESSAGE_ICON_URL = "https://cdn.discordapp.com/attachments/720193411113680913/723850143480152114/PzQwxlPN_400x400.jpg"
WELCOME_MESSAGE_IMAGE_URL = "https://cdn.discordapp.com/banners/415221296247341066/5feac1eee07f969ecbc6aa346738edb6.jpg?size=512"
WELCOME_MESSAGE_THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/720193411113680913/723850169036046346/qlash-transparent.png"
WELCOME_MESSAGE_FIRST_SECTION = """**Welcome to the QLASH Brawl Stars server!**
Let us be the first one to wish you a pleasant stay on our server.

Please make yourself comfortable by reading up on our rules and check out our clans in #👑all-qlash-clans.
"""

WELCOME_MESSAGE_SECOND_SECTION = discord.Embed(title="QLASH -- Brawl Stars", description="Official Discord Server QLASH Brawl Stars", color=0x00ccff)
WELCOME_MESSAGE_SECOND_SECTION.set_author(name="QLASH -- Brawl Stars", url=constants.QLASH_BRAWLSTARS_DISCORD_URL, icon_url=WELCOME_MESSAGE_ICON_URL)
WELCOME_MESSAGE_SECOND_SECTION.set_thumbnail(url=WELCOME_MESSAGE_THUMBNAIL_URL)
WELCOME_MESSAGE_SECOND_SECTION.set_image(url=WELCOME_MESSAGE_IMAGE_URL)
WELCOME_MESSAGE_SECOND_SECTION.add_field(name="Discord", value=constants.QLASH_BRAWLSTARS_DISCORD_URL, inline=False)
WELCOME_MESSAGE_SECOND_SECTION.add_field(name="Home page", value=constants.QLASH_BRAWLSTARS_HOMEPAGE_URL, inline=False)
WELCOME_MESSAGE_SECOND_SECTION.add_field(name="Instagram", value=constants.QLASH_BRAWLSTARS_INSTAGRAM_URL, inline=False)
WELCOME_MESSAGE_SECOND_SECTION.add_field(name="Telegram", value=constants.QLASH_BRAWLSTARS_TELEGRAM_URL, inline=False)
WELCOME_MESSAGE_SECOND_SECTION.add_field(name="Twitter", value=constants.QLASH_BRAWLSTARS_TWITTER_URL, inline=False)

RULES_SECTION = """**Rules**

Before you start to chat in our community channels please read the rules:

Basic  info about the server

We inform all our users that by joining this server you give the tacit approval to all the following rules.
This server has members of all nationalities, beliefs, religions, ages, orientations etc., so be respectful of others while you are here.

**General Rules**

1- Intolerance, racism or any kind of vulgarity is prohibited in this server in any form (Audio, text, private chat, tags, images etc.) please to be respectful to every other user, otherwise you will be kicked/banned regardless of your role.
2- Do not spam. This includes our discord channels and any users on the server; including, but not limited to admins, streamer, players, casters, influencers, moderators and coaches. This also includes spam of symbols, letters, images, links, emotes or videos.
3- Inappropriate Usernames or Profile Pics are not allowed.
4- No porn material is permitted in any form on this server, also sexism is forbidden.
5- Use common sense. This means no shitposting will be tolerated in any public channel under any means.
6- No flame will be tolerated in any way, both text and audio.
7- You can't sell your account here.
8- BrawlStars Account sharing is forbidden. So don't ask for account pushing or other things related to this topic.
9- You can't share links to other servers/groups
(Discord, telegram, etc...) without approval.
10- You can't promote external Clans without approval.


**Admin/Mod rules**

1- Admin/Moderators keep the server under control, if they ask you to stop doing something listen to them.
2- Don't impersonate other users, especially staff. If they ask you to stop, listen to them.
3- If you have any question or problem with other user please contact our staff.
4- Admin/Moderators cannot abuse their role, If they do so report it to another Admin.
"""

RULES_SECTION_IMAGE_URL = "https://cdn.discordapp.com/attachments/720193411113680913/723857824874233887/rules_discord.png"
