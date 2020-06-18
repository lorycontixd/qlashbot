#commands and bot descriptions

bot_description = """Welcome to the QLASH Bot Help Center. I am QLASH Bot and I allow users to do a bunch of cool and interesting stuff 😎.
To navigate in this help menu, please type ^help <category name> to view all possible commands under a category, and ^help <category name> <command name> for a detailed description of a command.
To run a command type ^<category> <command> <parameters (if any)>, for example ^util qlash-clan QLASH Olympus or ^fun roll
If you have any question or problem with my commands, please do not hesitate to contact our staff or the Bot creators directly.
I hope you have a pleasant stay in the discord server! 🤩😁 """

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

#*****************************************************************************************************************
#**********************************************       MOD     ****************************************************
#*****************************************************************************************************************

desc_bs_playerinfo = """Moderator Command
No Cooldown \n
Search for information about a specific PLAYER from the Brawl Stars game, including: \n-- Name & Tag \n-- Highest & Current Trophies \n-- Player Victories \n-- Championship Qualification"""

desc_bs_claninfo = """Moderator Command
No Cooldown \n
Search for information about a specific CLAN from the Brawl Stars game, including: \n-- Name & Tag \n-- Current & Required Trophies \n-- Player Count \n-- President & Highest Member"""

desc_bs_memberinfo =  """Moderator Command
No Cooldown \n
Search for information about a specific MEMBER in a given clan from the Brawl Stars game.
The difference from the player information is that, while in the previous function the parameter <#gametag> is required, for this function it is necessary to give the parameters <PlayerName> and <#clantag>, allowing you to not know the player's ingame tag.
Informations about the member include:
\n-- Name & Tag \n-- Clan Role \n-- Player Trophies"""

desc_clan_add = """Moderator Command
No Cooldown \n
Add a QLASH Clan to the database. The parameters are the clan's tag and the clan's name written correctly.
Moderator and Sub-Coordinator roles are required."""

desc_clann_remove = """Moderator Command
No Cooldown \n
Remove a QLASH Clan to the database. The parameter is the clan's name written correctly.
Moderator and Sub-Coordinator roles are required."""

desc_ip = """Moderator Command
No Cooldown \n
Locate an ip address with information such as country, city, postal code, longitude & latitude and much more.
Only the creators of the bot have access to this function. Please contact them."""

desc_memberinfo = """Moderator Command
No Cooldown \n
Show rich information about a discord member inside the server.
Information includes: \n-- Name, Tag & ID\n-- Member Status \n-- Server join date \n-- Top role and permissions."""

desc_serverinfo = """Moderator Command
No Cooldown \n
Shows all information of the current server.
These include: \n-- Name & ID \n-- Region \n-- Member count \n--Owner \n-- Date of creation. \n-- Much more"""

desc_member_dm = """Moderator Command
No Cooldown \n
The bot sends a private message to the specified member.
The member can be accessed by tagging or by name#discriminator, while the message is written after the member parameter."""

desc_announce = """Moderator Command
No Cooldown\n
The bot sends a message to the a specified channel.
The channel can be accessed by name, while the message is written after the channel parameter"""

desc_refresh_banlist = """Moderator Command
No Cooldown \n
Get a list of members who are currently banned from ingame QLASH clans, but that find themselves in one.
The information is gathered from the banlist channel, where the most relevant information is the player tag and the period of ban."""

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

desc_purge = """Moderator Command
No Cooldown \n
Clear a certain amount of messages in the channel where the command is invoked from.
"""

desc_view_members="""Moderator Command
No Cooldown \n
Get a list of players that left each QLASH Clan since the last time the database was updated (with the command ^mod write-members).
It is possible that the list of players will be long, therefore it might take some time.
"""

desc_write_members = """Moderator Command
No Cooldown \n
Update the database with clan members (see help for command view-members)
"""

#*****************************************************************************************************************
#**********************************************       FUN     ****************************************************
#*****************************************************************************************************************

desc_coinflip = """Fun command
30 seconds cooldown per user \n
Throw a coin to get a completely random outcome from either Heads or Tails."""

desc_tstatus = """Fun command
50 seconds cooldown in the server \n
Check the flip status of the table. It does not reset automatically.
"""

desc_bs_puns = """Fun command
60 seconds cooldown per channel \n
Post a random and very funny pun about Brawl Stars.
"""


#*****************************************************************************************************************
#*********************************************       UTIL     ****************************************************
#*****************************************************************************************************************

desc_hello = """Utility command
60 seconds cooldown per channel \n
Welcomes a user to the server. Bot presents itself and reveals help command"""

desc_qlash_allclans = """Utility command
60 seconds cooldown per channel \n
Print a list of all official QLASH Clans and the respective required trophies. No Parameters are needed for this function."""

desc_qlash_clan = """Utility command
60 seconds cooldown per channel \n
Print information about a specific QLASH Clan.
The parameter can be the clan tag (for precise search) or the clan name. In the second case, the name must be exact, or the command will not work."""

desc_set = """Utility command
60 seconds cooldown per user (only usable in the roles_assignement channel) \n
Get the discord role for the QLASH clan you belong to in Brawl Stars.
If you already have the right role, it will give it again. If you do not belong to an official clan, it will tell you explicitly.
The parameter required is your INGAME tag that you can find in your ingame profile."""

desc_weather_current = """Utility command
60 seconds cooldown per user \n
Get excellent information on the weather of a city. The parameters are <city> and <country_code>.
Both parameters are case insensitive, but need to be exact or the command will give an error.
Some country codes are:
    -Italy: IT
    -Great Britain: GB / United Kingdom: UK  --> Some functions take GB while some take UK, be careful
    -Spain: ES
    -France: FR
    -United States: US
    -Germany: DE
    -Marocco: MA
    -etc...
"""

desc_weather_5days = """Utility command
60 seconds cooldown per user \n
Get excellent information on a 5-days weather forecast of a city. The parameters are <city> and <country_code>.
Both parameters are case insensitive, but need to be exact or the command will give an error.
Only the most important information is desplayed, such as general weather and minimum/maximum temperature.
Some country codes are:
    -Italy: IT
    -Great Britain: GB / United Kingdom: UK  --> Some functions take GB while some take UK, be careful
    -Spain: ES
    -France: FR
    -United States: US
    -Germany: DE
    -Marocco: MA
    -etc...
"""

#*****************************************************************************************************************
#********************************************       VARIOUS     **************************************************
#*****************************************************************************************************************

desc_channels = """Print a list of the mosts important channels in the server and the corresponding descriptions.
"""

channels_response = """
```
Here is a list of the main channels in this server:
- #welcome: here you can read our main rules, that were written in order to establish order in the server. We advise you to read them carefully.
- #🔥announcements: we use this channel to announce changes, tournaments, competitions, application availability and more things within the server.
- #👑all-qlash-clans: here you can find a list of all official QLASH clans in Brawl Stars, with the corresponding trophy requirement.
- #roles-assignment: in this channel you can send a screenshot as a proof of your position in a qlash clan to unlock benefits such as tournaments, dedicated channels and more.
- there are various general chats for most of the languages worldwide. Please chat in the right channel based on the languages you speak.
- #📗support: in this channel you can publicly ask for help at any time and our staff will contact you as soon as possible.
- #🤖bot-spam: in this channel you can interact with our bots. We use this channel to avoid confusion in rooms for normal conversation.
- #📢tournament-announcements: here we give announcements on new qlash tournaments!

If you have more questions about channels, do not hesitate to contact our staff.
```
"""

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
