import discord
import pandas as pd
import time
import os
import io
import aiohttp
import subprocess
import pytz
import asyncio
import threading
import random
import timeit
#import holidayapi

from pyowm import OWM
from pytz import timezone
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from discord import Webhook, AsyncWebhookAdapter
from datetime import datetime
from random import randint
from dateutil import tz
from modules.verification.library import *
from modules.mongodb.library import *
from instances import *
from modules.games.library import *

cest = timezone('Europe/Rome')
##
bot_status = True
last_update = ''

#*************************************************************************************************
#********************************************  EVENTS  *******************************************
#*************************************************************************************************




async def get_member_count(ctx):
    guild = bot.get_guild(int(qlash_bs_id))
    return guild.member_count

#async def on_disconnect_():
    #print("Logging off: ",bot.user)
    #mych = await bot.fetch_channel(int(bot_testing))
    #await mych.send("Bot has logged off 🔴")


#def on_message_changelog(message):
#    ch = bot.get_channel(int(changelog_channel))
#    if message.channel != ch:
#        return
#    e = message.embeds[0]
#    if e == None:
#        return
#    logs = bot.get_channel(int(qlash_bot))
#    print()





#time zones







#*********************************************  VARIOUS  *******************************************
async def hi():
    ch = bot.get_channel(int(bot_testing))
    await ch.send("hi")


async def welcome_(ctx):
    author = ctx.message.author
    response=''
    print(author.name)
    if ctx.message.author.name == 'Lore' or ctx.message.author.name == 'Daddedavided':
        response = 'Welcome back, master! I`ve been waiting for you!'
    else:
        response = 'Hello '+str(author.name)+', my name is QLASH bot! 😎'
    reply = 'To view all available commands please type ^help'
    await ctx.channel.send(response)
    await ctx.channel.send(reply)

def GetClanTag(df,name):
    for i in range(len(df.index)):
        if name in str(df.iloc[i][0]):
            return str(df.iloc[i][1])
    print("Not Found")
    return


#---- SET FUNCTION (GIVE ROLE TO MEMBERS FOR CURRENT CLAN)
async def set_(ctx,player:discord.Member,gametag):
    await ctx.trigger_typing()
    if gametag[0] != '#':
        await ctx.send("BadArguement: GameTag needs to start with #")
        return
    botdev = discord.utils.get(player.guild.roles, name="DiscordDeveloper")
    gametag = gametag.upper()
    mess = ctx.message
    author = mess.author
    clanname = ''
    membergamename = ''
    rolename = ''
    foundRole = False
    list = LoadClans()
    for i in range(len(list)): #cycle through clans
        nname = str(list[i]["Name"])
        role = discord.utils.get(player.guild.roles, name=nname)
        if role in player.roles and role.name!="QLASH Girl":
            await player.remove_roles(role)
        tag = str(list[i]["Tag"])
        club = await myclient.get_club(tag)
        for member in club.members:
            if member.tag == gametag:
                foundRole = True
                await ctx.send("Position found in clan: "+str(club.name))
                await player.add_roles(role)
                wfr = discord.utils.get(player.guild.roles, name="waiting-for-role")
                if wfr in player.roles:
                    await player.remove_roles(wfr)
                membergamename = member.name
                clanname = nname
                rolename = str(role)
                break
    tz = pytz.timezone('Europe/Rome')
    now = datetime.now(tz=tz)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if not clanname:
        clanname = "None"

    member_dict = check_member(player)
    if member_dict == None:
        print("member_dict None")
        register_member(str(player),str(gametag),clanname,str(dt_string))
        print("Registered "+str(player)+" to database ("+str(gametag)+")")
    else:
        remove_member(str(player),str(gametag))
        print("Already registered")
        register_member(str(player),str(gametag),clanname,str(dt_string))

    if foundRole==True:
        await mess.add_reaction('✅')
        await ctx.send("Role set for member "+player.mention+'\t'+"Role: "+str(rolename)+"\t"+"Time: "+str(dt_string))
        return
    else:
        await ctx.send("No role found. If you think this is a mistake, please contact our staff or a "+botdev.mention+". Thank you!")
        wfr2 = discord.utils.get(player.guild.roles, name="waiting-for-role")
        await player.add_roles(wfr2)
        return




