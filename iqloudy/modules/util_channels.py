role_everyone = 415221296247341066


async def util_check_channel (cog, ctx, channel):
    for role in channel.overwrites:
        print(role)
        print(channel.overwrites[role])
    await ctx.send("not yet implemented")
