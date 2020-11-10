import random

async def bs_puns(self, ctx):
    choices = ['What do you call it when you get killed by a bull main? Bull-shit.','What do you call it when you get killed by a Shelly main? Shell shock.','What do you call it when you get killed by a Poco main? Hacks.','What do you call a team of crows? Toxic','How is franks super? Literally stunning','What is Nita without her super? UnBearable',"El primo isn't really a jokester, but he can pack quite a punch line",'Killing that little cactus man will give you a decent Spike in ego.','My club has barley any members.','All these puns are literally Tara-ble.','El Primo jumping in the enemy base with 11 gems.']
    myint = random.randint(1,len(choices))
    await ctx.send(str(choices[myint]))

async def roll(self, ctx):
    value = random.randint(1,6)
    await ctx.send("You rolled a "+str(value))

async def ping(self, ctx):
    response='pong 🏓'
    await ctx.send(response)

async def coin_flip(self,ctx):
    flip = random.choice(['Heads','Tails'])
    await ctx.channel.send('You flipped '+flip)

async def flip(self,ctx):
    if self.is_flipped == False:
        response = '(╯°□°）╯︵ ┻━┻ '
        await ctx.channel.send(response)
        self.is_flipped = True
    else:
        response = 'Sorry the table is already flipped!! ¯\_(ツ)_/¯ '
        await ctx.channel.send(response)

async def unflip(self,ctx):
    if self.is_flipped == True:
        response = '┬─┬ ノ( ゜-゜ノ)'
        await ctx.channel.send(response)
        self.is_flipped = False
    else:
        response = 'Sorry the table is already unflipped!! ¯\_(ツ)_/¯ '
        await ctx.channel.send(response)

async def table_status(self,ctx):
    if self.is_flipped == True:
        response = 'Table is flipped'
        await ctx.channel.send(response)
    else:
        response = 'Table is unflipped'
        await ctx.channel.send(response)


async def iqloudy_info(self, ctx):
    role = discord.utils.get(ctx.guild.roles, name="DiscordDeveloper")
    response = "This bot was written in the language of Python by a few users "+role.mention + \
        " with a passion for informatics and programming. \nThe core library used is the API offered by Discord called discordpy which grants access to an enormous amount of functions and events."
    response2 = "The brawlstats API was also used to gather information from the game, which allows to access a few but useful pieces of information. The bot commands can be viewed by typing ^help and navigating using groups (mod,util,sys and fun)"
    await ctx.send(response)
    await ctx.send(response2)
    e = discord.Embed(title="Bot info: " +str(self.bot.user.name), color=0xe392ff)
    e.set_author(name="QLASH Bot")
    e.add_field(name="Name", value=self.bot.user.mention, inline=True)
    e.add_field(name="ID", value=str(self.bot.user.id), inline=True)
    e.add_field(name="Is a Bot", value=str(self.bot.user.bot), inline=True)
    e.add_field(name="Creation Date", value=str(
        self.bot.user.created_at), inline=True)
    e.add_field(name="Latency", value=str(self.bot.latency), inline=True)
    e.add_field(name="Language", value=str(self.bot.user.locale), inline=True)
    e.set_footer(text="Bot created by "+role.mention)
    await ctx.send(embed=e)
