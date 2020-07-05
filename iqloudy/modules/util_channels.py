role_everyone = 415221296247341066


async def util_check_channel (cog, ctx, channel):
    await ctx.send(channel.overwrites)
