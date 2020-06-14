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
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from datetime import datetime
from random import randint
from dateutil import tz
from descriptions import *
from checks import *
from utility import *
from mongodb import *
from instances import *

from google import *
from weather import *
from modules import brawlstats

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=9)
#async def scheduled_job():
#    ch_it = bot.get_channel(int(it_general))
#    ch_en = bot.get_channel(int(en_general))
#    faces = ['😏','🐋','🤪','👋','🕘','😳','🤩']
#    it_random = ["Buongiorno splendori!","Buongiorno stelline!","Buongiorno fagiolini","Ciao a tutti!","Ben svegliati cuccioli!","Buongiorno!!"]
#    en_random = ["Good morning everyone!","Good morning!"]
#    it_int = randint(1,len(it_random))
#    en_int = randint(1,len(en_random))
#    emoji_int = randint(1,len(faces))
#    await ch_it.send(str(it_random[it_int])+str(faces[emoji_int]))
#    await ch_en.send(str(en_random[en_int])+str(faces[emoji_int]))

##
bot_status = True
last_update = ''

async def on_ready_():
    print('Logged in as: ',bot.user)
    print('Bot ID: ',bot.user.id)
    print('Creation Date: ',bot.user.created_at)
    print('Websocket Gateway: ',bot.ws)
    print('----------------')
    #mych = await bot.fetch_channel(int(bot_testing))
    #await mych.send("Bot has logged in 🟢")
    await bot.change_presence( activity=discord.Activity(type=discord.ActivityType.playing, name=" ^help for help"))

async def get_member_count(ctx):
    guild = bot.get_guild(int(qlash_bs_id))
    return guild.member_count

#async def on_disconnect_():
    #print("Logging off: ",bot.user)
    #mych = await bot.fetch_channel(int(bot_testing))
    #await mych.send("Bot has logged off 🔴")

watchouts = ['spongebob']
async def member_join_check(member:discord.Member):
    mychannel = bot.get_channel(int(qlash_bot))
    membername = str(member.name).lower()
    for item in watchouts:
        if item in membername:
            embed=discord.Embed(title="Suspicious member has joined the server: "+str(member), color=0xe32400)
            embed.set_author(name="QLASH Bot")
            embed.add_field(name="Account Creation Date", value=str(member.created_at), inline=True)
            embed.add_field(name="User ID", value=str(member.id), inline=True)
            embed.add_field(name="Mentionable", value=str(member.mention), inline=True)
            embed.add_field(name="Status", value=str(member.status), inline=True)
            embed.set_footer(text="Created by Lore")
            await mychannel.send(embed=embed)
            await mychannel.send("@Moderator")


async def on_member_update_role(before,after):
    if not check_equal_lists(before.roles,after.roles):
        list = LoadClans()
        clannames = [d["Name"] for d in list]
        for role in after.roles:
            if not role in before.roles:
                if role.name in clannames:
                    messages = ['We are delighted to have '+after.mention+' join us in '+role.mention,'Hello '+role.mention+'. Welcome to the team '+after.mention+'!','Hello '+role.mention+'. We would like to welcome '+after.mention+' to the club.',"We're glad you are here, "+after.mention+"! "+role.mention]
                    #myint = randint(1,len(messages))
                    print(after.name+" was given the role "+role.name)
                    id = role.id
                    #file = open('message.csv','r+')
                    #content = file.read()
                    #lines = content.split('\n')
                    #for line in lines:
                    ##    ll=line.split(',')
                    #    roleID = int(ll[1])
                    #    channelID = int(ll[2])
                    clan_doc = get_clan(str(role.name))
                    roleID = clan_doc["RoleID"]
                    channelID = clan_doc["ChannelID"]
                    if int(roleID) == id:
                        ch = bot.get_channel(int(channelID))
                        await ch.send(random.choice(messages))


#time zones
from_zone = tz.tzutc() #utc
to_zone = tz.tzlocal() #local

