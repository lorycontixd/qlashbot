from modules.cogs_moderation import Moderation
from modules.cogs_weather import Weather
from modules.cogs_fun import Fun
from modules.cogs_system import System

async def init_cogs(bot):
    bot.add_cog(Weather())
    bot.add_cog(Fun())
    bot.add_cog(Moderation())
    bot.add_cog(System())
