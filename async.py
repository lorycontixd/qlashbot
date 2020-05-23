import brawlstats
import discord
import os
import schedule
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from functions import *
from descriptions import *
import requests
import urllib
from urllib.request import Request, urlopen
import aiohttp
TOKEN = 'NzAxMTI1MzExMDQ3NDAxNDc0.XpyBZQ.RAsYlvnkrzI08mwFuXK8QF5K3BM'
#quotaguard ips = 54.72.12.1, 54.72.77.249
#quotaguard proxy = http://6cy3e5odaiitpe:gxag60u036717xavs35razjk18s2@eu-west-static-03.quotaguard.com:9293

#os.environ['http_proxy'] = os.environ['QUOTAGUARDSTATIC_URL']
#url = 'http://ip.quotaguard.com/'
#proxy = urllib.request.ProxyHandler()
#opener = urllib.request.build_opener(proxy)
#in_ = opener.open(url)
#res = in_.read()
#print(res)

#schedule.every().day.at("22:00").do(CheckBanlist)
schedule_switch=True

#*****************************************************************************************************************
#*********************************************       EVENTS     **************************************************
#*****************************************************************************************************************

@bot.event
async def on_ready():
    print('Logged in as: ',bot.user)
    print('Bot ID: ',bot.user.id)
    print('Creation Date: ',bot.user.created_at)
    print('----------------')
    #mych = await bot.fetch_channel(int(bot_testing))
    #await mych.send("Bot has logged in 🟢")
    await bot.change_presence( activity=discord.Activity(type=discord.ActivityType.playing, name=" ^help"))


@bot.event
async def on_disconnect():
    print("Logging off: ",bot.user)
    #mych = await bot.fetch_channel(int(bot_testing))
    #await mych.send("Bot has logged off 🔴")

#@bot.event
#async def on_member_join(member):
#    await member.create_dm()
#    response = "Hello and welcome to the QLASH Brawl Stars server. Please read the rules before you start interacting with other people. \n"+
#    "You can use the general chat of your language to talk to other people, the support channel to ask questions. If you have any question, please contact our moderators."
#    await member.dm_channel.send(response)

#@bot.event
#async def on_message(message):
#    print(message.author)
#    print(message.channel)
#    print(message.content)
#    print(" ")
#    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    commandname = ctx.invoked_with
    CommandLogs(ctx,commandname+'(failed)')
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('PermissionError: You do not have the correct role for this command. 😥')
    if isinstance(error, commands.errors.UserInputError):
        await ctx.send('ArguementError: Bad arguement was given. 😕')
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send('CommandError: Command is on cooldown. 😞')
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('CommandError: Command was not found. 😞')

@bot.event
async def on_command_completion(ctx):
    commandname = ctx.command.name
    CommandLogs(ctx,commandname)
#*****************************************************************************************************************
#*******************************************       GROUPS     ****************************************************
#*****************************************************************************************************************

