#record
import asyncio
from scheduler import *

async def r():
    await record()

loop = loop = asyncio.get_event_loop()
loop.run_until_complete(r())
loop.close()
