import discord
from discord.ext import commands

class BrawlStars(commands.Cog,name="Brawl Stars"):
    def __init__(self):
        pass

    @commands.cooldown(1,30,commands.BucketType.channel)
    @commands.command(name='map',brief='Shows a map in Brawl Stars.')
    async def map(self,ctx,name):
        await ctx.send("Not yet implemented.")