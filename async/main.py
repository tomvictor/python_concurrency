"""
Coroutines in python
====================


Coroutine methods
-----------------
cancel() - For cancelling
done() - Returns True, if the future object is completed or cancelled.
result() - Returns the result.
exception() - Returns any exception occured during the excecution of the program.
add_done_callback(fn)  - Adds callback to be run when done.

loop.run_until_complete(future) - loop stops after future is complete.

"""

import asyncio
import aiohttp
import async_timeout


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, "http://python.org")
        print(html)


if __name__ == "__main__":
    print("initializing . . . .")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
