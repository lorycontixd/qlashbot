import asyncpg
import discord
from discord.ext import tasks, commands
from instances import *

@tasks.loop(seconds=5.0, count=5)
async def slow_count(ctx):
    await ctx.end(slow_count.current_loop)

@slow_count.after_loop
async def after_slow_count(ctx):
    await ctx.send('done!')
