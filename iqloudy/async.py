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
from modules.previousscheduler import *
from tasks import check_banlist_channel
from mongodb import view_database
from events import *
from modules import cogs
#from scheduler import *
#from leagues import *

#quotaguard ips = 54.72.12.1, 54.72.77.249
#quotaguard proxy = http://6cy3e5odaiitpe:gxag60u036717xavs35razjk18s2@eu-west-static-03.quotaguard.com:9293

#*****************************************************************************************************************
#*********************************************       EVENTS     **************************************************
#*****************************************************************************************************************
#event_functions = EventFunctions()

@bot.event
async def on_ready():
    await on_ready_()
    await cogs.init_cogs(bot)

@bot.event
async def on_disconnect():
    #ch = bot.get_channel(int(bot_developer_channel))
    #messages = ["Logging off, I am.", "The connection, I'm closing down. Hrmmm.", "Gone I am!!", "Signed off, I have. Hrmmm."]
    #await ch.send(random.choice(messages))
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
    #await check_instarole(message)
    #await insta_role_ended(message)
    await check_roles_assignement(message)
    await read_file(message)
    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    await game1_reaction(payload)


#command events
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
        msg = await ctx.send('PermissionError: You do not have the permissions for this command 😥')
        reason = 'PermissionMissing'
        await msg.delete(delay=4.0)
        await message.delete(delay=6.0)
    elif isinstance(error, commands.errors.UserInputError):
        msg = await ctx.send('ArguementError: Given argument is invalid 😕')
        reason = 'UserInputError'
        await msg.delete(delay=4.0)
        await message.delete(delay=6.0)
    elif isinstance(error, commands.CommandOnCooldown):
        msg = await ctx.send('CommandError: The command is on cooldown 😞')
        reason = 'CommandOnCooldown'
        await msg.delete(delay=4.0)
        await message.delete(delay=6.0)
    elif isinstance(error, commands.CommandNotFound):
        msg = await ctx.send('CommandError: Command was not found 😞')
        reason = 'CommandNotFound'
        await msg.delete(delay=4.0)
        await message.delete(delay=6.0)
    elif isinstance(error, commands.DisabledCommand):
        msg = await ctx.send('CommandError: Command has been disabled')
        reason = 'DisabledCommand'
        await msg.delete(delay=4.0)
        await message.delete(delay=5.0)
    else:
        await ctx.send('ExternalError: '+str(error))
        #await ctx.send(error)
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

#@bot.group(pass_context=True,cog_name="Fun",case_insensitive=True)
#async def fun(ctx):
#        if ctx.invoked_subcommand is None:
#            await ctx.send("Invalid subcommand passed is - Fun ...")

#@bot.group(pass_context=True,cog_name="Mod",case_insensitive=True)
#async def mod(ctx):
#        if ctx.invoked_subcommand is None:
#            await ctx.send("Invalid subcommand passed is - Moderation ...")

#@bot.group(pass_context=True,cog_name="Util",case_insensitive=True)
#async def util(ctx):
#        if ctx.invoked_subcommand is None:
#            await ctx.send("Invalid subcommand passed is - Utility ...")

