import brawlstats
import discord
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
import pandas as pd
import time
from datetime import datetime
from random import randint
import ipapi
from dateutil import tz
from descriptions import *
from aiohttp_proxy import ProxyConnector,ProxyType
import os
from dotenv import load_dotenv
import aiohttp

env_path = os.path.dirname(os.path.realpath(__file__)) + '/.env'
load_dotenv(dotenv_path=env_path)

#quota_url = 'http://6cy3e5odaiitpe:gxag60u036717xavs35razjk18s2@eu-west-static-03.quotaguard.com:9293'
#connector = ProxyConnector.from_url(quota_url)
#session = aiohttp.ClientSession(connector=connector)

#quota_url = 'http://6cy3e5odaiitpe:gxag60u036717xavs35razjk18s2@eu-west-static-03.quotaguard.com:9293'
connector = ProxyConnector(
    proxy_type=ProxyType.SOCKS5,
    host='54.72.12.1',#'eu-west-static-03.quotaguard.com',
    port=1080,
    username='6cy3e5odaiitpe',
    password='gxag60u036717xavs35razjk18s2',
    rdns=True
)

bot = commands.Bot(command_prefix=commands.when_mentioned_or('^'), description = bot_description)
bot_status = True
last_update = ''

async def on_ready_():
    print('Logged in as: ',bot.user)
    print('Bot ID: ',bot.user.id)
    print('Creation Date: ',bot.user.created_at)
    print('Websocket Gateway: ',bot.ws)
    print('----------------')
    mych = await bot.fetch_channel(int(bot_testing))
    await mych.send("Bot has logged in 🟢")
    await bot.change_presence( activity=discord.Activity(type=discord.ActivityType.playing, name=" ^help"))

async def on_disconnect_():
    print("Logging off: ",bot.user)
    mych = await bot.fetch_channel(int(bot_testing))
    await mych.send("Bot has logged off 🔴")

#bot properties
TOKEN = 'NzAxMTI1MzExMDQ3NDAxNDc0.XpyBZQ.RAsYlvnkrzI08mwFuXK8QF5K3BM'
clientid = '701125311047401474'
clientsecret = '9R3Ys-YNtsrHCCLYShWLVhWuAoezQuX1'
ipapi.location(ip=None, key=None, field=None)

#test friends tags
ignick_lory = 'loryconti'
igtag_lory = '#20VYUG2L'
qlash_ares = '#98VQUC8R'
igtag_picoz = '#20VVVVYQ8'
igtag_elgarzy = '#RC9PVRCJ'

#discord channel IDs
roles_assignment = '434850121134637056'
bot_testing = '705823922402361437'
en_general = '464691619569074177'
it_general = '415221650481610762'
support = '464695005156737024'
banlist = '493151669849161743'
banlist_testing = '713322449915215923'
entry_exit = '713735004827418625'
entries_discord = '714161674432806972'

#database directories
qlash_clans_file = './qlash_clans.csv'
qc_directory = './qlashclans/'
qc_directory2 = './qlashclans2/' #this one is the right one

#<<<<<<< HEAD
TOKEN2 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImUyOTQ3MjlhLWE5YjYtNDIxNy05MTdlLTUxZDJhYzRmOWI4NSIsImlhdCI6MTU5MDI3MDMwNywic3ViIjoiZGV2ZWxvcGVyLzMwMWI3NDk1LWE0OTQtYmIzNy05MWFlLWM5MGEyZmRjMDBjOSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNTQuNzIuMTIuMSIsIjU0LjcyLjc3LjI0OSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.RODZQwDO2YZZF_JAazFccdrg1YiPcaqGmxtPe40ZN-zvVDK3sXuX1-yqGWwjBdd-MoyTqfrsPxhS3V_IUNf9qQ'
#=======
LoryToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImUyOTQ3MjlhLWE5YjYtNDIxNy05MTdlLTUxZDJhYzRmOWI4NSIsImlhdCI6MTU5MDI3MDMwNywic3ViIjoiZGV2ZWxvcGVyLzMwMWI3NDk1LWE0OTQtYmIzNy05MWFlLWM5MGEyZmRjMDBjOSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNTQuNzIuMTIuMSIsIjU0LjcyLjc3LjI0OSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.RODZQwDO2YZZF_JAazFccdrg1YiPcaqGmxtPe40ZN-zvVDK3sXuX1-yqGWwjBdd-MoyTqfrsPxhS3V_IUNf9qQ'
DaddeToken='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjZjMTU2MzBkLTQ0N2UtNDU3Zi1iNTczLWU4OGI2NjE3Y2NhZSIsImlhdCI6MTU5MDA5NzM0MSwic3ViIjoiZGV2ZWxvcGVyLzAwNWYyOWI0LTVjMTMtYTNkMC1iYzBhLTMwYzQ5NTBkZTVmMCIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMzcuMTYwLjY0LjE1NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.nXcEEkmIDFmG0KAI3FBbQUql-aZ7-izRYF5OXr5hjAbgxbjgd7bePT7UCvY3td3A2jKp4PxaPLxfgdH1ewv2gw'
#connector = ProxyConnector.from_url('http://6cy3e5odaiitpe:gxag60u036717xavs35razjk18s2@eu-west-static-03.quotaguard.com:9293')#os.environ['QUOTAGUARDSTATIC_URL'])
myclient = brawlstats.Client(LoryToken,is_async=True,debug=True,connector=connector)

