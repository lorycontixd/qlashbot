import discord
import pytz
import random
import asyncio

from bot_instances import *
from modules.mongodb.library import *
from dateutil import tz
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from modules.verification.library import check_equal_lists,validate_tag
from modules.gametag_upload.library import gametags_process

#*******************************************   ON READY   ************************************************

async def on_ready_():
    scheduler.add_default_tasks(apscheduler)
    print('--------------------------')
    print('Logged in as: ',bot.user)
    print('Bot ID: ',bot.user.id)
    print('Creation Date: ',bot.user.created_at)
    print('Websocket Gateway: ',bot.ws)
    tz = pytz.timezone('Europe/Rome')
    nnow = datetime.now(tz=tz)
    ttime = nnow.strftime("%d/%m/%Y %H:%M:%S")
    print("Current Time: "+str(ttime))
    print('--------------------------')
    app = await bot.application_info()
    print("Application owner: "+str(app.owner))
    print("Application Name: "+str(app.name))
    print("Application ID: "+str(app.id))
    print("Public Bot: "+str(app.bot_public))
    print('--------------------------')

    #mych = await bot.fetch_channel(int(bot_testing))
    #await mych.send("Bot has logged in 🟢")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="^help for help"))
    #ch = bot.get_channel(int(bot_developer_channel))
    #messages = ["Here I am. Hrmmm.", "Up and runnning I am.", "Hello again! I'm here. Yes. Hrmmmm.", "Back on track, I am."]
    #await ch.send(random.choice(messages))

async def on_member_ban_(guild,user):
    logs = bot_instances.bot.get_channel(int(bot_instances.qlash_bot))
    tz = pytz.timezone('Europe/Rome')
    e=discord.Embed(title="User has been banned from the server: "+str(user), description="--------------------------------------",color=0xe32400)
    e.add_field(name="User",value=str(user),inline=True)
    e.add_field(name="User ID",value=str(user.id),inline=True)
    e.add_field(name="Created at",value=str(user.created_at.strftime("%d/%m/%Y %H:%M%S")),inline=True)
    e.add_field(name="Time of ban",value=str(datetime.now(tz=tz).strftime("%d/%m/%Y %H:%M%S")),inline=True)
    e.set_footer(text="Created by Lore")
    await logs.send(embed=e)


#*******************************************   ON MEMBER JOIN   ******************************************

#check for Suspicious Member joining
watchouts = ['spongebob']
async def member_join_check(member:discord.Member):
    mychannel = bot.get_channel(int(qlash_bot))
    membername = str(member.name).lower()
    for item in watchouts:
        if item in membername:
            embed=discord.Embed(title="Suspicious member has joined the server: "+str(member), color=0xe32400)
            embed.set_author(name="QLASH Bot")
            embed.add_field(name="Account Creation Date", value=str(member.created_at), inline=True)
            embed.add_field(name="User ID", value=str(member.id), inline=True)
            embed.add_field(name="Mentionable", value=str(member.mention), inline=True)
            embed.add_field(name="Status", value=str(member.status), inline=True)
            embed.set_footer(text="Created by Lore")
            await mychannel.send(embed=embed)
            mod = discord.utils.get(message.guild.roles, name="Moderator")
            await mychannel.send(mod.mention)

