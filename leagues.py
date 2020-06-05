#league system
#sheet1 - bronze | sheet2 - silver | sheet3 - gold | sheet4 - diamond | sheet5 - master

import discord
import gspread
import os

from instances import *

credentials_path = './google-api/qlash-bot-c0a45565e4f0.json'
gc = gspread.service_account(filename=credentials_path)
worksheet = gc.open("League Database")

leagues = ['Bronze','Silver','Gold','Diamond','Master']
async def get_league(player):
    for role in player.roles:
        if role.name in leagues:
            return role

async def get_sheet(player):
    role = get_league(player)
    if role.name == 'Bronze':
        sheet = worksheet.sheet1
    elif role.name == 'Silver':
        sheet = worksheet.sheet2
    elif role.name == 'Gold':
        sheet = worksheet.sheet3
    elif role.name == 'Diamond':
        sheet = worksheet.sheet4
    elif role.name == 'Master':
        sheet = worksheet.sheet5
    else:
        return

async def get_cell(player):
    sheet = get_sheet(player)
    cell = sheet.find(name)
    return cell