existing_roles = ["IG-EUROPE","IG-AMERICA"]
async def check_instarole(message:discord.Message):
    dev = discord.utils.get(message.guild.roles, name="BotDeveloper")
    ch = message.channel
    if type(ch)!=discord.TextChannel:
        return
    auth = message.author
    registered = False
    foundrole = ''
    if ch.name == "insta-roles":
        if len(message.attachments)!=0:
            for r in auth.roles:
                if r.name in existing_roles:
                    registered = True
                    foundrole = r.name
                    break

            if registered==False:
                msg = await ch.send("Hi "+message.author.mention+". Are you from North or South America? If **YES**, please react to the American Flag. If **NO**, please react to the World Emoji.\nThis information is important for you to enter. \nPlease select the right region, or you may be disqualified.")
                await msg.add_reaction('🇺🇸')
                await msg.add_reaction('🌎')

                def check(reaction,user):
                    return str(message.author.name)==str(user.name)

                try:
                    await asyncio.sleep(1)
                    reaction,user = await bot.wait_for('reaction_add', timeout=600.0, check=check)
                    if str(reaction.emoji) == '🇺🇸':
                        role = discord.utils.get(message.guild.roles, name="IG-AMERICA")
                        await message.author.add_roles(role)
                    elif str(reaction.emoji) == '🌎':
                        role = discord.utils.get(message.guild.roles, name="IG-EUROPE")
                        await message.author.add_roles(role)
                    msg2 = await ch.send("Thank you for your answer "+str(message.author.name)+"!")
                    await msg.delete(delay=4.0)
                    await msg2.delete(delay=5.0)
                    await message.add_reaction('✅')
                    await auth.create_dm()
                    await auth.dm_channel.send(ig_t_it)
                    await auth.dm_channel.send(ig_t_en)
                    await auth.dm_channel.send(ig_t_es)
                except asyncio.TimeoutError:
                    await msg.delete()
                    await ch.send('Timeout for user '+str(message.author.name)+' 👎 ')
            else:
                await ch.send("You are already given the instagram role "+foundrole+". If you have problems please contact a Moderator or a "+dev.mention+". Thank you")

async def insta_role_ended(message):
    ch = message.channel
    if type(ch)!=discord.TextChannel:
        return
    auth = message.author
    if ch.name == "insta-roles":
        if len(message.attachments)!=0:
            msg = await ch.send("Hello "+auth.mention+". The Instagram Tournament finished in the evening of the 7th of June. \nPlease check the calendar or the announcement channels to keep updated with new tournaments that you can join. Thank you very much!")
            await message.delete(delay=6.0)
            await msg.delete(delay=6.0)

async def hi():
    ch = bot.get_channel(int(bot_testing))
    await ch.send("hi")
#*****************************************************************************************************************
#*****************************************************************************************************************
#**************************************       COMMAND FUNCTIONS     **********************************************
#*****************************************************************************************************************
#*****************************************************************************************************************


##******** BANLIST FUNCTION: writes to a specific channel whether a banned user is in a QLASH Clan
#banlist layout:  ingame name, ingame tag, days of ban (or perma)
async def CheckBanlist(ctx):
    count=0
    channel = bot.get_channel(int(qlash_bot))
    write_channel = bot.get_channel(int(banlist_testing))
    tempmsg = await ctx.send("Calculating and reporting bans in channel: "+channel.mention)
    await channel.trigger_typing()
    messages = await write_channel.history(limit=150).flatten()
    now = datetime.now()
    for message in messages:
        #convert utc time to est
        creationDate = message.created_at
        creationDate = creationDate.replace(tzinfo=from_zone)
        central = creationDate.astimezone(to_zone)
        dayToday = now.day
        dayCreation = central.day
        difference=dayToday-dayCreation

        #work messages
        content = message.content
        temp = content.split(",")
        playerTag = str(temp[1])
        dayBan = str(temp[2])
        if dayBan !='perma':
            if difference>=int(dayBan):
                await ctx.send("Ban for player "+str(temp[0])+" has expired.")
                continue
        list = LoadClans()
        for i in range(len(list)-1):
            clubName = list[i]["Name"]
            clubTag = list[i]["Tag"]
            cclub = await myclient.get_club(clubTag)
            for member in cclub.members:
                if str(member.tag) == str(playerTag):
                    count+=1
                    await ctx.send("Player "+str(member.name)+" found in clan "+str(cclub.name))
    if count==0: #if no players were found in clans
        await ctx.send("No banned players found in qlash clans")
    await tempsmg.delete() #deletes bot message

#************************************************ FUN **********************************************
is_flipped = False
async def flip(ctx):
	global is_flipped
	if is_flipped == False:
		response = '(╯°□°）╯︵ ┻━┻ '
		await ctx.channel.send(response)
		is_flipped = True
	else:
		response = 'Sorry the table is already flipped!! ¯\_(ツ)_/¯ '
		await ctx.channel.send(response)

async def hello_(ctx):
    await ctx.send("Hello "+ctx.message.author.name+"! \n My name is QLASH Bot, you can see my commands with ^help!")

async def unflip(ctx):
	global is_flipped
	if is_flipped == True:
		response = '┬─┬ ノ( ゜-゜ノ)'
		await ctx.channel.send(response)
		is_flipped = False
	else:
		response = 'Sorry the table is already unflipped!! ¯\_(ツ)_/¯ '
		await ctx.channel.send(response)

async def tstatus(ctx):
	global is_flipped
	if is_flipped == True:
		response = 'Table is flipped'
		await ctx.channel.send(response)
	else:
		response = 'Table is unflipped'
		await ctx.channel.send(response)

