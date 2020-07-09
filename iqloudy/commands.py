from modules.brawlstars.commands import BrawlStars
from modules.moderation.commands import Moderation
from modules.weather.commands import Weather
from modules.messages.commands import Messages
from modules.fun.commands import Fun
from modules.system.commands import System
from modules.channels.commands import Channels

async def init_cogs(bot,db):
    bot.add_cog(Weather())
    bot.add_cog(Fun())
    bot.add_cog(Moderation())
    bot.add_cog(System(db))
    bot.add_cog(BrawlStars())
    bot.add_cog(Messages())
    bot.add_cog(Channels())
