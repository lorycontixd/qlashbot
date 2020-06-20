import aiohttp

from discord.ext import tasks, commands
from instances import *
from datetime import datetime

#ugly workaroudn to trigger immediately
@apscheduler.scheduled_job('date')
async def reddit_webhook_now():
   await reddit_webhook()

#only triggers after 15 minutes (will be fixed in 4.0)
@apscheduler.scheduled_job('interval', seconds=10)
async def reddit_webhook():
    ch = bot.get_channel(int(bot_developer_channel))
    await ch.send("helo")
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.reddit.com/r/Brawlstars.json') as resp:
            if resp.status == 200:
                    await ch.send(await resp.text())
