#check file
import discord
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient

def is_me(m):
    return m.author == client.user

def checkforrole(member: discord.Member, *roles):
	temp = " ".join(roles[:])
	searchingrole = temp.split(" ") #contains the roles that member must have (list)
	for role in member.roles:
		if role.name in searchingrole:
			return True
	return False

async def Check(ctx,member):
    allowed = ["Daddedavided#2841","Lore#5934"]
    if member not in allowed:
        await ctx.send("You do not have the permission for this command! ")
        return False
    return True

async def check_roles_assignement(message:discord.Message):
    author = message.author
    att = len(message.attachments)
    mod = discord.utils.get(message.guild.roles, name="Moderator")
    #helper = discord.utils.get(message.guild.roles, name="Helper")
    #subcoord = discord.utils.get(message.guild.roles, name="Sub-Coordinator")
    if message.channel.name == "roles-assignement":
        print("in roles ass")
        if att==0:
            print("no attachments")
            if author.top_role < mod:
                print("role lower than mod")
                await message.delete()
                msg = await message.channel.send("You can only send screenshots for your role in this channel. If you have problems ask in support or contact a Moderator. Thank you")
                await msg.delete(delay=5.0)