@bot.group(pass_context=True,cog_name="Sys",case_insensitive=True)
async def sys(ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand passed is - System ...")

#*****************************************************************************************************************
#**********************************************       FUN     ****************************************************
#*****************************************************************************************************************

#@bot.command(name='start')
#async def start(ctx):
#    auth=ctx.message.author
#    await ctx.send(auth.mention+"\nYou are starting the QLASH Brawl stars server treasure hunt. Here are a few rules to follow during the game:\n-> Don't spam channels -> This game doesnt require any kind of spam\n-> Don't ask for answers, only for misunerstandings and translations\n-> Don't use inappropriate channels during the game\n\nHere is the first tip:\n```QLASH reactions are always number 1```")

#*****************************************************************************************************************
#**********************************************       UTILS     **************************************************
#*****************************************************************************************************************

async def invite_(channel):
    link = await channel.create_invite(max_age = 0,max_uses=0)
    await channel.send("Here is an instant invite to your server:  ")
    await channel.send(link)

@commands.cooldown(1, 60, commands.BucketType.channel)
@bot.command(name='hello',brief="Welcomes a user! ",description=desc_hello)
async def welcome(ctx):
    await welcome_(ctx)

@commands.cooldown(1, 60, commands.BucketType.channel)
@bot.command(name='qlash',brief='(UTIL) Display some information about QLASH.',description=
'Display information about the QLASH Organisation, such as their goal, the founders and more...')
async def qlash(ctx):
    await qlash_(ctx)

@commands.cooldown(1,60,commands.BucketType.user)
@bot.command(name='invite',brief="(UTIL) Create an invite")
async def invite(ctx):
    await invite_(ctx.channel)

#To be re-inserted soon
#@commands.cooldown(1, 60, commands.BucketType.channel)
#@commands.command(name='qlash-allclans',hidden=True,brief='(UTIL) (BS30+) List all ingame qlash clans.',description = desc_qlash_allclans)
#async def qlash_allclans(ctx):
#    await qlash_trophies(ctx)

#@commands.cooldown(1,60, commands.BucketType.user)
#@util.command(name='weather-current',brief='(UTIL) Shows current weather for a given city',description=desc_weather_current)
#async def weather_current(ctx,city,country_code):
#    myclass = Weather()
#    await myclass.weather_current_(ctx,city,country_code)

#@commands.cooldown(1,60, commands.BucketType.user)
#@util.command(name='weather-5days',brief='(UTIL) Shows 5-days weather forecase for a city',description=desc_weather_5days)
#async def weather_five_days(ctx,city,country_code):
#    myclass = Weather()
#    await myclass.weather_five_days_(ctx,city,country_code)

@commands.cooldown(1,60,commands.BucketType.channel)
@bot.command(name='bot-info',brief="(UTIL) Shows some details about the bot's development")
async def bot_info(ctx):
    await bot_info_(ctx)

@commands.cooldown(1,60,commands.BucketType.channel)
@bot.command(name='bot-stats',brief='(UTIL) Shows information about QLASH Bot')
async def bot_stats(ctx):
    await bot_stats_(ctx)

#@util.command(name='test_hol')
#async def test_hol(ctx):
#    print(holidays["holidays"])

#*****************************************************************************************************************
#**********************************************       MOD     ****************************************************
#*****************************************************************************************************************
"""
### SET ###
@mod.command(name='set',brief="(MOD)(BS1) Get the discord role for the clan you belong to.",description=desc_set)
async def set(ctx,player:discord.Member,ingame_tag):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await set_(ctx,player,ingame_tag)

#ADMIN
@mod.command(name='bs-playerinfo',brief='(MOD) (BS1) Search for information about a generic ingame player.',description=desc_bs_playerinfo)
async def bs_pinfo(ctx,player_tag):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Clan-Leader","Coordinator"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await getplayer(ctx,player_tag)

#ADMIN
@mod.command(name='bs-claninfo',brief='(MOD) (BS1) Search for information about an ingame clan.',description=desc_bs_claninfo,)
async def bs_cinfo(ctx,clan_tag):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Clan-Leader","Coordinator"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await getclan(ctx,clan_tag)

#ADMIN
@mod.command(name='bs-memberinfo',brief='(MOD) (BS1) Search for information about a member within a given clan.',description=desc_bs_memberinfo)
async def bs_minfo(ctx,name,clan_tag):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Clan-Leader","Coordinator"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
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
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    CommandLogs(ctx,'member-info')
    await member_info_(ctx,member)

@mod.command(name="server-info",brief="(MOD) Show information of the server",description=desc_serverinfo)
async def serverinfo(ctx):
    author = ctx.message.author
    if not checkforrole(author, "Moderator", "Sub-Coordinator"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await serverinfo_(ctx)

@mod.command(name='member-dm',pass_context=True,brief='(MOD) Send a private message to a member by the bot.',description=desc_member_dm)
async def dm(ctx,member: discord.Member, *message):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await poke(ctx,member,*message)

@mod.command(name='announce',brief='(MOD) Send a message to a specific channel by the bot.',description=desc_announce)
async def annouce(ctx,channel_name,*message):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await write_message(ctx,channel_name,*message)

@mod.command(name='welcome',brief='(MOD) Send a welcome message to a specific channel by the bot.')
async def welcome(ctx,channel_name):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await welcome_announcement(ctx,channel_name)

@mod.command(name='purge',brief='(MOD) Clear messages in the channel.',description=desc_purge)
async def purge(ctx,amount):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await purge_(ctx,amount)

@mod.command(name='purge-user',brief="(MOD) Clear all messages from a user inside a give channel")
async def purge_user(ctx,channelname,member:discord.Member):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
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
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await role_count_(ctx,*rolename)

@mod.command(name='all-roles')
async def print_report(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await print_report_(ctx)

@mod.command(name='role-members')
async def print_rolemembers(ctx,*rolename):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await print_rolemembers_(ctx,*rolename)

@mod.command(name='vice-count')
async def vice_(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await vice(ctx)

@mod.command(name="check-banlist",brief="(MOD) Check if banned players are in a QLASH Clan")
async def _banlist(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Coordinator",):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await check_banlist_channel()

@mod.command(name="giova")
async def _giova(ctx):
    await giova()
"""
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
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await view_database(ctx)

@sys.command(name='commandlog-view',hidden=False,brief='(SYS) View the logs of recorded commands',description=desc_commandlog_view)
async def commandlog_view(ctx,limit:int):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await commandlog_view_(ctx,limit)

@sys.command(name='commandlog-clear',hidden=False,brief='(SYS) Clears the log file of recorded commands',description=desc_commandlog_clear)
async def commandlog_clear(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
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
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await clan_add_(ctx,roleID,channelID,tag,*clan_name)

#ADMIN
@sys.command(name='clan-remove',brief='(SYS) Remove a qlash clan from the database.',description=desc_clann_remove)
async def clan_remove(ctx,*clan_name):
    author = ctx.message.author
    if not checkforrole(author, "Moderator", "Sub-Coordinator"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await clan_remove_(ctx,*clan_name)

@sys.command(name='graph-addsingle',brief='(SYS) Add a member count to the database')
async def add_single(ctx,date,membercount):
    author = ctx.message.author
    if not checkforrole(author, "Moderator", "Sub-Coordinator"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await addsingle(ctx,date,membercount)

@sys.command(name='graph-get',brief="(SYS) Get a graph to view member count through the month")
async def graph_get(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await analyze(ctx)

@sys.command(name='graph-reset',brief='(SYS) Clears a graph completely')
async def graph_reset(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await removeall(ctx)

@sys.command(name='graph-today',brief="(SYS) Record today's member count in the database")
async def graph_today(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    await record(ctx)

#********************************* achievements *************************************

@sys.command(name='achievement-add')
async def achievement_add(ctx,*params):
    parameters = " ".join(params[:])
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
        return
    name = achievement_register_(parameters)
    await ctx.send("Achievement '"+str(name)+"' added to the database!")

@sys.command(name='achievement-removeall')
async def achievement_removeall(ctx):
    author = ctx.message.author
    if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
        await ctx.send("Permission to use this command you do not have... Hrmmm...")
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


#@bot.command(name='countstart')
#async def t1(ctx):
#    a = MyCog()

#***************************************************************************************************************
#***************************************************************************************************************
#***************************************************************************************************************
#***************************************************************************************************************


async def mainmenu(ctx,member:discord.Member):
    await member.create_dm()
    message = "```\n---------------------------------------------------------------------\n----------------------------- MAIN MENU -----------------------------\n---------------------------------------------------------------------\n-- 1. QLASH Bot Command Logs\n-- 2. QLASH Clans database\n-- 3. Server Graph database\n\n-- 0. Exit Database```"
    await member.dm_channel.send(message)

async def opt1(ctx,member):
    await member.create_dm()
    message = "```\n-------------------------- COMMAND LOGS ----------------------------\n-- 1. Log Database View\n-- 2. Log Database Clear \n\n-- 0. Exit Database```"
    await member.dm_channel.send(message)

async def opt2(ctx,member):
    await member.create_dm()
    message = "```\n-------------------------- QLASH CLANS -----------------------------\n-- 1. Add new QLASH clan\n-- 2. Remove QLASH Clan\n-- 3. View registered clans \n\n-- 0. Exit Database```"
    await member.dm_channel.send(message)

async def _login(ctx):
    member = ctx.message.author
    await ctx.message.delete()
    sub = discord.utils.get(ctx.message.guild.roles, id=int("604761799505477635"))
    if member.top_role < sub:
        error = await ctx.send("You do not have the permissions to access QLASH Bot's database!")
        await error.delete(delay=5.0)
    await member.create_dm()
    password = "QLASH please"
    await member.dm_channel.send("Please enter the password: ")

    def check(m):
        return m.author == ctx.message.author and type(m.channel)==discord.DMChannel

    reply = await bot.wait_for('message',check=check)
    if reply.content == password:
        await member.dm_channel.send("Access Granted\nWelcome to the QLASH Database "+member.mention+"!")
        asyncio.sleep(1)
        await mainmenu(ctx,member)
        reply1_str = await bot.wait_for('message',check=check)
        reply1_int = int(reply1_str.content)
        numbers = [0,1,2,3]
        if reply1_int not in numbers:
            await member.dm_channel.send("InputError: Invalid option passed. Exiting..")
            return
        else:
            if reply1_int==0:
                await member.dm_channel.send("Exiting")
                return
            elif reply1_int==1:
                await opt1(ctx,member)
                reply2_str = await bot.wait_for('message',check=check)
                reply2_int = int(reply2_str.content)
                if reply2_int not in [0,1,2,3]:
                    await member.dm_channel.send("InputError: Invalid option passed. Exiting..")
                    return
                else:
                    if reply2_int == 0:
                        await member.dm_channel.send("Exiting")
                        return
                    elif reply2_int == 1:
                        await member.dm_channel.send("Option 1 still to be implemented")
                        return
                    elif reply2_int == 2:
                        await member.dm_channel.send("Option 1 still to be implemented")
                        return
                    elif reply2_int == 3:
                        await view_database(ctx,member)
                        return
            elif reply1_int==2:
                await opt2(ctx,member)
            elif reply1_int==3:
                await member.dm_channel.send("Option 3 still to be implemented")
                return
    else:
        await member.dm_channel.send("Wrong password")
        return



@bot.command(name='main-menu')
async def login(ctx):
    await _login(ctx)



try:
    bot.run(DISCORD_TOKEN)
except discord.errors.LoginFailure as e:
	print("Login unsuccessful was.")
