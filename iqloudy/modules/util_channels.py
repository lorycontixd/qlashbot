role_everyone = 415221296247341066


async def util_check_channel (cog, ctx, channel):
    for role in channel.overwrites:
        print(role)
        ow = channel.overwrites[role]
        print(ow.pair())
    await ctx.send("not yet implemented")
