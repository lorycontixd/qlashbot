import aiohttp
import asyncio

import random
from mongodb import *
import instances

from xml.etree import ElementTree as ET
from lxml import etree, html
from io import StringIO

INVALID_GAMETAG = "Invalid gametag"
NOT_FOUND = "Not found"
NOT_READ = "Input not read"

def _extract_banned_member(message):
    string = StringIO()
    string.write("<banned>")
    string.write("<player " + message + " />")
    string.write("</banned>")
    tree = ET.fromstring(string.getvalue())

    fields_dict = tree.find('.//player')
    string.close()
    return fields_dict.attrib

async def _retrieve_member(session, gametag):
    gametag = _retrieve_gametag(gametag)
    if not gametag:
        return NOT_READ
    elif not _is_valid_gametag(gametag):
        return INVALID_GAMETAG
    else:
        url = "https://brawlstats.com/profile/{PLAYER_ID}".format(PLAYER_ID = gametag[1:])
        async with session.get(url) as r:
            if r.status != 200:
                return NOT_FOUND
            myparser = etree.HTMLParser(encoding="utf-8")
            htmlPage = etree.HTML(await r.text(), parser=myparser)
            if (_check_missing_element(_retrieve_playerClub, htmlPage, gametag)):
                club = _retrieve_playerClub(htmlPage)
                return club
            else:
                return NOT_FOUND

async def _process_banned_member(session, member, message):
    club = await _retrieve_member(session, member['tag'])
    #print(member, message.created_at,club)
    await message.remove_reaction('✅', instances.bot.user)
    await message.remove_reaction('❌', instances.bot.user)
    await message.remove_reaction('❓', instances.bot.user)
    if club in [INVALID_GAMETAG, NOT_FOUND, NOT_READ]:
        await message.add_reaction('❓')
    elif club.startswith("QLASH"):
        await message.add_reaction('✅')
    else:
        await message.add_reaction('❌')

def _check_missing_element(function, htmlPage, playerID):
    found = False
    try:
        function(htmlPage)
        found = True
    except Exception:
        pass
    return found

def _retrieve_gametag(line):
    return line.replace('O','0').rstrip()

def _retrieve_playerClub(htmlPage):
    return htmlPage.xpath('//div[@class="_3lMfMVxY-knKo2dnVHMCWG _21sSMvccqXG6cJU-5FNqzv yVyPKdb4lsiRak5TAnxs3"]//..//div[2]//div/text()')[0].split("\n")[1].strip()

def _is_valid_gametag(gametag):
    return re.search("^#[P, Y, L, Q, G, R, J, C, U, V, 0, 2, 8, 9]{5,14}$", gametag) is not None

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
    connector = aiohttp.TCPConnector(limit_per_host=2)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'}
    async with aiohttp.ClientSession(connector=connector,headers=headers) as session:
        statements = []
        for message in messages:
            banned_member = _extract_banned_member(message.content)
            statements.append(_process_banned_member(session, banned_member, message))
        await asyncio.gather(*statements)
