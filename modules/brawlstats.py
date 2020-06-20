import aiohttp
import re
import asyncio
import timeit

from sys import stdin
from lxml import etree, html
from collections import defaultdict

INVALID_PLAYER_NAME = "Invalid Tag"
INVALID_CLUB = "Invalid"
NOT_FOUND_PLAYER_NAME = "Unknown Player"
NOT_FOUND_CLUB = "Unknown"

def _retrieve_gametag(line):
    return line.replace('O','0').rstrip()

def _is_valid_gametag(gametag):
    return re.search("^#[P, Y, L, Q, G, R, J, C, U, V, 0, 2, 8, 9]{5,14}$", gametag) is not None

def _retrieve_playerName(htmlPage):
    return htmlPage.xpath('//div[@class="_3lMfMVxY-knKo2dnVHMCWG _21sSMvccqXG6cJU-5FNqzv yVyPKdb4lsiRak5TAnxs3"]/text()')[0].split("\n")[1].strip()

def _retrieve_playerClub(htmlPage):
    return htmlPage.xpath('//div[@class="_3lMfMVxY-knKo2dnVHMCWG _21sSMvccqXG6cJU-5FNqzv yVyPKdb4lsiRak5TAnxs3"]//..//div[2]//div/text()')[0].split("\n")[1].strip()


def add_file_lines(f, clubs, print_clubs = True, print_members = False, print_found = True, print_invalid =  False, print_not_found = False):
    for k in clubs:
        if k == INVALID_CLUB and not print_invalid:
            continue
        elif k == NOT_FOUND_CLUB and not print_not_found:
            continue
        elif not print_found and k != NOT_FOUND_CLUB and k != INVALID_CLUB:
            continue
        if (print_clubs):
            f.write("{CLUB} {NO_PARTICIPANTS}\n".format(CLUB = k, NO_PARTICIPANTS = len(clubs[k])))
        if (print_members):
            f.write("\n{CLUB} members:\n".format(CLUB = k))
            for members in clubs[k]:
                gametag, playerName = members
                f.write("{GAMETAG} {PLAYER_NAME}\n".format(GAMETAG = gametag, PLAYER_NAME = playerName))

def _check_missing_element(function, htmlPage, playerID):
    found = False
    try:
        function(htmlPage)
        found = True
    except Exception:
        pass
    return found

async def retrieve_player(session, playerID):
    url = "https://brawlstats.com/profile/{PLAYER_ID}".format(PLAYER_ID = playerID[1:])
    async with session.get(url) as r:
        if r.status != 200:
            return NOT_FOUND_PLAYER_NAME, NOT_FOUND_CLUB
        myparser = etree.HTMLParser(encoding="utf-8")
        htmlPage = etree.HTML(await r.text(), parser=myparser)
        if (_check_missing_element(_retrieve_playerName, htmlPage, playerID) and _check_missing_element(_retrieve_playerClub, htmlPage, playerID)):
            return _retrieve_playerName(htmlPage), _retrieve_playerClub(htmlPage)
        else:
            return NOT_FOUND_PLAYER_NAME, NOT_FOUND_CLUB

async def read_tags(session, clubs, gametags, loading_msg, current, total_tags):
    for gametag in gametags:
        current += 1
        await read_tag(session, clubs, gametag, loading_msg, current, total_tags)

async def read_tag(session, clubs, gametag, loading_msg = None, current = 0, total_tags=0):
    gametag = _retrieve_gametag(gametag)
    if not gametag:
        clubs[INVALID_CLUB].append(("Input not read", INVALID_PLAYER_NAME))
        return
    if _is_valid_gametag(gametag):
        playerName, playerClub = await retrieve_player(session, gametag)
        clubs[playerClub].append((gametag,playerName))
    else:
        clubs[INVALID_CLUB].append((gametag, INVALID_PLAYER_NAME))
    if loading_msg is not None:
        await loading_msg.edit(content="{no} out of {TAGS} gametags processed".format(no = current, TAGS = total_tags))
        current += 1


async def count_clubs(gametags, loading_msg = None):
    connector = aiohttp.TCPConnector(limit_per_host=2)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'}

    async with aiohttp.ClientSession(connector=connector,headers=headers) as session:
        clubs = defaultdict(list)
        await asyncio.gather(read_tags(session, clubs, gametags, loading_msg, 0, len(gametags)))
        return clubs