#---- SEARCH MEMBERS (SEARCH FOR INFORMATION OF A SPECIFIC MEMBER INSIDE A CLAN (give clantag))
async def search_member(ctx,name,clubtag):
    await ctx.send("Getting member info: ")
    club = await myclient.get_club(clubtag)
    for member in club.members:
        if name in member.name:
            e=discord.Embed(title="Clan Member: "+str(member), description="------------------------------------------------", color=0x53d6fd)
            e.set_author(name="QLASH Bot")
            e.add_field(name="Member", value=str(member.name)+" ("+str(member.tag)+")", inline=False)
            e.add_field(name="Role", value=str(member.role), inline=True)
            e.add_field(name="Trophies", value=str(member.trophies), inline=True)
            e.set_footer(text="Created By Lore")
            await ctx.send(embed=e)

async def qlash_trophies(ctx): #all qlash clans with requires trophies
    await ctx.send("Gathering QLASH Clans information, please wait a few seconds...")
    await ctx.trigger_typing()
    list = LoadClans
    e=discord.Embed(title="List of all registered QLASH Clans", description="------------------------------------------------", color=0xffb43e)
    e2=discord.Embed(color=0xffb43e)
    e.set_author(name="QLASH Bot")
    for i in range(len(list)):
        tag = list[i]["Tag"]
        club = await myclient.get_club(str(tag))
        if i<21:
            e.add_field(name="Clan: "+str(club),value="Required Trophies: "+str(club.required_trophies),inline=True)
        else:
            e2.add_field(name="Clan: "+str(club),value="Required Trophies: "+str(club.required_trophies),inline=True)
    e2.set_footer(text="Created By Lore")
    await ctx.send(embed=e)
    await ctx.send(embed=e2)

###******************************* READ / WRITE / ADD / DELETE ***********
async def clan_add_(ctx,roleID,channelID,tag,*cname):
    if tag[0] != '#':
        await ctx.send("Invalid Argument "+str(tag)+". Please add # in front!" )
        return
    clanname = " ".join(cname[:])
    register_clan(roleID,channelID,tag,clanname) #frmo mongodb.py
    await ctx.send("Added QLASH clan: "+clanname+" ("+tag+") to the database.")
    return

async def clan_remove_(ctx,*cname):
    if not await Check(ctx,str(ctx.message.author)):
        return
    clanname = " ".join(cname[:])
    remove_clan(clanname) #from mongodb.py
    await ctx.send("Removed clan "+clanname+" from the database.")

async def giverole(ctx,member: discord.Member , *rolename):
	therolename = " ".join(rolename[:])
	role = discord.utils.get(ctx.guild.roles, name=therolename)
	if not role:
		await ctx.send("ArguementError: Role "+therolename+" does not exist. 😭")
		return
	await member.add_roles(role)

async def removerole(ctx,member:discord.Member , *rolename):
    therolename = " ".join(rolename[:])
    role = discord.utils.get(ctx.guild.roles, name=therolename)
    if not role:
        await ctx.send("ArguementError: Role "+therolename+" does not exist. 😭")
        return
    print(member,role)
    await member.remove_roles(role)

async def locate_(ctx,ip):
    print("Searching for location...")
    mydict = ipapi.location(ip)
    e=discord.Embed(title="Found location for ip: "+str(mydict["ip"]) , color=0xffaa00)
    e.set_author(name="QLASH Bot")
    e.add_field(name="City", value=str(mydict["city"]), inline=True)
    e.add_field(name="Region", value=str(mydict["region"]), inline=True)
    e.add_field(name="Country", value=str(mydict["country"]), inline=True)
    e.add_field(name="Continent Code", value=str(mydict["continent_code"]), inline=True)
    e.add_field(name="Postal Code", value=str(mydict["postal"]), inline=True)
    e.add_field(name="Latitude", value=str(mydict["latitude"]), inline=True)
    e.add_field(name="Longitude", value=str(mydict["longitude"]), inline=True)
    e.add_field(name="Timezone", value=str(mydict["timezone"]), inline=True)
    e.add_field(name="Country Calling Code", value=str(mydict["country_calling_code"]), inline=True)
    e.add_field(name="Currency", value=str(mydict["currency_name"]), inline=True)
    e.add_field(name="Country Population", value=str(mydict["country_population"]), inline=True)
    e.add_field(name="Organisation", value=str(mydict["org"]), inline=True)
    e.set_footer(text="Created by Lore")
    await ctx.send(embed=e)

