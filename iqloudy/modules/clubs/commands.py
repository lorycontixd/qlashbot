import discord
import json
from discord.ext import commands

from modules.clubs import library as clubs_library, descriptions as clubs_descriptions

#*****************************************************************************************************************
#**********************************************       FUN     ****************************************************
#*****************************************************************************************************************


class Clubs(commands.Cog, name="Clubs"):
    def __init__(self, bot, qlash_bs):
        self.bot = bot
        self.qlash_bs = qlash_bs
        pass

    @commands.cooldown(1,15,commands.BucketType.channel)
    @commands.has_any_role('Moderator','DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='is-official-club',brief='Check if a club is official.')
    async def is_official_club_(self,ctx,*gametag):
        await clubs_library.is_official_club(self, ctx, " ".join(gametag[:]))

    @commands.cooldown(1,15,commands.BucketType.channel)
    @commands.has_any_role('Moderator','DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='is-invited-club',brief='Check if a club is invited.')
    async def is_invited_club_(self,ctx,*gametag):
        await clubs_library.is_invited_club(self, ctx, " ".join(gametag[:]))

    @commands.cooldown(1,15,commands.BucketType.channel)
    @commands.has_any_role('Moderator','DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='print-club',brief='Print out one official clubs.')
    async def print_official_club_(self,ctx, *gametag):
        await clubs_library.print_official_club(self, ctx, " ".join(gametag[:]))

    @commands.cooldown(1,15,commands.BucketType.channel)
    @commands.has_any_role('Moderator','DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='print-all-clubs',brief='Print out all official clubs.')
    async def print_official_clubs_(self,ctx, channel:discord.TextChannel = None):
        await clubs_library.print_official_clubs(self, ctx, channel)

    @commands.cooldown(1,15,commands.BucketType.channel)
    @commands.has_any_role('Moderator','DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='print-all-clubs-as-embeds',brief='Print out all official clubs as embeds.')
    async def print_official_clubs_as_embeds(self,ctx, channel:discord.TextChannel = None):
        await clubs_library.print_official_clubs_as_embeds(self, ctx, channel)
