import discord
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from instances import *
from descriptions import *
from functions import *
from random import randint

class Fun(commands.Cog,name="Fun"):
    def __init__(self):
        self.is_flipped = False

    @commands.cooldown(1,30,commands.BucketType.channel)
    @commands.command(name='bs-puns',brief='Post a random and very funny pun about Brawl Stars',description=desc_bs_puns)
    async def bs_puns(self,ctx):
        choices = ['What do you call it when you get killed by a bull main? Bull-shit.','What do you call it when you get killed by a Shelly main? Shell shock.','What do you call it when you get killed by a Poco main? Hacks.','What do you call a team of crows? Toxic','How is franks super? Literally stunning','What is Nita without her super? UnBearable',"El primo isn't really a jokester, but he can pack quite a punch line",'Killing that little cactus man will give you a decent Spike in ego.','My club has barley any members.','All these puns are literally Tara-ble.','El Primo jumping in the enemy base with 11 gems.']
        myint = randint(1,len(choices))
        await ctx.send(str(choices[myint]))

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name='roll',brief='(FUN) Roll a 6 sided dice.',description='Fun Command \n 30 seconds cooldown per user \n \n'
    +'Roll a 6 sided dice to get a random number from 1 to 6.')
    async def roll(self,ctx):
        value = randint(1,6)
        await ctx.send("You rolled a "+str(value))

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
        if self.is_flipped == False:
    		response = '(╯°□°）╯︵ ┻━┻ '
    		await ctx.channel.send(response)
    		self.is_flipped = True
    	else:
    		response = 'Sorry the table is already flipped!! ¯\_(ツ)_/¯ '
    		await ctx.channel.send(response)

    @commands.cooldown(1, 50, commands.BucketType.guild)
    @commands.command(name='table-unflip',brief='(FUN) Unflip that table!!',description="Unflip that table!!  50 seconds cooldown in the server")
    async def unflip_(self,ctx):
        if self.is_flipped == True:
    		response = '┬─┬ ノ( ゜-゜ノ)'
    		await ctx.channel.send(response)
    		self.is_flipped = False
    	else:
    		response = 'Sorry the table is already unflipped!! ¯\_(ツ)_/¯ '
    		await ctx.channel.send(response)

    @commands.cooldown(1, 50, commands.BucketType.guild)
    @commands.command(name='table-status',brief="(FUN) Check table's status",desciption=desc_tstatus)
    async def tstatus_(self,ctx):
    	if self.is_flipped == True:
    		response = 'Table is flipped'
    		await ctx.channel.send(response)
    	else:
    		response = 'Table is unflipped'
    		await ctx.channel.send(response)
