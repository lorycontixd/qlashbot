from random import randint

async def bs_puns(self, ctx):
    choices = ['What do you call it when you get killed by a bull main? Bull-shit.','What do you call it when you get killed by a Shelly main? Shell shock.','What do you call it when you get killed by a Poco main? Hacks.','What do you call a team of crows? Toxic','How is franks super? Literally stunning','What is Nita without her super? UnBearable',"El primo isn't really a jokester, but he can pack quite a punch line",'Killing that little cactus man will give you a decent Spike in ego.','My club has barley any members.','All these puns are literally Tara-ble.','El Primo jumping in the enemy base with 11 gems.']
    myint = randint(1,len(choices))
    await ctx.send(str(choices[myint]))

async def roll(self, ctx):
    value = randint(1,6)
    await ctx.send("You rolled a "+str(value))

async def ping(self, ctx):
    response='pong 🏓'
    await ctx.send(response)

async def coin_flip(self,ctx):
    flip = random.choice(['Heads','Tails'])
    await ctx.channel.send('You flipped '+flip)

async def flip():
    if self.is_flipped == False:
        response = '(╯°□°）╯︵ ┻━┻ '
        await ctx.channel.send(response)
        self.is_flipped = True
    else:
        response = 'Sorry the table is already flipped!! ¯\_(ツ)_/¯ '
        await ctx.channel.send(response)

async def unflip_(self,ctx):
    if self.is_flipped == True:
        response = '┬─┬ ノ( ゜-゜ノ)'
        await ctx.channel.send(response)
        self.is_flipped = False
    else:
        response = 'Sorry the table is already unflipped!! ¯\_(ツ)_/¯ '
        await ctx.channel.send(response)

async def table_status_(self,ctx):
    if self.is_flipped == True:
        response = 'Table is flipped'
        await ctx.channel.send(response)
    else:
        response = 'Table is unflipped'
        await ctx.channel.send(response)
