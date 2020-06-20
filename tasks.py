from discord.ext import tasks, commands
from instances import *
from datetime import datetime

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