#welcome message for new users
async def member_join_welcome(member:discord.Member):
    await member.create_dm()
    welcome_message = """
    🇬🇧 **Welcome**

    In #💫welcome-and-rules, you will find all the rules that need to be followed in this server.
    In  #📅calendar you will find events for each month
    In #📢tournament-announcements you can find the most relevant information about tournaments
    In #👑all-qlash-clans you can find a list of all QLASH clans
    In #roles-assignment you can request the role of the clan you are in by sending a screenshot
    Finally in the lounge area you can talk with other players


    🇪🇸 **Bienvenido**

    En #💫welcome-and-rules, encontrará todas las reglas que deben seguirse en este servidor.
    En #📅calendar encontrarás eventos para cada mes
    En #📢tournament-ads puedes encontrar la información más relevante sobre torneos
    En #👑all-qlash-clans puedes encontrar una lista de todos los clanes QLASH
    En #roles-assignment puede solicitar el rol del clan en el que se encuentra enviando una captura de pantalla
    Finalmente en lounge puedes hablar con otros jugadores.


    🇮🇹 **Benvenuti**

    Su #💫welcome-and-rules troverai tutte le regole del server da rispettare
    In #📅calendar troverai gli eventi di ogni mese
    In #📢tournament-announcements troverai le info più importanti sui tornei
    In #👑all-qlash-clans è presente una lista con tutti i clan QLASH
    In #roles-assignment puoi chiedere il ruolo rispettivo al tuo clan
    Infine nell'area lounge potrai parlare con chiunque
    """
    try:
        await member.dm_channel.send(str(welcome_message))
    except:
        pass


#*******************************************   ON MEMBER UPDATE   ******************************************

#JOIN new club role
#async def on_member_update_role(before,after):
#    if not check_equal_lists(before.roles,after.roles):
#        list = LoadClans()
#        clannames = [d["Name"] for d in list]
#        for role in after.roles:
#            if not role in before.roles:
#                if role.name in clannames:
#                    messages = ['We are delighted to have '+after.mention+' join us in '+role.name,'Hello '+role.name+'. Welcome to the team '+after.mention+'!','Hello '+role.name+'. We would like to welcome '+after.mention+' to the club.',"We're glad you are here, "+after.mention+"! "+role.name]
#                    print(after.name+" was given the role "+role.name)
#                    id = role.id
#                    clan_doc = get_clan(str(role.name))
#                    roleID = clan_doc["RoleID"]
#                    channelID = clan_doc["ChannelID"]
#                    if int(roleID) == id:
#                        ch = bot.get_channel(int(channelID))
#                        await ch.send(random.choice(messages))

#started listening spotify track
async def on_member_update_activity(before,after):
    ch = bot.get_channel(int(spotify_tracks))
    if not check_equal_lists(before.activities,after.activities):
        for a in after.activities:
            if a.type==discord.ActivityType.listening:
                messages = await ch.history(limit=500).flatten()
                a_list = a.artist.split(";")
                print(a_list)
                for art in a_list:
                    found = False
                    for message in messages:
                        if art == message.content.split('\t')[0]:
                            count = int(message.content.split('\t')[1])
                            response = str(art)+'\t'+str(count+1)
                            await message.edit(content=response)
                            found = True
                            break
                    if found==False:
                        await ch.send(str(art)+'\t1')

#*******************************************   ON MESSAGE   ******************************************

def LoadBadWords():
    dict = {}
    FILEPATH = './media/csv/bad_words.csv'
    file = open(FILEPATH,'r+')
    content = file.read()
    lines = content.split('\n')
    for i in range(len(lines)-1):
        ll = lines[i].split(',')
        badword = str(ll[0])
        language = str(ll[1])
        dict[badword]=language
    return dict

async def caps_spam_check(message):
    if type(message.channel)!= discord.TextChannel:
        return
    author = message.author
    if type(author)!=discord.Member:
        return
    sub = discord.utils.get(message.guild.roles, name="Sub-Coordinator")
    if author.top_role>=sub:
        return
    log_channel = bot.get_channel(int(qlash_bot))
    message_content = message.content
    parsed_message = message_content.split(" ")
    upper_cases = 0
    total_chars = len(message_content)
    if total_chars==0:
        return
    message_length = len(parsed_message)
    for word in parsed_message:
        for char in word:
            if char.isupper():
                upper_cases += 1
    percentage = float(upper_cases/total_chars)*100
    if int(percentage)>=60 and total_chars>7:
        mod = discord.utils.get(message.guild.roles, name="Moderator")
        embed=discord.Embed(title="Detected CAPS spam from "+str(author), color=0xff4013)
        embed.set_author(name="QLASH Bot")
        embed.add_field(name="Author", value=author.mention, inline=True)
        embed.add_field(name="Channel",value=message.channel.mention, inline = True)
        embed.add_field(name="Message date",value=message.created_at,inline=True)
        embed.add_field(name="ID",value=message.id,inline=True)
        embed.add_field(name="Capped character percentage",value=str(percentage)+"%",inline=True)
        embed.set_footer(text="Created By Lore")
        await log_channel.send(embed=embed)
        #await log_channel
    else:
        return

