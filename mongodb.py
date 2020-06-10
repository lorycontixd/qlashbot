#tournament count file
from pprint import pprint
from instances import *

db = mongoclient.heroku_q2z34tjm
coll_registered = db.QLASHBot_Registered
coll_commandlogs = db.QLASHBot_CommandLogs
coll_qlashclans = db.QLASHBot_Clans
coll_membercount = db.QLASHBot_MemberCount

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
    return document #type <dict>

def remove_member(discord,tag):
    coll_registered.delete_one({"Discord":{"$eq":str(discord)}})

async def view_database(ctx):
    response='```\n'
    response+="Name\tTag\tRoleID\tChannelID\n"
    i=1
    for document in coll_qlashclans.find():
        name = str(document["Name"])
        tag = str(document["Tag"])
        roleID = str(document["RoleID"])
        channelID = str(document["ChannelID"])
        response += str(i)+'. '+name+'\t'+tag+'\t'+roleID+'\t'+channelID+'\n'
        i+=1
    response+='```'
    await ctx.send(response)



#*****************************************************************************************************************
#*********************************************       CLANS     ***************************************************
#*****************************************************************************************************************

def get_clan(*nname):
    name = " ".join(nname[:])
    document = coll_qlashclans.find_one({"Name":{"$eq":str(name)}})
    return document #type <dict>

def LoadClans():
    list = []
    for document in coll_qlashclans.find():
        list.append(document)
    return list #list of dicts ("Name","Tag","RoleID","ChannelID")

def register_clan(roleID,channelID,tag,name):
    mydict = {
        "Name" : name,
        "Tag" : tag,
        "RoleID": str(roleID),
        "ChannelID": str(channelID)
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

def delete_commandlogs():
    coll_commandlogs.delete_many({})

#*****************************************************************************************************************
#*******************************************       TOURNAMENTS     ***********************************************
#*****************************************************************************************************************
