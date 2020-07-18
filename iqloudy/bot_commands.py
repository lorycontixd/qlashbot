from modules.brawlstars.commands import BrawlStars
from modules.moderation.commands import Moderation
from modules.weather.commands import Weather
from modules.messages.commands import Messages
from modules.fun.commands import Fun
from modules.system.commands import System
from modules.channels.commands import Channels
from modules.clubs.commands import Clubs

async def init(bot,db,qlash_bs):
    bot.add_cog(Weather())
    bot.add_cog(Fun())
    bot.add_cog(Moderation())
    bot.add_cog(System(bot,db))
    bot.add_cog(BrawlStars())
    bot.add_cog(Messages())
    bot.add_cog(Channels())
    bot.add_cog(Clubs(qlash_bs))
