import discord
from discord.ext import commands

from modules.fun import library as fun_library, descriptions as fun_descriptions

#*****************************************************************************************************************
#**********************************************       FUN     ****************************************************
#*****************************************************************************************************************


class Fun(commands.Cog, name="Fun"):
    def __init__(self):
        self.is_flipped = False

    @commands.cooldown(1,30,commands.BucketType.channel)
    @commands.command(name='bs-puns',brief='Post a random and very funny pun about Brawl Stars.',description=fun_descriptions.desc_bs_puns)
    async def bs_puns_(self,ctx):
        await fun_library.bs_puns(self, ctx)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name='roll',brief='Roll a 6 sided dice.',description=fun_descriptions.desc_roll)
    async def roll_(self,ctx):
        await fun_library.roll(self, ctx)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name='ping',brief = 'Pong! 🏓',description='Fun Command \n 30 seconds cooldown per user \n \nNothing to describe. Play some Ping Pong with the Bot')
    async def ping_(self,ctx):
        await fun_library.ping(self, ctx)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name='coin-flip',brief='Flip a coin',pass_context = True,description=fun_descriptions.desc_coinflip)
    async def coin_flip_(self,ctx):
        await fun_library.coin_flip(self,ctx)

    @commands.cooldown(1, 50, commands.BucketType.guild)
    @commands.command(name='table-flip',brief='Flip that table!!',description="Flip that table!!  50 seconds cooldown in the server")
    async def flip_(self,ctx):
        await fun_library.flip(self, ctx)

    @commands.cooldown(1, 50, commands.BucketType.guild)
    @commands.command(name='table-unflip',brief='Unflip that table!!',description="Unflip that table!!  50 seconds cooldown in the server")
    async def unflip_(self,ctx):
        await fun_library.unflip(self, ctx)

    @commands.cooldown(1, 50, commands.BucketType.guild)
    @commands.command(name='table-status',brief="Check table's status",desciption=fun_descriptions.desc_tstatus)
    async def table_status_(self,ctx):
        await fun_library.table_status(self, ctx)
