#tournament count file
from pprint import pprint
from instances import *

db = mongoclient.heroku_q2z34tjm
coll_registered = db.QLASHBot_Registered
coll_commandlogs = db.QLASHBot_CommandLogs

#*****************************************************************************************************************
#*******************************************       REGISTERED     ************************************************
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
    if document = None:
        print("MONGO_DB: Nothing returned from Check Member ")
        return
    return document #type <dict>


#*****************************************************************************************************************
#*********************************************       LOGS     ****************************************************
#*****************************************************************************************************************

#collection.insert_one(mydict1)