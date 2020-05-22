import brawlstats
import discord
import os
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from functions import *
import os
import requests
import urllib
from urllib.request import Request, urlopen
import aiohttp
TOKEN = 'NzAxMTI1MzExMDQ3NDAxNDc0.XpyBZQ.RAsYlvnkrzI08mwFuXK8QF5K3BM'
#quotaguard ips = 54.72.12.1, 54.72.77.249
#quotaguard proxy = http://6cy3e5odaiitpe:gxag60u036717xavs35razjk18s2@eu-west-static-03.quotaguard.com:9293
bot = commands.Bot(command_prefix='^' , description = "Qlash Bot ")

os.environ['http_proxy'] = os.environ['QUOTAGUARDSTATIC_URL']
url = 'http://ip.quotaguard.com/'
proxy = urllib.request.ProxyHandler()
opener = urllib.request.build_opener(proxy)
in_ = opener.open(url)
res = in_.read()
print(res)
#*****************************************************************************************



#************************************ EVENTS ********************************************
@bot.event
async def on_ready():
     print('Logged in as: ',bot.user.name)
     print('Bot ID: ',bot.user.id)
     print('----------------')
     await bot.change_presence( activity=discord.Activity(type=discord.ActivityType.playing, name=" ^help"))

#@bot.event
#async def on_member_join(member):
#    await member.create_dm()
#    response = "Hello and welcome to the QLASH Brawl Stars server. Please read the rules before you start interacting with other people. \n"+
#    "You can use the general chat of your language to talk to other people, the support channel to ask questions. If you have any question, please contact our moderators."
#    await member.dm_channel.send(response)

@bot.event
async def on_command_error(ctx, error):
     if isinstance(error, commands.errors.CheckFailure):
         await ctx.send('PermissionError: You do not have the correct role for this command. 😥')
     if isinstance(error, commands.errors.UserInputError):
     	await ctx.send('ArguementError: Bad arguement was given. 😕')
     if isinstance(error, commands.CommandOnCooldown):
     	await ctx.send('CommandError: Command is on cooldown. 😞')
     if isinstance(error, commands.CommandNotFound):
     	await ctx.send('CommandError: Command was not found. 😞')

#***********************************  FUN  ***********************************************
@commands.cooldown(1, 60, commands.BucketType.user)
@bot.command(name='roll')
async def roll(ctx):
    await roll_(ctx)

#BucketType.user can be changed to default: global ratelimit, channel: channel ratelimit, guild: server ratelimit, user: user ratelimit /for that command

@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command(name='ping',brief = 'Pong! 🏓')
async def ping(ctx):
	response='pong'
	await ctx.send(response)
#*****************************************************************************************
@commands.cooldown(1, 60, commands.BucketType.channel)
@bot.command(name='qlash')
async def qlash(ctx):
    await qlash_(ctx)

#ADMIN
@bot.command(name='bs-playerinfo',brief='Search for information about a generic ingame player.')
async def bs_pinfo(ctx,tag):
    await getplayer(ctx,tag)

#ADMIN
@bot.command(name='bs-claninfo',brief='Search for information about an ingame clan.')
async def bs_cinfo(ctx,tag):
    await getclan(ctx,tag)

#ADMIN
@bot.command(name='bs-memberinfo',brief='Search for information about a member within a given clan.')
async def bs_minfo(ctx,name,ctag):
    await search_member(ctx,name,ctag)

@commands.cooldown(1, 60, commands.BucketType.channel)
@bot.command(name='qlash-allclans',brief='List all ingame qlash clans.')
async def qlash_allclans(ctx):
    await qlash_trophies(ctx)

@commands.cooldown(1, 60, commands.BucketType.user)
@bot.command(name='qlash-clan',brief="Search for information about a specific QLASH clan. Parameter accepts either clan name or clan tag. Clan name has to be identical to the ingame clan name.")
async def qlash_clan(ctx,name_tag):
    await qlash_cclan(ctx,name_tag)

#ADMIN
@bot.command(name='set')
async def set(ctx,gametag):
    await set_(ctx,gametag)

#ADMIN
@bot.command(name='clan-add',brief='Add a qlash clan to the database. Parameters require <tag> and <clan_name>')
async def clan_add(ctx,tag,*cname):
    await clan_add_(ctx,tag,*cname)

#ADMIN
@bot.command(name='clan-remove',brief='Remove a qlash clan from the database. Parameter only requies <clan_name>')
async def clan_remove(ctx,*cname):
    await clan_remove_(ctx,*cname)

#ADMIN
@bot.command(name='qlash-clan-members',brief='Shows a list of all members of a given QLASH clan. Parameter accepts either clan name or clan tag. Clan name must be identical to the ingame clan name.')
async def qlashclanmembers(ctx,clan_or_tag):
    await GetClanMembers(ctx,clan_or_tag)

@bot.command(name='locate')
async def locate(ctx,ip):
    await locate_(ctx,ip)

@commands.cooldown(1, 30, commands.BucketType.guild)
@bot.command(name="server-info",brief="(MOD)Show information of the server",description=
	"Moderator Command \n \n"
	"Shows all information of the server, such as: Name, ID, Region, Member count, Owner and Date of creation.")
async def serverinfo(ctx):
    await serverinfo_(ctx)

@commands.cooldown(1, 30, commands.BucketType.guild)
@bot.command(name='member-dm',pass_context=True,brief='(MOD)Send a private message to a member by the bot',description=
	"Moderator Command \n \n"
	"The bot sends a private message to <member>. The member can be accessed by tag or by name#discriminator")
async def dm(ctx,member: discord.Member, *args):
    await poke(ctx,member,*args)

@bot.command(name='member-info,brief=(MOD)Show inforation of a discord member')
async def memberinfo(ctx,member:discord.Member):
    await member_info_(ctx,member)

#@bot.command(name='view-members',brief='')
#async def viewmembers(ctx):
#    await CompareMembers(ctx)

#@bot.command(name='write-members',brief="TEST command to write all members to file")
#async def writemembers(ctx):
#    await WriteMembersToFile2(ctx)







bot.run(TOKEN)
