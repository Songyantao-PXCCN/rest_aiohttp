import aiohttp
import asyncio ,time

async def fetch(session, url):
    print(time.time())
    async with session.get(url,headers = {'sss':'23'},data = 'sss',params = {'s':'32'},verify_ssl = False) as response:
        print(time.time())
        print(type(response.status))
        tmp = await response.text()
        print(tmp[:10])
        hdr = response.headers
        print(type(hdr.get('Content-Type')))


async def main():
    async with aiohttp.ClientSession() as session:
        await fetch(session, 'http://192.168.124.10')
        # print(html)
        return 100

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    a = loop.run_until_complete(main())

    print(a)