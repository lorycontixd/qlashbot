import discord
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from instances import *
from descriptions import *
from modules.util_functions import *
from modules import util_messages as messages

class Messages(commands.Cog,name="Messages"):
    def __init__(self):
        pass


    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='member-dm',pass_context=True,brief='Send a private message to a member by the bot.',description=desc_member_dm)
    async def dm(self,ctx,member: discord.Member, *message):
        mess = ctx.message
        await member.create_dm()
        await member.dm_channel.send(" ".join(message[:]))
        await mess.add_reaction('✅')

    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='say',brief='Send a message to a specific channel by the bot.',description=desc_announce)
    async def say(self, ctx, channel:discord.TextChannel, *message):
        if not channel:
            channel = ctx.channel

        msg = ctx.message
        guild = ctx.guild

        try:
            await channel.send(" ".join(message[:]))
            await msg.add_reaction('✅')
        except:
            await ctx.channel.send("Error sending message")

    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='image',brief='Send a message to a specific channel by the bot.',description=desc_announce)
    async def image(self, ctx, channel:discord.TextChannel, url, filename):
        if not channel:
            channel = ctx.channel

        msg = ctx.message
        guild = ctx.guild

        try:
            await messages.send_file(channel, url, filename)
            await msg.add_reaction('✅')
        except:
            await ctx.channel.send("Error sending message")

    @commands.has_any_role('DiscordDeveloper','QLASH')
    @commands.command(name='welcome',brief='Sends a welcome message to a specific channel by the bot.',hidden=True)
    async def welcome(self, ctx, channel:discord.TextChannel = None):
        if not channel:
            channel = ctx.channel

        msg = ctx.message
        guild = ctx.guild

        await messages.send_file(channel, messages.WELCOME_MESSAGE_SECTION_IMAGE_URL, "banner.png")
        await channel.send(messages.WELCOME_MESSAGE_FIRST_SECTION.format(ALL_QLASH_CLANS_CHANNEL = bot.get_channel(566213862756712449).mention))
        await msg.add_reaction('✅')

    @commands.command(name='info',brief='Sends an infobox to a specific channel by the bot.',hidden=True)
    async def info(self, ctx, channel:discord.TextChannel = None):
        if not channel:
            channel = ctx.channel

        msg = ctx.message
        guild = ctx.guild

        await channel.send(embed=messages.QLASH_BRAWLSTARS_INFOBOX)
        await msg.add_reaction('✅')

    @commands.has_any_role('DiscordDeveloper','QLASH')
    @commands.command(name='rules',brief='Sends the rules to a specific channel by the bot.',hidden=True)
    async def rules(self, ctx, channel:discord.TextChannel = None):
        if not channel:
            channel = ctx.channel

        msg = ctx.message
        guild = ctx.guild

        await messages.send_file(channel, messages.RULES_SECTION_IMAGE_URL,  "rules.png")
        await channel.send(messages.RULES_MESSAGE_FIRST_SECTION)
        await channel.send(messages.RULES_MESSAGE_SECOND_SECTION)
        await msg.add_reaction('✅')
