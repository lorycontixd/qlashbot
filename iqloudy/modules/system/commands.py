import discord
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from modules.util_functions import *

from modules.system.library import *

#*****************************************************************************************************************
#*********************************************       UTIL     ****************************************************
#*****************************************************************************************************************

desc_hello = """Utility command
60 seconds cooldown per channel \n
Welcomes a user to the server. Bot presents itself and reveals help command"""


desc_set = """Utility command
60 seconds cooldown per user (only usable in the roles_assignement channel) \n
Get the discord role for the QLASH clan you belong to in Brawl Stars.
If you already have the right role, it will give it again. If you do not belong to an official clan, it will tell you explicitly.
The parameter required is your INGAME tag that you can find in your ingame profile."""

desc_database_view="""Moderator Command
No Cooldown \n
Gets a list of all registered QLASH Clans in the database.
"""

desc_commandlog_view ="""Moderator Command
No Cooldown \n
View the log of recently called commands with QLASH Bot.
The parameter takes an integer which corresponds to the number of messages you want to view, starting from the bottom (now we're here).
"""

desc_commandlog_clear = """Moderator Command
No Cooldown \n
Clear the log file containing a list of all commands called from this bot. Please use wisely.
"""

desc_clan_add = """Moderator Command
No Cooldown \n
Add a QLASH Clan to the database. The parameters are the clan's tag and the clan's name written correctly.
Moderator and Sub-Coordinator roles are required."""

desc_clann_remove = """Moderator Command
No Cooldown \n
Remove a QLASH Clan to the database. The parameter is the clan's name written correctly.
Moderator and Sub-Coordinator roles are required."""


class System(commands.Cog,name="System"):
    def __init__(self,db):
        self.coll_membercount = db.QLASHBot_MemberCount

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='shutdown',brief='Shutdowns the instance (developer-only)')
    async def shutdown(self,ctx):
        await ctx.send("Not yet implemented.")


    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='invite',brief='Create a link to the server.')
    async def invite(self,ctx,channel:discord.TextChannel):
        link = await channel.create_invite(max_age = 0,max_uses=0)
        await ctx.send("Here is an instant invite to your server:  ")
        await ctx.send(link)


    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='hello',brief='Welcome a user to the server.')
    async def hello(self,ctx):
        await welcome_(ctx)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='qlash',brief='Displays some information about QLASH.')
    async def qlash(self,ctx):
        await qlash_(ctx)

#To be re-inserted soon
#@commands.cooldown(1, 60, commands.BucketType.channel)
#@commands.command(name='qlash-allclans',hidden=True,brief='(UTIL) (BS30+) List all ingame qlash clans.',description = desc_qlash_allclans)
#async def qlash_allclans(ctx):
#    await qlash_trophies(ctx)

#@commands.cooldown(1,60, commands.BucketType.user)
#@util.command(name='weather-current',brief='(UTIL) Shows current weather for a given city',description=desc_weather_current)
#async def weather_current(ctx,city,country_code):
#    myclass = Weather()
#    await myclass.weather_current_(ctx,city,country_code)

#@commands.cooldown(1,60, commands.BucketType.user)
#@util.command(name='weather-5days',brief='(UTIL) Shows 5-days weather forecase for a city',description=desc_weather_5days)
#async def weather_five_days(ctx,city,country_code):
#    myclass = Weather()
#    await myclass.weather_five_days_(ctx,city,country_code)

    @commands.cooldown(1,60,commands.BucketType.channel)
    @commands.command(name='iqloudy-info',brief="(UTIL) Shows some details about the bot's development")
    async def iqloudy_info(self,ctx):
        await iqloudy_info_(ctx)

    #@commands.cooldown(1,60,commands.BucketType.channel,hidden=True)
    #@commands.command(name='iqloudy-stats',brief='(UTIL) Shows information about QLASH Bot')
    #async def iqloudy__stats(self,ctx):
    #    await iqloudy_stats(ctx)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='get-audit-logs',brief='Audit view.')
    async def get_audit_logs(self,ctx,member:discord.Member):
        await get_audit_logs_(ctx,member)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='database-view',brief='View registered QLASH clans..')
    async def view_database_(self,ctx):
        await view_database(ctx)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='commandlog-view',brief='View the logs of recorded commands',description=desc_commandlog_view)
    async def commandlog_view(self,ctx,limit:int):
        await commandlog_view_(ctx,limit)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='commandlog-clear',brief='Clears the log file of recorded commands',description=desc_commandlog_clear)
    async def commandlog_clear(self,ctx):
        await commandlog_clear_(ctx)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='registry-view')
    async def registery_view(self,ctx,roleID,channelID,tag,*clan_name):
        await registry_view_(ctx)


    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='clan-add',brief='Add a qlash clan to the database.',description=desc_clan_add)
    async def clan_add(self,ctx,roleID,channelID,tag,*clan_name):
        await clan_add_(ctx,roleID,channelID,tag,*clan_name)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='clan-remove',brief='Remove a qlash clan from the database.',description=desc_clann_remove)
    async def clan_remove(self,ctx,*clan_name):
        await clan_remove_(ctx,*clan_name)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='add-single',brief='Add a member count to the database')
    async def add_single(self,ctx,date,membercount):
        await addsingle(ctx,self.coll_membercount,date,membercount)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='graph-get',brief='Get a graph to view member count through the month')
    async def graph_get(self,ctx):
        await analyze(ctx,self.coll_membercount)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='graph-reset',brief='Clears a graph completely')
    async def graph_reset(self,ctx):
        await removeall(ctx,self.coll_membercount)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='graph-today',brief='Record today\'s member count in the database')
    async def graph_today(self,ctx):
        await record(ctx,self.coll_membercount)

