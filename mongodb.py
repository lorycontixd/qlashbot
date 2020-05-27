#tournament count file
from pprint import pprint
from instances import *

db = mongoclient.heroku_q2z34tjm
coll_registered = db.QLASHBot_Registered
coll_commandlogs = db.QLASHBot_CommandLogs
coll_qlashclans = db.QLASHBot_Clans

#*****************************************************************************************************************
#********************************************       MEMBERS     **************************************************
#*****************************************************************************************************************

def register_member(discord,gametag,clan,time):
    mydict = {
        "Discord" : discord,
        "Gametag" : gametag,
        "Clan" : clan,
        "Date" : time
    }
    coll_registered.insert_one(mydict)

def check_member(discord):
    document = coll_registered.find_one({"Discord":{"$eq":str(discord)}})
    if document == None:
        print("MONGO_DB: Nothing returned from Check Member ")
    return document #type <dict>

#*****************************************************************************************************************
#*********************************************       CLANS     ***************************************************
#*****************************************************************************************************************

def register_clan(tag,name):
    mydict = {
        "Name" : name,
        "Tag" : tag
    }
    coll_qlashclans.insert_one(mydict)

def remove_clan(name):
    result = coll_qlashclans.delete_one({"Name":{"$eq":str(name)}})

#*****************************************************************************************************************
#******************************************       COMMAND LOGS     ***********************************************
#*****************************************************************************************************************

def register_commandlog(user,command,time,failed,reason):
    mydict = {
        "User" : user,
        "Command" : command,
        "Time" : time,
        "Failed" : failed,
        "Reason" : reason
    }
    coll_commandlogs.insert_one(mydict)

def view_commandlog(int):
    list = []
    for document in coll_commandlogs.find():
        list.append(document)
    list = list[-int:]
    return list
#*****************************************************************************************************************
#*********************************************       LOGS     ****************************************************
#*****************************************************************************************************************
remove_clan("TestClan")
#collection.insert_one(mydict1)
