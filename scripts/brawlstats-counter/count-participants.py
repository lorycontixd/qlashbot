import requests
import re

from sys import stdin
from time import sleep
from lxml import html
from collections import defaultdict

def _is_valid_gametag(gametag):
    return re.search("^#[P, Y, L, Q, G, R, J, C, U, V, 0, 2, 8, 9]{5,14}$", gametag) is not None

def _retrieve_playerName(htmlPage):
    return htmlPage.xpath('//div[@class="_3lMfMVxY-knKo2dnVHMCWG _21sSMvccqXG6cJU-5FNqzv yVyPKdb4lsiRak5TAnxs3"]/text()')[0].split("\n")[1].strip()
def _retrieve_playerClub(htmlPage):
    return htmlPage.xpath('//div[@class="_3lMfMVxY-knKo2dnVHMCWG _21sSMvccqXG6cJU-5FNqzv yVyPKdb4lsiRak5TAnxs3"]//..//div[2]//div/text()')[0].split("\n")[1].strip()

def _print_clubs(clubs):
    for k in clubs:
        print(k, len(clubs[k]))
def _print_members(clubs):
    for k in clubs:
        print("{CLUB}:".format(CLUB = k))
        for members in clubs[k]:
            gametag, playerName = members
            print(gametag,playerName)

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
    _check_response_code(r)
    htmlPage = html.fromstring(r.content)
    if (_check_missing_element(_retrieve_playerName, htmlPage, playerID) and _check_missing_element(_retrieve_playerClub, htmlPage, playerID)):
        return _retrieve_playerName(htmlPage), _retrieve_playerClub(htmlPage)
    else:
        return "Unknown name", "Unknown club"

def read_tags(session):
    clubs = defaultdict(list)
    for line in stdin:
        gametag = line.rstrip()
        if not gametag:
            break;
        elif _is_valid_gametag(gametag):
            playerName, playerClub = retrieve_player(session,gametag)
            clubs[playerClub].append((gametag,playerName))
            sleep(1)
        else:
            clubs["Invalid"].append((gametag, "Invalid"))
    return clubs

def main_program():
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    clubs = read_tags(session)
    _print_clubs(clubs)
    #_print_members(clubs)
    session.close()

main_program()
