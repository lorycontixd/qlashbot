from discord.ext import tasks, commands

class MyCog(commands.Cog):
    def __init__(self):
        self.index = 0
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=5.0)
    async def counter(self):
        print(self.index)
        self.index += 1

    async def stopper(self):
        self.printer.stop()
