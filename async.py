import brawlstats
import discord
import os
import schedule
import random
import requests
import urllib

from urllib.request import Request, urlopen
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from utility import *
from functions import *
from descriptions import *
from weather import *
from checks import *


DISCORD_TOKEN = 'NzAxMTI1MzExMDQ3NDAxNDc0.XpyBZQ.RAsYlvnkrzI08mwFuXK8QF5K3BM'

#quotaguard ips = 54.72.12.1, 54.72.77.249
#quotaguard proxy = http://6cy3e5odaiitpe:gxag60u036717xavs35razjk18s2@eu-west-static-03.quotaguard.com:9293

#*****************************************************************************************************************
#*********************************************       EVENTS     **************************************************
#*****************************************************************************************************************

@bot.event
async def on_ready():
    await on_ready_()


@bot.event
async def on_disconnect():
    print("Logging off: ",bot.user)
    #mych = await bot.fetch_channel(int(bot_testing))
    #await mych.send("Bot has logged off 🔴")

@bot.event
async def on_member_join(member:discord.Member):
    await member_join_check(member)

#@bot.event
#async def on_member_join(member:discord.Member):
#    channel = bot.get_channel(int(entries_discord))
#    await member.create_dm()
#    text = "Hello and welcome to the QLASH Brawl Stars server. Please read the rules before you start interacting with other people. \nI kindly ask you to write your brawl stars game tag here."
#    msg = await member.dm_channel.send(text)
#    def check(message):
#        return message.channel.type == discord.ChannelType.private
#    reply = await bot.wait_for('message', check=check)
#    content = str(reply.content)
#    while not content.startswith('#'):
#        await member.dm_channel.send("You entered a wrong gametag, please send it again")
#        reply = await bot.wait_for('message', check=check)
#        content = str(reply.content)
#    await member.dm_channel.send("Thank you very much for the response. Please have fun in our friendly server! 😊")
#    await channel.send( "Registered: "+str(member)+'\t'+str(content)+'\t'+str(datetime.now()) )


@bot.event
async def on_message(message):
    await check_bad_words(message)

@bot.event
async def on_command_error(ctx, error):
    commandname = ctx.invoked_with
    reason = ''
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('PermissionError: You do not have the correct permissions for this command. 😥')
        reason = 'PermissionMissing'
    elif isinstance(error, commands.errors.UserInputError):
        await ctx.send('ArguementError: Bad arguement was given. 😕')
        reason = 'UserInputError'
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send('CommandError: Command is on cooldown. 😞')
        reason = 'CommandOnCooldown'
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('CommandError: Command was not found. 😞')
        reason = 'CommandNotFound'
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send('This command has been disabled.')
        reason = 'DisabledCommand'
    #else:
    #    await ctx.send('We got something unexpected...')
    #    await ctx.send(error)
    #    reason = 'ExternalError'
    CommandLogs(ctx,commandname+'(failed: '+reason+')')

@bot.event
async def on_command_completion(ctx):
    mychannel = bot.get_channel(int(bot_testing))
    commandname = ctx.invoked_with
    CommandLogs(ctx,commandname)

#*****************************************************************************************************************
#*******************************************       GROUPS     ****************************************************
#*****************************************************************************************************************

