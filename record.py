#record

import asyncio
from scheduler import *

async def daily_record():
    await record()

loop = asyncio.get_event_loop()
loop.run_until_complete(daily_record())
loop.close()
