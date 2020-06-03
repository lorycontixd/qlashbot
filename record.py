#record

import asyncio
import discord
from scheduler import *
from instances import *

DISCORD_TOKEN = 'NzAxMTI1MzExMDQ3NDAxNDc0.Xs0bXg.anf5etgix45lRISsKaN6ANzMdYY'

bot = discord.Client()

async def record2():
    guild = bot.get_guild(int(qlash_bs_id))
    membercount = guild.member_count
    #membercount = 14540
    today = date.today()
    mydict = {
        "Date":str(today),
        "Members":int(membercount)
    }
    coll_membercount.insert_one(mydict)
    #msg = await ctx.send("Registered today's member count")


async def hello():
    name = str(bot.user)
    print(name)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await hello()

try:
    bot.run(DISCORD_TOKEN)
except discord.errors.LoginFailure as e:
	print("Login unsuccessful.")