async def msg_spam_check(message):
    print("msg spam check called")
    author = message.author
    if type(message.channel)!= discord.TextChannel:
        return
    sub = discord.utils.get(message.guild.roles, name="Sub-Coordinator")
    if author.top_role>=sub:
        return
    log_channel = bot.get_channel(int(qlash_bot))
    message_content = message.content

    counter = 0
    async for old_message in message.channel.history(limit=6):
        if old_message.author == message.author:
            counter+=1
    print("counter ",counter)
    if counter > 5:
        print("entered if statement")
        mod = discord.utils.get(message.guild.roles, name="Moderator")
        embed=discord.Embed(title="Detected possible spam from "+str(author), color=0xff4013)
        embed.set_author(name="QLASH Bot")
        embed.add_field(name="Author", value=author.mention, inline=True)
        embed.add_field(name="Channel",value=message.channel.mention, inline = True)
        embed.add_field(name="Message date",value=message.created_at,inline=True)
        embed.add_field(name="ID",value=message.id,inline=True)
        embed.set_footer(text="Created By Lore")
        await log_channel.send(embed=embed)
    else:
        return

async def check_bad_words(message):
    author = message.author
    if message.channel.type != discord.TextChannel:
        return
    sub = discord.utils.get(message.guild.roles, name="Sub-Coordinator")
    if author.top_role>=sub:
        return
    mychannel = bot.get_channel(int(qlash_bot))
    message_content = message.content.lower()
    badword_dict = LoadBadWords()
    mod = discord.utils.get(message.guild.roles, name="Moderator")
    for badword in badword_dict:
        if badword in message_content:
            channel = bot.get_channel(int(qlash_bot))
            embed=discord.Embed(title="Detected Bad Word usage from user "+str(author), color=0xff4013)
            embed.set_author(name="QLASH Bot")
            embed.add_field(name="Author", value=author.mention, inline=True)
            embed.add_field(name="Bad Word", value=str(badword), inline=True)
            embed.add_field(name="Language", value=str(badword_dict[badword]), inline=True)
            embed.add_field(name="Channel",value=message.channel.mention, inline = True)
            embed.add_field(name="ID",value=message.id)
            embed.set_footer(text="Created By Lore")
            await mychannel.send(embed=embed)
            await mychannel.send(mod.mention)
            mess = await mychannel.send("Do I have permission to delete the message? (A moderatos has to react within 10 minutes)")
            await mess.add_reaction('✅')
            await mess.add_reaction('❌')

            def check(reaction,user):
                sub = discord.utils.get(message.guild.roles, name="Sub-Coordinator")
                return sub in user.roles

            try:
                await asyncio.sleep(1)
                reaction,user = await bot.wait_for('reaction_add', timeout=600.0, check=check)
                if str(reaction.emoji) == '✅':
                    await message.delete()
                    await mychannel.send("Message was successfully deleted.")
                    return
                elif str(reaction.emoji) == '❌':
                    await mychannel.send("Message was NOT deleted.")
                    return
            except asyncio.TimeoutError:
                await channel.send('Timeout Error 👎')

