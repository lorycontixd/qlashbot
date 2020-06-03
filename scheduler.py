#schedule
import schedule
import time
import calendar
from matplotlib import pyplot as plt
from datetime import date
from datetime import datetime
from instances import *
from mongodb import *

async def addsingle(date,member):
    mydict = {
        "Date":str(date),
        "Members":int(member)
    }
    coll_membercount.insert_one(mydict)

async def record():
    #guild = bot.get_guild(int(qlash_bs_id))
    #membercount = guild.member_count
    membercount = 14540
    today = date.today()
    mydict = {
        "Date":str(today),
        "Members":int(membercount)
    }
    coll_membercount.insert_one(mydict)

async def removeall():
    coll_membercount.delete_many({})

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
    plt.plot(list_date,list_members)
    pathname = './graphs/'+month+year+'.png'
    plt.savefig(pathname)
    #cloudinary.uploader.upload(pathname)
    await ctx.send(file=discord.File(pathname))

#addsingle('2020-06-01',15654)
#addsingle('2020-06-02',15120)
#addsingle('2020-06-03',13564)
#analyze()
