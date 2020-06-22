import aiohttp
import asyncio

from datetime import datetime,date
import re
import discord

import random
from mongodb import *
import instances

from xml.etree import ElementTree as ET
from lxml import etree, html
from io import StringIO

INVALID_GAMETAG = "Invalid gametag"
NOT_FOUND = "Not found"
NOT_READ = "Input not read"
XML_FORM_ERROR = "Input not read"

def _extract_banned_member(message):
    string = StringIO()
    string.write("<banned>")
    string.write("<player " + message + " />")
    string.write("</banned>")
    try:
        tree = ET.fromstring(string.getvalue())
        string.close()
        fields_dict = tree.find('.//player')
        return fields_dict.attrib
    except:
        return NOT_READ


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
    if(member == XML_FORM_ERROR):
        await message.add_reaction('❓')
        return

    time_expire = None
    try:
        await message.remove_reaction('📅', instances.bot.user)
        regex = re.compile("(\d+?)d")
        str_integer_match = regex.match(member['ban']).group(1)
        time_expire = int(str_integer_match)
        if time_expire is None:
            raise Exception
    except:
        await message.add_reaction('📅')
        return

    if(_check_time_expired(message.created_at.date(), time_expire)):
        await message.delete()
        return

    await message.remove_reaction('✅', instances.bot.user)
    await message.remove_reaction('❌', instances.bot.user)
    await message.remove_reaction('❓', instances.bot.user)

    club = await _retrieve_member(session, member['tag'])
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

def _check_time_expired(d0, time_expire):
    d1 = datetime.now().date()
    delta = d1 - d0
    return delta.days >= time_expire

async def reddit_webhook():
   ch = instances.bot.get_channel(int(instances.bot_developer_channel))
   async with aiohttp.ClientSession() as session:
       async with session.get('https://www.reddit.com/r/Brawlstars.json') as resp:
           if resp.status == 200:
               await ch.send("Reddit?")
               await ch.send(await resp.text())

async def reg_member():
    ch = instances.bot.get_channel(int(instances.bot_developer_channel))
    qlchannel = instances.bot.get_channel(int(instances.qlash_bot))
    db = instances.mongoclient.heroku_q2z34tjm
    coll_membercount = db.QLASHBot_MemberCount
    today = date.today()
    mydict = {
        "Date":str(today),
        "Members":int(membercount)
    }
    coll_membercount.insert_one(mydict)
    time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    e=discord.Embed(title="New scheduled event:", description="------------------------------------------------", color=0xd357fe)
    e.add_field(name="Event type",value="Registration",inline=True)
    e.add_field(name="Variable",value="Server members",inline=True)
    e.add_field(name="Channel",value="None",inline=True)
    e.add_field(name="Date",value=str(time),inline=True)
    e.set_footer(text="Created by Lore")
    await qlchannel.send(embed=e)


async def check_banlist_channel():
    botdev = instances.bot.get_channel(int(instances.bot_developer_channel))
    qlchannel = instances.bot.get_channel(int(instances.qlash_bot))
    ch = instances.bot.get_channel(724193592536596490)#int(instances.bot_banlist_channel))
    messages = await ch.history(limit=200).flatten()
    connector = aiohttp.TCPConnector(limit_per_host=2)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'}
    async with aiohttp.ClientSession(connector=connector,headers=headers) as session:
        statements = []
        for message in messages:
            banned_member = _extract_banned_member(message.content)
            statements.append(_process_banned_member(session, banned_member, message))
        await asyncio.gather(*statements)
    time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    e=discord.Embed(title="New scheduled event:", description="------------------------------------------------", color=0xd357fe)
    e.add_field(name="Event type",value="Check Banlist",inline=True)
    e.add_field(name="Channel",value=ch.name,inline=True)
    e.add_field(name="Date",value=str(time),inline=True)
    e.set_footer(text="Created by Lore")
    await qlchannel.send(embed=e)

async def hello_en():
    ch = instances.bot.get_channel(int(instances.en_general))
    qlchannel = instances.bot.get_channel(int(instances.qlash_bot))
    time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    message="Goodmorning everyone!"
    await ch.send(message)
    e=discord.Embed(title="New scheduled event:", description="------------------------------------------------", color=0xd357fe)
    e.add_field(name="Event type",value="Message",inline=True)
    e.add_field(name="Content",value=message,inline=True)
    e.add_field(name="Channel",value=ch.name,inline=True)
    e.add_field(name="Date",value=str(time),inline=True)
    e.set_footer(text="Created by Lore")
    await qlchannel.send(embed=e)