async def check_roles_assignement(message:discord.Message):
    author = message.author
    att = len(message.attachments)
    ch=message.channel
    #helper = discord.utils.get(message.guild.roles, name="Helper")
    #subcoord = discord.utils.get(message.guild.roles, name="Sub-Coordinator")
    if type(ch)!=discord.TextChannel:
        return
    if ch.name == "roles-assignment":
        if att==0:
            mod = discord.utils.get(message.guild.roles, name="Moderator")
            if author.top_role < mod:
                await message.delete()
                msg = await ch.send(author.mention+" You can only send screenshots for your role in this channel. If you have problems ask in support or contact a Moderator. Thank you!")
                await msg.delete(delay=8.0)

#on message event to gather gametags shared with starlist
async def bot_commands_gametag(message):
    ch = bot.get_channel(int(bot_commands_channel))
    if message.channel != ch:
        return
    if not message.startswith(".save"):
        return
    print("Received message from bot_commands channel")
    list = message.split(" ")
    tag = list[1]
    if validate_tag(tag):
        register_member(message.author,tag)


#*******************************************   ON REACTION ADD   ******************************************
async def reaction_check(payload):
    unwanted = ["💩","🖕","🔪","🤮"]
    if payload.emoji.name in unwanted:
        mod = discord.utils.get(payload.member.guild.roles, name="Moderator")
        if payload.member.top_role <= mod:
            mychannel = bot.get_channel(int(qlash_bot))
            e = discord.Embed(title="Detected unwanted emoji",description="-------------------------------------",color=0xff4013)
            e.add_field(name="Emoji",value=payload.emoji)
            e.add_field(name="Author",value=payload.member)
            ch = bot.get_channel(int(payload.channel_id))
            e.add_field(name="Channel",value=ch.mention)
            m = await ch.fetch_message(int(payload.message_id))
            e.add_field(name="Message",value="From "+str(m.author)+" at "+str(m.created_at.strftime("%d/%m/%Y, %H:%M:%S")))
            await mychannel.send(embed=e)
            await mychannel.send(mod.mention)

#*******************************************   SPECIAL EVENTS   ******************************************

from_zone = tz.tzutc() #utc
to_zone = tz.tzlocal() #local
ig_t_it= """🇮🇹
Una volta ricevuto il ruolo “IG-EUROPE” e avuto accesso alla lobby di registrazione (Instagram Tournament - EU - 07/06), se sei il capitano, dai il comando !register e si aprirà una finestra nei messaggi privati nella quale effettuare la registrazione in questo modo:
!createteam <Nome squadra> <nickname in game>

Se avrai fatto tutto correttamente il bot genererà un codice team che dovrai condividere solo con i tuoi due compagni di squadra.
- Per unirti ad una squadra già creata, dopo il comando !register scrivi al bot in privato il seguente comando:
!jointeam <code team> <nickname in game>

-Regole: #📕tournament-rules  sotto la voce "regole generali valide" per ogni modalità e "#Regole 3v3"
-Premi: #💰tournament-prizes
- Tutte le informazioni su come completare l'iscrizione puoi trovarle in #tournament-announcement


"""


ig_t_en="""🇬🇧
Once you'll get the role “IG-EUROPE” or “IG-AMERICA” and get the access into the registration's lobby Instagram Tournament – EU/AM - 07/06), if you're the captain, you have to put the command !register and you will have a window in private messages in which you can do the registration as it follows:
!createteam <Team's name> <In game nickname>

If you'll do all correctly the bot will generate a Team code that you have to share with your 2 teammates.
- To join in a Team already created, after the command !register write to the bot in private messages the following command:
!jointeam <Team code> <In game nickname>

-Rules: #📕tournament-rules  under #Rules 3v3
-Prizes: #💰tournament-prizes
- You can find all the information about how to complete the registration in #tournament-announcement


"""


