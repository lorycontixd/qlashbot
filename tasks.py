import aiohttp

from discord.ext import tasks, commands
from instances import *
import random
from mongodb import *

#ugly workaroudn to trigger immediately
#@apscheduler.scheduled_job('date')
#async def reddit_webhook_now():
#   await reddit_webhook()

#only triggers after 15 minutes (will be fixed in 4.0)
#@apscheduler.scheduled_job('interval', minutes=15)
#async def reddit_webhook():
#    ch = bot.get_channel(int(bot_developer_channel))
#    async with aiohttp.ClientSession() as session:
#        async with session.get('https://www.reddit.com/r/Brawlstars.json') as resp:
#            if resp.status == 200:
#                await ch.send("Reddit?")
                #await ch.send(await resp.text())

async def reg_member():
    ch = bot.get_channel(int(bot_developer_channel))
    #membercount = 14540
    today = date.today()
    mydict = {
        "Date":str(today),
        "Members":int(membercount)
    }
    coll_membercount.insert_one(mydict)
    msg = await ch.send("Registered today's member count")

async def hello():
    ch = bot.get_channel(int(bot_developer_channel))
    await ch.send("Goodmorning Alex, this message is scheduled!")
