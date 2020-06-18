from instances import *

#***************** treasure_hunt *****************
async def game1_reaction(payload):
    ch = bot.get_channel(payload.channel_id)
    if ch.id == int(testchannel):
        if payload.message_id == 723182220910526486:
            msg3 = await ch.fetch_message(int(payload.message_id))
            list = msg3.reactions
            if payload.emoji.name=='qlash':
                await ch.send("Hi "+payload.member.mention+". Enter the password within 30 seconds please")

                def check(message):
                    return message.author == payload.member

                reply = await bot.wait_for('message',timeout=30.0, check=check)
                if reply.content == 'Luca Pagano':
                    await payload.member.create_dm()
                    await payload.member.dm_channel.send("Well done +"str(payload.member.name+"for completing step 1.\n \nThe tip for the next step is the following:\n**I think I know the nickname of the brawler posted from Qlash_brawlstars on the 27th May**")
                    role = discord.utils.get(message.guild.roles, name="step1")
                    await payload.member.add_roles(role)
                    return
                else:
                    await payload.member.create_dm()
                    await payload.member.dm_channel.send("Sorry wrong password!")
                    return

async def game1_nickname(before,after):
    role1 = discord.utils.get(message.guild.roles, name="step1")
    if role1 not in before.roles and role1 not in after.roles:
        return
    if before.nick != after.nick:
        if str(after.nick).lower() == 'bibi':
            await after.create_dm()
            await after.dm_channel.send("You passed step 2, well done!")
            role2 = discord.utils.get(message.guild.roles, name="step2")
            await after.add_roles(role2)
