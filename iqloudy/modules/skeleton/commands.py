import discord
from discord.ext import commands

from modules.skeleton import library as skeleton_library, descriptions as skeleton_descriptions

#*****************************************************************************************************************
#**********************************************       FUN     ****************************************************
#*****************************************************************************************************************


class Skeleton(commands.Cog, name="Skeleton"):
    def __init__(self):
        pass

    @commands.cooldown(1,30,commands.BucketType.channel)
    @commands.has_any_role('Moderator','DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='skel-hello',brief='A sample command.',description=skeleton_descriptions.desc_hello)
    async def hello_(self,ctx):
        await skeleton_library.hello(self, ctx)
