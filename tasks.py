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


#@apscheduler.scheduled_job('cron', hour=21, minute=47)
#async def print_console_h():
#    print("h")
