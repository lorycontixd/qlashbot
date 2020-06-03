import gspread
import os
credentials_path = './google-api/qlash-bot-c0a45565e4f0.json'
gc = gspread.service_account(filename=credentials_path)

async def writeall(ctx):
    sheet = gc.open("Registrations").sheet1
    colA = "A"
    colB = "B"
    int = 2
    for member in ctx.guild.members:
        row = str(int)
        cell1 = colA+row
        cell2 = colB+row
        sheet.update(cell1,str(member))
        sheet.update(cell2,str(member.joined_at))
        i+=1
    print("test write done")

async def xcel_member_search(name):
    sheet = gc.open("Registrations").sheet1
    cell = sheet.find(name)
    return cell
    print("member searched")

async def xcel_member_remove(cell):
    sheet = gc.open("Registrations").sheet1
    sheet.update(cell,"")
    print("member removed")

#async def xcel_member_add(name,):

#########################################################

async def xcel_responses():
    worksheet = gc.open("QLASH Brawl Stars -- Community Club Membership (Responses)")
    s1 = worksheet.sheet1
    