@bot.group(pass_context=True,cog_name="Fun",case_insensitive=True)
async def fun(ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand passed - Fun ...")

@bot.group(pass_context=True,cog_name="Mod",case_insensitive=True)
async def mod(ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand passed - Moderation ...")

@bot.group(pass_context=True,cog_name="Util",case_insensitive=True)
async def util(ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand passed - Utility ...")

@bot.group(pass_context=True,cog_name="Sys",case_insensitive=True)
async def sys(ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand passed - System ...")

#*****************************************************************************************************************
#**********************************************       FUN     ****************************************************
#*****************************************************************************************************************

@commands.cooldown(1, 30, commands.BucketType.user)
@fun.command(name='roll',brief='(FUN) Roll a 6 sided dice.',description='Fun Command \n 30 seconds cooldown per user \n \n'
+'Roll a 6 sided dice to get a random number from 1 to 6.')
async def roll(ctx):
    await roll_(ctx)

#BucketType.user can be changed to default: global ratelimit, channel: channel ratelimit, guild: server ratelimit, user: user ratelimit /for that command

@commands.cooldown(1, 30, commands.BucketType.user)
@fun.command(name='ping',brief = '(FUN) Pong! 🏓',description='Fun Command \n 30 seconds cooldown per user \n \nNothing to describe. Play some Ping Pong with the Bot')
async def ping(ctx):
    response='pong 🏓'
    await ctx.send(response)

@commands.cooldown(1, 30, commands.BucketType.user)
@fun.command(name='coin-flip',brief='(FUN) Flip a coin',pass_context = True,description=desc_coinflip)
async def coin_flip(ctx):
    flip = random.choice(['Heads','Tails'])
    await ctx.channel.send('You flipped '+flip)

@commands.cooldown(1, 50, commands.BucketType.guild)
@fun.command(name='table-flip',brief='(FUN) Flip that table!!',description="Flip that table!!  50 seconds cooldown in the server")
async def flip_(ctx):
    await flip(ctx)

@commands.cooldown(1, 50, commands.BucketType.guild)
@fun.command(name='table-unflip',brief='(FUN) Unflip that table!!',description="Unflip that table!!  50 seconds cooldown in the server")
async def unflip_(ctx):
    await unflip(ctx)

@commands.cooldown(1, 50, commands.BucketType.guild)
@fun.command(name='table-status',brief="(FUN) Check table's status",desciption=desc_tstatus)
async def tstatus_(ctx):
    await tstatus(ctx)

@commands.cooldown(1,60,commands.BucketType.channel)
@fun.command(name='bs-puns',brief='Post a random and very funny pun about Brawl Stars',description=desc_bs_puns)
async def bs_puns(ctx):
    await bs_puns_(ctx)

#*****************************************************************************************************************
#**********************************************       UTILS     **************************************************
#*****************************************************************************************************************

@commands.cooldown(1, 60, commands.BucketType.channel)
@util.command(name='qlash',brief='(UTIL) Display some information about QLASH.',description=
'Display information about the QLASH Organisation, such as their goal, the founders and more...')
async def qlash(ctx):
    await qlash_(ctx)

@commands.cooldown(1, 60, commands.BucketType.channel)
@util.command(name='qlash-allclans',hidden=True,brief='(UTIL) (BS30+) List all ingame qlash clans.',description = desc_qlash_allclans)
async def qlash_allclans(ctx):
    await qlash_trophies(ctx)

@commands.cooldown(1, 60, commands.BucketType.channel)
@util.command(name='qlash-clan',hidden=True,brief="(UTIL)(BS1) Search for information about a specific QLASH clan.",description=desc_qlash_clan)
async def qlash_clan(ctx,name_or_tag):
    await qlash_cclan(ctx,name_or_tag)

@commands.cooldown(1, 60, commands.BucketType.user)
@util.command(name='set',brief="(UTIL)(BS1) Get the discord role for the clan you belong to.",description=desc_set)
async def set(ctx,ingame_tag):
    await set_(ctx,ingame_tag)

@commands.cooldown(1,60,commands.BucketType.user)
@util.command(name='channels',pass_context=True,brief='(UTIL) Get a list of all channels in the server.',description=desc_channels)
async def channels(ctx):
    await ChannelList(ctx)

@commands.cooldown(1, 60, commands.BucketType.channel)
@util.command(name='hello',brief="(UTIL) Welcomes a user! ",description=desc_hello)
async def welcome(ctx):
    await welcome_(ctx)

@commands.cooldown(1,60, commands.BucketType.user)
@util.command(name='weather-current',brief='(UTIL) Shows current weather for a given city',description=desc_weather_current)
async def weather_current(ctx,city,country_code):
    await weather_current_(ctx,city,country_code)

@commands.cooldown(1,60, commands.BucketType.user)
@util.command(name='weather-5days',brief='(UTIL) Shows 5-days weather forecase for a city',description=desc_weather_5days)
async def weather_five_days(ctx,city,country_code):
    await weather_five_days_(ctx,city,country_code)
#*****************************************************************************************************************
#**********************************************       MOD     ****************************************************
#*****************************************************************************************************************

#ADMIN
@mod.command(name='bs-playerinfo',brief='(MOD) (BS1) Search for information about a generic ingame player.',description=desc_bs_playerinfo)
async def bs_pinfo(ctx,player_tag):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    await getplayer(ctx,player_tag)

#ADMIN
@mod.command(name='bs-claninfo',brief='(MOD) (BS1) Search for information about an ingame clan.',description=desc_bs_claninfo,)
async def bs_cinfo(ctx,clan_tag):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    await getclan(ctx,clan_tag)

#ADMIN
@mod.command(name='bs-memberinfo',brief='(MOD) (BS1) Search for information about a member within a given clan.',description=desc_bs_memberinfo)
async def bs_minfo(ctx,name,clan_tag):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    await search_member(ctx,name,clan_tag)


#ADMIN
@mod.command(name='clan-add',brief='(MOD) Add a qlash clan to the database.',description=desc_clan_add)
async def clan_add(ctx,tag,*clan_name):
    author = ctx.message.author
    if not checkforrole(author, "Moderator", "Sub-Coordinator"):
        await ctx.send("You don't have the permission for this command!")
        return
    await clan_add_(ctx,tag,*clan_name)

#ADMIN
@mod.command(name='clan-remove',brief='(MOD) Remove a qlash clan from the database.',description=desc_clann_remove)
async def clan_remove(ctx,*clan_name):
    author = ctx.message.author
    if not checkforrole(author, "Moderator", "Sub-Coordinator"):
        await ctx.send("You don't have the permission for this command!")
        return
    await clan_remove_(ctx,*clan_name)

#ADMIN
@mod.command(name='qlash-clan-members',brief='(MOD) (BS1) Shows a list of all members of a given QLASH clan.')
async def qlashclanmembers(ctx,clanname_or_tag):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    await GetClanMembers(ctx,clanname_or_tag)

@mod.command(name='locate',brief = '(MOD) Locate an ip address',description=desc_ip)
async def locate(ctx,ip):
    author = ctx.message.author
    if Check(ctx,author):
        await locate_(ctx,ip)
    else:
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
    await serverinfo_(ctx)

@mod.command(name='member-dm',pass_context=True,brief='(MOD) Send a private message to a member by the bot.',description=desc_member_dm)
async def dm(ctx,member: discord.Member, *message):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    await poke(ctx,member,*message)

@mod.command(name='announce',brief='(MOD) Send a message to a specific channel by the bot.',description=desc_announce)
async def annouce(ctx,channel_name,*message):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    await write_message(ctx,channel_name,*message)

@mod.command(name='refresh-banlist',brief='(MOD) (BS~) Get members who break the ingame banlist.',description=desc_refresh_banlist)
async def test(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    await CheckBanlist(ctx)

@mod.command(name='purge',brief='(MOD) Clear messages in the channel.',description=desc_purge)
async def purge(ctx,amount):
    await purge_(ctx,amount)


@bot.command(name="role-give",hidden=True,pass_context=True)
async def role_give(ctx,member: discord.Member , *rolename):
    await giverole(ctx,member,*rolename)

@mod.command(name='view-members',brief='(MOD) (BS30+) Get a list of players that left ingame clubs.',description=desc_view_members )
async def viewmembers(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    await CompareMembers(ctx)

@mod.command(name='write-members',brief="(MOD) (BS30+) Write all clan members to database",description=desc_write_members)
async def writemembers(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    await WriteMembersToFile2(ctx)

#*****************************************************************************************************************
#**********************************************       SYS     ****************************************************
#*****************************************************************************************************************


@sys.command(name='database-view',hidden=False,brief='(SYS) View registered QLASH clans',description=desc_database_view)
async def view_database_(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    await view_database(ctx)

@sys.command(name='commandlog-view',hidden=False,brief='(SYS) View the logs of recorded commands',description=desc_commandlog_view)
async def commandlog_view(ctx,limit:int):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    await commandlog_view_(ctx,limit)

@sys.command(name='commandlog-clear',hidden=False,brief='(SYS) Clears the log file of recorded commands',description=desc_commandlog_clear)
async def commandlog_clear(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("You don't have the permission for this command!")
        return
    await commandlog_clear_(ctx)

@sys.command(name='maintainance',brief='(SYS) Close the Bot for maintainance purposes')
async def maintainance(ctx):
    mychannel = bot.get_channel(int(bot_testing))
    botdev = discord.utils.get(ctx.guild.roles, name='BotDeveloper')
    if not Check(ctx,ctx.message.author):
        await ctx.send("You do not have permissions for this command!")
        return
    await mychannel.send("Bot is closing for maintainance. If you need support, please contact a "+botdev.mention)
    await bot.logout()

try:
	bot.run(DISCORD_TOKEN)
except discord.errors.LoginFailure as e:
	print("Login unsuccessful.")
