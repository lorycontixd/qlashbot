import discord
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from descriptions import *
from functions import *

class Moderation(commands.Cog,name="Moderation"):
    def __init__(self):
        print("Moderation Cog called")

    @commands.command(name='set',brief="(MOD)(BS1) Get the discord role for the clan you belong to.",description=desc_set)
    async def set(self,ctx,player:discord.Member,ingame_tag):
        await set_(ctx,player,ingame_tag)

    #ADMIN
    @commands.command(name='bs-playerinfo',brief='(MOD) (BS1) Search for information about a generic ingame player.',description=desc_bs_playerinfo)
    async def bs_pinfo(self,ctx,player_tag):
        await getplayer(ctx,player_tag)

    #ADMIN
    @commands.command(name='bs-claninfo',brief='(MOD) (BS1) Search for information about an ingame clan.',description=desc_bs_claninfo,)
    async def bs_cinfo(self,ctx,clan_tag):
        await getclan(ctx,clan_tag)

    #ADMIN
    @commands.command(name='bs-memberinfo',brief='(MOD) (BS1) Search for information about a member within a given clan.',description=desc_bs_memberinfo)
    async def bs_minfo(self,ctx,name,clan_tag):
        await search_member(ctx,name,clan_tag)

    @commands.command(name='locate',brief = '(MOD) Locate an ip address',description=desc_ip)
    async def locate(self,ctx,ip):
        await locate_(ctx,ip)

    @commands.command(name='member-info',brief='(MOD) Show information of a discord member',description=desc_memberinfo)
    async def memberinfo(self,ctx,member:discord.Member):
        await member_info_(ctx,member)

    @commands.command(name="server-info",brief="(MOD) Show information of the server",description=desc_serverinfo)
    async def serverinfo(self,ctx):
        await serverinfo_(ctx)

    @commands.command(name='member-dm',pass_context=True,brief='(MOD) Send a private message to a member by the bot.',description=desc_member_dm)
    async def dm(self,ctx,member: discord.Member, *message):
        await poke(ctx,member,*message)

    @commands.command(name='announce',brief='(MOD) Send a message to a specific channel by the bot.',description=desc_announce)
    async def annouce(self,ctx,channel_name,*message):
        await write_message(ctx,channel_name,*message)

    @commands.command(name='welcome',brief='(MOD) Send a welcome message to a specific channel by the bot.')
    async def welcome(self,ctx,channel_name):
        await welcome_announcement(ctx,channel_name)

    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator')
    @commands.command(name='purge',brief='(MOD) Clear messages in the channel.',description=desc_purge)
    async def purge(self,ctx,amount):
        author = ctx.message.author
        await ctx.channel.purge(limit=int(amount)+1)
        msg = await ctx.send("Deleted "+str(amount)+" messages from "+author.mention+" in channel "+str(ctx.message.channel))
        await msg.delete(delay=5.0)

    @commands.command(name='purge-user',brief="(MOD) Clear all messages from a user inside a give channel")
    async def purge_user(self,ctx,channelname,member:discord.Member):
        await purge_user_(ctx,channelname,member)

    @commands.command(name="role-give",hidden=True,pass_context=True)
    async def role_give(self,ctx,member: discord.Member , *rolename):
        await giverole(ctx,member,*rolename)

    @commands.command(name="role-remove",hidden=True,pass_context=True)
    async def role_rem(self,ctx,member: discord.Member , *rolename):
        await removerole(ctx,member,*rolename)

    @commands.has_any_role('DiscordDeveloper', 'Sub-Coordinator')
    @commands.command(name='role-count')
    async def role_count(self,ctx,*rolename):
        role_name = " ".join(rolename[:])
        dev = discord.utils.get(ctx.guild.roles, name="DiscordDeveloper")
        for role in ctx.guild.roles:
            if role.name == str(role_name):
                rolecount = int(len(role.members))
                await ctx.send("In the role "+str(role.name)+" there are "+str(rolecount)+" members! ")
                return
        await ctx.send("No roles found for role "+role_name+"! If you think this is a mistake please contact a "+dev.mention)

    @commands.has_any_role('QLASH', 'Coordinator')
    @commands.command(name='all-roles')
    async def print_report(self,ctx):
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

    @commands.command(name='role-members')
    async def print_rolemembers(self,ctx,*rolename):
        await print_rolemembers_(ctx,*rolename)

    @commands.command(name='vice-count')
    async def vice_(self,ctx):
        await vice(ctx)

    @commands.command(name="check-banlist",brief="(MOD) Check if banned players are in a QLASH Clan")
    async def _banlist(self,ctx):
        await check_banlist_channel()

    @commands.command(name="giova")
    async def _giova(self,ctx):
        await giova()