ig_t_es="""🇪🇦
Una vez que tengas el rol “IG-EUROPE” o “IG-AMERICA” y el acceso al lobby de registro, si eres el capitán, debes poner el comando !register y tendrás una ventana privada en la que puedes hacer el registro de la siguiente manera:
!createteam <Nombre del equipo> <Apodo en el juego>

Si haces todo correctamente, el bot generará un código de equipo que debes compartir con tus 2 compañeros de equipo.
- Para unirte a un equipo ya creado, después del registro de comando escribe al bot en privado el siguiente comando:
!jointeam <Código de equipo> <Apodo en el juego>

-Reglas: #📕tournament-rules  abajo #Rules 3v3
- Premios: #💰tournament-prizes
- Puedes encontrar todas las informaciones sobre como registrarse en #tournament-announcement
"""

existing_roles = ["IG-EUROPE","IG-AMERICA"]
async def check_instarole(message:discord.Message):

    ch = message.channel
    if type(ch)!=discord.TextChannel:
        return
    dev = discord.utils.get(message.guild.roles, name="DiscordDeveloper")
    auth = message.author
    registered = False
    foundrole = ''
    if ch.name == "insta-roles":
        if len(message.attachments)!=0:
            for r in auth.roles:
                if r.name in existing_roles:
                    registered = True
                    foundrole = r.name
                    break

            if registered==False:
                msg = await ch.send("Hi "+message.author.mention+". Are you from North or South America? If **YES**, please react to the American Flag. If **NO**, please react to the World Emoji.\nThis information is important for you to enter. \nPlease select the right region, or you may be disqualified.")
                await msg.add_reaction('🇺🇸')
                await msg.add_reaction('🌎')

                def check(reaction,user):
                    return str(message.author.name)==str(user.name)

                def check2(reaction,user):
                    mod = discord.utils.get(message.guild.roles, name="Moderator")
                    sub = discord.utils.get(message.guild.roles, name="Sub-Coordinator")
                    return mod in user.roles or sub in user.roles

                try:
                    await asyncio.sleep(1)
                    reaction,user = await bot.wait_for('reaction_add', timeout=600.0, check=check)
                    if str(reaction.emoji) == '🇺🇸':
                        role = discord.utils.get(message.guild.roles, name="IG-AMERICA")
                        await message.author.add_roles(role)
                    elif str(reaction.emoji) == '🌎':
                        role = discord.utils.get(message.guild.roles, name="IG-EUROPE")
                        await message.author.add_roles(role)
                    msg2 = await ch.send("Thank you for your answer "+str(message.author.name)+"!")
                    await msg.delete(delay=4.0)
                    await msg2.delete(delay=5.0)
                    await message.add_reaction('✅')
                    await auth.create_dm()
                    await auth.dm_channel.send(ig_t_it)
                    await auth.dm_channel.send(ig_t_en)
                    await auth.dm_channel.send(ig_t_es)
                except asyncio.TimeoutError:
                    await msg.delete()
                    await ch.send('Timeout for user '+str(message.author.name)+' 👎\nPlease send a screenshot again and reply to the message')
            else:
                await ch.send("You are already given the instagram role "+foundrole+". If you have problems please contact a **Moderator** or a **DiscordDeveloper**. Thank you")

async def insta_role_ended(message):
    ch = message.channel
    if type(ch)!=discord.TextChannel:
        return
    auth = message.author
    if ch.name == "insta-roles":
        if len(message.attachments)!=0:
            msg = await ch.send("Hello "+auth.mention+". The Instagram Tournament registrations are closed. \nPlease check the calendar or the announcement channels to keep updated with new tournaments that you can join. Thank you very much!")
            await message.delete(delay=6.0)
            await msg.delete(delay=6.0)

async def read_file(message):
    ch = message.channel
    if ch.id == int(file_managing):
        if not message.author.bot:
            if len(message.attachments)!=0:
                await gametags_process(ch,message)
            elif message.content.startswith('#'):
                await gametags_process(ch,message)
            else:
                dev = discord.utils.get(message.guild.roles, name="DiscordDeveloper")
                #await message.delete(delay=3.0)
                #alert1 = await ch.send("This channel only takes in attachments. If this is a mistake, please contact a "+dev.mention+".")
                #await alert1.delete(delay=5.0)