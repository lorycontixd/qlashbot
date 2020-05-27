#tournament count file
from pymongo import MongoClient
from pprint import pprint
from instances import *

db = mongoclient.heroku_q2z34tjm
collection = db.QLASHBot_Collection

def register_member(discord,gametag,time):
    mydict = {
        "Discord" : discord,
        "Gametag" : gametag,
        "Clan" : clan,
        "Date" : time
    }
    return mydict

mydict1 = register_member("Daddedavided#1234","23VVA333","QLASH Ares","Tomorrow")
mydict2 = register_member("Lore#5934","#20VYUG2L","Now")
list = [mydict1,mydict2]

collection.insert_one(mydict1)
