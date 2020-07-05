#schedule
import discord
import schedule
import time
import calendar
from matplotlib import pyplot as plt
from datetime import date
from datetime import datetime
from modules.util_mongodb import *
from syncer import sync


async def iqloudy_info_(ctx):
    role = discord.utils.get(ctx.guild.roles, name="DiscordDeveloper")
    response = "This bot was written in the language of Python by a few users "+role.mention+" with a passion for informatics and programming. \nThe core library used is the API offered by Discord called discordpy which grants access to an enormous amount of functions and events."
    response2 = "The brawlstats API was also used to gather information from the game, which allows to access a few but useful pieces of information. The bot commands can be viewed by typing ^help and navigating using groups (mod,util,sys and fun)"
    await ctx.send(response)
    await ctx.send(response2)
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


#**************************  database interaction  ********************************

async def addsingle(ctx,coll_membercount,date,member):
    mydict = {
        "Date":str(date),
        "Members":int(member)
    }
    coll_membercount.insert_one(mydict)
    msg = await ctx.send("Member count added to the database")

async def record(ctx,coll_membercount):
    membercount = ctx.guild.member_count
    #membercount = 14540
    today = date.today()
    mydict = {
        "Date":str(today),
        "Members":int(membercount)
    }
    coll_membercount.insert_one(mydict)
    msg = await ctx.send("Registered today's member count")

async def removeall(ctx,coll_membercount):
    coll_membercount.delete_many({})
    msg = await ctx.send("Cleared!")

async def analyze(ctx,coll_membercount):
    firstdays = ['01','02','03','04','05','06','07','08','09']
    list_date = []
    list_members = []
    mydate = datetime.now()
    month = mydate.strftime("%B")
    year = mydate.strftime("%Y")
    for document in coll_membercount.find():
        date = str(document["Date"])
        mcount = int(document["Members"])
        date = str(date[-2:])
        if date in firstdays:
            date = str(date[1])
        date = int(date)
        list_date.append(date)
        list_members.append(mcount)
    plt.title("Member counts for "+month+" "+year)
    plt.xlabel("Date of "+month)
    plt.ylabel("Number of members in server")
    plt.plot(list_date,list_members)
    pathname = './media/images/membergraph-'+month+year+'.png'
    plt.savefig(pathname,bbox_inches='tight')
    #cloudinary.uploader.upload(pathname)
    await ctx.send(file=discord.File(pathname))
    await ctx.send("Current member count: "+str(ctx.guild.member_count))
