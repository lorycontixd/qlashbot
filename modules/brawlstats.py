import requests
import re
import asyncio
import timeit

from sys import stdin
from time import sleep
from lxml import etree, html
from collections import defaultdict

INVALID_PLAYER_NAME = "Invalid Tag"
INVALID_CLUB = "Invalid"
NOT_FOUND_PLAYER_NAME = "Unknown Player"
NOT_FOUND_CLUB = "Unknown"

def _is_valid_gametag(gametag):
    return re.search("^#[P, Y, L, Q, G, R, J, C, U, V, 0, 2, 8, 9]{5,14}$", gametag) is not None

def _retrieve_playerName(htmlPage):
    return htmlPage.xpath('//div[@class="_3lMfMVxY-knKo2dnVHMCWG _21sSMvccqXG6cJU-5FNqzv yVyPKdb4lsiRak5TAnxs3"]/text()')[0].split("\n")[1].strip()
def _retrieve_playerClub(htmlPage):
    return htmlPage.xpath('//div[@class="_3lMfMVxY-knKo2dnVHMCWG _21sSMvccqXG6cJU-5FNqzv yVyPKdb4lsiRak5TAnxs3"]//..//div[2]//div/text()')[0].split("\n")[1].strip()
def _retrieve_gametag(line):
    gametag = line.replace('O','0').rstrip()

def _print(clubs, print_clubs = True, print_members = False, print_found = True, print_invalid =  False, print_not_found = False):
    for k in clubs:
        if k == INVALID_CLUB and not print_invalid:
            continue
        elif k == NOT_FOUND_CLUB and not print_not_found:
            continue
        elif not print_found and k != NOT_FOUND_CLUB and k != INVALID_CLUB:
            continue
        if (print_clubs):
            print(k, len(clubs[k]))
        if (print_members):
            print("{CLUB} members:".format(CLUB = k))
            for members in clubs[k]:
                gametag, playerName = members
                print(gametag,playerName)

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

def _check_response_code(r):
    if r.status_code != 200:
        raise Exception("page retrieval error.", playerID)

def _check_missing_element(function, htmlPage, playerID):
    found = False
    try:
        function(htmlPage)
        found = True
    except Exception:
        pass
    return found

def retrieve_player(session,playerID):
    url = "https://brawlstats.com/profile/{PLAYER_ID}".format(PLAYER_ID = playerID[1:])
    r = session.get(url)
    if r.encoding is None:
        r.encoding = 'utf-8'
    _check_response_code(r)
    myparser = etree.HTMLParser(encoding="utf-8")
    htmlPage = etree.HTML(r.content, parser=myparser)
#    htmlPage = html.fromstring(r.content)
    if (_check_missing_element(_retrieve_playerName, htmlPage, playerID) and _check_missing_element(_retrieve_playerClub, htmlPage, playerID)):
        return _retrieve_playerName(htmlPage), _retrieve_playerClub(htmlPage)
    else:
        return NOT_FOUND_PLAYER_NAME, NOT_FOUND_CLUB

def read_tags(session, lines):
    clubs = defaultdict(list)
    for line in lines:
        gametag = line.rstrip()
        if not gametag:
            break;
        elif _is_valid_gametag(gametag):
            playerName, playerClub = retrieve_player(session,gametag)
            clubs[playerClub].append((gametag,playerName))
            sleep(1)
        else:
            clubs[INVALID_CLUB].append((gametag, INVALID_PLAYER_NAME))
    return clubs

def count_clubs(gametags):
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    clubs = read_tags(session, gametags)
    session.close()
    return clubs