#********************************* achievements *************************************

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='achievement-add')
    async def achievement_add(self, ctx,*params):
        parameters = " ".join(params[:])
        name = achievement_register_(parameters)
        await ctx.send("Achievement '"+str(name)+"' added to the database!")

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='achievemnt-removeall')
    async def achievement_removeall(self,ctx):
        achievement_removeall_(ctx)
        await ctx.send("All achievements were removed from the database")

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='login')
    async def login(self,ctx):
        await _login(ctx)

#********************************* tournaments *************************************

#@bot.command(name='tournament-members')
#async def get_tournament_members_(ctx,tournament_role):
#    await get_tournament_members(ctx,tournament_role)

#to write all members on a google spreadsheet
#@bot.command(name='writeall')
#async def writeall_(ctx):
#    await writeall(ctx)

#@bot.command(name='test-getleague')
#async def getleague(ctx,player:discord.Member):
#    await get_player_league(ctx,player)

#@bot.command(name='test-addpoints')
#async def addpoints(ctx,player):


#@bot.command(name='countstart')
#async def t1(ctx):
#    a = MyCog()

#***************************************************************************************************************
#***************************************************************************************************************
#***************************************************************************************************************
#***************************************************************************************************************


async def mainmenu(ctx,member:discord.Member):
    await member.create_dm()
    message = "```\n---------------------------------------------------------------------\n----------------------------- MAIN MENU -----------------------------\n---------------------------------------------------------------------\n-- 1. QLASH Bot Command Logs\n-- 2. QLASH Clans database\n-- 3. Server Graph database\n\n-- 0. Exit Database```"
    await member.dm_channel.send(message)

async def opt1(ctx,member):
    await member.create_dm()
    message = "```\n-------------------------- COMMAND LOGS ----------------------------\n-- 1. Log Database View\n-- 2. Log Database Clear \n\n-- 0. Exit Database```"
    await member.dm_channel.send(message)

async def opt2(ctx,member):
    await member.create_dm()
    message = "```\n-------------------------- QLASH CLANS -----------------------------\n-- 1. Add new QLASH clan\n-- 2. Remove QLASH Clan\n-- 3. View registered clans \n\n-- 0. Exit Database```"
    await member.dm_channel.send(message)

