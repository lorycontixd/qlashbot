import aiohttp

import random
from mongodb import *
import instances

from xml.etree import ElementTree as ET
from io import StringIO

def _extract_banned_member(message):
    string = StringIO()
    string.write("<banned>")
    string.write("<player " + message + " />")
    string.write("</banned>")
    tree = ET.fromstring(string.getvalue())

    fields_dict = tree.find('.//player')
    string.close()
    return fields_dict.attrib


async def reddit_webhook():
   ch = instances.bot.get_channel(int(bot_developer_channel))
   async with aiohttp.ClientSession() as session:
       async with session.get('https://www.reddit.com/r/Brawlstars.json') as resp:
           if resp.status == 200:
               await ch.send("Reddit?")
               await ch.send(await resp.text())

async def reg_member():
    ch = instances.bot.get_channel(int(instances.bot_developer_channel))
    db = instances.mongoclient.heroku_q2z34tjm
    coll_membercount = db.QLASHBot_MemberCount
    today = date.today()
    mydict = {
        "Date":str(today),
        "Members":int(membercount)
    }
    coll_membercount.insert_one(mydict)
    msg = await ch.send("Today's member count registered has been... Hrmm... Yes!")

async def hello(param):
    ch = instances.bot.get_channel(int(instances.bot_developer_channel))
    await ch.send("Goodmorning, scheduled this message has been with " + param)

async def check_banlist_channel():
    ch = instances.bot.get_channel(724193592536596490)#int(instances.bot_banlist_channel))
    messages = await ch.history(limit=123).flatten()
    for message in messages:
        banned_member = _extract_banned_member(message.content)
        print(banned_member)
