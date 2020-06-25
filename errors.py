#Error Handler Class

import discord
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient

class Errors():
    def __init__(self):
        print("Cog Loaded: Errors")

    async def ChannelNotFound(self)
