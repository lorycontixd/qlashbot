#tournament count file
from pprint import pprint
from datetime import date
import re
import instances

# coll_registered = db.QLASHBot_Registered
# coll_commandlogs = db.QLASHBot_CommandLogs
# coll_qlashclans = db.QLASHBot_Clans
# coll_membercount = db.QLASHBot_MemberCount
# coll_achievements = db.QLASHBot_Achievements

#*****************************************************************************************************************
#********************************************       MEMBERS     **************************************************
#*****************************************************************************************************************

def register_member(member,gametag):
    db = instances.mongoclient.heroku_q2z34tjm
    coll_registered = db.QLASHBot_Registered
    mydict = {
        "Discord" : str(member),
        "DiscordID" : int(member.id),
        "Gametag" : gametag,
        "Date" : str(date.today()),
        "Achievements" : []
    }
    coll_registered.insert_one(mydict)

def check_member(discord):
    db = instances.mongoclient.heroku_q2z34tjm
    coll_registered = db.QLASHBot_Registered
    document = coll_registered.find_one({"Discord":{"$eq":str(discord)}})
    return document #type <dict>

def remove_member(discord,tag):
    db = mongoclient.heroku_q2z34tjm
    coll_registered = db.QLASHBot_Registered
    coll_registered.delete_one({"Discord":{"$eq":str(discord)}})

async def view_database(ctx,member):
    db = instances.mongoclient.heroku_q2z34tjm
    coll_qlashclans = db.QLASHBot_Clans
    response='```\n'
    response+="Name\tTag\tRoleID\tChannelID\n"
    i=1
    for document in coll_qlashclans.find():
        name = str(document["Name"])
        tag = str(document["Tag"])
        roleID = str(document["RoleID"])
        channelID = str(document["ChannelID"])
        response += str(i)+'. '+name+'\t'+tag+'\n'
        i+=1
    response+='```'
    await member.create_dm
    await member.dm_channel.send(response)



#*****************************************************************************************************************
#*********************************************       CLANS     ***************************************************
#*****************************************************************************************************************

def get_clan(*nname):
    db = instances.mongoclient.heroku_q2z34tjm
    coll_qlashclans = db.QLASHBot_Clans
    name = " ".join(nname[:])
    document = coll_qlashclans.find_one({"Name":{"$eq":str(name)}})
    return document #type <dict>

def LoadClans():
    db = instances.mongoclient.heroku_q2z34tjm
    coll_qlashclans = db.QLASHBot_Clans
    list = []
    for document in coll_qlashclans.find():
        list.append(document)
    return list #list of dicts ("Name","Tag","RoleID","ChannelID")

def register_clan(roleID,channelID,tag,name):
    db = instances.mongoclient.heroku_q2z34tjm
    coll_qlashclans = db.QLASHBot_Clans
    mydict = {
        "Name" : name,
        "Tag" : tag,
        "RoleID": str(roleID),
        "ChannelID": str(channelID)
    }
    coll_qlashclans.insert_one(mydict)


def remove_clan(name):
    db = instances.mongoclient.heroku_q2z34tjm
    coll_qlashclans = db.QLASHBot_Clans
    result = coll_qlashclans.delete_one({"Name":{"$eq":str(name)}})

#*****************************************************************************************************************
#******************************************       COMMAND LOGS     ***********************************************
#*****************************************************************************************************************

def register_commandlog(user,command,time,failed,reason):
    db = instances.mongoclient.heroku_q2z34tjm
    coll_commandlogs = db.QLASHBot_CommandLogs
    mydict = {
        "User" : user,
        "Command" : command,
        "Time" : time,
        "Failed" : failed,
        "Reason" : reason
    }
    coll_commandlogs.insert_one(mydict)

def view_commandlog(int):
    db = instances.mongoclient.heroku_q2z34tjm
    coll_commandlogs = db.QLASHBot_CommandLogs
    list = []
    for document in coll_commandlogs.find():
        list.append(document)
    list = list[-int:]
    return list

def delete_commandlogs():
    db = instances.mongoclient.heroku_q2z34tjm
    coll_commandlogs = db.QLASHBot_CommandLogs
    coll_commandlogs.delete_many({})

#*****************************************************************************************************************
#******************************************       ACHIEVEMENTS     ***********************************************
#*****************************************************************************************************************

def achievement_register_(parameters): #name,description,value
    db = instances.mongoclient.heroku_q2z34tjm
    coll_achievements = db.QLASHBot_Achievements
    print(parameters)
    list = re.findall("\<(.*?)\>", parameters)
    print(list)
    mydict = {
        "Name" : str(list[0]),
        "Description" : str(list[1]),
        "Value" : int(list[2]),
        "Date" : str(date.today())
    }
    coll_achievements.insert_one(mydict)
    return list[0]

def achievement_removeall_(ctx):
    db = instances.mongoclient.heroku_q2z34tjm
    coll_achievements = db.QLASHBot_Achievements
    coll_achievements.delete_many({})

#def achievement_removeone(ctx,*achievementname):
#    name = " ".join(achievementname[:])
#    document = coll_achievements.find_one({"Name":{"$eq":str(name)}})
#    #

#achievement_register_("<Tournament Player> <Participated in 5 tournaments in a row> <100>")
