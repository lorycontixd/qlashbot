import aiohttp
import asyncio

from datetime import datetime,date
import re
import discord

import random
from mongodb import *
from utility import *
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
    await message.remove_reaction('📅', instances.bot.user)
    await message.remove_reaction('✅', instances.bot.user)
    await message.remove_reaction('❌', instances.bot.user)
    await message.remove_reaction('❓', instances.bot.user)

    if(member == XML_FORM_ERROR):
        await message.add_reaction('❓')
        return

    if 'ban' in member:
        time_expire = None
        try:
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
    db = instances.mongoclient.heroku_q2z34tjm

    coll_membercount = db.QLASHBot_MemberCount
    today = date.today()
    mydict = {
        "Date":str(today),
        "Members":int(membercount)
    }
    coll_membercount.insert_one(mydict)
    logs = instances.bot.get_channel(int(instances.qlash_bot))
    tz = pytz.timezone('Europe/Rome')
    time=str(datetime.now(tz=tz).strftime("%d/%m/%Y, %H:%M:%S"))
    embed=discord.Embed(title="New scheduled event triggered", description="--------------------------------------", color=0xd357fe)
    embed.add_field(name="Event Type", value="Member registration", inline=True)
    embed.add_field(name="Content", value="None", inline=True)
    embed.add_field(name="Channel", value="None", inline=True)
    embed.add_field(name="Time", value=time, inline=True)
    embed.set_footer(text="Created by Lore")
    await logs.send(embed=embed)

async def hello(param):
    ch = instances.bot.get_channel(int(instances.bot_developer_channel))
    await ch.send("Goodmorning everyone!")
    logs = instances.bot.get_channel(int(instances.qlash_bot))
    tz = pytz.timezone('Europe/Rome')
    time=str(datetime.now(tz=tz).strftime("%d/%m/%Y, %H:%M:%S"))
    embed=discord.Embed(title="New scheduled event triggered", description="--------------------------------------", color=0xd357fe)
    embed.add_field(name="Event Type", value="Message", inline=True)
    embed.add_field(name="Content", value="Good Morning", inline=True)
    embed.add_field(name="Channel", value=ch.name, inline=True)
    embed.add_field(name="Time", value=time, inline=True)
    embed.set_footer(text="Created by Lore")
    await logs.send(embed=embed)

async def check_banlist_channel():
    botdev = instances.bot.get_channel(int(instances.bot_developer_channel))
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
    logs = instances.bot.get_channel(int(instances.qlash_bot))
    tz = pytz.timezone('Europe/Rome')
    time=str(datetime.now(tz=tz).strftime("%d/%m/%Y, %H:%M:%S"))
    embed=discord.Embed(title="New scheduled event triggered", description="--------------------------------------", color=0xd357fe)
    embed.add_field(name="Event Type", value="Check Banlist", inline=True)
    embed.add_field(name="Content", value="None", inline=True)
    embed.add_field(name="Channel", value="None", inline=True)
    embed.add_field(name="Time", value=time, inline=True)
    embed.set_footer(text="Created by Lore")
    await logs.send(embed=embed)

async def giova():
    #g = await bot.fetch_guild(415221296247341066)
    member = await bot.fetch_user(349225999164243969)
    if member==None:
        print("No member found with this ID")
    lines = fileread('./textfile/santi.txt')
    for i in range(len(lines)):
        ll=lines[i].split(":")
        date = str(ll[0])
        text = str(ll[1])
        tz = pytz.timezone('Europe/Rome')
        dday=str(datetime.now(tz=tz).strftime("%d"))
        month = ""
        mmonth = str(datetime.now(tz=tz).strftime("%m"))
        if mmonth=='01':
            month="gennaio"
        elif mmonth=='02':
            month="febbraio"
        elif mmonth=='03':
            month="marzo"
        elif mmonth=='04':
            month="aprile"
        elif mmonth=='05':
            month="maggio"
        elif mmonth=='06':
            month="giugno"
        elif mmonth=='07':
            month="luglio"
        elif mmonth=='08':
            month="agosto"
        elif mmonth=='09':
            month="settembre"
        elif mmonth=='10':
            month="ottobre"
        elif mmonth=='11':
            month="novembre"
        elif mmonth=='12':
            month="dicembre"
        string = dday+" "+month
        if string in date:
            print(string)
            await member.create_dm()
            message="Bona jurnat Giova, oggi è il "+string+'\nEcco i santi di oggi:\n\n'+text
            await member.dm_channel.send(text)
            break
    logs = instances.bot.get_channel(int(instances.qlash_bot))
    tz = pytz.timezone('Europe/Rome')
    time=str(datetime.now(tz=tz).strftime("%d/%m/%Y, %H:%M:%S"))
    embed=discord.Embed(title="New scheduled event triggered", description="--------------------------------------", color=0xd357fe)
    embed.add_field(name="Event Type", value="Message", inline=True)
    embed.add_field(name="Content", value="Daily Saint", inline=True)
    embed.add_field(name="Channel", value=str(member)+"'s DM'", inline=True)
    embed.add_field(name="Time", value=time, inline=True)
    embed.set_footer(text="Created by Lore")
    await logs.send(embed=embed)
