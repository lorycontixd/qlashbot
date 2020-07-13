import brawlstats
import discord
import os
import schedule
import pytz
import random


from modules.mongodb.library import register_commandlog


#import holidayapi

from datetime import datetime
from discord.ext import commands
import bot_commands, bot_events as events
import bot_instances

@bot_instances.bot.event
async def on_ready():
    await events.on_ready_()
    db = bot_instances.mongoclient.heroku_q2z34tjm
    bot = bot_instances.bot
    await bot_commands.init(bot,db)

@bot_instances.bot.event
async def on_disconnect():
    #ch = bot.get_channel(int(bot_developer_channel))
    #messages = ["Logging off, I am.", "The connection, I'm closing down. Hrmmm.", "Gone I am!!", "Signed off, I have. Hrmmm."]
    #await ch.send(random.choice(messages))
    print("Logging off: ",str(bot_instances.bot.user)+" "+str(datetime.now()))

@bot_instances.bot.event
async def on_member_join(member:discord.Member):
    await events.member_join_check(member)
    await events.member_join_welcome(member)

@bot_instances.bot.event
async def on_member_update(before,after):
    await events.on_member_update_role(before,after)
    #await game1_nickname(before,after)
    #await on_member_update_activity(before,after)

@bot_instances.bot.event
async def on_member_ban(guild,user):
    await events.on_member_ban_(guild,user)

@bot_instances.bot.event
async def on_message(message):
    await events.check_bad_words(message)
    await events.check_instarole(message)
    #await insta_role_ended(message)
    await events.check_roles_assignement(message)
    await events.read_file(message)
    await bot_instances.bot.process_commands(message)

@bot_instances.bot.event
async def on_raw_reaction_add(payload):
    await events.reaction_check(payload)
    #await game1_reaction(payload)


#command events
@bot_instances.bot.event
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

@bot_instances.bot.event
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
    bot_instances.bot.run(bot_instances.DISCORD_TOKEN)
except discord.errors.LoginFailure as e:
    print("Login unsuccessful!")
    print("Error: "+str(e))
