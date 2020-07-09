import discord
from discord.ext import commands

from modules.messages import library as messages_library, descriptions as messages_descriptions

class Messages(commands.Cog,name="Messages"):
    def __init__(self):
        pass


    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='member-dm',pass_context=True,brief='Send a private message to a member by the bot.',description=messages_descriptions.desc_member_dm)
    async def dm_(self,ctx,member: discord.Member, *message):
        string_message = " ".join(message[:])
        await messages_library.dm(self, ctx, member, string_message)

    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='say',brief='Send a message to a specific channel by the bot.',description=messages_descriptions.desc_announce)
    async def say_(self, ctx, channel:discord.TextChannel, *message):
        string_message = " ".join(message[:])
        await messages_library.say(self, ctx, channel, string_message)

    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='image',brief='Send a message to a specific channel by the bot.',description=messages_descriptions.desc_announce)
    async def image_(self, ctx, channel:discord.TextChannel, url, filename):
        await messages_library.image(self, ctx, channel, url, filename)

    @commands.has_any_role('DiscordDeveloper','QLASH')
    @commands.command(name='welcome',brief='Sends a welcome message to a specific channel by the bot.',hidden=True)
    async def welcome_(self, ctx, channel:discord.TextChannel = None):
        await messages_library.welcome(self, ctx, channel)

    @commands.has_any_role('DiscordDeveloper','QLASH')
    @commands.command(name='info',brief='Sends an infobox to a specific channel by the bot.',hidden=True)
    async def info_(self, ctx, channel:discord.TextChannel = None):
        await messages_library.info(self, ctx, channel)

    @commands.has_any_role('DiscordDeveloper','QLASH')
    @commands.command(name='rules',brief='Sends the rules to a specific channel by the bot.',hidden=True)
    async def rules_(self, ctx, channel:discord.TextChannel = None):
        await messages_library.rules(self, ctx, channel)
