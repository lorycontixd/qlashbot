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
                print("winner"+str(payload.member))