async def _login(ctx):
    member = ctx.message.author
    await ctx.message.delete()
    sub = discord.utils.get(ctx.message.guild.roles, id=int("604761799505477635"))
    if member.top_role < sub:
        error = await ctx.send("You do not have the permissions to access QLASH Bot's database!")
        await error.delete(delay=5.0)
    await member.create_dm()
    password = "QLASH please"
    await member.dm_channel.send("Please enter the password: ")

    def check(m):
        return m.author == ctx.message.author and type(m.channel)==discord.DMChannel

    reply = await bot.wait_for('message',check=check)
    if reply.content == password:
        await member.dm_channel.send("Access Granted\nWelcome to the QLASH Database "+member.mention+"!")
        asyncio.sleep(1)
        await mainmenu(ctx,member)
        reply1_str = await bot.wait_for('message',check=check)
        reply1_int = int(reply1_str.content)
        numbers = [0,1,2,3]
        if reply1_int not in numbers:
            await member.dm_channel.send("InputError: Invalid option passed. Exiting..")
            return
        else:
            if reply1_int==0:
                await member.dm_channel.send("Exiting")
                return
            elif reply1_int==1:
                await opt1(ctx,member)
                reply2_str = await bot.wait_for('message',check=check)
                reply2_int = int(reply2_str.content)
                if reply2_int not in [0,1,2,3]:
                    await member.dm_channel.send("InputError: Invalid option passed. Exiting..")
                    return
                else:
                    if reply2_int == 0:
                        await member.dm_channel.send("Exiting")
                        return
                    elif reply2_int == 1:
                        await member.dm_channel.send("Option 1 still to be implemented")
                        return
                    elif reply2_int == 2:
                        await member.dm_channel.send("Option 1 still to be implemented")
                        return
                    elif reply2_int == 3:
                        await view_database(ctx,member)
                        return
            elif reply1_int==2:
                await opt2(ctx,member)
            elif reply1_int==3:
                await member.dm_channel.send("Option 3 still to be implemented")
                return
    else:
        await member.dm_channel.send("Wrong password")
        return



    #@util.command(name='test_hol')
    #async def test_hol(ctx):
    #    print(holidays["holidays"])

    #*****************************************************************************************************************
    #**********************************************       MOD     ****************************************************
    #*****************************************************************************************************************
    """
    ### SET ###
    @mod.command(name='set',brief="(MOD)(BS1) Get the discord role for the clan you belong to.",description=desc_set)
    async def set(ctx,player:discord.Member,ingame_tag):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await set_(ctx,player,ingame_tag)

    #ADMIN
    @mod.command(name='bs-playerinfo',brief='(MOD) (BS1) Search for information about a generic ingame player.',description=desc_bs_playerinfo)
    async def bs_pinfo(ctx,player_tag):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator","Clan-Leader","Coordinator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await getplayer(ctx,player_tag)

    #ADMIN
    @mod.command(name='bs-claninfo',brief='(MOD) (BS1) Search for information about an ingame clan.',description=desc_bs_claninfo,)
    async def bs_cinfo(ctx,clan_tag):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator","Clan-Leader","Coordinator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await getclan(ctx,clan_tag)

    #ADMIN
    @mod.command(name='bs-memberinfo',brief='(MOD) (BS1) Search for information about a member within a given clan.',description=desc_bs_memberinfo)
    async def bs_minfo(ctx,name,clan_tag):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator","Clan-Leader","Coordinator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await search_member(ctx,name,clan_tag)

    @mod.command(name='locate',brief = '(MOD) Locate an ip address',description=desc_ip)
    async def locate(ctx,ip):
        author = ctx.message.author
        if await Check(ctx,author):
            await locate_(ctx,ip)
        else:
            return

    @mod.command(name='member-info',brief='(MOD) Show information of a discord member',description=desc_memberinfo)
    async def memberinfo(ctx,member:discord.Member):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator","Clan-Leader","Coordinator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        CommandLogs(ctx,'member-info')
        await member_info_(ctx,member)

    @mod.command(name="server-info",brief="(MOD) Show information of the server",description=desc_serverinfo)
    async def serverinfo(ctx):
        author = ctx.message.author
        if not checkforrole(author, "Moderator", "Sub-Coordinator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await serverinfo_(ctx)

    @mod.command(name='member-dm',pass_context=True,brief='(MOD) Send a private message to a member by the bot.',description=desc_member_dm)
    async def dm(ctx,member: discord.Member, *message):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await poke(ctx,member,*message)

    @mod.command(name='announce',brief='(MOD) Send a message to a specific channel by the bot.',description=desc_announce)
    async def annouce(ctx,channel_name,*message):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await write_message(ctx,channel_name,*message)

    @mod.command(name='welcome',brief='(MOD) Send a welcome message to a specific channel by the bot.')
    async def welcome(ctx,channel_name):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await welcome_announcement(ctx,channel_name)

    @mod.command(name='purge',brief='(MOD) Clear messages in the channel.',description=desc_purge)
    async def purge(ctx,amount):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await purge_(ctx,amount)

    @mod.command(name='purge-user',brief="(MOD) Clear all messages from a user inside a give channel")
    async def purge_user(ctx,channelname,member:discord.Member):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await purge_user_(ctx,channelname,member)

    @mod.command(name="role-give",hidden=True,pass_context=True)
    async def role_give(ctx,member: discord.Member , *rolename):
        await giverole(ctx,member,*rolename)

    @mod.command(name="role-remove",hidden=True,pass_context=True)
    async def role_rem(ctx,member: discord.Member , *rolename):
        await removerole(ctx,member,*rolename)

    @mod.command(name='role-count')
    async def role_count(ctx,*rolename):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await role_count_(ctx,*rolename)

    @mod.command(name='all-roles')
    async def print_report(ctx):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await print_report_(ctx)

    @mod.command(name='role-members')
    async def print_rolemembers(ctx,*rolename):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await print_rolemembers_(ctx,*rolename)

    @mod.command(name='vice-count')
    async def vice_(ctx):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator","QLASH"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await vice(ctx)

    @mod.command(name="check-banlist",brief="(MOD) Check if banned players are in a QLASH Clan")
    async def _banlist(ctx):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Coordinator",):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await check_banlist_channel()

    @mod.command(name="giova")
    async def _giova(ctx):
        await giova()
    """
    #*****************************************************************************************************************
    #**********************************************       SYS     ****************************************************
    #*****************************************************************************************************************
