import discord
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
#from util_functions import *

from modules.mongodb import library as mongo_library
from modules.system import library as system_library, descriptions as system_descriptions

#*****************************************************************************************************************
#*********************************************       UTIL     ****************************************************
#*****************************************************************************************************************


class System(commands.Cog,name="System"):
    def __init__(self,bot, db):
        self.bot = bot
        self.coll_membercount = db.QLASHBot_MemberCount
        self.mongovoice = mongo_library.MongoVoiceSystem()
        self.mongovoicestats = mongo_library.MongoVoiceStats()
        self.mongostats = mongo_library.MongoVoiceStats()

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
    async def welcome_(self,ctx):
        await system_library.welcome(self,ctx)

    @commands.cooldown(1,60,commands.BucketType.channel)
    @commands.command(name='iqloudy-info',brief="(UTIL) Shows some details about the bot's development")
    async def iqloudy_info_(self,ctx):
        await system_library.iqloudy_info(self,ctx)

    #@commands.has_any_role('DiscordDeveloper')
    #@commands.command(name='qlash',brief='Displays some information about QLASH.')
    #async def qlash(self,ctx):
    #    await qlash_(ctx)

    #@commands.cooldown(1,60,commands.BucketType.channel,hidden=True)
    #@commands.command(name='iqloudy-stats',brief='(UTIL) Shows information about QLASH Bot')
    #async def iqloudy__stats(self,ctx):
    #    await iqloudy_stats(ctx)

    #To be re-inserted soon
    #@commands.cooldown(1, 60, commands.BucketType.channel)
    #@commands.command(name='qlash-allclans',hidden=True,brief='(UTIL) (BS30+) List all ingame qlash clans.',description = desc_qlash_allclans)
    #async def qlash_allclans(ctx):
    #    await qlash_trophies(ctx)

    #@commands.has_any_role('DiscordDeveloper')
    #@commands.command(name='get-audit-logs',brief='Audit view.')
    #async def get_audit_logs_(self,ctx,member:discord.Member):
    #    await system_library.get_audit_logs(self,ctx,member)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='database-view',brief='View registered QLASH clans..')
    async def view_database_(self,ctx):
        m = mongo_library.MongoClans()
        await m.view_database(ctx)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='commandlog-view',brief='View the logs of recorded commands',description=system_descriptions.desc_commandlog_view)
    async def commandlog_view_(self,ctx,limit:int):
        await system_library.commandlog_view(self,ctx,limit)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='commandlog-clear',brief='Clears the log file of recorded commands',description=system_descriptions.desc_commandlog_clear)
    async def commandlog_clear(self,ctx):
        await system_library.commandlog_clear(self,ctx)

    #@commands.has_any_role('DiscordDeveloper')
    #@commands.command(name='registry-view')
    #async def registery_view(self,ctx,roleID,channelID,tag,*clan_name):
    #    await registry_view_(ctx)


    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='clan-add',brief='Add a qlash clan to the database.',description=system_descriptions.desc_clan_add)
    async def clan_add(self,ctx,roleID,channelID,tag,*clan_name):
        await clan_add_(ctx,roleID,channelID,tag,*clan_name)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='clan-remove',brief='Remove a qlash clan from the database.',description=system_descriptions.desc_clann_remove)
    async def clan_remove(self,ctx,*clan_name):
        await clan_remove_(ctx,*clan_name)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='add-single',brief='Add a member count to the database')
    async def add_single(self,ctx,date,membercount):
        await system_library.addsingle(self,ctx,self.coll_membercount,date,membercount)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='graph-get',brief='Get a graph to view member count through the month')
    async def graph_get(self,ctx):
        await system_library.analyze(self,ctx,self.coll_membercount)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='graph-reset',brief='Clears a graph completely')
    async def graph_reset(self,ctx):
        await system_library.removeall(self,ctx,self.coll_membercount)

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='graph-today',brief='Record today\'s member count in the database')
    async def graph_today(self,ctx):
        await system_library.record(self,ctx,self.coll_membercount)

