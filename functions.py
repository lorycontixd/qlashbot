import brawlstats
import logging
import discord
import pandas as pd
import schedule
import time
from random import randint

roles_assignment = '434850121134637056'
bot_testing = '705823922402361437'

qc_directory = './qlashclans/'
qc_directory2 = './qlashclans2/'

TOKEN2 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6Ijc0ODcyNDJkLTliMWYtNGVlMi04ZjQyLTZmMmRiNzY3MDg5ZiIsImlhdCI6MTU5MDA1MTU3MCwic3ViIjoiZGV2ZWxvcGVyLzMwMWI3NDk1LWE0OTQtYmIzNy05MWFlLWM5MGEyZmRjMDBjOSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMzcuMTE2LjI1LjI3Il0sInR5cGUiOiJjbGllbnQifV19.74PJnDjJkn6YPSJ55yf7-Og2ASr-vd67Cb_xIpbZ59utmwCTfQpWX7AtPixk7lZG2UD6pNGAztWoo3AkRYr9mQ'
myclient = brawlstats.Client(TOKEN2,is_async=True)

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

def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]
#**************************************** FUN **********************************************
async def hello_(ctx):
    await ctx.send("Hello "+ctx.message.author.name+"! \n My name is QLASH Bot, you can see my commands with ^help!")

async def qlash_(ctx):
    e=discord.Embed(title="QLASH", url="http://www.qlash.gg", description="Il Team QLASH è una organizzazione eSportiva con base in Italia. Co-fondata da Luca Pagano e Eugene Katchalov nel 2017, ha come scopo principale la promozione degli eSports in Italia e in Europa, creando sinergie con varie altre organizzazioni.",color=0x0061ff)
    e.set_author(name="QLASH Bot")
    e.set_image(url='https://liquipedia.net/commons/images/thumb/0/08/QLASH-PRO_black.png/600px-QLASH-PRO_black.png')
    await ctx.send(embed=e)

async def roll_(ctx):
    value = randint(1,6)
    await ctx.send("You rolled a "+str(value))
#**************************************  VARIOUS  *******************************************
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
    if not await Check(ctx,str(ctx.message.author)):
        return
    player = await myclient.get_player(tag)
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
    if not await Check(ctx,str(ctx.message.author)):
        return
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

async def set_(ctx,gametag):
    if gametag[0] != '#':
        await ctx.send("BadArguement: GameTag needs to start with #")
        return
    clanname = ''
    membergamename = ''
    author = ctx.message.author
    readfile = 'qlash_clans.csv'
    writefile = 'registered.txt'
    file = open(readfile,'r+')
    content = file.read()
    lines = content.split('\n')
    file.close()
    for i in range(len(lines)-1): #cycle through clans
        ll=lines[i].split(",")
        #print(ll)
        nname = str(ll[0])
        tag = str(ll[1])
        club = await myclient.get_club(tag)
        for member in club.members:
            if member.tag == gametag:
                await ctx.send("Position found in clan: "+str(club.name))
                role = discord.utils.get(author.guild.roles, name=nname)
                await author.add_roles(role)
                membergamename = member.name
                clanname = nname
                break
        if clanname:
            break
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    file2 = open(writefile,'w+')
    file2.write( str(ctx.author)+'\t'+str(membergamename)+'\t'+str(gametag)+str(dt_string) )
    file2.close()


async def search_member(ctx,name,clubtag):
    if not await Check(ctx,str(ctx.message.author)):
        return
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
    if not await Check(ctx,str(ctx.message.author)):
        return
    await ctx.send("Gathering QLASH Clans information...")
    df = LoadCsv()
    e=discord.Embed(title="List of QLASH Clans", description="------------------------------------------------", color=0xffb43e)
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
    if not await Check(ctx,str(ctx.message.author)):
        return
    sourcefile = 'qlash_clans.csv'
    if tag[0] != '#':
        await ctx.send("Invalid Argument "+str(tag)+"! Please add # in front" )
        return
    clanname = " ".join(cname[:])
    print(clanname)
    file = open(sourcefile,'a+')
    content = str(clanname)+","+str(tag)+"\n"
    file.write(content)
    file.close()
    await ctx.send("Added QLASH clan: "+clanname+" ("+tag+")")
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
            await ctx.send("Successfully removed "+str(removedline))
    if not removedline:
        await ctx.send("Could not find the clan you are looking for!")
    return

async def WriteMembersToFile2(ctx):
    sourcefile = 'qlash_clans.csv'
    file = open(sourcefile,'r+')
    content = file.read()
    lines = content.split('\n')
    file.close()
    for i in range(len(lines)-1): #cycle through clans
        ll=lines[i].split(",")
        #print(ll)
        name = str(ll[0])
        tag = str(ll[1])
        club = await myclient.get_club(tag)
        memberlist = club.members
        fr = open(qc_directory2+name+'.txt','w+')
        print("----"+name+"----")
        for member in memberlist:
            fr.write(str(member.name)+'\t'+str(member.role)+'\t'+str(member.tag)+'\n')
    print("Database Updated!")
    await ctx.send("Database Updated!")

async def CompareMembers(ctx):
    sourcefile = 'qlash_clans.csv'
    file = open(sourcefile,'r+')
    content = file.read()
    lines = content.split('\n')
    file.close()
    for i in range(len(lines)-1): #cycle through clans
        oldtags = []
        newtags = []
        ll=lines[i].split(",")
        name = str(ll[0])
        print(name)
        tag = str(ll[1])
        file2 = open(qc_directory2+name+'.txt','r+') #file vecchio
        content2 = file2.read()
        lines2 = content2.split('\n')
        file2.close()
        for j in range(len(lines2)-1):
            ll2=lines2[j].split("\t")
            membertag = str(ll2[2])
            membertag.replace("''", '')
            oldtags.append(membertag)

        club = await myclient.get_club(tag)
        for member in club.members:
            newtags.append(str(member.tag))

        for it1 in newtags:
            if it1 not in oldtags:
                print(it1," ","joined")

        for it2 in oldtags:
            if it2 not in newtags:
                print(it2," ","left")
