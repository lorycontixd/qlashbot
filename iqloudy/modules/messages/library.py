import aiohttp
import discord

from io import BytesIO

QLASH_BRAWLSTARS_HOMEPAGE_URL="https://www.qlash.gg"
QLASH_BRAWLSTARS_DISCORD_URL="https://www.discord.gg/qlash-brawlstars"
QLASH_BRAWLSTARS_TELEGRAM_URL="https://www.telegram.me/QLASHBS"
QLASH_BRAWLSTARS_INSTAGRAM_URL="https://www.instagram.com/qlash_brawlstars"
QLASH_BRAWLSTARS_FACEBOOK_URL="https://www.facebook.com/qlashbrawlstars"
QLASH_BRAWLSTARS_TIKTOK_URL="https://www.tiktok.com/@qlash"
QLASH_BRAWLSTARS_TWITTER_URL="https://www.twitter.com/brawlqlash"
QLASH_BRAWLSTARS_TWITCH_URL="https://www.twitch.tv/qlash_eng"
QLASH_BRAWLSTARS_YOUTUBE_URL="https://www.youtube.com/qlash"
#"https://www.youtube.com/channel/UCC4BUTrLaGrcIhSwVhPgMOA"

WELCOME_MESSAGE_FIRST_SECTION = """**Welcome to the QLASH Brawl Stars server!**
Let us be the first to wish you a pleasant stay on our server.

Please make yourself comfortable by reading up on our rules and check out our clans in {ALL_QLASH_CLANS_CHANNEL}.
"""

WELCOME_MESSAGE_SECTION_IMAGE_URL = "https://cdn.discordapp.com/attachments/720193411113680913/723873104798941234/e50a80e8-6335-42c2-b82e-abf46b175893-profile_banner-480.png"

QLASH_BRAWLSTARS_INFOBOX_ICON_URL = "https://cdn.discordapp.com/attachments/720193411113680913/723850143480152114/PzQwxlPN_400x400.jpg"
QLASH_BRAWLSTARS_INFOBOX_IMAGE_URL = "https://cdn.discordapp.com/banners/415221296247341066/5feac1eee07f969ecbc6aa346738edb6.jpg?size=512"
QLASH_BRAWLSTARS_INFOBOX_THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/720193411113680913/723850169036046346/qlash-transparent.png"
QLASH_BRAWLSTARS_INFOBOX = discord.Embed(title="QLASH -- Brawl Stars", description="Official Discord Server QLASH Brawl Stars", color=0x00ccff)
QLASH_BRAWLSTARS_INFOBOX.set_author(name="QLASH -- Brawl Stars", url=QLASH_BRAWLSTARS_DISCORD_URL, icon_url=QLASH_BRAWLSTARS_INFOBOX_ICON_URL)
QLASH_BRAWLSTARS_INFOBOX.set_thumbnail(url=QLASH_BRAWLSTARS_INFOBOX_THUMBNAIL_URL)
QLASH_BRAWLSTARS_INFOBOX.set_image(url=QLASH_BRAWLSTARS_INFOBOX_IMAGE_URL)
QLASH_BRAWLSTARS_INFOBOX.add_field(name="Home page", value="[qlash.gg]({url})".format(url=QLASH_BRAWLSTARS_HOMEPAGE_URL), inline=False)
QLASH_BRAWLSTARS_INFOBOX.add_field(name="Discord", value="[discord.gg/qlash-brawlstars]({url})".format(url=QLASH_BRAWLSTARS_DISCORD_URL), inline=True)
QLASH_BRAWLSTARS_INFOBOX.add_field(name="Telegram", value="[t.me/QLASHBS]({url})".format(url=QLASH_BRAWLSTARS_TELEGRAM_URL), inline=True)
QLASH_BRAWLSTARS_INFOBOX.add_field(name="Facebook", value="[QLASH Brawl Stars]({url})".format(url=QLASH_BRAWLSTARS_FACEBOOK_URL), inline=False)
QLASH_BRAWLSTARS_INFOBOX.add_field(name="Twitter", value="[@brawlQLASH]({url})".format(url=QLASH_BRAWLSTARS_TWITTER_URL), inline=True)
QLASH_BRAWLSTARS_INFOBOX.add_field(name="Instagram", value="[@qlash_brawlstars]({url})".format(url=QLASH_BRAWLSTARS_INSTAGRAM_URL), inline=True)
QLASH_BRAWLSTARS_INFOBOX.add_field(name="YouTube", value="[QLASH YouTube]({url})".format(url=QLASH_BRAWLSTARS_YOUTUBE_URL), inline=False)

