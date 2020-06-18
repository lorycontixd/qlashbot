#check file
import discord
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient

def is_me(message):
    return message.author == client.user

def checkforrole(member: discord.Member, *roles):
	temp = " ".join(roles[:])
	searchingrole = temp.split(" ") #contains the roles that member must have (list)
	for role in member.roles:
		if role.name in searchingrole:
			return True
	return False

async def Check(ctx,member):
    allowed = ["Daddedavided#2841","Lore#5934"]
    if str(member) not in allowed:
        await ctx.send("You do not have the permission for this command! ")
        return False
    return True

async def check_roles_assignement(message:discord.Message):
    author = message.author
    att = len(message.attachments)
    ch=message.channel
    #helper = discord.utils.get(message.guild.roles, name="Helper")
    #subcoord = discord.utils.get(message.guild.roles, name="Sub-Coordinator")
    if type(ch)!=discord.TextChannel:
        return
    if ch.name == "roles-assignment":
        if att==0:
            mod = discord.utils.get(message.guild.roles, name="Moderator")
            if author.top_role < mod:
                await message.delete()
                msg = await ch.send(author.mention+" You can only send screenshots for your role in this channel. If you have problems ask in support or contact a Moderator. Thank you!")
                await msg.delete(delay=8.0)

def check_equal_lists(x,y): #x,y two lists
    if set(x)==set(y):
        return True
    else:
        return False
