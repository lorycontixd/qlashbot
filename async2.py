import aiohttp
from aiohttp_proxy import ProxyConnector, ProxyType

import brawlstats
import asyncio

connector = ProxyConnector(
	proxy_type=ProxyType.SOCKS5,
	host='54.72.12.1',#'eu-west-static-03.quotaguard.com',
	port=1080,
	username='6cy3e5odaiitpe',
	password='gxag60u036717xavs35razjk18s2',
    rdns=True
)

client = brawlstats.Client('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImUyOTQ3MjlhLWE5YjYtNDIxNy05MTdlLTUxZDJhYzRmOWI4NSIsImlhdCI6MTU5MDI3MDMwNywic3ViIjoiZGV2ZWxvcGVyLzMwMWI3NDk1LWE0OTQtYmIzNy05MWFlLWM5MGEyZmRjMDBjOSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNTQuNzIuMTIuMSIsIjU0LjcyLjc3LjI0OSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.RODZQwDO2YZZF_JAazFccdrg1YiPcaqGmxtPe40ZN-zvVDK3sXuX1-yqGWwjBdd-MoyTqfrsPxhS3V_IUNf9qQ', is_async=True, connector=connector)
async def main():
    try:
        player = await client.get_profile('PCJ9CVJUG')
        print(player.trophies)  # access attributes using dot.notation
        print(player.solo_victories)  # access using snake_case instead of camelCase

        club = await player.get_club()
        print(club.tag)
        members = await club.get_members()
        best_players = members[:5]  # members sorted by trophies, gets best 5 players
        for player in best_players:
            print(player.name, player.trophies)

        ranking = await client.get_rankings(ranking='players', limit=5)  # gets top 5 players
        for player in ranking:
            print(player.name, player.rank)

        # Get top 5 mortis players in the US
        ranking = await client.get_rankings(
            ranking='brawlers',
            region='us',
            limit=5,
            brawler='mortis'
        )
        for player in ranking:
            print(player.name, player.rank)

        battles = await client.get_battle_logs('GGJVJLU2')
        print(battles[0].battle.mode)
    except Exception as e:
        print(e)
    finally:
        await connector.close()
        await client.close()


# run the async loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
