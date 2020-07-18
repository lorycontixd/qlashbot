import io
import asyncio
import discord
from collections import defaultdict

from modules.countries import library as countries_library

async def is_official_club(self, ctx, gametag):
    found = False
    for c in self.qlash_bs['official_clubs']:
        if gametag.startswith("#") and c['tag'] == gametag:
            found = True
            break
        elif c['name'] == gametag:
            found = True
            break

    if found:
        await ctx.send("Yes, it is official.")
    else:
        await ctx.send("Not official")


async def is_invited_club(self, ctx, gametag):
    found = False
    for c in self.qlash_bs['invited_clubs']:
        if gametag.startswith("#") and c['tag'] == gametag:
            found = True
            break
        elif c['name'] == gametag:
            found = True
            break

    if found:
        await ctx.send("Yes, it is invited.")
    else:
        await ctx.send("Not invited.")

async def print_official_club(self, ctx, gametag):
    found = False

    for c in self.qlash_bs['official_clubs']:
        #   {
        #   "tag": "#VGR08YLV",
        #   "name": "QLASH Storm ARG",
        #   "country": "Argentina",
        #   "esl_region": "LATAM South",
        #   "leader": "AT|♠️Marquito♠️",
        #   "required_trophies": "22,000",
        #   "discord": "https://discord.com/channels/415221296247341066/695763723264196760"
        # }
        if gametag.startswith("#") and c['tag'] == gametag or c['name'] == gametag:
            found = True
            QLASH_BRAWLSTARS_INFOBOX_ICON_URL = "https://cdn.discordapp.com/attachments/720193411113680913/723850143480152114/PzQwxlPN_400x400.jpg"
            QLASH_BRAWLSTARS_INFOBOX_THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/720193411113680913/723850169036046346/qlash-transparent.png"
            QLASH_BRAWLSTARS_DISCORD_URL = self.qlash_bs['QLASH_BRAWLSTARS_DISCORD_URL']
            QLASH_BRAWLSTARS_INFOBOX = discord.Embed(title="QLASH -- Brawl Stars", description="Official Discord Club in Brawl Stars", color=0x00ccff)
            QLASH_BRAWLSTARS_INFOBOX.set_author(name="QLASH -- Brawl Stars", url=QLASH_BRAWLSTARS_DISCORD_URL, icon_url=QLASH_BRAWLSTARS_INFOBOX_ICON_URL)
            QLASH_BRAWLSTARS_INFOBOX.set_thumbnail(url=QLASH_BRAWLSTARS_INFOBOX_THUMBNAIL_URL)
            QLASH_BRAWLSTARS_INFOBOX.add_field(name="Club", value=c["name"])
            QLASH_BRAWLSTARS_INFOBOX.add_field(name="Tag", value=c["tag"])
            QLASH_BRAWLSTARS_INFOBOX.add_field(name="Nation", value=c["country"] + " " + countries_library.get_flag_emoji(c["country"]))
            QLASH_BRAWLSTARS_INFOBOX.add_field(name="President", value=c["leader"], inline=False)
            QLASH_BRAWLSTARS_INFOBOX.add_field(name="Required trophies", value=c["required_trophies"], inline=False)
            if len(c["discord"]) > 0:
                QLASH_BRAWLSTARS_INFOBOX.add_field(name="Discord", value=c["discord"], inline=False)
            QLASH_BRAWLSTARS_INFOBOX.add_field(name="Club page", value="https://www.starlist.pro/stats/club/" + c["tag"][1:], inline=False)
            QLASH_BRAWLSTARS_INFOBOX.add_field(name="Join this club!", value="https://link.brawlstars.com/invite/band/en?tag=" + c["tag"][1:], inline=False)
            await ctx.send(embed=QLASH_BRAWLSTARS_INFOBOX)
            break
    if not found:
        await ctx.send(gametag + " is not an official club.")

async def print_official_clubs(self, ctx, channel):
    qlash_bs_nation_clubs = defaultdict(list)

    for c in self.qlash_bs['official_clubs']:
        qlash_bs_nation_clubs[c['country']].append(c)

    if channel is None:
        channel = ctx.channel

    for nation in qlash_bs_nation_clubs:
        with io.StringIO() as output:
            output.write(nation + " " + countries_library.get_flag_emoji(nation) + "\n")
            output.write("```r\n")
            for c in qlash_bs_nation_clubs[nation]:
                output.write(c['name'] + "\n")
                output.write(c['tag'] + "\n")
                output.write("Required trophies: " + c['required_trophies'] + "\n")
                output.write("President: " + c['leader'] + "\n")
                #output.write("Region: " + c['esl_region'] + "\n")
                output.write("Discord: " + c['discord'] + "\n")
                if output.tell() >= 1400:
                    output.write("```")
                    await channel.send(output.getvalue())
                    output.truncate(0)
                    output.seek(0)
                    output.write("```r\n")
            output.write("```")
            await channel.send(output.getvalue())
            await asyncio.sleep(1)
