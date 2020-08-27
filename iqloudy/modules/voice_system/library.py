import discord
import time
from discord.ext import commands
from discord.voice_client import VoiceClient
import asyncio
import bot_instances
from modules.mongodb import library as mongo
from collections import Counter


class VoiceSystem(commands.Cog,name="VoiceSystem"):
    """
    Class to deal with voice connections.
    """
    def __init__(self):
        self.m_voice =mongo.MongoVoiceSystem()
        self.m_voicestats = mongo.MongoVoiceStats()
        self.room_docs = self.m_voice.LoadRooms()
        self.channel_ids = [int(item["ID"]) for item in self.room_docs]
        self.channels = [bot_instances.bot.get_channel(item) for item in self.channel_ids]
        print(self.channels)
        self.channel_names = [item.name for item in self.channels]
        self.ch_commands = bot_instances.bot.get_channel(int(bot_instances.text_commands))
        self.waitingroom = bot_instances.bot.get_channel(int(bot_instances.waitingroom))

    @commands.command(name="connect",brief="Test command for Voice System")
    async def print_channel1(self,ctx,*channelname):
        #-- CHECKS --
        author = ctx.message.author
        role_sub = discord.utils.get(ctx.guild.roles, id=int(bot_instances.id_role_sub))
        if ctx.channel != self.ch_commands and author.top_role < role_sub:
            await ctx.send("This command can only be called in "+self.ch_commands.mention)
            return
        channelname = " ".join(channelname[:])
        channel = discord.utils.get(ctx.guild.voice_channels, name=channelname)
        if channel is None:
            await ctx.send("Invalid channel name was given: "+str(channelname))
            return
        if channel not in self.channels:
            await ctx.send("Invalid channel for connection: "+str(channelname))
            return
        voice_state = author.voice
        if voice_state is None:
            await ctx.send("You must be in the waiting room to connect to a Voice Channel.")
            return
        else:
            if voice_state.channel != self.waitingroom:
                await ctx.send("You must be in the waiting room to connect to a Voice Channel.")
                return
        
        def check(m):
            return m.author == author and type(m.channel) == discord.DMChannel
        
        #OPERATIONS
        await author.create_dm()
        if len(channel.members) == 0:
            message = """
            You are the host of a new Voice Channel, please set a password for this channel and share it only with your teammates.

            You have __**60 seconds**__ to set a password before getting disconnected.
            """
            await author.dm_channel.send(message)

            try:
                await asyncio.sleep(1)
                p = await bot_instances.bot.wait_for('message', check=check,timeout=60.0)
                password = p.content
                await author.move_to(channel)
                self.m_voice.register_voicechannel(str(author),channel.name,channel.id,password)
                user_limit = channel.user_limit
                if user_limit == 0:
                    user_limit = "No Limit"
                accept_msg = "Hello "+author.name+", you successfully created a room:\n- Channel Name: "+channel.name+"\n- Channel Bitrate: "+str(channel.bitrate)+"\n- Password: "+str(password)+"\n- User Limit: "+str(user_limit)+"\n\nGive the password only to those players that you want in your voice room."
                await author.dm_channel.send(accept_msg)
                self.m_voicestats.add_room_counter(channel.name)
                return
            except asyncio.TimeoutError:
                await author.dm_channel.send('TimeoutError, you will be disconnected. 👎')
                return
        else:
            #Get password from user, check if room exists in mLab and process data
            mongo_channel = self.m_voice.get_voicechannel(channel.id)
            if mongo_channel == None:
                await ctx.send("An error has occured finding the channel. Please contact our staff.")
                return

            message = "You are joining the Voice Channel "+channel.name+", please type the password for this room __**within 60 seconds**__."
            await author.dm_channel.send(message)

            try:
                await asyncio.sleep(1)
                p=await bot_instances.bot.wait_for('message', check=check, timeout=60.0)
                password=p.content

                if str(password)==mongo_channel["Password"]:
                    await author.move_to(channel)
                    await author.dm_channel.send("Hello {auth}, you successfully joined the room {ch_name}".format(auth=author.name, ch_name=channel.name))
                    return
                else:
                    await author.dm_channel.send("The password for the Voice Channel {ch} is incorrect.\nPlease check the password with the host, or contact a staff member if you have problems.".format(ch=channel.name))
                    return
            except asyncio.TimeoutError:
                await author.dm_channel.send('TimeoutError, you will be disconnected. 👎')
                return


        #use change_activity_event + 0 members left to delete voice room

    @commands.command(name="set-bitrate",brief="Set bitrate of the channel you are hosting")
    async def setbitrate(self,ctx,bit_rate:int):
        author = ctx.message.author
        ch_msg = ctx.channel
        if ch_msg != self.ch_commands:
            await ctx.send("This command can only be called in "+self.ch_commands.mention)
            return
        if author.voice == None:
            await ctx.send("You must be connected to a voice channel to call this command.")
            return
        voice_ch_id = author.voice.channel.id
        if voice_ch_id not in bot_instances.voice_ids:
            await ctx.send("Cannot change the bitrate of this VoiceChannel")
            return
        ch_doc = self.m_voice.get_voicechannel(voice_ch_id)
        if str(author) != str(ch_doc["CreatedBy"]):
            await ctx.send("You must be the room host to change the bitrate.")
            return
        if bit_rate<8000 or bit_rate>96000:
            await ctx.send("Invalid value for bitrate ("+str(bit_rate)+"), must be between 8'000 and 96'000.\nHigher bitrate means better call resolution, but it is not recommended for low internet connections. (Default is 64'000).")
            return
        ch = bot_instances.bot.get_channel(int(voice_ch_id))
        await ch.edit(bitrate=bit_rate)
        self.m_voicestats.add_bitrate_counter(author.voice.channel.name)
        await ctx.send("Bitrate was set successfully to "+str(bit_rate))

    @commands.command(name="request-channel",brief="Request a temporary VoiceChannel when all protected channels are full.",hidden=True)
    async def requestchannel(self,ctx):
        author = ctx.author
        l = len(self.channels)
        #isOccupied
        rooms = dict((item.name,False) if len(item.members) == 0 else (item.name,True) for item in self.channels)

        values = list(rooms.values())
        if True in values:
            x = Counter(values)
            await ctx.send("There are "+str(x[False])+" free rooms. You cannot ask for a new one.")
        else:
            msg = await ctx.send("Your request has been taken into account. Please stand by.")
            #await bot_instances.channel_moderators.send(bot_instances.role_mod.mention+"\nA protected room has been requested by user "+author.name+".")
            category_protectedrooms = bot_instances.bot.get_channel(bot_instances.id_category_protectedrooms)
            newchannel = await category_protectedrooms.create_voice_channel(name="Room "+str(l+1),reason="All protected rooms were taken.")
            await newchannel.edit(sync_permissions=True)
            await asyncio.sleep(2)
            self.m_voice.register_voiceroom(name=newchannel.name, id=newchannel.id, type="Extra")
            await msg.edit(content="A new VoiceRoom has been created.")
            self.channels.append(newchannel)
            
        
        



        
