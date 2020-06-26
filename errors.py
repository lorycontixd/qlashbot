#Error Handler Class

import discord
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient

class Error(Exception):
    """Base class for other exceptions"""
    pass

class InputError(Error):
    """Input error class"""
    pass

class BadArguement(InputError):
    """Bad Argument"""
    pass