async def serverinfo_(ctx):
    guild = ctx.guild
    e=discord.Embed(title="Server info: "+str(guild.name), color=0xe392ff)
    e.set_author(name="QLASH Bot")
    e.add_field(name="Region:", value=str(guild.region), inline=True)
    e.add_field(name="ID: ", value=str(guild.id), inline=True)
    e.add_field(name="Owner:", value=str(guild.owner), inline=True)
    e.add_field(name="Member count:", value=str(guild.member_count), inline=True)
    e.add_field(name="Premium Subscription count:", value=str(guild.premium_subscription_count), inline=True)
    e.add_field(name="System Channel:", value=str(guild.system_channel), inline=True)
    e.add_field(name="Rules Channel:",value=str(guild.rules_channel),inline=True)
    #e.add_field(name="Public Updates Channel:",value=str(guild.public_updates_channel),inline=True)
    e.add_field(name="Role count:", value=str(len(guild.roles)), inline=True)
    e.add_field(name="Creation date:", value=str(guild.created_at), inline=True)
    e.set_footer(text="Bot created by Lore")
    await ctx.send(embed=e)

async def poke(ctx, member: discord.Member, *args):
	mess = ctx.message
	await member.create_dm()
	await member.dm_channel.send(" ".join(args[:]))
	await mess.add_reaction('✅')

async def bot_stats_(ctx):
    role = discord.utils.get(ctx.guild.roles, name="DiscordDeveloper")
    e=discord.Embed(title="Bot info: "+str(bot.user.name), color=0xe392ff)
    e.set_author(name="QLASH Bot")
    e.add_field(name="Name", value=bot.user.mention, inline=True)
    e.add_field(name="ID",value=str(bot.user.id),inline=True)
    e.add_field(name="Is a Bot",value=str(bot.user.bot),inline=True)
    e.add_field(name="Creation Date",value=str(bot.user.created_at),inline=True)
    e.add_field(name="Latency",value=str(bot.latency),inline=True)
    e.add_field(name="Language",value=str(bot.user.locale),inline=True)
    e.set_footer(text="Bot created by "+role.mention)
    await ctx.send(embed=e)

async def bot_info_(ctx):
    role = discord.utils.get(ctx.guild.roles, name="DiscordDeveloper")
    response = "This bot was written in the language of Python by a few users "+role.mention+" with a passion for informatics and programming. \nThe core library used is the API offered by Discord called discordpy which grants access to an enormous amount of functions and events."
    response2 = "The brawlstats API was also used to gather information from the game, which allows to access a few but useful pieces of information. The bot commands can be viewed by typing ^help and navigating using groups (mod,util,sys and fun)"
    await ctx.send(response)
    await ctx.send(response2)

async def member_info_(ctx,member:discord.Member):
    member_dict = check_member(member)
    e=discord.Embed(title="Member info: "+str(member), description=str(member.mention), color=0x74a7ff)
    e.set_author(name="QLASH Bot")
    if member_dict != None:
        ingame_tag = member_dict["Gametag"]
        registered_clan = member_dict["Clan"]
        registered_date = member_dict["Date"]
        e.add_field(name="Game Tag ", value=str(ingame_tag), inline=True)
        if registered_clan:
            e.add_field(name="Last DB_Registered Clan ", value=str(registered_clan), inline=True)
        e.add_field(name="DB_Registration Date ", value=str(registered_date), inline=True)
    e.add_field(name="Created", value=str(member.created_at), inline=True)
    e.add_field(name="ID", value=str(member.id), inline=True)
    e.add_field(name="Joined Server", value=str(member.joined_at), inline=True)
    e.add_field(name="Premium Since", value=str(member.premium_since), inline=True)
    e.add_field(name="Status", value=str(member.status), inline=True)
    e.add_field(name="Mobile status", value=str(member.mobile_status),inline=True)
    e.add_field(name="Desktop status", value=str(member.desktop_status),inline=True)
    e.add_field(name="Top Role", value=str(member.top_role), inline=True)
    e.add_field(name="Permissions ", value=str(member.guild_permissions), inline=True)
    #e.set_image(member.default_avatar)
    e.set_footer(text="Bot created by Lore")
    await ctx.send(embed=e)

async def write_message(ctx,channelname,*message):
    msg = ctx.message
    temp = " ".join(message[:])
    guild = ctx.guild
    for channel in guild.text_channels:
        if str(channel.name) == str(channelname):
            print("channel: ",str(channel))
            print("channelname: ",str(channelname))
            await channel.send(temp)
    await msg.add_reaction('✅')

