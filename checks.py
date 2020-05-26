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

watchouts = ['spongebob']
async def member_join_check(member:discord.Member):
    mychannel = bot.get_channel(int(qlash_bot))
    membername = str(member.name).lower()
    for item in watchouts:
        if item in membername:
            embed=discord.Embed(title="Suspicious member has joined the server"+str(member), color=0xe32400)
            embed.set_author(name="QLASH Bot")
            embed.add_field(name="Account Creation Date", value=str(member.created_at), inline=True)
            embed.add_field(name="User ID", value=str(member.id), inline=True)
            embed.add_field(name="Mentionable", value=str(member.mention), inline=True)
            embed.add_field(name="Status", value=str(member.status), inline=True)
            embed.set_footer(text="Created by Lore")
            await mychannel.send(embed=embed)