async def qlash_(ctx):
    e=discord.Embed(title="QLASH", url="http://www.qlash.gg", description="Il Team QLASH è una organizzazione eSportiva con base in Italia. Co-fondata da Luca Pagano e Eugene Katchalov nel 2017, ha come scopo principale la promozione degli eSports in Italia e in Europa, creando sinergie con varie altre organizzazioni.",color=0x0061ff)
    e.set_author(name="QLASH Bot")
    e.set_image(url='https://liquipedia.net/commons/images/thumb/0/08/QLASH-PRO_black.png/600px-QLASH-PRO_black.png')
    await ctx.send(embed=e)

async def roll_(ctx):
    value = randint(1,6)
    await ctx.send("You rolled a "+str(value))

async def bs_puns_(ctx):
    choices = ['What do you call it when you get killed by a bull main? Bull-shit.','What do you call it when you get killed by a Shelly main? Shell shock.','What do you call it when you get killed by a Poco main? Hacks.','What do you call a team of crows? Toxic','How is franks super? Literally stunning','What is Nita without her super? UnBearable',"El primo isn't really a jokester, but he can pack quite a punch line",'Killing that little cactus man will give you a decent Spike in ego.','My club has barley any members.','All these puns are literally Tara-ble.','El Primo jumping in the enemy base with 11 gems.']
    myint = randint(1,len(choices))
    await ctx.send(str(choices[myint]))


#*********************************************  VARIOUS  *******************************************
async def ChannelList(ctx):
	guild = ctx.guild
	txt = guild.text_channels
	voice = guild.voice_channels
	await ctx.send(channels_response)

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


def LoadBadWords():
    dict = {}
    FILEPATH = './bad_words.csv'
    file = open(FILEPATH,'r+')
    content = file.read()
    lines = content.split('\n')
    for i in range(len(lines)-1):
        ll = lines[i].split(',')
        badword = str(ll[0])
        language = str(ll[1])
        dict[badword]=language
    return dict


async def check_bad_words(message):
    mychannel = bot.get_channel(int(qlash_bot))
    message_content = message.content.lower()
    author = message.author
    badword_dict = LoadBadWords()
    for badword in badword_dict:
        if badword in message_content:
            channel = bot.get_channel(int(qlash_bot))
            embed=discord.Embed(title="Detected Bad Word usage from user "+str(author), color=0xff4013)
            embed.set_author(name="QLASH Bot")
            embed.add_field(name="Author", value=author.mention, inline=True)
            embed.add_field(name="Bad Word", value=str(badword), inline=True)
            embed.add_field(name="Language", value=str(badword_dict[badword]), inline=True)
            embed.add_field(name="Channel",value="#"+message.channel.name, inline = True)
            embed.add_field(name="ID",value=message.id)
            embed.set_footer(text="Created By Lore")
            await mychannel.send(embed=embed)
            mess = await mychannel.send("Do I have permission to delete the message? (A moderatos has to react within 10 minutes)")
            await mess.add_reaction('✅')
            await mess.add_reaction('❌')

            def check(reaction,user):
                return str(reaction.emoji)=='✅' or str(reaction.emoji) == '❌'
            try:
                await asyncio.sleep(1)
                reaction,user = await bot.wait_for('reaction_add', timeout=600.0, check=check)
                if str(reaction.emoji) == '✅':
                    await message.delete()
                    await mychannel.send("Message was successfully deleted.")
                    return
                elif str(reaction.emoji) == '❌':
                    await mychannel.send("Message was NOT deleted.")
                    return
            except asyncio.TimeoutError:
                await channel.send('Timeout Error 👎')

async def getplayer(ctx,tag):
	role=''
	player = await myclient.get_player(tag)
	if not player:
		await ctx.send("Player with this tag was not found. If you think this was a problem, contact the Bot creators.")
		return
	e=discord.Embed(title="Player info: "+str(player), description="------------------------------------------------", color=0xf6ec00)
	e.set_author(name="QLASH Bot")
	e.add_field(name="Player", value=str(player), inline=False)
	e.add_field(name="Current Trophies", value=str(player.trophies), inline=True)
	e.add_field(name="Highest Trophies", value=str(player.highest_trophies), inline=True)
	e.add_field(name="Current Power Play", value=str(player.power_play_points), inline=True)
	e.add_field(name="Highest Power Play", value=str(player.highest_power_play_points), inline=True)
	e.add_field(name="Is Qualified in Championship Challenge", value=player.is_qualified_from_championship_challenge, inline=True)
	e.add_field(name="3v3 Victories", value=str(player.x3v3_victories), inline=True)
	e.add_field(name="Solo Victories", value=str(player.solo_victories), inline=True)
	e.add_field(name="Duo Victories", value=str(player.duo_victories), inline=True)
	cclub = player.club["tag"]
	pclub = await myclient.get_club(cclub)
	for member in pclub.members:
		if member.name == player.name:
			role = str(member.role)
	e.add_field(name="Player Club", value=str(pclub.name)+'\n'+str(pclub.tag)+'\n'+role, inline=True)
	e.add_field(name="Brawler Count", value=str(len(player.brawlers)), inline=True)
	e.set_footer(text="Created By Lore")
	await ctx.send(embed=e)