# async def welcome_announcement(ctx,channelname):
#     msg = ctx.message
#     guild = ctx.guild
#     for channel in guild.text_channels:
#         if str(channel.name) == str(channelname):
#             await welcome_message.send_file(channel, welcome_message.WELCOME_MESSAGE_SECTION_IMAGE_URL, "banner.png")
#             await channel.send(welcome_message.WELCOME_MESSAGE_FIRST_SECTION.format(ALL_QLASH_CLANS_CHANNEL = _mention_channel(566213862756712449)))
#             await channel.send(embed=welcome_message.QLASH_BRAWLSTARS_INFOBOX)
#             await welcome_message.send_file(channel, welcome_message.RULES_SECTION_IMAGE_URL,  "rules.png")
#             await channel.send(welcome_message.RULES_MESSAGE_FIRST_SECTION)
#             await channel.send(welcome_message.RULES_MESSAGE_SECOND_SECTION)
#     await msg.add_reaction('✅')

async def purge_(ctx,amount):
	author = ctx.message.author
	await ctx.channel.purge(limit=int(amount)+1)
	msg = await ctx.send("Deleted "+str(amount)+" messages from "+author.mention+" in channel "+str(ctx.message.channel))
	await msg.delete(delay=5.0)

async def purge_user_(ctx,channelname,member:discord.Member):
    i=0
    m = ctx.message
    for channel in ctx.guild.channels:
        if channel.name == channelname:
            messages = await channel.history(limit=1999).flatten()
            for message in messages:
                if message.author == member:
                    await message.delete()
                    i+=1
            msg = await ctx.send("Deleted all messages from user "+str(member)+" in channel "+channelname+" ("+str(i)+")")
            await msg.delete(delay=6.0)
            await m.add_reaction('✅')
            return
    await ctx.send(ctx.message.author.mention+", no channel found with name "+channelname)


async def commandlog_view_(ctx,limit):
    response = "``` \n"
    list = view_commandlog(limit)
    for item in list:
        response+="User: "+str(item["User"])+" Time: "+str(item["Time"])+" Command: "+str(item["Command"])+" Failed: "+str(item["Failed"])+" Reason: "+str(item["Reason"])+"\n"
    response+="```"
    await ctx.send(response)

async def commandlog_clear_(ctx):
    delete_commandlogs()
    await ctx.send("Command Log File cleared!")

#******************************** ENTRA/ESCI *******************************

async def WriteMembersToFile2(ctx):
	"""
	Writes all members of a clan in the database, in the file of the corresponding clan.
	Layout of clan file: member_name	  member_role	member_tag
	Clan file directory: ./media/texts/qlash_brawlstars_clubs
	"""
	global last_update
	last_update = str(datetime.now())
	await ctx.trigger_typing()
	sourcefile = 'qlash_clans.csv'
	file = open(sourcefile,'r+')
	content = file.read()
	lines = content.split('\n')
	file.close()
	for i in range(len(lines)-1): #cycle through clan
		ll=lines[i].split(",")
		#print(ll)
		name = str(ll[0])
		tag = str(ll[1])
		club = await myclient.get_club(tag)
		memberlist = club.members
		tempfile = open(qc_directory2+name+'.txt','w+')
		for member in memberlist:
			tempfile.write(str(member.name)+'\t'+str(member.role)+'\t'+str(member.tag)+'\n')
		tempfile.close()
	print("Database Updated!")
	await ctx.send("Database Updated!")

async def CompareMembers(ctx):
	"""
	Compares all members of a clan in the database with current member in clans.
	Layout of clan file: member_name	  member_role	member_tag
	Clan file directory: ./mecia/texts/qlash_brawlstars_clubs
	"""
	global last_update
	#response = ' ``` \n'
	mychannel = await bot.fetch_channel(int(entry_exit))
	tempmsg = await ctx.send("Printing information about members left in channel: "+mychannel.mention)
	await mychannel.trigger_typing()
	await mychannel.send("Fetching data of player that left a QLASH clan since last update "+str(last_update)+" (call ^mod write-members to update) ")
	sourcefile = 'qlash_clans.csv'
	file = open(sourcefile,'r+')
	content = file.read()
	lines = content.split('\n')
	file.close()
	for i in range(len(lines)-1): #cycle through clans
		ll=lines[i].split(",")
		name = str(ll[0])
		tag = str(ll[1])
		taglist = []
		club = await myclient.get_club(tag)
		memberlist = club.members
		for member in memberlist:
			taglist.append(str(member.tag))
		tfile = open(qc_directory2+name+'.txt','r+')
		tcontent = tfile.read()
		tlines = tcontent.split('\n')
		tfile.close()
		#response += "----------- Clan: "+name+" -------------\n"
		await mychannel.send("----------- Clan: "+name+" -------------\n")
		for j in range(len(tlines)-1):
			tll=tlines[j].split("\t")
			membername = str(tll[0])
			membertag = str(tll[2])
			if membertag not in taglist: #membertag is the old list, taglist is the new list
				#response+="Member "+membername+" left clan "+name+"\n"
				await mychannel.send("Member "+membername+" left clan "+name+"\n")
	#response +="```"
	print("sending response")
	await mychannel.send(str(response))
	print("sending confirmation")
	await mychannel.send("Action completed")
	await tempmsg.delete()
	print("Action Completed!")

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

