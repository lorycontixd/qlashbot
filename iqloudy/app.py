import brawlstats
import discord
import os
import schedule
import pytz
import random

from modules.mongodb import library as mongo

#import holidayapi

from datetime import datetime
from discord.ext import commands
import bot_commands, bot_events as events
import bot_instances
from modules.voice_system import library as voice

@bot_instances.bot.event
async def on_ready():
    await events.on_ready_()
    db = bot_instances.mongoclient.heroku_q2z34tjm
    bot = bot_instances.bot
    qlash_bs = bot_instances.qlash_bs
    await bot_commands.init(bot,db,qlash_bs)

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
    pass
    #await events.on_member_update_role(before,after)
    #await game1_nickname(before,after)
    #await on_member_update_activity(before,after)

@bot_instances.bot.event
async def on_member_ban(guild,user):
    await events.on_member_ban_(guild,user)

@bot_instances.bot.event
async def on_message(message):
    await events.check_bad_words(message)
    await events.caps_spam_check(message)
    #await events.msg_spam_check(message)
    await events.check_instarole(message)
    #await insta_role_ended(message)
    await events.check_roles_assignement(message)
    await events.read_file(message)
    await bot_instances.bot.process_commands(message)

@bot_instances.bot.event
async def on_raw_reaction_add(payload):
    await events.reaction_check(payload)
    #await game1_reaction(payload)

#Voice state change for VoiceSystem

@bot_instances.bot.event
async def on_guild_channel_create(channel):
    if isinstance(channel,discord.VoiceChannel):
        if channel.category_id == bot_instances.id_category_protectedrooms:
            pass

@bot_instances.bot.event
async def on_voice_state_update(member,before,after):
    """
    Parameters:
        - member (Member) – The member whose voice states changed.
        - before (VoiceState) – The voice state prior to the changes.
        - after (VoiceState) – The voice state after to the changes.
    """
    m_voice = mongo.MongoVoiceSystem()
    voicesystem = voice.VoiceSystem()
    waitingroom = bot_instances.bot.get_channel(int(bot_instances.waitingroom))
    ch1 = bot_instances.bot.get_channel(int(bot_instances.voice_ch1))
    iqloudylogs = bot_instances.bot.get_channel(int(bot_instances.qlash_bot))
    if before.channel == None:
        return

    if before.channel.id in bot_instances.voice_ids and before.channel!=waitingroom:
        if len(before.channel.members)==0:
            ch_id = before.channel.id
            doc = m_voice.get_voicechannel(ch_id)
            if doc == None:
                return
            m_voice.remove_voicechannel(ch_id)
            await before.channel.edit(bitrate=64000)
            e = discord.Embed(title="VocalRoom has been deleted from the database: "+str(before.channel.name), color=discord.Color.dark_gold())
            e.set_author(name="QLASH Bot")
            e.add_field(name="Channel",value=str(before.channel.name))
            e.add_field(name="Host",value=str(doc["CreatedBy"]))
            e.add_field(name="Password",value=str(doc["Password"]))
            e.add_field(name="Created At",value=str(doc["CreatedAt"]))
            e.set_footer(text="Created by Lore.")
            await iqloudylogs.send(embed=e)
            
            room = m_voice.get_room(before.channel.id)
            print(room["Name"]," ",room["ID"]," ",room["Type"])
            if room["Type"] == "Extra":
                print(room["Name"]+" is extra. removing")
                await before.channel.delete(reason="VoiceRoom Extra was cleared.")
                m_voice.delete_voiceroom(before.channel.id)
                voicesystem.channels.remove(before.channel)

"""
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
    m_comm = mongo.MongoCommandLogs
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
        await ctx.send('CommandError: Command was not found 😞')
        return
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send('CommandError: Command has been disabled')
        return
    
    else:
        await ctx.send('ExternalError!')
    #    #await ctx.send(error)
        reason = 'ExternalError'
    await ctx.send("Error: "+str(error))
    m_comm.register_commandlog(str(author),str(commandname),str(time),str(failed),reason)
    #CommandLogs(ctx,commandname+'(failed: '+reason+')')
"""
@bot_instances.bot.event
async def on_command_completion(ctx):

    commandname = ctx.invoked_with
    author = ctx.message.author
    tz = pytz.timezone('Europe/Rome')
    nnow = datetime.now(tz=tz)
    time = nnow.strftime("%d/%m/%Y %H:%M:%S")
    reason = 'None'
    failed=False
    mongo.MongoCommandLogs().register_commandlog(str(author),str(commandname),str(time),str(failed),reason)
    #CommandLogs(ctx,commandname)

try:
    bot_instances.bot.run(bot_instances.DISCORD_TOKEN)
except discord.errors.LoginFailure as e:
    print("Login unsuccessful!")
