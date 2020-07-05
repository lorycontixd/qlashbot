import discord
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from modules.util_permissions import *

class Permissions(commands.Cog,name="Permissions"):
    def __init__(self):
        pass

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='check-all-channels ',brief='check all channel perms')
    async def check_all_channels(self,ctx):
        await ctx.send("Not yet implemented.")

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='check-channel',brief='check channel perms')
    async def check_channel(self,ctx,channel:discord.TextChannel):
        await util_check_channel(self, ctx, channel)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='lock-channel',brief='lock channel')
    async def lock_channel(self,ctx,channel:discord.TextChannel):
        await ctx.send("Not yet implemented.")

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='lock-all-channels',brief='lock all channels')
    async def lock_channel(self,ctx,channel:discord.TextChannel):
        await ctx.send("Not yet implemented.")

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='make-private-channel',brief='make a private channel')
    async def make_private_channel(self,ctx,channel:discord.TextChannel):
        await ctx.send("Not yet implemented.")

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='make-public-channel',brief='make a public channel')
    async def make_public_Channel(self,ctx,channel:discord.TextChannel):
        await ctx.send("Not yet implemented.")
