
from pprint import pprint
from datetime import date,datetime
import re
import pymongo
import bot_instances

# coll_registered = db.QLASHBot_Registered
# coll_commandlogs = db.QLASHBot_CommandLogs
# coll_qlashclans = db.QLASHBot_Clans
# coll_membercount = db.QLASHBot_MemberCount
# coll_achievements = db.QLASHBot_Achievements
# coll_voicechannels = db.QLASHBot_VoiceChannels

class MongoDatabase():
    def __init__(self):
        """
        #client = pymongo.MongoClient("mongodb+srv://lorenzoconti2:Lowzz.12@cluster0.li0yy.mongodb.net/QlashBot?retryWrites=true&w=majority")
        
        self.db = bot_instances.mongoclient.QlashBot
        self.coll_registered = self.db.QLASHBot_Registered
        self.coll_commandlogs = self.db.QLASHBot_CommandLogs
        self.coll_qlashclans = self.db.QLASHBot_Clans
        self.coll_membercount = self.db.QLASHBot_MemberCount
        self.coll_achievements = self.db.QLASHBot_Achievements
        self.coll_voicechannels = self.db.QLASHBot_VoiceChannels
        self.coll_statistics = self.db.QLASHBot_Statistics
        self.coll_voicerooms = self.db.QLASHBot_VoiceRooms
        """
        self.db = bot_instances.mongoclient.QlashBot
        self.coll_clans = self.db["Clans"]
        self.coll_statistics = self.db["Statistics"]
        self.coll_players = self.db["Players"]
        self.coll_voicesystem = self.db["VoiceSystem"]
        self.coll_commandlogs = self.db["CommandLogs"]

#*****************************************************************************************************************
#********************************************       MEMBERS     **************************************************
#*****************************************************************************************************************

class MongoMembers(MongoDatabase):
    def __init__(self):
        super().__init__()

    def register_member(self,member,gametag,day = date.today()):
        #db = bot_instances.mongoclient.QlashBot
        #coll_registered = db.QLASHBot_Registered
        mydict = {
            "Discord" : str(member),
            "DiscordID" : int(member.id),
            "Gametag" : gametag,
            "Date" : str(day)
        }
        self.coll_players.insert_one(mydict)

    def check_member(self,discord):
        #db = bot_instances.mongoclient.QlashBot
        #coll_registered = db.QLASHBot_Registered
        document = self.coll_players.find_one({"Discord":{"$eq":str(discord)}})
        return document #type <dict>

    def remove_member(self,discord):
        #db = bot_instances.mongoclient.QlashBot
        #coll_registered = db.QLASHBot_Registered
        self.coll_players.delete_one({"Discord":{"$eq":str(discord)}})

#*****************************************************************************************************************
#*********************************************       CLANS     ***************************************************
#*****************************************************************************************************************

class MongoClans(MongoDatabase):
    def __init__(self):
        super().__init__()

    def get_clan(self,*nname):
        #db = bot_instances.mongoclient.QlashBot
        #coll_qlashclans = db.QLASHBot_Clans
        name = " ".join(nname[:])
        document = self.coll_clans.find_one({"Name":{"$eq":str(name)}})
        return document #type <dict>

    def LoadClans(self):
        #db = bot_instances.mongoclient.QlashBot
        #coll_qlashclans = db.QLASHBot_Clans
        list = []
        for document in self.coll_clans.find():
            list.append(document)
        return list #list of dicts ("Name","Tag","RoleID","ChannelID")

    def register_clan(self,roleID,channelID,tag,name):
        #db = bot_instances.mongoclient.QlashBot
        #coll_qlashclans = db.QLASHBot_Clans
        mydict = {
            "Name" : name,
            "Tag" : tag,
            "RoleID": str(roleID),
            "ChannelID": str(channelID)
        }
        self.coll_clans.insert_one(mydict)

    def remove_clan(self,name):
        #db = bot_instances.mongoclient.QlashBot
        #coll_qlashclans = db.QLASHBot_Clans
        result = self.coll_clans.delete_one({"Name":{"$eq":str(name)}})

#view all clans
    async def view_database(self,ctx):
        #member = ctx.message.author
        #db = bot_instances.mongoclient.QlashBot
        #coll_qlashclans = db.QLASHBot_Clans
        response='```\n'
        response+="Name\tTag\tRoleID\tChannelID\n"
        i=1
        for document in self.coll_qlashclans.find():
            name = str(document["Name"])
            tag = str(document["Tag"])
            roleID = str(document["RoleID"])
            channelID = str(document["ChannelID"])
            response += str(i)+'. '+name+'\t'+tag+'\n'
            i+=1
        response+='```'
        await ctx.send(response)

