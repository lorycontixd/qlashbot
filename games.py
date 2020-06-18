from instances import *
async def check_message_reaction(payload):
    ch = bot.get_channel(payload.channel_id)
    if ch.id == int(testchannel):
        print("in test channel")
        if payload.message_id == 723161253631098931:
            print("message 3")
            msg3 = await ch.fetch_message(int(payload.message_id))
            list = msg3.reactions
            if payload.emoji.name=='qlash':
                await ch.send("Hi "+payload.member.mention+". Enter the password within 30 seconds please")

                def check(message):
                    return message.author == payload.member

                reply = await bot.wait_for('message', check=check)
                if reply.content == 'qlashforthewin':
                    await ch.send("Well done "+payload.member.mention+". You won!")
                    return
