import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
import instances
import mongodb as mongo

class VoiceSystem(commands.Cog,name="VoiceSystem"):
    """
    Class to deal with voice connections.
    """
    def __init__(self):
        self.waiting = instances.bot.fetch_channel(747588681627336786)
        self.ch1 = instances.bot.fetch_channel(747588721544790117)
    
    @commands.command(name="test",brief="Test command for Voice System")
    def print_channel1(self):
        print(self.ch1)


