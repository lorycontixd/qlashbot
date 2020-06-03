#schedule
import schedule
import time
import calendar
from matplotlib import pyplot as plt
from datetime import date
from datetime import datetime
from instances import *
from mongodb import *
from syncer import sync

async def addsingle(ctx,date,member):
    mydict = {
        "Date":str(date),
        "Members":int(member)
    }
    coll_membercount.insert_one(mydict)
    msg = await ctx.send("Member count added to the database")
    await msg.delete(delay=5.0)

async def record(ctx):
    membercount = ctx.guild.member_count
    #membercount = 14540
    today = date.today()
    mydict = {
        "Date":str(today),
        "Members":int(membercount)
    }
    coll_membercount.insert_one(mydict)
    msg = await ctx.send("Registered today's member count")
    await msg.delete(delay=5.0)

async def removeall(ctx):
    coll_membercount.delete_many({})
    msg = await ctx.send("Cleared!")
    await msg.delete(delay=5.0)

async def analyze(ctx):
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
    pathname = './graphs/'+month+year+'.png'
    plt.savefig(pathname,bbox_inches='tight')
    #cloudinary.uploader.upload(pathname)
    await ctx.send(file=discord.File(pathname))
    await ctx.send("Current member count: "+str(ctx.guild.member_count))
