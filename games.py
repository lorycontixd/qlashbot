
async def check_message_reaction(reaction,user):
    ch = bot.get_channel(int(testchannel))
    chosenmsg = await ch.fetch_message(723161252020355214)
    list = chosenmsg.reactions
    for i in range(len(list)-1):
        if list[i].emoji == ':qlash:':
            if list[i].emoji == '🔝':
                users = await list[i].users().flatten()
                users2 = await list[i+1].users().flatten()
                for u in users:
                    if u in users2:
                        print(str(u)+" has won")