RULES_MESSAGE_FIRST_SECTION = """**Rules**

Before you start to chat in our community channels please read these rules. We inform all our users that by joining this server you give the tacit approval to all of the following rules.

This server has members of all nationalities, beliefs, religions, ages and orientations, so please be respectful of others while you are staying on the server.

**General Rules**

1- Intolerance, racism or any kind of vulgarity is prohibited on this server in any form (audio, text, private chat, tags, images etc.) please to be respectful to every other user, otherwise you will be kicked/banned regardless of your role.
2- Do not spam. This includes our discord channels and any users on the server; including, but not limited to admins, streamer, players, casters, influencers, moderators and coaches. This also includes spam of symbols, letters, images, links, emotes or videos.
3- Inappropriate Usernames or Profile Pics are not allowed.
4- No porn or NSFW material is permitted in any form on this server, also sexism is forbidden.
5- Use common sense. This means no shitposting will be tolerated in any public channel under any means.
6- No flame will be tolerated in any way, both in text and audio.
7- You can't sell your account here and you have to follow the Terms of Service and other applicable policies by Supercell.
8- BrawlStars Account sharing is also forbidden. So please don't ask for sharing account for pushing trophies or other things related to this topic.
9- You can't advertise or share links to other servers/groups (Discord, telegram, etc...) without prior approval of management.
10- You can't promote unofficial or external clans without prior approval from management.
"""

RULES_MESSAGE_SECOND_SECTION ="""
**Admin/Moderator rules**

1- Admins and Moderators keep the server under control, if they ask you to stop doing something, please listen to them.
2- Don't impersonate other users, especially staff. If they ask you to stop, please listen to them.
3- If you have any question or problem with another user, please contact our staff members and let them know of your experience.
4- Admins and Moderators are not allowed to abuse their authority. If you feel an Admin or a Moderator does, please report your experience to another Admin.
"""

RULES_SECTION_IMAGE_URL = "https://cdn.discordapp.com/attachments/720193411113680913/723857824874233887/rules_discord.png"

async def dm(self,ctx,member: discord.Member, message):
    mess = ctx.message
    await member.create_dm()
    await member.dm_channel.send(message)
    await mess.add_reaction('✅')

async def say(self, ctx, channel:discord.TextChannel, message):
    if not channel:
        channel = ctx.channel

    msg = ctx.message
    guild = ctx.guild

    try:
        await channel.send(message)
        await msg.add_reaction('✅')
    except:
        await ctx.channel.send("Error sending message")

async def image(self, ctx, channel:discord.TextChannel, url, filename):
    if not channel:
        channel = ctx.channel

    msg = ctx.message
    guild = ctx.guild

    try:
        await _send_file(channel, url, filename)
        await msg.add_reaction('✅')
    except:
        await ctx.channel.send("Error sending message")

async def welcome(self, ctx, channel:discord.TextChannel = None):
    if not channel:
        channel = ctx.channel

    msg = ctx.message
    guild = ctx.guild

    await _send_file(channel, messages_library.WELCOME_MESSAGE_SECTION_IMAGE_URL, "banner.png")
    await channel.send(messages_library.WELCOME_MESSAGE_FIRST_SECTION.format(ALL_QLASH_CLANS_CHANNEL = bot.get_channel(566213862756712449).mention))
    await msg.add_reaction('✅')

async def info(self, ctx, channel:discord.TextChannel = None):
    if not channel:
        channel = ctx.channel

    msg = ctx.message
    guild = ctx.guild

    await channel.send(embed=QLASH_BRAWLSTARS_INFOBOX)

async def rules(self, ctx, channel:discord.TextChannel = None):
    if not channel:
        channel = ctx.channel

    msg = ctx.message
    guild = ctx.guild

    await _send_file(channel, messages_library.RULES_SECTION_IMAGE_URL,  "rules.png")
    await channel.send(messages_library.RULES_MESSAGE_FIRST_SECTION)
    await channel.send(messages_library.RULES_MESSAGE_SECOND_SECTION)
    await msg.add_reaction('✅')

async def _send_file(channel, url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            await channel.send(file=discord.File(BytesIO(await resp.read()),filename=filename))
