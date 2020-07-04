import discord
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from discord import Webhook, AsyncWebhookAdapter

from modules.util_scheduler import *

class EventFunctions():
    def __init__(self):
        self.status = False
        self.watchouts = ['spongebob']

    async def on_ready_(self):
        self.status = True
        tz = pytz.timezone('Europe/Rome')
        time=str(datetime.now(tz=tz).strftime("%d/%m/%Y, %H:%M:%S"))
        scheduler.add_default_tasks(apscheduler)
        print('Logged in as: ',bot.user)
        print('Bot ID: ',bot.user.id)
        print('Creation Date: ',bot.user.created_at)
        print('Websocket Gateway: ',bot.ws)
        print('Time: ',time)
        print('----------------')
        await bot.change_presence( activity=discord.Activity(type=discord.ActivityType.playing, name=" ^help for help"))

    async def member_join_check(self,member:discord.Member):
        mychannel = bot.get_channel(int(qlash_bot))
        membername = str(member.name).lower()
        for item in self.watchouts:
            if item in membername:
                embed=discord.Embed(title="Suspicious member has joined the server: "+str(member), color=0xe32400)
                embed.set_author(name="QLASH Bot")
                embed.add_field(name="Account Creation Date", value=str(member.created_at), inline=True)
                embed.add_field(name="User ID", value=str(member.id), inline=True)
                embed.add_field(name="Mentionable", value=str(member.mention), inline=True)
                embed.add_field(name="Status", value=str(member.status), inline=True)
                embed.set_footer(text="Created by Lore")
                await mychannel.send(embed=embed)
                mod = discord.utils.get(message.guild.roles, name="Moderator")
                await mychannel.send(mod.mention)
