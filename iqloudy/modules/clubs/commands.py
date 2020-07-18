import discord
import json
from discord.ext import commands

from modules.clubs import library as clubs_library, descriptions as clubs_descriptions

#*****************************************************************************************************************
#**********************************************       FUN     ****************************************************
#*****************************************************************************************************************


class Clubs(commands.Cog, name="Clubs"):
    def __init__(self, qlash_bs):
        self.qlash_bs = qlash_bs
        pass

    @commands.cooldown(1,1,commands.BucketType.channel)
    @commands.command(name='is-official-club',brief='Check if a club is official.')
    async def is_official_club_(self,ctx,*gametag):
        await clubs_library.is_official_club(self, ctx, " ".join(gametag[:]))