#*****************************************************************************************************************
#******************************************       COMMAND LOGS     ***********************************************
#*****************************************************************************************************************
class MongoCommandLogs(MongoDatabase):
    def __init__(self):
        super().__init__()

    def register_commandlog(self,user,command,time,failed,reason):
        #db = bot_instances.mongoclient.QlashBot
        #coll_commandlogs = db.QLASHBot_CommandLogs
        mydict = {
            "User" : user,
            "Command" : command,
            "Time" : time,
            "Failed" : failed,
            "Reason" : reason
        }
        self.coll_commandlogs.insert_one(mydict)

    def view_commandlog(self,int):
        #db = bot_instances.mongoclient.QlashBot
        #coll_commandlogs = db.QLASHBot_CommandLogs
        list = []
        for document in self.coll_commandlogs.find():
            list.append(document)
        list = list[-int:]
        return list

    def delete_commandlogs(self):
        #db = bot_instances.mongoclient.QlashBot
        #coll_commandlogs = db.QLASHBot_CommandLogs
        self.coll_commandlogs.delete_many({})

#*****************************************************************************************************************
#******************************************       ACHIEVEMENTS     ***********************************************
#*****************************************************************************************************************


def achievement_register_(parameters): #name,description,value
    db = bot_instances.mongoclient.QlashBot
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
    db = bot_instances.mongoclient.QlashBot
    coll_achievements = db.QLASHBot_Achievements
    coll_achievements.delete_many({})


#*****************************************************************************************************************
#******************************************       VOICE SYSTEM     ***********************************************
#*****************************************************************************************************************

class MongoVoiceSystem(MongoDatabase):
    def __init__(self):
        super().__init__()

    #-----------  VOICE ROOMS  ----------------
    def register_voiceroom(self,name,id,type="Standard"):
        mydict = {
            "Name" : name,
            "ID" : id,
            "Type" : type
        }
        self.coll_voicesystem.insert_one(mydict)

    def delete_voiceroom(self,name_or_id):
        if str(name_or_id[0]).isdigit(): #it's an ID
            self.coll_voicesystem.delete_one({"ID": {"$eq": name_or_id}})
        else:
            self.coll_voicesystem.delete_one({"Name": {"$eq": name_or_id}})

    def LoadRooms(self):
        list = []
        for document in self.coll_voicesystem.find():
            list.append(document)
        return list

    def get_room(self,name_or_id):
        document = None
        if str(name_or_id[0]).isdigit():  # it's an ID
            document = self.coll_voicesystem.find_one(
                {"ID": {"$eq": name_or_id}})
        else:
            document = self.coll_voicesystem.find_one(
                {"Name": {"$eq": name_or_id}})
        return document

    def get_usages(self,name):
        document = self.coll_voicesystem.find_one(
            {"Name": {"$eq": name_or_id}})
        return document

    #-----------  VOICE CHANNELS  ----------------

    def register_voicechannel(self, author, channel, channelID, password):
        #db = bot_instances.mongoclient.QlashBot
        #coll_voicechannels = db.QLASHBot_VoiceChannels

        mydict = {
            "Channel" : channel,
            "ID" : channelID,
            "Password" : password,
            "CreatedBy" : author,
            "CreatedAt" : datetime.now()
        }

        self.coll_voicesystem.insert_one(mydict)

    def get_voicechannel(self,ch_id):
        #db = bot_instances.mongoclient.QlashBot
        #coll_voicechannels = db.QLASHBot_VoiceChannels
        document = self.coll_voicesystem.find_one({"ID": {"$eq": ch_id}})
        return document  # type <dict>


    def remove_voicechannel(self,ch_id):
        #db = bot_instances.mongoclient.QlashBot
        #coll_voicechannels = db.QLASHBot_VoiceChannels
        self.coll_voicesystem.delete_one({"ID": {"$eq": ch_id}})

#*****************************************************************************************************************
#******************************************        STATISTICS      ***********************************************
#*****************************************************************************************************************

class MongoStats(MongoDatabase):
    def __init__(self):
        super().__init__()

    def reset_document(self):
        pass


class MongoVoiceStats(MongoStats):
    def __init__(self):
        super().__init__()
        self.voice = MongoVoiceSystem()

    def initialize_document(self):
        docs = self.voice.LoadRooms()
        mydict = {
            "Name" : "VoiceStatistics",
            "TotalUsages" : 0,
            "RoomRequests" : 0,
            "Rooms": {
                "Room "+str(i): {
                    "Usages" : 0,
                    "BitrateChanges" : 0
                }
                for i in range(1, len(docs))
            }
        }
        self.coll_statistics.insert_one(mydict)


    def add_room_counter(self,roomname):
        document = self.coll_statistics.find_one({"Name" : {"$eq": "VoiceStatistics"}})
        standardrooms = [item["Name"] for item in self.voice.LoadRooms() if item["Type"]=="Standard"]
        print(standardrooms)
        if roomname in standardrooms:
            document["Rooms"][roomname]["Usages"] += 1
            self.coll_statistics.delete_one({"Name": {"$eq": "VoiceStatistics"}})
            self.coll_statistics.insert_one(document)

    def add_bitrate_counter(self,roomname):
        document = self.coll_statistics.find_one({"Name": {"$eq": "VoiceStatistics"}})
        document["Rooms"][roomname]["BitrateChanges"] += 1
        self.coll_statistics.delete_one({"Name": {"$eq": "VoiceStatistics"}})
        self.coll_statistics.insert_one(document)
