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
from modules.util_functions import *
from modules.util_mongodb import view_database
from modules import cogs
import events
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
    await events.on_ready_()
    db = instances.mongoclient.heroku_q2z34tjm
    await cogs.init_cogs(bot,db)

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
    await events.member_join_check(member)
    await events.member_join_welcome(member)

@bot.event
async def on_member_update(before,after):
    await events.on_member_update_role(before,after)
    #await game1_nickname(before,after)
    #await on_member_update_activity(before,after)

@bot.event
async def on_message(message):
    await events.check_bad_words(message)
    #await check_instarole(message)
    #await insta_role_ended(message)
    await events.check_roles_assignement(message)
    await read_file(message)
    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    await events.reaction_check(payload)
    #await game1_reaction(payload)


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

try:
    bot.run(DISCORD_TOKEN)
except discord.errors.LoginFailure as e:
	print("Login unsuccessful was.")