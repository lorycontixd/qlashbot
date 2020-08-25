import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
import asyncio
import bot_instances
from modules.mongodb import library as mongo

    

class VoiceSystem(commands.Cog,name="VoiceSystem"):
    """
    Class to deal with voice connections.
    """
    def __init__(self):
        #here goes a list of all voice channels (also add them to bot_instances/channels)
        self.waitingroom = bot_instances.bot.get_channel(747588681627336786)
        self.ch1 = bot_instances.bot.get_channel(747588721544790117)
    
    @commands.command(name="connect",brief="Test command for Voice System")
    async def print_channel1(self,ctx,*channelname):
        channelname = " ".join(channelname[:])
        channel = discord.utils.get(ctx.guild.voice_channels, name=channelname)
        if channel is None:
            await ctx.send("Invalid channel name was given: "+str(channelname))
            return

        author = ctx.message.author
        voice_state = author.voice
        
        if voice_state is None:
            await ctx.send("You must be in the waiting room to connect to a Voice Channel.")
            return
        else:
            print("Voice State: ", voice_state)
            print("Connected Channel: ", voice_state.channel)
            if voice_state.channel != self.waitingroom:
                await ctx.send("You must be in the waiting room to connect to a Voice Channel.")
                return
        
        def check(m):
            return m.author == author and type(m.channel) == discord.DMChannel
        
        await author.create_dm()
        if len(channel.members) == 0:
            message = """
            You are the host of a new Voice Channel, please set a password for this channel and share it only with your teammates.

            You have __**30 seconds**__ to set a password before getting disconnected.
            """
            await author.dm_channel.send(message)

            try:
                await asyncio.sleep(1)
                p = await bot_instances.bot.wait_for('message', check=check,timeout=30.0)
                password = p.content
                await author.move_to(channel)
                mongo.register_voicechannel(str(author),channel.name,channel.id,password)
                user_limit = channel.user_limit
                if user_limit == 0:
                    user_limit = "No Limit"
                accept_msg = "Hello "+author.name+", you successfully created a room:\n- Channel Name: "+channel.name+"\n- Channel Bitrate: "+str(channel.bitrate)+"\n- Password: "+str(password)+"\n- User Limit: "+str(user_limit)+"\n\nGive the password only to those players that you want in your voice room."
                await author.dm_channel.send(accept_msg)
                return
            except asyncio.TimeoutError:
                await author.dm_channel.send('TimeoutError, you will be disconnected. 👎')
                return
        else:
            #Get password from user, check if room exists in mLab and process data
            mongo_channel=mongo.get_voicechannel(channel.id)
            if mongo_channel == None:
                await ctx.send("An error has occured finding the channel. Please contact our staff.")
                return

            message = """
            You are joining the Voice Channel {ch}, please type the password for this room __**within 30 seconds**__.
            """.format(channel.name)
            await author.dm_channel.send(message)

            try:
                await asyncio.sleep(1)
                p=await bot_instances.bot.wait_for('message', check=check, timeout=30.0)
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


        



        
