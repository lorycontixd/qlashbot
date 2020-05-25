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
