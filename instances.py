#instances
import os
import discord
import brawlstats
import ipapi
from pymongo import MongoClient
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from datetime import datetime
from dotenv import load_dotenv
from aiohttp_proxy import ProxyConnector,ProxyType
from descriptions import *

#*****************************************************************************************************************
#********************************************       SETTINGS     *************************************************
#*****************************************************************************************************************

env_path = os.path.dirname(os.path.realpath(__file__)) + '/.env'
load_dotenv(dotenv_path=env_path)
#quota_url = 'http://6cy3e5odaiitpe:gxag60u036717xavs35razjk18s2@eu-west-static-03.quotaguard.com:9293'

connector = ProxyConnector(
    proxy_type=ProxyType.SOCKS5,
    host='54.72.12.1',#'eu-west-static-03.quotaguard.com',
    port=1080,
    username='6cy3e5odaiitpe',
    password='gxag60u036717xavs35razjk18s2',
    rdns=True
)

h_parameters = {
	# Required
	'country': 'IT',
	'year':    2019,
	# Optional
	# 'month':    7,
	# 'day':      4,
	# 'previous': True,
	# 'upcoming': True,
    'public':   True,
	# 'pretty':   True,
}

#*****************************************************************************************************************
#*********************************************       TOKENS     **************************************************
#*****************************************************************************************************************

BS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImUyOTQ3MjlhLWE5YjYtNDIxNy05MTdlLTUxZDJhYzRmOWI4NSIsImlhdCI6MTU5MDI3MDMwNywic3ViIjoiZGV2ZWxvcGVyLzMwMWI3NDk1LWE0OTQtYmIzNy05MWFlLWM5MGEyZmRjMDBjOSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNTQuNzIuMTIuMSIsIjU0LjcyLjc3LjI0OSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.RODZQwDO2YZZF_JAazFccdrg1YiPcaqGmxtPe40ZN-zvVDK3sXuX1-yqGWwjBdd-MoyTqfrsPxhS3V_IUNf9qQ'

TOKEN = 'NzAxMTI1MzExMDQ3NDAxNDc0.XpyBZQ.RAsYlvnkrzI08mwFuXK8QF5K3BM' #token for discord api

HOLIDAY_TOKEN = 'c1512589-4ee9-40eb-9d65-9c6063113c3f'

clientid = '701125311047401474'
clientsecret = '9R3Ys-YNtsrHCCLYShWLVhWuAoezQuX1'

#*****************************************************************************************************************
#*********************************************       CLIENTS     *************************************************
#*****************************************************************************************************************
myclient = brawlstats.Client(BS_TOKEN,is_async=True,debug=True,connector=connector) #BRAWLSTATS
bot = commands.Bot(command_prefix='^', description = bot_description) #DISCORD
ipapi.location(ip=None, key=None, field=None) #IP
mongoclient = MongoClient('mongodb://heroku_q2z34tjm:bn6uqg4ufjontd6s5snbiuvh3l@ds145486.mlab.com:45486/heroku_q2z34tjm',retryWrites=False) #MONGODB

#hapi = holidayapi.v1(HOLIDAY_TOKEN)
#holidays = hapi.holidays(h_parameters)

#*****************************************************************************************************************
#********************************************       CHANNELS     *************************************************
#*****************************************************************************************************************

#test friends tags
ignick_lory = 'loryconti'
igtag_lory = '#20VYUG2L'
qlash_ares = '#98VQUC8R'
igtag_picoz = '#20VVVVYQ8'
igtag_elgarzy = '#RC9PVRCJ'

#discord channel IDs
roles_assignment = '434850121134637056'
bot_testing = '705823922402361437'
en_general = '464691619569074177'
it_general = '415221650481610762'
support = '464695005156737024'
banlist = '493151669849161743'
banlist_testing = '713322449915215923'
entry_exit = '713735004827418625'
entries_discord = '714161674432806972'
qlash_bot = '714161674432806972'
ig_role_channel = '703596640593903716'

#database directories
qc_directory2 = './qlashclans2/' #this one is the right one
