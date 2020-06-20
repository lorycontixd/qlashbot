from discord.ext import tasks, commands

class MyCog(commands.Cog):
    def __init__(self):
        self.index = 0
        self.counter.start()

    def cog_unload(self):
        print("stopping...")
        self.counter.cancel()

    @tasks.loop(seconds=5.0)
    async def counter(self):
        print(self.index)
        self.index += 1
        if self.index == 15:
            cog_unload(self)

    @counter.before_loop
    async def before_counter(self):
        print('waiting...')
        await self.bot.wait_until_ready()