@bot.group(pass_context=True,cog_name="Fun",case_insensitive=True)
async def fun(ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand passed - Fun...")

@bot.group(pass_context=True,cog_name="Mod",case_insensitive=True)
async def mod(ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand passed - Mod...")

@bot.group(pass_context=True,cog_name="Util",case_insensitive=True)
async def util(ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand passed - Util...")

#*****************************************************************************************************************
#**********************************************       FUN     ****************************************************
#*****************************************************************************************************************

@commands.cooldown(1, 30, commands.BucketType.user)
@fun.command(name='roll',brief='(FUN) Roll a 6 sided dice.',description='Fun Command \n 30 seconds cooldown per user \n \n'
+'Roll a 6 sided dice to get a random number from 1 to 6.')
async def roll(ctx):
    #CommandLogs(ctx,'roll')
    await roll_(ctx)

#BucketType.user can be changed to default: global ratelimit, channel: channel ratelimit, guild: server ratelimit, user: user ratelimit /for that command

@commands.cooldown(1, 30, commands.BucketType.user)
@fun.command(name='ping',brief = '(FUN) Pong! 🏓',description='Fun Command \n 30 seconds cooldown per user \n \nNothing to describe. Play some Ping Pong with the Bot')
async def ping(ctx):
    response='pong 🏓'
    #CommandLogs(ctx,'ping')
    await ctx.send(response)

@commands.cooldown(1, 30, commands.BucketType.user)
@fun.command(name='coin-flip',brief='(FUN) Flip a coin',pass_context = True,description=desc_coinflip)
async def coin_flip(ctx):
    flip = random.choice(['Heads','Tails'])
    #CommandLogs(ctx,'coin-flip')
    await ctx.channel.send('You flipped '+flip)

#*****************************************************************************************************************
#**********************************************       UTILS     **************************************************
#*****************************************************************************************************************

@commands.cooldown(1, 60, commands.BucketType.channel)
@util.command(name='qlash',brief='(UTIL) Display some information about QLASH.',description=
'Display information about the QLASH Organisation, such as their goal, the founders and more...')
async def qlash(ctx):
    #CommandLogs(ctx,'qlash')
    await qlash_(ctx)

@commands.cooldown(1, 60, commands.BucketType.channel)
@util.command(name='qlash-allclans',brief='(UTIL) List all ingame qlash clans.',description = desc_qlash_allclans)
async def qlash_allclans(ctx):
    #CommandLogs(ctx,'qlash-allclans')
    await qlash_trophies(ctx)

@commands.cooldown(1, 60, commands.BucketType.channel)
@util.command(name='qlash-clan',hidden=True,brief="(UTIL) Search for information about a specific QLASH clan.",description=desc_qlash_clan)
async def qlash_clan(ctx,name_or_tag):
    #CommandLogs(ctx,'qlash-clan')
    await qlash_cclan(ctx,name_or_tag)

@commands.cooldown(1, 60, commands.BucketType.user)
@util.command(name='set',brief="(UTIL) Get the discord role for the clan you belong to.",description=desc_set)
async def set(ctx,ingame_tag):
    #CommandLogs(ctx,'set')
    await set_(ctx,ingame_tag)

@util.command(name='channels',pass_context=True,brief='(UTIL) Get a list of all channels in the server.')
async def channels(ctx):
    await ChannelList(ctx)

#*****************************************************************************************************************
#**********************************************       MOD     ****************************************************
#*****************************************************************************************************************

#ADMIN
@mod.command(name='bs-playerinfo',brief='(MOD) Search for information about a generic ingame player.',description=desc_bs_playerinfo)
async def bs_pinfo(ctx,player_tag):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    #CommandLogs(ctx,'bs_playerinfo')
    await getplayer(ctx,player_tag)

#ADMIN
@mod.command(name='bs-claninfo',brief='(MOD) Search for information about an ingame clan.',description=desc_bs_claninfo,)
async def bs_cinfo(ctx,clan_tag):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    #CommandLogs(ctx,'bs_claninfo')
    await getclan(ctx,clan_tag)

#ADMIN
@mod.command(name='bs-memberinfo',brief='(MOD) Search for information about a member within a given clan.',description=desc_bs_memberinfo)
async def bs_minfo(ctx,name,clan_tag):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    #CommandLogs(ctx,'bs_memberinfo')
    await search_member(ctx,name,clan_tag)


#ADMIN
@mod.command(name='clan-add',brief='(MOD) Add a qlash clan to the database.',description=desc_clan_add)
async def clan_add(ctx,tag,*clan_name):
    author = ctx.message.author
    if not checkforrole(author, "Moderator", "Sub-Coordinator"):
        await ctx.send("You don't have the permission for this command!")
        return
    #CommandLogs(ctx,'clan-add')
    await clan_add_(ctx,tag,*clan_name)

#ADMIN
@mod.command(name='clan-remove',brief='(MOD) Remove a qlash clan from the database.',description=desc_clann_remove)
async def clan_remove(ctx,*clan_name):
    author = ctx.message.author
    if not checkforrole(author, "Moderator", "Sub-Coordinator"):
        await ctx.send("You don't have the permission for this command!")
        return
    #CommandLogs(ctx,'clan-remove')
    await clan_remove_(ctx,*clan_name)

#ADMIN
@mod.command(name='qlash-clan-members',brief='(MOD) Shows a list of all members of a given QLASH clan.')
async def qlashclanmembers(ctx,clanname_or_tag):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    #CommandLogs(ctx,'qlash-clan-members')
    await GetClanMembers(ctx,clanname_or_tag)

@mod.command(name='locate',brief = '(MOD) Locate an ip address',description=desc_ip)
async def locate(ctx,ip):
    author = ctx.message.author
    if Check(ctx,author):
        await locate_(ctx,ip)
        #CommandLogs(ctx,'locate')
    else:
        #CommandLogs(ctx,'locate (no-success)')
        return

@mod.command(name='member-info',brief='(MOD) Show information of a discord member',description=desc_memberinfo)
async def memberinfo(ctx,member:discord.Member):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    CommandLogs(ctx,'member-info')
    await member_info_(ctx,member)

@mod.command(name="server-info",brief="(MOD) Show information of the server",description=desc_serverinfo)
async def serverinfo(ctx):
    author = ctx.message.author
    if not checkforrole(author, "Moderator", "Sub-Coordinator"):
        await ctx.send("You don't have the permission for this command!")
        return
    #CommandLogs(ctx,'server-info')
    await serverinfo_(ctx)

@mod.command(name='member-dm',pass_context=True,brief='(MOD) Send a private message to a member by the bot.',description=desc_member_dm)
async def dm(ctx,member: discord.Member, *message):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    #CommandLogs(ctx,'member-dm')
    await poke(ctx,member,*message)

@mod.command(name='announce',brief='(MOD) Send a message to a specific channel by the bot.',description=desc_announce)
async def annouce(ctx,channel_name,*message):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    #CommandLogs(ctx,'announce')
    await write_message(ctx,channel_name,*message)

@mod.command(name='refresh-banlist',brief='(MOD) Get members who break the ingame banlist.',description=desc_refresh_banlist)
async def test(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    #CommandLogs(ctx,'refresh-banlist')
    await CheckBanlist(ctx)

@mod.command(name='purge')
async def purge(ctx,amount):
    await purge_(ctx,amount)


@bot.command(name="role-give",hidden=True,pass_context=True)
async def role_give(ctx,member: discord.Member , *rolename):
    #CommandLogs(ctx,'role-give')
    await giverole(ctx,member,*rolename)

@mod.command(name='view-members',brief='TEST')
async def viewmembers(ctx):
    await CompareMembers(ctx)

@mod.command(name='write-members',brief="TEST command to write all members to file")
async def writemembers(ctx):
    await WriteMembersToFile2(ctx)





#schedule.every().minute.at(":17").do(test)
#while schedule_switch==True:
    #schedule.run_pending()

try:
	bot.run(TOKEN)
except discord.errors.LoginFailure as e:
	print("Login unsuccessful.")
