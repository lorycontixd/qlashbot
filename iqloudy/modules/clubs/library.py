
async def is_official_club(self, ctx, gametag):
    found = False
    for c in self.qlash_bs['official_clubs']:
        if gametag.startswith("#") and c['tag'] == gametag:
            found = True
            break
        elif c['name'] == gametag:
            found = True
            break

    if found:
        await ctx.send("Yes, it is official.")
    else:
        await ctx.send("Not official")
