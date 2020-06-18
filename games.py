
async def check_message_reaction(reaction,user):
    msg = reaction.message
    if msg.id == 723161253631098931:
        print("reaction added to 3"+str(reaction.emoji))
        list = msg.reactions
        for i in range(len(list-1)):
            if list[i].emoji.name == ':qlash:':
                if list[i+1].emoji == '🔝':
                    users = await list[i].users().flatten()
                    users2 = await list[i+1].users().flatten()
                    for u in users:
                        if u in users2:
                            print(str(u)+" is the winner")
