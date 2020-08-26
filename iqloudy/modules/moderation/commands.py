import discord
import json
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
#from functions import set_
import ipapi
import bot_exceptions
from modules.mongodb.library import *
from modules.scheduler.library import check_banlist_channel,giova,check_banlist_api
from bot_instances import myclient
from modules.moderation import descriptions as moderation_descriptions

#*****************************************************************************************************************
#**********************************************       MOD     ****************************************************
#*****************************************************************************************************************
def valid_tag(tag):
    allowed = ["#","P", "Y", "L", "Q", "G", "R", "J", "C", "U", "V", "0", "2", "8", "9"]
    for c in tag:
        if str(c) not in allowed:
            print("Assertion failed in Set Function: character "+str(c)+" not allowed in brawl tag.")
            return False
    return True

def valid_len_tag(tag):
    length = len(str(tag))
    if length<=5 or length>=14:
        print("Assertion failed in Set Function: tag length not valid ("+str(length)+")")
        return False
    else:
        return True

class Moderation(commands.Cog,name="Moderation"):
    def __init__(self):
        ipapi.location(ip=None, key=None)

    @commands.has_any_role('Moderator','DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='set',brief="Get the discord role for the clan you belong to. (BS1) ",description=moderation_descriptions.desc_set)
    async def set(self,ctx,player:discord.Member,ingame_tag):
        if not str(ingame_tag).startswith("#"):
            raise bot_exceptions.TagError(ingame_tag,"Player tag must start with # character.")
            return
        if not valid_tag(ingame_tag):
            raise bot_exceptions.TagError(ingame_tag,"Player tag does not meet the requirements.")
            return
        if not valid_len_tag(ingame_tag):
            raise bot_exceptions.TagError(ingame_tag,"Player tag does not meet length requirements.")
            return
        temp = await ctx.send("Looking for clan for player "+str(player.mention))
        await asyncio.sleep(1)
        msg = ctx.message
        tag = ingame_tag.replace('O','0').rstrip()
        myplayer=None
        try:
            myplayer = await myclient.get_player(tag)
        except:
            raise bot_exceptions.TagError(tag,"Player not found.")
            return
        if check_member(player) == None:
            register_member(player,myplayer.tag)
        player_club = myplayer.club
        if not player_club:
            await temp.edit(content="Player does not belong to any club.")
            return
        official_clubs = LoadClans()
        #await asyncio.sleep(0.5)
        for club in official_clubs:
            club_role = discord.utils.get(ctx.guild.roles, name=str(club["Name"]))
            if club_role in player.roles and club_role.name != "QLASH Girls" and club_role.name != "QLASH Eris":
                await player.remove_roles(club_role)
            if club["Tag"] == str(player_club.tag):
                await temp.edit(content="Clan found: **"+str(player_club.name)+"**")
                await player.add_roles(club_role)
                wfr = discord.utils.get(ctx.guild.roles, name="waiting-for-role")
                if wfr in player.roles:
                    await player.remove_roles(wfr)
                await asyncio.sleep(1)
                await temp.edit(content="Role **"+str(club_role.name)+"** was given to player "+str(player.mention)+".")
                return
        await asyncio.sleep(1)
        await temp.edit(content="Clan "+str(player_club)+" does not belong to QLASH. No role was given to member "+player.mention+".")

    #ADMIN
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.has_any_role('Moderator','DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='bs-playerinfo',brief='Search for information about a generic ingame player. (BS1) ',description=moderation_descriptions.desc_bs_playerinfo)
    async def bs_pinfo(self,ctx,player_tag):
        role=''
        player = await myclient.get_player(player_tag)
        if not player:
            await ctx.send("No players were found with such tag. If you think this was a problem, contact the Bot creators.")
            return
        e=discord.Embed(title="Player info: "+str(player), description="------------------------------------------------", color=0xf6ec00)
        e.set_author(name="QLASH Bot")
        e.add_field(name="Player", value=str(player), inline=False)
        e.add_field(name="Current Trophies", value=str(player.trophies), inline=True)
        e.add_field(name="Highest Trophies", value=str(player.highest_trophies), inline=True)
        e.add_field(name="Current Power Play", value=str(player.power_play_points), inline=True)
        e.add_field(name="Highest Power Play", value=str(player.highest_power_play_points), inline=True)
        e.add_field(name="Is Qualified in Championship Challenge", value=player.is_qualified_from_championship_challenge, inline=True)
        e.add_field(name="3v3 Victories", value=str(player.x3v3_victories), inline=True)
        e.add_field(name="Solo Victories", value=str(player.solo_victories), inline=True)
        e.add_field(name="Duo Victories", value=str(player.duo_victories), inline=True)
        cclub = player.club["tag"]
        pclub = await myclient.get_club(cclub)
        for member in pclub.members:
            if member.name == player.name:
                role = str(member.role)
        e.add_field(name="Player Club", value=str(pclub.name)+'\n'+str(pclub.tag)+'\n'+role, inline=True)
        e.add_field(name="Brawler Count", value=str(len(player.brawlers)), inline=True)
        e.set_footer(text="Created By Lore")
        await ctx.send(embed=e)

    #ADMIN
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.has_any_role('Moderator','DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='bs-claninfo',brief='Search for information about an ingame clan. (BS1)',description=moderation_descriptions.desc_bs_claninfo,)
    async def bs_cinfo(self,ctx,clan_tag):
        presname = ''
        prestr = ''
        await ctx.send("Getting club info: ")
        club = await myclient.get_club(clan_tag)
        members = club.members
        for member in members:
            if str(member.role).lower() == 'president':
                presname = str(member.name)
                prestr = str(member.trophies)
        e=discord.Embed(title="Clan Info: "+str(club), description="------------------------------------------------", color=0xbe37f4)
        e.set_author(name="QLASH Bot")
        e.add_field(name="Clan", value=str(club), inline=False)
        e.add_field(name="Member Count", value=str(len(members)), inline=True)
        e.add_field(name="Description", value=str(club.description), inline=True)
        e.add_field(name="Trophies", value=str(club.trophies), inline=True)
        e.add_field(name="Required Trophies", value=str(club.required_trophies), inline=True)
        e.add_field(name="Type", value=str(club.type), inline=True)
        e.add_field(name="President",value=presname+'\n'+prestr,inline=True)
        e.add_field(name="Top member", value=str(members[0].name)+'\n'+str(members[0].trophies)+'\n'+str(members[0].role), inline=True)
        e.set_footer(text="Created By Lore")
        await ctx.send(embed=e)

    @commands.cooldown(1, 60, commands.BucketType.channel)
    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='qlash-allclans',hidden=True,brief='List all ingame qlash clans. (BS30+) ',description = moderation_descriptions.desc_qlash_allclans)
    async def qlash_allclans(self,ctx):
        await ctx.send("Gathering QLASH Clans information, please wait a few seconds...")
        await ctx.trigger_typing()
        list = LoadClans()
        e=discord.Embed(title="List of all registered QLASH Clans", description="------------------------------------------------", color=0xffb43e)
        e2=discord.Embed(color=0xffb43e)
        e.set_author(name="QLASH Bot")
        for i in range(len(list)):
            tag = list[i]["Tag"]
            club = await myclient.get_club(str(tag))
            if i<21:
                e.add_field(name="Clan: "+str(club),value="Required Trophies: "+str(club.required_trophies),inline=True)
            else:
                e2.add_field(name="Clan: "+str(club),value="Required Trophies: "+str(club.required_trophies),inline=True)
        e2.set_footer(text="Created By Lore")
        await ctx.send(embed=e)
        await ctx.send(embed=e2)

    @commands.is_owner()
    @commands.command(name='locate',brief = 'Locate an ip address',description=moderation_descriptions.desc_ip)
    async def locate(self,ctx,ip):
        await ctx.send("Searching for location...")
        mydict = ipapi.location(ip)
        e=discord.Embed(title="Found location for ip: "+str(mydict["ip"]) , color=0xffaa00)
        e.set_author(name="QLASH Bot")
        e.add_field(name="City", value=str(mydict["city"]), inline=True)
        e.add_field(name="Region", value=str(mydict["region"]), inline=True)
        e.add_field(name="Country", value=str(mydict["country"]), inline=True)
        e.add_field(name="Continent Code", value=str(mydict["continent_code"]), inline=True)
        e.add_field(name="Postal Code", value=str(mydict["postal"]), inline=True)
        e.add_field(name="Latitude", value=str(mydict["latitude"]), inline=True)
        e.add_field(name="Longitude", value=str(mydict["longitude"]), inline=True)
        e.add_field(name="Timezone", value=str(mydict["timezone"]), inline=True)
        e.add_field(name="Country Calling Code", value=str(mydict["country_calling_code"]), inline=True)
        e.add_field(name="Currency", value=str(mydict["currency_name"]), inline=True)
        e.add_field(name="Country Population", value=str(mydict["country_population"]), inline=True)
        e.add_field(name="Organisation", value=str(mydict["org"]), inline=True)
        e.set_footer(text="Created by Lore")
        await ctx.send(embed=e)

    @commands.has_any_role('Moderator','DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='member-info',brief='Show information of a discord member',description=moderation_descriptions.desc_memberinfo)
    async def memberinfo(self,ctx,member:discord.Member):
        member_dict = check_member(member)
        e=discord.Embed(title="Member info: "+str(member), description=str(member.mention), color=0x74a7ff)
        e.set_author(name="QLASH Bot")
        if member_dict != None:
            ingame_tag = member_dict["Gametag"]
            registered_clan = member_dict["Clan"]
            registered_date = member_dict["Date"]
            e.add_field(name="Game Tag ", value=str(ingame_tag), inline=True)
            if registered_clan:
                e.add_field(name="Last DB_Registered Clan ", value=str(registered_clan), inline=True)
            e.add_field(name="DB_Registration Date ", value=str(registered_date), inline=True)
        e.add_field(name="Created", value=str(member.created_at), inline=True)
        e.add_field(name="ID", value=str(member.id), inline=True)
        e.add_field(name="Joined Server", value=str(member.joined_at), inline=True)
        e.add_field(name="Premium Since", value=str(member.premium_since), inline=True)
        e.add_field(name="Status", value=str(member.status), inline=True)
        e.add_field(name="Mobile status", value=str(member.mobile_status),inline=True)
        e.add_field(name="Desktop status", value=str(member.desktop_status),inline=True)
        e.add_field(name="Top Role", value=str(member.top_role), inline=True)
        e.add_field(name="Permissions ", value=str(member.guild_permissions), inline=True)
        #e.set_image(member.default_avatar)
        e.set_footer(text="Bot created by Lore")
        await ctx.send(embed=e)

    @commands.has_any_role('Moderator','DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name="server-info",brief="Show information of the server",description=moderation_descriptions.desc_serverinfo)
    async def serverinfo(self,ctx):
        guild = ctx.guild
        e=discord.Embed(title="Server info: "+str(guild.name), color=0xe392ff)
        e.set_author(name="QLASH Bot")
        e.add_field(name="Region:", value=str(guild.region), inline=True)
        e.add_field(name="ID: ", value=str(guild.id), inline=True)
        e.add_field(name="Owner:", value=str(guild.owner), inline=True)
        e.add_field(name="Member count:", value=str(guild.member_count), inline=True)
        e.add_field(name="Premium Subscription count:", value=str(guild.premium_subscription_count), inline=True)
        e.add_field(name="System Channel:", value=str(guild.system_channel), inline=True)
        e.add_field(name="Rules Channel:",value=str(guild.rules_channel),inline=True)
        #e.add_field(name="Public Updates Channel:",value=str(guild.public_updates_channel),inline=True)
        e.add_field(name="Role count:", value=str(len(guild.roles)), inline=True)
        e.add_field(name="Creation date:", value=str(guild.created_at), inline=True)
        e.set_footer(text="Bot created by Lore")
        await ctx.send(embed=e)

    @commands.has_any_role('Moderator','DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='purge',brief='Clear messages in the channel.',description=moderation_descriptions.desc_purge)
    async def purge(self,ctx,amount):
        author = ctx.message.author
        await ctx.channel.purge(limit=int(amount)+1)
        msg = await ctx.send("Deleted "+str(amount)+" messages from "+author.mention+" in channel "+str(ctx.message.channel))
        await msg.delete(delay=5.0)

    @commands.has_any_role('Moderator','DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='purge-user',brief="Clear all messages from a user inside a give channel")
    async def purge_user(self,ctx,member:discord.Member,amount):
        i=0
        m = ctx.message
        channel = m.channel
        channelname = channel.name
        if channel == None:
            await ctx.send(ctx.message.author.mention+", no channel found with name "+channelname)
            return
        messages = await channel.history(limit=int(amount)).flatten()
        for message in messages:
            if message.author == member:
                await message.delete()
                i+=1
        msg = await ctx.send("Deleted all messages from user "+str(member)+" in channel "+channelname+" ("+str(i)+")")
        if m.author != member:
            await msg.delete(delay=6.0)
            await m.add_reaction('✅')

    @commands.is_owner()
    @commands.command(name="role-give",hidden=True,pass_context=True)
    async def role_give(self,ctx,member: discord.Member , *rolename):
    	temp = " ".join(rolename[:])
    	role = discord.utils.get(ctx.guild.roles, name=temp)
    	if not role:
    		await ctx.send("ArguementError: Role "+temp+" does not exist. 😭")
    		return
    	await member.add_roles(role)

    @commands.is_owner()
    @commands.command(name="role-remove",hidden=True,pass_context=True)
    async def role_remove(self,ctx,member: discord.Member , *rolename):
        temp = " ".join(rolename[:])
        role = discord.utils.get(ctx.guild.roles, name=temp)
        if not role:
            await ctx.send("ArguementError: Role "+temp+" does not exist. 😭")
            return
        print("Role "+role.name+" removed from "+member.name+" using *role-remove")
        await member.remove_roles(role)

    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='role-count')
    async def role_count(self,ctx,*rolename):
        temp = " ".join(rolename[:])
        dev = discord.utils.get(ctx.guild.roles, name="DiscordDeveloper")
        role = discord.utils.get(ctx.guild.roles, name=temp)
        if role == None:
            await ctx.send("No roles found for role "+temp+"! If you think this is a mistake please contact a "+dev.mention)
            return
        rolecount = int(len(role.members))
        await ctx.send("In the role "+str(role.name)+" there are "+str(rolecount)+" members! ")
        return

    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='all-roles')
    async def print_report(self,ctx):
        """Prints all ingame clans with respective member count"""
        await ctx.trigger_typing()
        author = ctx.author
        guild = ctx.guild
        list = LoadClans()
        total_clans = len(list)
        sections = int(total_clans/21)+1
        listembeds=[]
        for k in range(sections):
            if k==0:
                e=discord.Embed(title="Report for roles",color=0xf6ec00)
                e.set_author(name="QLASH Bot")
            else:
                e=discord.Embed(color=0xf6ec00)
            listembeds.append(e)

        for i in range(total_clans):
            current_section = int(i/21)
            clubName = list[i]["Name"]
            clubTag = list[i]["Tag"]
            role = discord.utils.get(ctx.guild.roles, name=clubName)
            if role == None:
                await ctx.send(clubName+" role not found")
            else:
                listembeds[current_section].add_field(name=role.name,value=str(len(role.members)))
        wfr = discord.utils.get(ctx.guild.roles, name="waiting-for-role")
        wfr_count = len(wfr.members)
        #ig_europe = discord.utils.get(ctx.guild.roles, name="IG-EUROPE")
        #ig_america = discord.utils.get(ctx.guild.roles, name="IG-AMERICA")
        listembeds[-1].add_field(name=wfr.name,value=str(wfr_count))
        #listembeds[-1].add_field(name=ig_europe.name,value=str(len(ig_europe.members)))
        #listembeds[-1].add_field(name=ig_america.name,value=str(len(ig_america.members)))
        listembeds[-1].set_footer(text='Bot Created by Lore')
        for emb in listembeds:
            await ctx.send(embed=emb)

    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='role-members')
    async def print_rolemembers(self,ctx,*role_name):
        rolename = " ".join(role_name[:])
        await ctx.trigger_typing()
        author = ctx.author
        guild = ctx.guild
        role = discord.utils.get(ctx.guild.roles, name=rolename)
        memberlist = role.members
        if role == None:
            await ctx.send("No role found with that name!")
            return
        membercount = len(memberlist)
        sections = int(membercount/21)+1
        listembeds=[]
        for k in range(sections):
            if k==0:
                e=discord.Embed(title="Members in role "+str(role.name),color=0xf6ec00)
                e.set_author(name="QLASH Bot")
            else:
                e=discord.Embed(color=0xf6ec00)
            listembeds.append(e)
        for i in range(membercount):
            current_section = int(i/21)
            nname = str(memberlist[i])
            vvalue = str(memberlist[i].status)
            listembeds[current_section].add_field(name=nname,value=vvalue,inline=True)
        listembeds[-1].set_footer(text='Bot Created by Lore')
        for e in listembeds:
            await ctx.send(embed=e)

    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='vice-count')
    async def vice_(self,ctx):
        clans = LoadClans()#list of dicts
        for i in range(11):
            tag = clans[i]["Tag"]
            club = await myclient.get_club(tag)
            count=0
            for member in club.members:
                if member.role == 'vicePresident':
                    count+=1
            await ctx.send(str(clans[i]["Name"])+": "+str(count))

    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name="check-banlist",brief="Check if banned players are in a QLASH Clan",hidden=True)
    async def _banlist(self,ctx):
        await check_banlist_api()

    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name="giova",hidden=True)
    async def _giova(self,ctx):
        await giova()

    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name="ban",brief="Bans a user",hidden=False,pass_context=True)
    async def ban(member,delete_message_days,*reason):
        reason_ = " ".join(reason[:])
        if member == None:
            await ctx.send("InputError: Invalid member")
            return
        if int(delete_message_days) < 0 or int(delete_message_days) > 7:
            await ctx.send("InputError: Invalid integer for deleting messages (Min - 0 , Max - 7)")
            return
        await ctx.guild.ban(member,int(delete_message_days),reason_)