async def role_count_(ctx,*rolename):
    role_name = " ".join(rolename[:])
    dev = discord.utils.get(ctx.guild.roles, name="DiscordDeveloper")
    for role in ctx.guild.roles:
        if role.name == str(role_name):
            rolecount = int(len(role.members))
            await ctx.send("In the role "+str(role.name)+" there are "+str(rolecount)+" members! ")
            return
    await ctx.send("No roles found for role "+role_name+"! If you think this is a mistake please contact a "+dev.mention)

async def print_report_(ctx):
    await ctx.trigger_typing()
    author = ctx.author
    guild = ctx.guild
    list = LoadClans()
    total_clans = len(list)
    sections = int(total_clans/21)+1
    listembeds=[]
    for k in range(sections):
        if k==0:
            e=discord.Embed(title="Report for roles",color=0xf6ec00)
            e.set_author(name="QLASH Bot")
        else:
            e=discord.Embed(color=0xf6ec00)
        listembeds.append(e)

    for i in range(total_clans):
        current_section = int(i/21)
        clubName = list[i]["Name"]
        clubTag = list[i]["Tag"]
        role = discord.utils.get(ctx.guild.roles, name=clubName)
        if role == None:
            await ctx.send(clubName+" role not found")
        else:
            listembeds[current_section].add_field(name=role.name,value=str(len(role.members)))
    wfr = discord.utils.get(ctx.guild.roles, name="waiting-for-role")
    wfr_count = len(wfr.members)
    #ig_europe = discord.utils.get(ctx.guild.roles, name="IG-EUROPE")
    #ig_america = discord.utils.get(ctx.guild.roles, name="IG-AMERICA")
    listembeds[-1].add_field(name=wfr.name,value=str(wfr_count))
    #listembeds[-1].add_field(name=ig_europe.name,value=str(len(ig_europe.members)))
    #listembeds[-1].add_field(name=ig_america.name,value=str(len(ig_america.members)))
    listembeds[-1].set_footer(text='Bot Created by Lore')
    for emb in listembeds:
        await ctx.send(embed=emb)

async def print_rolemembers_(ctx,*role_name):
    rolename = " ".join(role_name[:])
    await ctx.trigger_typing()
    author = ctx.author
    guild = ctx.guild
    role = discord.utils.get(ctx.guild.roles, name=rolename)
    memberlist = role.members
    if role == None:
        await ctx.send("No role found with that name!")
        return
    membercount = len(memberlist)
    sections = int(membercount/21)+1
    listembeds=[]
    for k in range(sections):
        if k==0:
            e=discord.Embed(title="Members in role "+str(role.name),color=0xf6ec00)
            e.set_author(name="QLASH Bot")
        else:
            e=discord.Embed(color=0xf6ec00)
        listembeds.append(e)
    for i in range(membercount):
        current_section = int(i/21)
        nname = str(memberlist[i])
        vvalue = str(memberlist[i].status)
        listembeds[current_section].add_field(name=nname,value=vvalue,inline=True)
    listembeds[-1].set_footer(text='Bot Created by Lore')
    for e in listembeds:
        await ctx.send(embed=e)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def check_in_dict(dict,name):
    if name in dict:
        return True
    else:
        return False

