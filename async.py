import brawlstats
import logging
import discord
import os
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from functions import *

TOKEN = 'NzAxMTI1MzExMDQ3NDAxNDc0.Xps72g.Oqb3TRaaUolJECiGgfrUbVtKHk8'

ignick_lory = 'loryconti'
igtag_lory = '#20VYUG2L'
qlash_ares = '#98VQUC8R'
igtag_picoz = '#20VVVVYQ8'
igtag_elgarzy = '#RC9PVRCJ'

bot = commands.Bot(command_prefix='^' , description = "Qlash Bot ")
myclient = brawlstats.Client(TOKEN2,is_async=True)

#****************************************************************************************

@bot.event
async def on_ready():
    print('Logged in as: ',bot.user.name)
    print('Bot ID: ',bot.user.id)
    print('------')
    await bot.change_presence( activity=discord.Activity(type=discord.ActivityType.playing, name=" ,help"))

@bot.command(name='qlash')
async def qlash(ctx):
    await qlash_(ctx)

@bot.command(name='bs-playerinfo')
async def bs_pinfo(ctx,tag):
    await getplayer(ctx,tag)

@bot.command(name='bs-claninfo')
async def bs_cinfo(ctx,tag):
    await getclan(ctx,tag)
@bot.command(name='bs-memberinfo')
async def bs_minfo(ctx,name,ctag):
    await search_member(ctx,name,ctag)

@bot.command(name='qlash-allclans')
async def qlash_allclans(ctx):
    await qlash_trophies(ctx)

@bot.command(name='qlash-clan')
async def qlash_clan(ctx,name_tag):
    await qlash_cclan(ctx,name_tag)








bot.run(TOKEN)
