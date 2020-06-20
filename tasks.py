from discord.ext import tasks, commands
from instances import *
from datetime import datetime

import aiohttp
class MyCog(commands.Cog):
    def __init__(self):
        self.index = 0
        self.counter.start()
        self.ch = bot.get_channel(int(bot_developer_channel))

    def cog_unload(self):
        self.counter.cancel()

    @tasks.loop(seconds=30.0)
    async def counter(self):
        t = datetime.now()
        await self.ch.send("It's "+t.strftime("%d%m%Y , %H%M%S"))
        self.index += 1
        if self.index == 5:
            cog_unload(self)

#ugly workaroudn to trigger immediately
@apscheduler.scheduled_job('date')
async def reddit_webhook_now():
   await reddit_webhook()

#only triggers after 15 minutes (will be fixed in 4.0)
@apscheduler.scheduled_job('interval', minutes=15)
async def reddit_webhook():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.reddit.com/r/Brawlstars.json') as resp:
            if resp.status == 200:
                    print(await resp.text())
