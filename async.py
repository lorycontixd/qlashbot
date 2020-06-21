import brawlstats
import discord
import os
import schedule
import random
import requests
import urllib
#import holidayapi

from urllib.request import Request, urlopen
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from functions import *
#from scheduler import *
#from leagues import *

#quotaguard ips = 54.72.12.1, 54.72.77.249
#quotaguard proxy = http://6cy3e5odaiitpe:gxag60u036717xavs35razjk18s2@eu-west-static-03.quotaguard.com:9293

#*****************************************************************************************************************
#*********************************************       EVENTS     **************************************************
#*****************************************************************************************************************

@bot.event
async def on_ready():
    ch = instances.bot.get_channel(int(bot_developer_channel))
    messages = ["Here I am. Hrmmm.", "Up and runnning I am.", "Hello again! I'm here. Yes. Hrmmmm.", "Back on track, I am."]
    await ch.send(random.choice(messages))
    await on_ready_()

@bot.event
async def on_disconnect():
    ch = bot.get_channel(int(bot_developer_channel))
    messages = ["Logging off, I am.", "The connection, I'm closing down. Hrmmm.", "Gone I am!!", "Signed off, I have. Hrmmm."]
    await ch.send(random.choice(messages))
    print("Logging off: ",str(bot.user)+" "+str(datetime.now()))
    #mych = await bot.fetch_channel(int(bot_testing))
    #await mych.send("Bot has logged off 🔴")

@bot.event
async def on_member_join(member:discord.Member):
    await member_join_check(member)
    await member_join_welcome(member)

@bot.event
async def on_member_update(before,after):
    await on_member_update_role(before,after)
    await game1_nickname(before,after)
    #await on_member_update_activity(before,after)

@bot.event
async def on_message(message):
    await check_bad_words(message)
    await check_instarole(message)
    #await insta_role_ended(message)
    await check_roles_assignement(message)
    await read_file(message)
    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    await game1_reaction(payload)



@bot.event
async def on_command_error(ctx, error):
    commandname = ctx.invoked_with
    author = ctx.message.author
    message = ctx.message
    tz = pytz.timezone('Europe/Rome')
    nnow = datetime.now(tz=tz)
    time = nnow.strftime("%d/%m/%Y %H:%M:%S")
    reason = ''
    failed=True
    if isinstance(error, commands.errors.CheckFailure):
        msg = await ctx.send('PermissionError: Have the correct permissions for this command you do not. 😥')
        reason = 'PermissionMissing'
        await msg.delete(delay=4.0)
        await message.delete(delay=5.0)
    elif isinstance(error, commands.errors.UserInputError):
        msg = await ctx.send('ArguementError: Given argument bad was.. 😕')
        reason = 'UserInputError'
        await msg.delete(delay=4.0)
        await message.delete(delay=5.0)
    elif isinstance(error, commands.CommandOnCooldown):
        msg = await ctx.send('CommandError: On cooldown the command is. 😞')
        reason = 'CommandOnCooldown'
        await msg.delete(delay=4.0)
        await message.delete(delay=5.0)
    elif isinstance(error, commands.CommandNotFound):
        msg = await ctx.send('CommandError: Found command was not. 😞')
        reason = 'CommandNotFound'
        await msg.delete(delay=4.0)
        await message.delete(delay=5.0)
    elif isinstance(error, commands.DisabledCommand):
        msg = await ctx.send('Hrmmm... Disabled this command has been.')
        reason = 'DisabledCommand'
        await msg.delete(delay=4.0)
        await message.delete(delay=5.0)
    else:
        await ctx.send('Something unxpected we got... Hrmmm...')
        await ctx.send(error)
        reason = 'ExternalError'
    register_commandlog(str(author),str(commandname),str(time),str(failed),reason)
    #CommandLogs(ctx,commandname+'(failed: '+reason+')')

@bot.event
async def on_command_completion(ctx):
    commandname = ctx.invoked_with
    author = ctx.message.author
    tz = pytz.timezone('Europe/Rome')
    nnow = datetime.now(tz=tz)
    time = nnow.strftime("%d/%m/%Y %H:%M:%S")
    reason = 'None'
    failed=False
    register_commandlog(str(author),str(commandname),str(time),str(failed),reason)
    #CommandLogs(ctx,commandname)

#*****************************************************************************************************************
#*******************************************       GROUPS     ****************************************************
#*****************************************************************************************************************

