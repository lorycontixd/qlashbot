import discord
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from instances import *
from descriptions import *
from functions import *

class Fun(commands.Cog,name="Fun"):
    def __init__(self):
        self.is_Flipped = False

    @commands.cooldown(1,30,commands.BucketType.channel)
    @commands.command(name='bs-puns',brief='Post a random and very funny pun about Brawl Stars',description=desc_bs_puns)
    async def bs_puns(ctx):
        await bs_puns_(ctx)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name='roll',brief='(FUN) Roll a 6 sided dice.',description='Fun Command \n 30 seconds cooldown per user \n \n'
    +'Roll a 6 sided dice to get a random number from 1 to 6.')
    async def roll(self,ctx):
        try:
            await roll_(ctx)
        except:
            print("Failed")

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name='ping',brief = '(FUN) Pong! 🏓',description='Fun Command \n 30 seconds cooldown per user \n \nNothing to describe. Play some Ping Pong with the Bot')
    async def ping(self,ctx):
        response='pong 🏓'
        await ctx.send(response)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name='coin-flip',brief='(FUN) Flip a coin',pass_context = True,description=desc_coinflip)
    async def coin_flip(self,ctx):
        flip = random.choice(['Heads','Tails'])
        await ctx.channel.send('You flipped '+flip)

    @commands.cooldown(1, 50, commands.BucketType.guild)
    @commands.command(name='table-flip',brief='(FUN) Flip that table!!',description="Flip that table!!  50 seconds cooldown in the server")
    async def flip_(self,ctx):
        await flip(ctx)

    @commands.cooldown(1, 50, commands.BucketType.guild)
    @commands.command(name='table-unflip',brief='(FUN) Unflip that table!!',description="Unflip that table!!  50 seconds cooldown in the server")
    async def unflip_(self,ctx):
        await unflip(ctx)

    @commands.cooldown(1, 50, commands.BucketType.guild)
    @commands.command(name='table-status',brief="(FUN) Check table's status",desciption=desc_tstatus)
    async def tstatus_(self,ctx):
        await tstatus(ctx)
