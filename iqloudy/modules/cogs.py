from modules.cogs_brawlstars import BrawlStars
from modules.cogs_moderation import Moderation
from modules.cogs_weather import Weather
from modules.cogs_messages import Messages
from modules.cogs_fun import Fun
from modules.cogs_system import System
from modules.cogs_permissions import Permissions

async def init_cogs(bot):
    bot.add_cog(Weather())
    bot.add_cog(Fun())
    bot.add_cog(Moderation())
    bot.add_cog(System())
    bot.add_cog(BrawlStars())
    bot.add_cog(Messages())
    bot.add_cog(Permissions())
