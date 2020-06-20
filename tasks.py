from discord.ext import tasks, commands
from instances import *

class MyCog(commands.Cog):
    def __init__(self):
        self.index = 0
        self.counter.start()
        self.ch = bot.get_channel(int(bot_developer_channel))

    def cog_unload(self):
        self.counter.cancel()

    @tasks.loop(seconds=1.0)
    async def counter(self):
        await self.ch.send(self.index)
        self.index += 1
        if self.index == 15:
            cog_unload(self)
