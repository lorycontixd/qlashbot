import requests
import re
import asyncio
import timeit

from sys import stdin
from time import sleep
from lxml import html
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

# def _print_clubs(clubs, print_found = True, print_invalid = True, print_not_found = True):
#     for k in clubs:
#         if k == INVALID_CLUB and not print_invalid:
#             continue
#         elif k == NOT_FOUND_CLUB and not print_not_found:
#             continue
#         elif not print_found and k != NOT_FOUND_CLUB and k != INVALID_CLUB:
#             continue
#         print(k, len(clubs[k]))

# def _print_members(clubs, print_found = False, print_invalid = True, print_not_found = True):
#     for k in clubs:
#         if k == INVALID_CLUB and not print_invalid:
#             continue
#         elif k == NOT_FOUND_CLUB and not print_not_found:
#             continue
#         elif not print_found and k != NOT_FOUND_CLUB and k != INVALID_CLUB:
#             continue
#         print("{CLUB}:".format(CLUB = k))
#         for members in clubs[k]:
#             gametag, playerName = members
#             print(gametag,playerName)

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
        return NOT_FOUND_PLAYER_NAME, NOT_FOUND_CLUB

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
            clubs[INVALID_CLUB].append((gametag, INVALID_PLAYER_NAME))
    return clubs

def main_program():
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    clubs = read_tags(session)
    # print("Nothing#000")
    # _print_clubs(clubs, False, False, False)
    # print("")
    # print("Not found#001")
    # _print_clubs(clubs, False, False, True)
    # print("")
    # print("Invalid#010")
    # _print_clubs(clubs, False, True, False)
    # print("")
    # print("Members#100")
    # _print_clubs(clubs, True, False, False)
    # print("")
    # print("Members and not found#101")
    # _print_clubs(clubs, True, False, True)
    # print("")
    # print("Members and invalid#110")
    # _print_clubs(clubs, True, True, False)
    # print("")
    # print("All#111")
    # _print_clubs(clubs, True, True, True)
    # print("")
    # _print_members(clubs)

    print ("These members were not found:")
    print("")
    _print(clubs, False, True, False, False, True)
    print("")
    print ("These gametags were not valid:")
    print("")
    _print(clubs, False, True, False, True, False)
    print("")
    print("Printing found clubs and no. participants:")
    print("")
    _print(clubs, True, False, True, False, False)

    session.close()

main_program()
