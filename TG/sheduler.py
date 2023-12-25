import asyncio

from handlers import Reporting


async def sheduler():
    while 1:
        get_status_url = await Reporting.get_reporting_status_false()
        for i in get_status_url:

            print(i.url)
        await asyncio.sleep(30)