import aiohttp

from discord.ext import tasks, commands
from instances import *
from datetime import datetime

class MyCog(commands.Cog):
    def __init__(self):
        self.index = 0
        self.sent = False
        self.counter.start()
        self.it = bot.get_channel(int(it_general))

    def cog_unload(self):
        self.counter.cancel()

    @tasks.loop(minutes=1.0)
    async def counter(self):
        t = datetime.now()
        if t.strftime("%h")==22:
            if self.sent==False:
                await it.send("Buonanotte!")
                self.sent=True
        else:
            self.sent=False

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
