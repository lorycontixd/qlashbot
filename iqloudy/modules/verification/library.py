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
        await ctx.send("Permisison to use this command you do not have... Hrmmm...")
        return False
    return True

def check_equal_lists(x,y): #x,y two lists
    if set(x)==set(y):
        return True
    else:
        return False

def validate_tag(tag):
    if not tag.startswith("#"):
        return False
    allowed = ['P','Y','L','Q','G','R','J','C','U','V','0','2','8','9']
    for c in tag:
        if c not in allowed:
            return False
    if len(tag) not in range(5,15):
        return False
    return True