async def getclan(ctx,tag):
    presname = ''
    prestr = ''
    await ctx.send("Getting club info: ")
    club = await myclient.get_club(tag)
    members = club.members
    for member in members:
        if str(member.role).lower() == 'president':
            presname = str(member.name)
            prestr = str(member.trophies)
    e=discord.Embed(title="Clan Info: "+str(club), description="------------------------------------------------", color=0xbe37f4)
    e.set_author(name="QLASH Bot")
    e.add_field(name="Clan", value=str(club), inline=False)
    e.add_field(name="Member Count", value=str(len(members)), inline=True)
    e.add_field(name="Description", value=str(club.description), inline=True)
    e.add_field(name="Trophies", value=str(club.trophies), inline=True)
    e.add_field(name="Required Trophies", value=str(club.required_trophies), inline=True)
    e.add_field(name="Type", value=str(club.type), inline=True)
    e.add_field(name="President",value=presname+'\n'+prestr,inline=True)
    e.add_field(name="Top member", value=str(members[0].name)+'\n'+str(members[0].trophies)+'\n'+str(members[0].role), inline=True)
    e.set_footer(text="Created By Lore")
    await ctx.send(embed=e)

#---- SET FUNCTION (GIVE ROLE TO MEMBERS FOR CURRENT CLAN)
async def set_(ctx,player:discord.Member,gametag):
    await ctx.trigger_typing()
    if gametag[0] != '#':
        await ctx.send("BadArguement: GameTag needs to start with #")
        return
    botdev = discord.utils.get(player.guild.roles, name="BotDeveloper")
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
    print("Function qlash clans called")
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
	if not await Check(ctx,ctx.message.author):
		#await ctx.send("You do not have permissions for this command!")
		return
	therolename = " ".join(rolename[:])
	role = discord.utils.get(ctx.guild.roles, name=therolename)
	if not role:
		await ctx.send("ArguementError: Role "+therolename+" does not exist. 😭")
		return
	print(member,role)
	await member.add_roles(role)

async def removerole(ctx,member:discord.Member , *rolename):
    if not await Check(ctx,ctx.message.author):
        #await ctx.send("You do not have permissions for this command!")
        return
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
    role = discord.utils.get(ctx.guild.roles, name="BotDeveloper")
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
    role = discord.utils.get(ctx.guild.roles, name="BotDeveloper")
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

async def purge_(ctx,amount):
	author = ctx.message.author
	await ctx.channel.purge(limit=int(amount)+1)
	msg = await ctx.send("Deleted "+str(amount)+" messages from "+author.mention+" in channel "+str(ctx.message.channel))
	await msg.delete(delay=5.0)

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
	Clan file directory: ./qlashclans2
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
	Clan file directory: ./qlashclans2
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
    dev = discord.utils.get(ctx.guild.roles, name="BotDeveloper")
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


async def read_file(message):
    ch = message.channel
    if ch.id == int(file_managing):
        if len(message.attachments)!=0 and not message.author.bot:
            start = timeit.default_timer()
            await ch.trigger_typing()
            att = message.attachments[0]
            await ch.send("Message received: \tName: "+str(att.filename)+" \tSize: "+str(att.size)+" \tID: "+str(att.id))
            content = await att.read()
            gametags = content.decode('utf-8').split('\n')
            clubs = brawlstats.count_clubs(gametags)
            file = io.StringIO()
            # Uknown
            brawlstats.add_file_lines(file, clubs, False, True, False, False, True)
            # Invalid
            brawlstats.add_file_lines(file, clubs, False, True, False, True, False)
            file.write("\n")
            file.write("Printing found clubs and no. participants:\n")
            brawlstats.add_file_lines(file, clubs, True, False, True, False, False)
            # Club members
            brawlstats.add_file_lines(file, clubs, False, True, True, False, False)
            file.seek(0)
            await ch.send(content=message.author.mention+", please see the file below to check out the number of participants.", file=discord.File(fp=file, filename="tournament_info.txt"))
            file.close()
            end = timeit.default_timer()
            await ch.send("The command took {EXECUTION_TIME:2f} seconds".format(EXECUTION_TIME = end - start))
