#record

import asyncio
import discord
from scheduler import *
from instances import *

DISCORD_TOKEN = 'NzAxMTI1MzExMDQ3NDAxNDc0.Xs0bXg.anf5etgix45lRISsKaN6ANzMdYY'

bot2 = discord.Client()

async def record2():
    guild = bot2.get_guild(int(qlash_bs_id))
    print(guild)
    membercount = guild.member_count
    print(membercount)
    #membercount = 14540
    today = date.today()
    mydict = {
        "Date":str(today),
        "Members":int(membercount)
    }
    coll_membercount.insert_one(mydict)
    #msg = await ctx.send("Registered today's member count")


async def hello(): 
    name = str(bot2.user)
    print(name)

@bot2.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot2))
    await hello()
    #await bot.close()

try:
    bot2.run(DISCORD_TOKEN)
except discord.errors.LoginFailure as e:
	print("Login unsuccessful.")
