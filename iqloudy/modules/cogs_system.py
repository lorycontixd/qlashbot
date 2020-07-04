import discord
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from instances import *
from descriptions import *
from functions import *

class System(commands.Cog,name="System"):
    def __init__(self):
        pass

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='shutdown',brief='Shutdowns the instance (developer-only)')
    async def shutdown(self,ctx):
        await ctx.send("Not yet implemented.")
