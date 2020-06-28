#First implementation for a better Help Command
import discord
from discord.ext import commands

_help = commands.DefaultHelpCommand()
help.no_category='Main Category'
print(_help.no_category)