async def get_tournament_members(ctx,tournament_rolee):
    tournament_role = discord.utils.get(ctx.guild.roles, name=tournament_rolee)
    mydict = {} #
    list = LoadClans()
    clannames = [d["Name"] for d in list]
    for member in tournament_role.members:
        for role in member.roles:
            if role.name in clannames:
                if not check_in_dict(mydict,role.name):
                    mydict[role.name]=1
                else:
                    mydict[role.name]+=1

    total_clans = len(mydict)
    sections = int(total_clans/21)+1
    listembeds=[]
    for k in range(sections):
        if k==0:
            e=discord.Embed(title="Report for roles",color=0xf6ec00)
            e.set_author(name="QLASH Bot")
        else:
            e=discord.Embed(color=0xf6ec00)
        listembeds.append(e)
    for i in range(total_clans):
        current_section = int(i/21)
        clubName = mydict[i]
        club_count = mydict[clubName]
        listembeds[current_section].add_field(name=clubName,value=str(club_count))
    for emb in listembeds:
        await ctx.send(embed=emb)

#++++++++++++++++++++++++++++ achievements ++++++++++++++++++++++++++++++++++


async def gametags_process(ch,message):
    start = timeit.default_timer()
    await ch.trigger_typing()
    att = None
    if len(message.attachments)!=0:
        att = message.attachments[0]
    msg = None
    if len(message.attachments)!=0:
        msg = await ch.send("Message received: \tName: "+str(att.filename)+" \tSize: "+str(att.size)+" \tID: "+str(att.id)+'\nDo you want to process the information?')
    elif message.content.startswith('#'):
        msg =  await ch.send("Message received:\nDo you want to process the information?")
    else:
        await ch.send("Not processed.")
        return
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')

    def check(reaction,user):
        return str(message.author.name)==str(user.name)

    try:
        await asyncio.sleep(1)
        reaction,user = await bot.wait_for('reaction_add', timeout=600.0, check=check)
        if str(reaction.emoji) == '❌':
            t = await ch.send("Information will not be processed.")
            await t.delete(delay=2.0)
            await message.delete(delay=4.0)
            await msg.delete(delay=3.0)
            return
        temp = await ch.send("--- Starting ---")
        gametags = None
        if len(message.attachments)!=0:
            content = await att.read()
            gametags = content.decode('utf-8').split('\n')
        elif message.content.startswith('#'):
            content = message.content
            gametags = content.split('\n')
        else:
            await ch.send("Not processed.")
            return
        loading_msg = await ch.send("0 out of {TAGS} gametags processed".format(TAGS = len(gametags)))
        clubs = await brawlstats.count_clubs(gametags, loading_msg)
        file = io.StringIO()
        file.write("\n")
        brawlstats.add_file_lines(file, clubs, False, True, False, False, True)
        file.write("\n")
        brawlstats.add_file_lines(file, clubs, False, True, False, True, False)
        file.write("\n")
        file.write("Printing found clubs and no. participants:\n")
        brawlstats.add_file_lines(file, clubs, True, False, True, False, False)
        file.write("\n")
        #file.write("Printing found club members:\n")
        brawlstats.add_file_lines(file, clubs, False, True, True, False, False)
        file.seek(0)
        await ch.send(content=message.author.mention+", please see the file below to check out the number of participants.", file=discord.File(fp=file, filename="tournament_info.txt"))
        file.close()
        end = timeit.default_timer()
        await ch.send("The command took {EXECUTION_TIME:2f} seconds".format(EXECUTION_TIME = end - start))
        await temp.delete(delay=1.0)
        await loading_msg.edit(content="All tags processed")
    except asyncio.TimeoutError:
        await msg.delete()
        await ch.send('Timeout for user '+str(message.author.name)+' 👎 ')

async def read_file(message):
    ch = message.channel
    if ch.id == int(file_managing):
        if not message.author.bot:
            if len(message.attachments)!=0:
                await gametags_process(ch,message)
            elif message.content.startswith('#'):
                await gametags_process(ch,message)
            else:
                dev = discord.utils.get(message.guild.roles, name="DiscordDeveloper")
                #await message.delete(delay=3.0)
                #alert1 = await ch.send("This channel only takes in attachments. If this is a mistake, please contact a "+dev.mention+".")
                #await alert1.delete(delay=5.0)

#****************

async def get_audit_logs_(ctx,member:discord.Member):
    entries = await ctx.guild.audit_logs(limit=None, user=member).flatten()
    await ctx.send("First Audit Log entry for user"+str(member)+"\n"+str([0]))

#****************

async def webhook_insta():
    async with aiohttp.ClientSession() as session:
        url = 'https://discordapp.com/api/webhooks/723918930766200892/HN79cUZPMfXtMbF4JnZkuRUkCepDR1cH_JvqBs4IOfU3h6KaehjSqPtAyHzLhZ5Vkd35'
        webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
        await webhook.send('Hello World', username='Foo')



#***********************************************
