import discord
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from instances import *
from descriptions import *
from functions import *

class BrawlStars(commands.Cog,name="Brawl Stars"):
    def __init__(self):
        pass

    @commands.cooldown(1,30,commands.BucketType.channel)
    @commands.command(name='map',brief='Shows a map in Brawl Stars.')
    async def map(self,ctx,name):
        await ctx.send("Not yet implemented.")
