import discord
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from descriptions import *
#from functions import set_
from instances import *
from mongodb import *
from tasks import check_banlist_channel,giova

class Moderation(commands.Cog,name="Moderation"):
    def __init__(self):
        ipapi.location(ip=None, key=None, field=None)

    #@commands.command(name='set',brief="Get the discord role for the clan you belong to. (BS1) ",description=desc_set)
    #async def set(self,ctx,player:discord.Member,ingame_tag):
    #    await set_(ctx,player,ingame_tag)

    #ADMIN
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.has_any_role('Moderator','DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='bs-playerinfo',brief='Search for information about a generic ingame player. (BS1) ',description=desc_bs_playerinfo)
    async def bs_pinfo(self,ctx,player_tag):
        role=''
        player = await myclient.get_player(player_tag)
        if not player:
            await ctx.send("Player with this tag was not found. If you think this was a problem, contact the Bot creators.")
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
    @commands.command(name='bs-claninfo',brief='Search for information about an ingame clan. (BS1)',description=desc_bs_claninfo,)
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
    @commands.command(name='qlash-allclans',hidden=True,brief='List all ingame qlash clans. (BS30+) ',description = desc_qlash_allclans)
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
    @commands.command(name='locate',brief = 'Locate an ip address',description=desc_ip)
    async def locate(self,ctx,ip):
        print("Searching for location...")
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
    @commands.command(name='member-info',brief='Show information of a discord member',description=desc_memberinfo)
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
    @commands.command(name="server-info",brief="Show information of the server",description=desc_serverinfo)
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

    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='member-dm',pass_context=True,brief='Send a private message to a member by the bot.',description=desc_member_dm)
    async def dm(self,ctx,member: discord.Member, *message):
        mess = ctx.message
        await member.create_dm()
        await member.dm_channel.send(" ".join(message[:]))
        await mess.add_reaction('✅')

    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='announce',brief='Send a message to a specific channel by the bot.',description=desc_announce)
    async def annouce(self,ctx,channelname,*message):
        msg = ctx.message
        temp = " ".join(message[:])
        guild = ctx.guild
        channel = discord.utils.get(guild.text_channels, name=channelname)
        if channel == None:
            await ctx.send("Channel not found")
            return
        try:
            await channel.send(temp)
            await msg.add_reaction('✅')
        except:
            await ctx.send("Error sending message")

    @commands.has_any_role('DiscordDeveloper','QLASH')
    @commands.command(name='welcome',brief='Send a welcome message to a specific channel by the bot.',hidden=True)
    async def welcome(self,ctx,channelname):
        msg = ctx.message
        guild = ctx.guild
        channel = discord.utils.get(guild.text_channels, name=channelname)
        if channel == None:
            await ctx.send("Channel not found")
            return
        await welcome_message.send_file(channel, welcome_message.WELCOME_MESSAGE_SECTION_IMAGE_URL, "banner.png")
        await channel.send(welcome_message.WELCOME_MESSAGE_FIRST_SECTION.format(ALL_QLASH_CLANS_CHANNEL = _mention_channel(566213862756712449)))
        await channel.send(embed=welcome_message.WELCOME_MESSAGE_SECOND_SECTION)
        await welcome_message.send_file(channel, welcome_message.RULES_SECTION_IMAGE_URL,  "rules.png")
        await channel.send(welcome_message.RULES_MESSAGE_FIRST_SECTION)
        await channel.send(welcome_message.RULES_MESSAGE_SECOND_SECTION)
        await msg.add_reaction('✅')

    @commands.has_any_role('Moderator','DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='purge',brief='Clear messages in the channel.',description=desc_purge)
    async def purge(self,ctx,amount):
        author = ctx.message.author
        await ctx.channel.purge(limit=int(amount)+1)
        msg = await ctx.send("Deleted "+str(amount)+" messages from "+author.mention+" in channel "+str(ctx.message.channel))
        await msg.delete(delay=5.0)

    @commands.has_any_role('Moderator','DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name='purge-user',brief="Clear all messages from a user inside a give channel")
    async def purge_user(self,ctx,channelname,member:discord.Member):
        i=0
        m = ctx.message
        channel = discord.utils.get(ctx.guild.text_channels, name=channelname)
        if channel == None:
            await ctx.send(ctx.message.author.mention+", no channel found with name "+channelname)
            return
        messages = await channel.history(limit=1000).flatten()
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
        print(member,role)
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

    @commands.has_any_role('Moderator','DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
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
        await check_banlist_channel()

    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator','Coordinator','QLASH')
    @commands.command(name="giova",hidden=True)
    async def _giova(self,ctx):
        await giova()
