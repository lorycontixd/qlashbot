from discord.ext import tasks, commands

class MyCog(commands.Cog,ctx):
    def __init__(self):
        self.index = 0
        self.counter.start()

    def cog_unload(self):
        await
        self.counter.cancel()

    @tasks.loop(seconds=1.0)
    async def counter(self,ctx):
        await ctx.send(self.index)
        self.index += 1
        if self.index == 15:
            cog_unload(self)