#********************************* achievements *************************************

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='achievement-add',hidden=True)
    async def achievement_add(self, ctx,*params):
        return #TO BE WORKED ON
        parameters = " ".join(params[:])
        name = achievement_register_(parameters)
        await ctx.send("Achievement '"+str(name)+"' added to the database!")

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='achievemnt-removeall',hidden=True)
    async def achievement_removeall(self,ctx):
        return #TO BE WORKED ON
        achievement_removeall_(ctx)
        await ctx.send("All achievements were removed from the database")

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name='login',hidden=True)
    async def login(self,ctx):
        return #TO BE WORKED ON
        await system_library.login(self,ctx)
    
    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name="voiceroom-add")
    async def voiceroomadd(self,ctx,id,*roomname):
        name = " ".join(roomname[:])
        self.mongovoice.register_voiceroom(name,id)
        await ctx.send("VoiceRoom has been added to the database:\n- Name: "+str(name)+"\n- ID: "+str(id))

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name="voiceroom-remove")
    async def voiceroomremove(self,ctx,name_or_id):
        self.mongovoice.delete_voiceroom(name_or_id)
        await ctx.send("VoiceRoom "+str(name_or_id)+"has been removed from the database")

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name="test")
    async def test(self,ctx):
        self.mongovoicestats.initialize_document()
        await ctx.send("Done")

    @commands.has_any_role('DiscordDeveloper')
    @commands.command(name="vieww")
    async def v(self, ctx,*roomname):
        name = " ".join(roomname[:])
        self.mongostats.add_room_counter(name)

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



    #@util.command(name='test_hol')
    #async def test_hol(ctx):
    #    print(holidays["holidays"])

    #*****************************************************************************************************************
    #**********************************************       MOD     ****************************************************
    #*****************************************************************************************************************
    """
    ### SET ###
    @mod.command(name='set',brief="(MOD)(BS1) Get the discord role for the clan you belong to.",description=system_descriptions.desc_set)
    async def set(ctx,player:discord.Member,ingame_tag):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator","Coordinator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await set_(ctx,player,ingame_tag)

    #ADMIN
    @mod.command(name='bs-playerinfo',brief='(MOD) (BS1) Search for information about a generic ingame player.',description=system_descriptions.desc_bs_playerinfo)
    async def bs_pinfo(ctx,player_tag):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator","Clan-Leader","Coordinator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await getplayer(ctx,player_tag)

    #ADMIN
    @mod.command(name='bs-claninfo',brief='(MOD) (BS1) Search for information about an ingame clan.',description=system_descriptions.desc_bs_claninfo,)
    async def bs_cinfo(ctx,clan_tag):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator","Clan-Leader","Coordinator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await getclan(ctx,clan_tag)

    #ADMIN
    @mod.command(name='bs-memberinfo',brief='(MOD) (BS1) Search for information about a member within a given clan.',description=system_descriptions.desc_bs_memberinfo)
    async def bs_minfo(ctx,name,clan_tag):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator","Clan-Leader","Coordinator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await search_member(ctx,name,clan_tag)

    @mod.command(name='locate',brief = '(MOD) Locate an ip address',description=system_descriptions.desc_ip)
    async def locate(ctx,ip):
        author = ctx.message.author
        if await Check(ctx,author):
            await locate_(ctx,ip)
        else:
            return

    @mod.command(name='member-info',brief='(MOD) Show information of a discord member',description=system_descriptions.desc_memberinfo)
    async def memberinfo(ctx,member:discord.Member):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator","Clan-Leader","Coordinator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        CommandLogs(ctx,'member-info')
        await member_info_(ctx,member)

    @mod.command(name="server-info",brief="(MOD) Show information of the server",description=system_descriptions.desc_serverinfo)
    async def serverinfo(ctx):
        author = ctx.message.author
        if not checkforrole(author, "Moderator", "Sub-Coordinator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await serverinfo_(ctx)

    @mod.command(name='member-dm',pass_context=True,brief='(MOD) Send a private message to a member by the bot.',description=system_descriptions.desc_member_dm)
    async def dm(ctx,member: discord.Member, *message):
        author = ctx.message.author
        if not checkforrole(author,"Sub-Coordinator","Moderator"):
            await ctx.send("Permission to use this command you do not have... Hrmmm...")
            return
        await poke(ctx,member,*message)

    @mod.command(name='announce',brief='(MOD) Send a message to a specific channel by the bot.',description=system_descriptions.desc_announce)
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

    @mod.command(name='purge',brief='(MOD) Clear messages in the channel.',description=system_descriptions.desc_purge)
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
