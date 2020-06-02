import gspread
import os
credentials_path = './google-api/qlash-bot-c0a45565e4f0.json'
gc = gspread.service_account(filename=credentials_path)

async def testwrite(ctx):
    sheet = gc.open("Registrations")
    colA = "A"
    colB
    int = 2
    for member in ctx.guild.members:
        row = str(int)
        cell1 = colA+row
        cell2 = colB+row
        sheet.update(cell1,str(member))
        sheet.update(cell2,str(member.joined_at))
    print("test write done")

async def xcel_member_search(name):
    sheet = gc.open("Registrations")
    cell = sheet.find(name)
    return cell
    print("member searched")

async def xcel_member_remove(cell):
    sheet = gc.open("Registrations")
    sheet.update(cell,"")
    print("member removed")


#async def xcel_member_add(name,):
