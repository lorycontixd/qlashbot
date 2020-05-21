import brawlstats
#import logging
import discord
import os
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from functions import *
import os
from urllib.request import Request, urlopen
apiinvestigator_key = '809O044FN563WZ7IXJTMLP1U63G1HEQ2R8VC7S9KABYD52'
request = Request('https://ipinvestigator.expeditedaddons.com/?api_key=' + os.environ[apiinvestigator_key] + '&ip=68.10.149.45')

response_body = urlopen(request).read()
print(response_body)

bot = commands.Bot(command_prefix='^' , description = "Qlash Bot ")
#myclient = brawlstats.Client(TOKEN2,is_async=True)
#*********************************** CHANNELS ********************************************
botconfig = '450694573161709569'
itgeneral = '415221650481610762'

#*****************************************************************************************

@bot.event
async def on_ready():
    print('Logged in as: ',bot.user.name)
    print('Bot ID: ',bot.user.id)
    print('----------------')
    await bot.change_presence( activity=discord.Activity(type=discord.ActivityType.playing, name=" ^help"))

@bot.event
async def on_message(message):
    print("New Message in "+str(message.channel)+", author: "+str(message.author))
    roles_channel = bot.get_channel(int(bot_testing))
    if message.channel == roles_channel:
        if not message.content.startswith('^set'):
            if not message.attachments:
                if not message.author.bot:
                    await message.delete()
                    message2 = await roles_channel.send("No allowed messages apart from set commands. If you need support please write in the support channel or contact our staff.")
                    await message2.delete(delay=4.0)
    await bot.process_commands(message)

#***********************************  FUN  ***********************************************
@commands.cooldown(1, 20, commands.BucketType.user)
@bot.command(name='roll')
async def roll(ctx):
    await roll_(ctx)

#BucketType.user can be changed to default: global ratelimit, channel: channel ratelimit, guild: server ratelimit, user: user ratelimit /for that command
#*****************************************************************************************
@commands.cooldown(1, 20, commands.BucketType.user)
@bot.command(name='qlash')
async def qlash(ctx):
    await qlash_(ctx)

@bot.command(name='bs-playerinfo',brief='Search for information about a generic ingame player.')
async def bs_pinfo(ctx,tag):
    await getplayer(ctx,tag)

@bot.command(name='bs-claninfo',brief='Search for information about an ingame clan.')
async def bs_cinfo(ctx,tag):
    await getclan(ctx,tag)

@bot.command(name='bs-memberinfo',brief='Search for information about a member within a given clan.')
async def bs_minfo(ctx,name,ctag):
    await search_member(ctx,name,ctag)

@bot.command(name='qlash-allclans',brief='List all ingame qlash clans.')
async def qlash_allclans(ctx):
    await qlash_trophies(ctx)

@bot.command(name='qlash-clan',brief="Search for information about a specific QLASH clan. Parameter accepts either clan name or clan tag. Clan name has to be identical to the ingame clan name.")
async def qlash_clan(ctx,name_tag):
    await qlash_cclan(ctx,name_tag)

@bot.command(name='set')
async def set(ctx,gametag):
    await set_(ctx,gametag)

@bot.command(name='clan-add',brief='Add a qlash clan to the database. Parameters require <tag> and <clan_name>')
async def clan_add(ctx,tag,*cname):
    await clan_add_(ctx,tag,*cname)

@bot.command(name='clan-remove',brief='Remove a qlash clan from the database. Parameter only requies <clan_name>')
async def clan_remove(ctx,*cname):
    await clan_remove_(ctx,*cname)

@bot.command(name='view-members',brief='')
async def viewmembers(ctx):
    await CompareMembers(ctx)

@bot.command(name='qlash-clan-members',brief='Shows a list of all members of a given QLASH clan. Parameter accepts either clan name or clan tag. Clan name must be identical to the ingame clan name.')
async def qlashclanmembers(ctx,clan_or_tag):
    await GetClanMembers(ctx,clan_or_tag)

@bot.command(name='write-members',brief="TEST command to write all members to file")
async def writemembers(ctx):
    await WriteMembersToFile2(ctx)






bot.run(TOKEN)
