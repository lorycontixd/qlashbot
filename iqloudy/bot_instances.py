
import os
import discord
import json
import brawlstats
import cloudinary
import cloudinary.uploader
import cloudinary.api

from pymongo import MongoClient
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from datetime import datetime
from dotenv import load_dotenv
from aiohttp_proxy import ProxyConnector,ProxyType
from apscheduler.schedulers.blocking import BlockingScheduler

from modules.scheduler import scheduler

#*****************************************************************************************************************
#********************************************       SETTINGS     *************************************************
#*****************************************************************************************************************

#env_path = os.path.dirname(os.path.realpath(__file__)) + '/.env'
#load_dotenv(dotenv_path=env_path)
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
DISCORD_TOKEN = 'NzAxMTI1MzExMDQ3NDAxNDc0.Xs0bXg.anf5etgix45lRISsKaN6ANzMdYY'

BS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImUyOTQ3MjlhLWE5YjYtNDIxNy05MTdlLTUxZDJhYzRmOWI4NSIsImlhdCI6MTU5MDI3MDMwNywic3ViIjoiZGV2ZWxvcGVyLzMwMWI3NDk1LWE0OTQtYmIzNy05MWFlLWM5MGEyZmRjMDBjOSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNTQuNzIuMTIuMSIsIjU0LjcyLjc3LjI0OSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.RODZQwDO2YZZF_JAazFccdrg1YiPcaqGmxtPe40ZN-zvVDK3sXuX1-yqGWwjBdd-MoyTqfrsPxhS3V_IUNf9qQ'

TOKEN = 'NzAxMTI1MzExMDQ3NDAxNDc0.XpyBZQ.RAsYlvnkrzI08mwFuXK8QF5K3BM' #token for discord api

HOLIDAY_TOKEN = 'c1512589-4ee9-40eb-9d65-9c6063113c3f'

cloudinary_name = 'hhqbheeei'
cloudinary_api_key = '171123752436489'
cloudinary_api_secret = 'NRtgMGzkwO3vk-i89Axtwj8NhLE'
cloudinary_api_env_var = 'cloudinary://171123752436489:NRtgMGzkwO3vk-i89Axtwj8NhLE@hhqbheeei'

qlash_bs_id = '415221296247341066'
clientid = '701125311047401474'
clientsecret = '9R3Ys-YNtsrHCCLYShWLVhWuAoezQuX1'

#*****************************************************************************************************************
#*********************************************       CLIENTS     *************************************************
#*****************************************************************************************************************
myclient = None

if myclient is None:
    myclient = brawlstats.Client(BS_TOKEN,is_async=True,debug=True,connector=connector) #BRAWLSTATS

bot = None

bot_description = """Welcome to the QLASH Bot Help Center. I am QLASH Bot and I allow users to do a bunch of cool and interesting stuff 😎.
To navigate in this help menu, please type ^help <command_name> to see how a command works.
If you have any question or problem with my commands, please do not hesitate to contact our staff or the Bot creators directly.
I hope you have a pleasant stay in the discord server! 🤩😁 """

if bot is None:
    bot = commands.Bot(command_prefix='^', description = bot_description) #DISCORD

mongoclient = None

if mongoclient is None:
    mongoclient = MongoClient('mongodb://heroku_q2z34tjm:bn6uqg4ufjontd6s5snbiuvh3l@ds145486.mlab.com:45486/heroku_q2z34tjm',retryWrites=False) #MONGODB

apscheduler = None
if apscheduler is None:
    apscheduler = scheduler.init_scheduler(mongoclient)

qlash_bs = None

if qlash_bs is None:
    qlash_bs = json.load(open('./media/json/qlash_brawlstars.json', encoding="utf-8"))

#sched = BlockingScheduler()

#hapi = holidayapi.v1(HOLIDAY_TOKEN)
#holidays = hapi.holidays(h_parameters)

cloudinary.config(
  cloud_name = cloudinary_name,
  api_key = cloudinary_api_key,
  api_secret = cloudinary_api_secret
)

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
bot_commands_channel = '446051853357154307'
banlist = '493151669849161743'
banlist_testing = '713322449915215923'
entry_exit = '713735004827418625'
qlash_bot = '714161674432806972'
ig_role_channel = '703596640593903716'
file_managing = '721658324327858236'
testchannel = '723161066124607599'
bot_developer_channel='720193411113680913'
changelog_channel = '728165928939814952'

#database directories
qc_directory2 = './media/texts/qlash_brawlstars_clubs/'
