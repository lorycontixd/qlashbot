#record

import asyncio
from scheduler import *
from instances import *

async def record2():
    guild = bot.get_guild(int(qlash_bs_id))
    membercount = guild.member_count
    #membercount = 14540
    today = date.today()
    mydict = {
        "Date":str(today),
        "Members":int(membercount)
    }
    coll_membercount.insert_one(mydict)
    #msg = await ctx.send("Registered today's member count")


async def daily_record():
    await record2()

loop = asyncio.get_event_loop()
loop.run_until_complete(daily_record())
loop.close()
