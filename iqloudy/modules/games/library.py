
#***************** treasure_hunt *****************
async def game1_reaction(payload):
    ch = bot.get_channel(payload.channel_id)
    if ch.id == int(testchannel):
        if payload.message_id == 723182220910526486:
            msg3 = await ch.fetch_message(int(payload.message_id))
            list = msg3.reactions
            if payload.emoji.name=='qlash':
                await ch.send("Hi "+payload.member.mention+". In order to access the next checkpoint, please answer this quiz:\nWhen was Qlash founded?")

                def check(message):
                    return message.author == payload.member

                reply = await bot.wait_for('message',timeout=30.0, check=check)
                if reply.content == '2017':
                    await payload.member.create_dm()
                    await payload.member.dm_channel.send("Well done "+str(payload.member.name)+" for completing step 1.\n \nThe tip for the next step is the following:\n**I think I know the nickname of the brawler posted from Qlash_brawlstars on the 27th May**")
                    role = discord.utils.get(payload.member.guild.roles, name="step1")
                    await payload.member.add_roles(role)
                    return
                else:
                    await payload.member.create_dm()
                    await payload.member.dm_channel.send("Sorry wrong password!")
                    return

async def game1_nickname(before,after):
    role1 = discord.utils.get(after.guild.roles, name="step1")
    if role1 not in before.roles and role1 not in after.roles:
        return
    if before.nick != after.nick:
        if str(after.nick).lower() == 'bibi':
            await after.create_dm()
            await after.dm_channel.send("\nIn order to advance, please answer this quiz:\nWhich member of the staff is also the clan leader of QLASH Ares?")

            def check(message):
                return type(message.channel)==discord.DMChannel

            reply = await bot.wait_for('message',timeout=60.0, check=check)
            if reply.content.lower=="lore":
                role2 = discord.utils.get(after.guild.roles, name="step2")
                await after.dm_channel.send("Well done, you passed step 2!")
                await after.add_roles(role2)