#time zones
from_zone = tz.tzutc() #utc
to_zone = tz.tzlocal() #local

#*****************************************************************************************************************
#*****************************************************************************************************************
#******************************************       NON-ASYNC     **************************************************
#*****************************************************************************************************************
#*****************************************************************************************************************

#FUNCTION REPLACING HAS_ANY_ROLE
def checkforrole(member: discord.Member, *roles):
	temp = " ".join(roles[:])
	searchingrole = temp.split(" ") #contains the roles that member must have (list)
	for role in member.roles:
		if role.name in searchingrole:
			return True
	return False

def removeEmoji(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

def CommandLogs(ctx,commandname):
    author = ctx.message.author
    time = datetime.now()
    logfile = open('command_logs.txt','a+')
    logfile.write(str(author)+" has called the command "+str(commandname)+" at time "+str(time)+'\n')
    logfile.close()

def LoadCsv():
    df = pd.DataFrame(columns = ['Name','Tag'])
    sourcefile = 'qlash_clans.csv'
    file = open(sourcefile,'r+')
    content = file.read()
    lines = content.split('\n')
    for i in range(len(lines)-1):
        ll = lines[i].split(',')
        cols = {'Name':[ll[0]],'Tag':[ll[1]]}
        df_temp = pd.DataFrame(cols,columns = ['Name','Tag'])
        df = df.append(df_temp,ignore_index = True)
    file.close()
    #print(df)
    return df

def is_me(m):
    return m.author == client.user

#*****************************************************************************************************************
#*****************************************************************************************************************
#**************************************       COMMAND FUNCTIONS     **********************************************
#*****************************************************************************************************************
#*****************************************************************************************************************


#stile banlist:  days of ban, tag ingame, nome ingame,
async def CheckBanlist(ctx):
	count=0
	channel = bot.get_channel(int(entry_exit))
	write_channel = bot.get_channel(int(banlist_testing))
	tempmsg = await ctx.send("Calculating and reporting bans in channel: "+channel.mention)
	await channel.trigger_typing()
	messages = await channel.history(limit=150).flatten()
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
				await writechannel.send("Ban for player "+str(temp[0])+" has expired.")
				continue
		file = open(qlash_clans_file,'r+')
		content = file.read()
		lines = content.split('\n')
		for i in range(len(lines)-1):
			ll = lines[i].split(',')
			clubTag = str(ll[1])
			cclub = await myclient.get_club(clubTag)
			for member in cclub.members:
				if str(member.tag) == str(playerTag):
					count+=1
					await writechannel.send("Player "+str(member.name)+" found in clan "+str(cclub.name))
	if count==0: #if no players were found in clans
		await writechannel.send("No banned players found in qlash clans")
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

async def Check(ctx,member):
    allowed = ["Daddedavided#2841","Lore#5934"]
    if member not in allowed:
        await ctx.send("You do not have the permission for this command! ")
        return False
    return True

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
async def set_(ctx,gametag):
	await ctx.trigger_typing()
	if gametag[0] != '#':
		await ctx.send("BadArguement: GameTag needs to start with #")
		return
	mess = ctx.message
	author = mess.author
	clanname = ''
	membergamename = ''
	rolename = ''
	readfile = 'qlash_clans.csv'
	writefile = 'registered.txt'
	file = open(readfile,'r+')
	content = file.read()
	lines = content.split('\n')
	foundRole = False
	file.close()
	for i in range(len(lines)-1): #cycle through clans
		ll=lines[i].split(",")
		nname = str(ll[0])
		role = discord.utils.get(author.guild.roles, name=nname)
		if role in author.roles and role.name!="QLASH Girl":
			await author.remove_roles(role)
		tag = str(ll[1])
		club = await myclient.get_club(tag)
		for member in club.members:
			if member.tag == gametag:
				foundRole = True
				await ctx.send("Position found in clan: "+str(club.name))
				#role = discord.utils.get(author.guild.roles, name=nname)
				await author.add_roles(role)
				membergamename = member.name
				clanname = nname
				rolename = str(role)
				break
		if foundRole == True:
			break
	#await ctx.trigger_typing()
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

	filetemp = open('registered.txt','r+')
	contenttemp = filetemp.read()
	linestemp = contenttemp.split('\n')
	filetemp.close()
	exists = False
	for k in range(len(linestemp)-1): #cycle through users in database
		lltemp=linestemp[k].split("\t")
		if str(author)==str(lltemp[0]):
			print("Found in database")
			exists = True
			break
	file2 = open(writefile,'a+')
	if exists == False:
		file2.write( str(ctx.author)+'\t'+str(gametag)+'\t'+str(dt_string)+'\n' )
		print("Registered")
	else:
		print("Already registered")
	file2.close()
	if foundRole==True:
		await mess.add_reaction('✅')
		await ctx.send("Role set for member "+author.mention+'\t'+"Role: "+str(rolename)+"\t"+"Time: "+str(dt_string))
		return
	else:
		await ctx.send("No role found. If you think this is a mistake, please contact our staff. Thank you!")
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
	df = LoadCsv()
	e=discord.Embed(title="List of all registered QLASH Clans", description="------------------------------------------------", color=0xffb43e)
	e2=discord.Embed(color=0xffb43e)
	e.set_author(name="QLASH Bot")
	for i in range(21):
		club = await myclient.get_club(str(df.iloc[i][1]))
		print("Club: "+str(df.iloc[i][0])+"/"+str(df.iloc[i][1]))
		e.add_field(name="Clan: "+str(club),value="Required Trophies: "+str(club.required_trophies),inline=True)
	for i in range(22,len(df.index)):
		club = await myclient.get_club(str(df.iloc[i][1]))
		print("Club: "+str(df.iloc[i][0])+"/"+str(df.iloc[i][1]))
		e2.add_field(name="Clan: "+str(club),value="Required Trophies: "+str(club.required_trophies),inline=True)
	e2.set_footer(text="Created By Lore")
	await ctx.send(embed=e)
	await ctx.send(embed=e2)
	print(" ")

async def qlash_cclan(ctx,name_tag):
    if not await Check(ctx,str(ctx.message.author)):
        return
    presname = ''
    prestr = ''
    qlashnames = ['QLASH','Qlash','qlash']
    name_tag = name_tag.capitalize()
    #if name_tag in qlashnames:
    #    await ctx.send("Invalid clan name: "+name_tag)
    #    return
    thetag = ''
    df = LoadCsv()
    for i in range(len(df.index)):
        if name_tag in str(df.iloc[i][0]):
            thetag = str(df.iloc[i][1])
            break
        elif name_tag == str(df.iloc[i][1]):
            thetag = str(df.iloc[i][1])
            break
    if not thetag:
        await ctx.send("Could not find QLASH Clan")
        return
    clan = await myclient.get_club(thetag)
    members = clan.members
    for member in members:
        if str(member.role).lower() == 'president':
            presname = str(member.name)
            prestr = str(member.trophies)
    await ctx.send("Collecting information for QLASH Clan: "+name_tag)
    e=discord.Embed(title="Qlash Clan Info: "+str(clan), description="------------------------------------------------", color=0x53d6fd)
    e.set_author(name="QLASH Bot")
    e.add_field(name="Clan", value=str(clan), inline=False)
    e.add_field(name="Member Count", value=str(len(clan.members)), inline=True)
    e.add_field(name="Description", value=str(clan.description), inline=True)
    e.add_field(name="Trophies", value=str(clan.trophies), inline=True)
    e.add_field(name="Required Trophies", value=str(clan.required_trophies), inline=True)
    e.add_field(name="Type", value=str(clan.type), inline=True)
    e.add_field(name="President",value=presname+'\n'+prestr,inline=True)
    e.add_field(name="Top member", value=str(members[0].name)+'\n'+str(members[0].trophies)+'\n'+str(members[0].role), inline=True)
    e.set_footer(text="Created By Lore")
    await ctx.send(embed=e)

async def GetClanMembers(ctx,name_tag):
    thename = ''
    thetag = ''
    df = LoadCsv()
    stringa = '```'
    for i in range(len(df.index)):
        if name_tag in str(df.iloc[i][0]):
            thename = str(df.iloc[i][0])
            thetag = str(df.iloc[i][1])
            break
        elif name_tag == str(df.iloc[i][1]):
            thename = str(df.iloc[i][1])
            thetag = str(df.iloc[i][1])
            break
    if not thetag:
        await ctx.send("Could not find QLASH Clan")
        return
    club = await myclient.get_club(thetag)
    e=discord.Embed(title="List of members for clan "+str(thename), description="------------------------------------------------", color=0xffb43e)
    e.set_author(name="QLASH Bot")
    i=1
    for member in club.members:
        stringa = stringa + str(member.name)+'\t'+str(member.role)+'\t'+str(member.tag)+'\n'
        #e.add_field(name="("+str(i)+") Member: "+str(member.name),value=str(member.trophies)+","+str(member.role),inline=True)
        #i=i+1
    #e.set_footer(text="Created By Lore")
    #await ctx.send(embed=e)
    stringa = stringa + '```'
    await ctx.send(stringa)
###******************************* READ / WRITE / ADD / DELETE ***********
async def clan_add_(ctx,tag,*cname):
    sourcefile = 'qlash_clans.csv'
    if tag[0] != '#':
        await ctx.send("Invalid Argument "+str(tag)+"! Please add # in front" )
        return
    clanname = " ".join(cname[:])
    #print(clanname)
    file = open(sourcefile,'a+')
    content = str(clanname)+","+str(tag)+"\n"
    file.write(content)
    file.close()
    await ctx.send("Added QLASH clan: "+clanname+" ("+tag+") to the database")
    return

async def clan_remove_(ctx,*cname):
    if not await Check(ctx,str(ctx.message.author)):
        return
    sourcefile = 'qlash_clans.csv'
    removedline = ''
    clanname = " ".join(cname[:])
    file = open(sourcefile,'r+')
    content = file.read()
    lines = content.split('\n')
    file.close()

    file2 = open(sourcefile,'w+')
    for line in lines:
        if clanname not in line:
            file2.write(line+'\n')
        elif clanname in line:
            print(line)
            removedline = line
            await ctx.send("Successfully removed "+str(removedline)+" from the database")
    if not removedline:
        await ctx.send("Could not find the clan you are looking for!")
    return

async def giverole(ctx,member: discord.Member , *rolename):
	if not Check(ctx,ctx.message.author):
		await ctx.send("You do not have permissions for this command!")
		return
	therolename = " ".join(rolename[:])
	mychannel = bot.get_channel(int(bot_logs))
	role = discord.utils.get(ctx.guild.roles, name=therolename)
	if not role:
		await ctx.send("ArguementError: Role "+therolename+" does not exist. 😭")
		return
	print(member,role)
	await member.add_roles(role)

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

async def member_info_(ctx,member:discord.Member):
	e=discord.Embed(title="Member info: "+str(member), description=str(member.mention), color=0x74a7ff)
	e.set_author(name="QLASH Bot")
	e.add_field(name="Created", value=str(member.created_at), inline=True)
	e.add_field(name="ID", value=str(member.id), inline=True)
	e.add_field(name="Joined Server", value=str(member.joined_at), inline=True)
	e.add_field(name="Premium Since", value=str(member.premium_since), inline=True)
	e.add_field(name="Status", value=str(member.status), inline=True)
	e.add_field(name="Mobile status", value=str(member.mobile_status),inline=True)
	e.add_field(name="Desktop status", value=str(member.desktop_status),inline=True)
	e.add_field(name="Top Role", value=str(member.top_role), inline=False)
	e.add_field(name="Permissions ", value=str(member.guild_permissions), inline=False)
	#e.set_image(member.default_avatar)
	e.set_footer(text="Bot created by Lore")
	await ctx.send(embed=e)

async def write_message(ctx,channelname,*message):
	temp = " ".join(message[:])
	guild = ctx.guild
	for channel in guild.text_channels:
		if str(channelname) in str(channel.name):
			await channel.send(temp)
			print("message sent in channel "+str(channel.name)+" using the bot")

async def purge_(ctx,amount):
	author = ctx.message.author
	await ctx.channel.purge(limit=int(amount))
	msg = await ctx.send("Deleted "+str(amount)+" messages from "+author.name)
	await msg.delete(delay=4.0)

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

async def view_database(ctx):
    response='```\n'
    sourcefile = 'qlash_clans.csv'
    file = open(sourcefile,'r+')
    content = file.read()
    lines = content.split('\n')
    file.close()
    for i in range(len(lines)-1): #cycle through clans
        ll=lines[i].split(",")
        name = str(ll[0])
        tag = str(ll[1])
        response+=str(name)+'\t'+str(tag)+'\n'
    response+='```'
    await ctx.send(response)
