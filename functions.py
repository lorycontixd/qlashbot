import brawlstats
import logging
import discord
import pandas as pd

TOKEN2 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImQ2YmJiYjY2LTQwNjEtNDU2NS1hMWMxLThlYzE4Y2M5NTczYiIsImlhdCI6MTU4NzI5MTA0OCwic3ViIjoiZGV2ZWxvcGVyLzMwMWI3NDk1LWE0OTQtYmIzNy05MWFlLWM5MGEyZmRjMDBjOSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNS4xNzEuOTAuMjI2Il0sInR5cGUiOiJjbGllbnQifV19.LDyqQhx8ICH9OYJoS2QeOl-mTGTmCj-5A4z01KmUM1wStLlrDsMsZIIKmQREzlUOcLxcwiYmn8H0pAB9AKHgYg'
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
    return df

async def hello_(ctx):
    await ctx.send("Hello "+ctx.message.author.name+"! \n My name is QLASH Bot, you can see my commands with ^help!")

async def qlash_(ctx):
    e=discord.Embed(title="QLASH", url="http://www.qlash.gg", description="Il Team QLASH è una organizzazione eSportiva con base in Italia. Co-fondata da Luca Pagano e Eugene Katchalov nel 2017, ha come scopo principale la promozione degli eSports in Italia e in Europa, creando sinergie con varie altre organizzazioni.",color=0x0061ff)
    e.set_author(name="QLASH Bot")
    e.set_image(url='https://liquipedia.net/commons/images/thumb/0/08/QLASH-PRO_black.png/600px-QLASH-PRO_black.png')
    await ctx.send(embed=e)

def GetClanTag(df,name):
    for i in range(len(df.index)):
        if name in str(df.iloc[i][0]):
            return str(df.iloc[i][1])
    print("Not Found")
    return

#async def getplayer(tag):
#    print("Getting player info: ")
#    player = await myclient.get_player(tag)
#    print("Player name: "+str(player))
#    print("Current Trophies: "+str(player.trophies))
#    print("Highest Trophies: "+str(player.highest_trophies))
#    print("Highest Power play points: "+str(player.highest_power_play_points))
#    print("Is qualified for Championship Challenge: ",player.is_qualified_from_championship_challenge)
#    print("3v3 Victories: "+str(player.x3vs3_victories))
#    print("Solo Victories: "+str(player.solo_victories))
#    print("Duo Victories: "+str(player.duo_victories))
#    print("Player Club: "+str(player.club.name)+" ("+str(player.club.tag)+")")
#    print("Brawler count: "+str(len(player.brawlers)))

async def getplayer(ctx,tag):
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
    e.add_field(name="Player Club", value=str(player.club), inline=True)
    e.add_field(name="Brawler Count", value=str(len(player.brawlers)), inline=True)
    e.set_footer(text="Created By Lore")
    await ctx.send(embed=e)

async def getclan(ctx,tag):
    await ctx.send("Getting club info: ")
    club = await myclient.get_club(tag)
    e=discord.Embed(title="Clan Info: "+str(club), description="------------------------------------------------", color=0xbe37f4)
    e.set_author(name="QLASH Bot")
    e.add_field(name="Clan", value=str(club), inline=False)
    e.add_field(name="Member Count", value=str(len(club.members)), inline=True)
    e.add_field(name="Description", value=str(club.description), inline=True)
    e.add_field(name="Trophies", value=str(club.trophies), inline=True)
    e.add_field(name="Required Trophies", value=str(club.required_trophies), inline=True)
    e.add_field(name="Type", value=str(club.type), inline=True)
    e.set_footer(text="Created By Lore")
    await ctx.send(embed=e)

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

async def qlash_trophies(ctx):
    await ctx.send("Gathering QLASH Clans information...")
    df = LoadCsv()
    e=discord.Embed(title="List of QLASH Clans", description="------------------------------------------------", color=0xffb43e)
    e.set_author(name="QLASH Bot")
    for i in range(len(df.index)):
        club = await myclient.get_club(str(df.iloc[i][1]))
        e.add_field(name="Clan: "+str(club),value="Required Trophies: "+str(club.required_trophies),inline=True)
    e.set_footer(text="Created By Lore")
    await ctx.send(embed=e)

async def qlash_cclan(ctx,name_tag):
    qlashnames = ['QLASH','Qlash','qlash']
    name_tag = name_tag.capitalize()
    if name_tag in qlashnames:
        await ctx.send("Invalid clan name: "+name_tag)
        return
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
    await ctx.send("Collecting information for QLASH Clan: "+name_tag)
    e=discord.Embed(title="Qlash Clan Info: "+str(clan), description="------------------------------------------------", color=0x53d6fd)
    e.set_author(name="QLASH Bot")
    e.add_field(name="Clan", value=str(clan), inline=False)
    e.add_field(name="Member Count", value=str(len(clan.members)), inline=True)
    e.add_field(name="Description", value=str(clan.description), inline=True)
    e.add_field(name="Trophies", value=str(clan.trophies), inline=True)
    e.add_field(name="Required Trophies", value=str(clan.required_trophies), inline=True)
    e.add_field(name="Type", value=str(clan.type), inline=True)
    e.set_footer(text="Created By Lore")
    await ctx.send(embed=e)
