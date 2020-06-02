import gspread
import os
credentials_path = './qlash-bot-c0a45565e4f0.json'
gc = gspread.service_account(filename=credentials_path)
sheet = gc.open("League Database")
print(sheet.sheet1.get('A1'))