@bot.group(pass_context=True,cog_name="Fun",case_insensitive=True)
async def fun(ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand passed was - Fun ...")

@bot.group(pass_context=True,cog_name="Mod",case_insensitive=True)
async def mod(ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand passed was - Moderation ...")

@bot.group(pass_context=True,cog_name="Util",case_insensitive=True)
async def util(ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand passed was - Utility ...")

@bot.group(pass_context=True,cog_name="Sys",case_insensitive=True)
async def sys(ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand passed was - System ...")

#*****************************************************************************************************************
#**********************************************       FUN     ****************************************************
#*****************************************************************************************************************

@bot.command(name='start')
async def start(ctx):
    auth=ctx.message.author
    await ctx.send(auth.mention+"\nYou are starting the QLASH Brawl stars server treasure hunt. Here are a few rules to follow during the game:\n-> Don't spam channels -> This game doesnt require any kind of spam\n-> Don't ask for answers, only for misunerstandings and translations\n-> Don't use inappropriate channels during the game\n\nHere is the first tip:\n```QLASH reactions are always number 1```")

@commands.cooldown(1, 30, commands.BucketType.user)
@fun.command(name='roll',brief='(FUN) Roll a 6 sided dice.',description='Fun Command \n 30 seconds cooldown per user \n \n'
+'Roll a 6 sided dice to get a random number from 1 to 6.')
async def roll(ctx):
    try:
        await roll_(ctx)
    except:
        print("Failed")

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

@commands.cooldown(1,30,commands.BucketType.channel)
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

@commands.cooldown(1,60,commands.BucketType.user)
@util.command(name='invite',brief="(UTIL) Create an invite")
async def invite(ctx):
    await invite_(ctx)

@commands.cooldown(1, 60, commands.BucketType.channel)
@util.command(name='qlash-allclans',hidden=True,brief='(UTIL) (BS30+) List all ingame qlash clans.',description = desc_qlash_allclans)
async def qlash_allclans(ctx):
    await qlash_trophies(ctx)

@commands.cooldown(1,60,commands.BucketType.user)
@util.command(name='channels',pass_context=True,brief='(UTIL) Get a list of all channels in the server.',description=desc_channels)
async def channels(ctx):
    await ChannelList(ctx)

@commands.cooldown(1, 60, commands.BucketType.channel)
@bot.command(name='hello',brief="Welcomes a user! ",description=desc_hello)
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

@commands.cooldown(1,30,commands.BucketType.channel)
@util.command(name='bot-info',brief="(UTIL) Shows some details about the bot's development")
async def bot_info(ctx):
    await bot_info_(ctx)

@commands.cooldown(1,60,commands.BucketType.channel)
@util.command(name='bot-stats',brief='(UTIL) Shows information about QLASH Bot')
async def bot_stats(ctx):
    await bot_stats_(ctx)

#@util.command(name='test_hol')
#async def test_hol(ctx):
#    print(holidays["holidays"])

#*****************************************************************************************************************
#**********************************************       MOD     ****************************************************
#*****************************************************************************************************************

### SET ###
@mod.command(name='set',brief="(MOD)(BS1) Get the discord role for the clan you belong to.",description=desc_set)
async def set(ctx,player:discord.Member,ingame_tag):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await set_(ctx,player,ingame_tag)

#ADMIN
@mod.command(name='bs-playerinfo',brief='(MOD) (BS1) Search for information about a generic ingame player.',description=desc_bs_playerinfo)
async def bs_pinfo(ctx,player_tag):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Clan-Leader","Coordinator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await getplayer(ctx,player_tag)

#ADMIN
@mod.command(name='bs-claninfo',brief='(MOD) (BS1) Search for information about an ingame clan.',description=desc_bs_claninfo,)
async def bs_cinfo(ctx,clan_tag):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Clan-Leader","Coordinator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await getclan(ctx,clan_tag)

#ADMIN
@mod.command(name='bs-memberinfo',brief='(MOD) (BS1) Search for information about a member within a given clan.',description=desc_bs_memberinfo)
async def bs_minfo(ctx,name,clan_tag):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Clan-Leader","Coordinator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await search_member(ctx,name,clan_tag)

@mod.command(name='locate',brief = '(MOD) Locate an ip address',description=desc_ip)
async def locate(ctx,ip):
    author = ctx.message.author
    if await Check(ctx,author):
        await locate_(ctx,ip)
    else:
        return

@mod.command(name='member-info',brief='(MOD) Show information of a discord member',description=desc_memberinfo)
async def memberinfo(ctx,member:discord.Member):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Clan-Leader","Coordinator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    CommandLogs(ctx,'member-info')
    await member_info_(ctx,member)

@mod.command(name="server-info",brief="(MOD) Show information of the server",description=desc_serverinfo)
async def serverinfo(ctx):
    author = ctx.message.author
    if not checkforrole(author, "Moderator", "Sub-Coordinator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await serverinfo_(ctx)

@mod.command(name='member-dm',pass_context=True,brief='(MOD) Send a private message to a member by the bot.',description=desc_member_dm)
async def dm(ctx,member: discord.Member, *message):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await poke(ctx,member,*message)

@mod.command(name='announce',brief='(MOD) Send a message to a specific channel by the bot.',description=desc_announce)
async def annouce(ctx,channel_name,*message):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await write_message(ctx,channel_name,*message)

@mod.command(name='welcome',brief='(MOD) Send a welcome message to a specific channel by the bot.')
async def welcome(ctx,channel_name):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await welcome_announcement(ctx,channel_name)

@mod.command(name='refresh-banlist',brief='(MOD) (BS~) Get members who break the ingame banlist.',description=desc_refresh_banlist)
async def test(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await CheckBanlist(ctx)

@mod.command(name='purge',brief='(MOD) Clear messages in the channel.',description=desc_purge)
async def purge(ctx,amount):
    await purge_(ctx,amount)

@mod.command(name='purge-user',brief="(MOD) Clear all messages from a user inside a give channel")
async def purge_user(ctx,channelname,member:discord.Member):
    await purge_user_(ctx,channelname,member)

@mod.command(name="role-give",hidden=True,pass_context=True)
async def role_give(ctx,member: discord.Member , *rolename):
    await giverole(ctx,member,*rolename)

@mod.command(name="role-remove",hidden=True,pass_context=True)
async def role_rem(ctx,member: discord.Member , *rolename):
    await removerole(ctx,member,*rolename)

@mod.command(name='role-count')
async def role_count(ctx,*rolename):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await role_count_(ctx,*rolename)

@mod.command(name='all-roles')
async def print_report(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await print_report_(ctx)

@mod.command(name='role-members')
async def print_rolemembers(ctx,*rolename):
    if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await print_rolemembers_(ctx,*rolename)

@mod.command(name='view-members',brief='(MOD) (BS30+) Get a list of players that left ingame clubs.',description=desc_view_members )
async def viewmembers(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await CompareMembers(ctx)

@mod.command(name='write-members',brief="(MOD) (BS30+) Write all clan members to database",description=desc_write_members)
async def writemembers(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await WriteMembersToFile2(ctx)


#*****************************************************************************************************************
#**********************************************       SYS     ****************************************************
#*****************************************************************************************************************

@sys.command(name='audit-view')
async def get_audit_logs(ctx,member:discord.Member):
    await get_audit_logs_(ctx,member)

@sys.command(name='database-view',hidden=False,brief='(SYS) View registered QLASH clans',description=desc_database_view)
async def view_database_(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await view_database(ctx)

@sys.command(name='commandlog-view',hidden=False,brief='(SYS) View the logs of recorded commands',description=desc_commandlog_view)
async def commandlog_view(ctx,limit:int):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await commandlog_view_(ctx,limit)

@sys.command(name='commandlog-clear',hidden=False,brief='(SYS) Clears the log file of recorded commands',description=desc_commandlog_clear)
async def commandlog_clear(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await commandlog_clear_(ctx)

#@sys.command(name='registry-view')
#async def registry_view(ctx):
#    author = ctx.message.author
#    if not checkforrole(author,"Sub-Coordinator","Moderator"):
#        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
#        return
#    await registry_view_(ctx)

#ADMIN
@sys.command(name='clan-add',brief='(SYS) Add a qlash clan to the database.',description=desc_clan_add)
async def clan_add(ctx,roleID,channelID,tag,*clan_name):
    author = ctx.message.author
    if not checkforrole(author, "Moderator", "Sub-Coordinator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await clan_add_(ctx,roleID,channelID,tag,*clan_name)

#ADMIN
@sys.command(name='clan-remove',brief='(SYS) Remove a qlash clan from the database.',description=desc_clann_remove)
async def clan_remove(ctx,*clan_name):
    author = ctx.message.author
    if not checkforrole(author, "Moderator", "Sub-Coordinator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await clan_remove_(ctx,*clan_name)

@sys.command(name='graph-addsingle',brief='(SYS) Add a member count to the database')
async def add_single(ctx,date,membercount):
    author = ctx.message.author
    if not checkforrole(author, "Moderator", "Sub-Coordinator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await addsingle(ctx,date,membercount)

@sys.command(name='graph-get',brief="(SYS) Get a graph to view member count through the month")
async def graph_get(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await analyze(ctx)

@sys.command(name='graph-reset',brief='(SYS) Clears a graph completely')
async def graph_reset(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await removeall(ctx)

@sys.command(name='graph-today',brief="(SYS) Record today's member count in the database")
async def graph_today(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    await record(ctx)

@sys.command(name='vice-count')
async def vice_(ctx):
    await vice(ctx)
#********************************* achievements *************************************

@sys.command(name='achievement-add')
async def achievement_add(ctx,*params):
    parameters = " ".join(params[:])
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    name = achievement_register_(parameters)
    await ctx.send("Achievement '"+str(name)+"' added to the database!")

@sys.command(name='achievement-removeall')
async def achievement_removeall(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return
    achievement_removeall_(ctx)
    await ctx.send("All achievements were removed from the database")

#********************************* tournaments *************************************

#@bot.command(name='tournament-members')
#async def get_tournament_members_(ctx,tournament_role):
#    await get_tournament_members(ctx,tournament_role)

#to write all members on a google spreadsheet
#@bot.command(name='writeall')
#async def writeall_(ctx):
#    await writeall(ctx)

#@bot.command(name='test-getleague')
#async def getleague(ctx,player:discord.Member):
#    await get_player_league(ctx,player)

#@bot.command(name='test-addpoints')
#async def addpoints(ctx,player):


@bot.command(name='countstart')
async def t1(ctx):
    a = MyCog()




try:
    bot.run(DISCORD_TOKEN)
except discord.errors.LoginFailure as e:
	print("Login unsuccessful was.")
