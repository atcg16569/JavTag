import aiohttp
import asyncio
from bs4 import BeautifulSoup

bus = {'name': 'javbus', 'url': 'https://www.javbus.com/',
       'selector': {'director': "a[href*='director']", 'studio': "a[href*='studio']", 'genre': '.genre>label>a',
                    'star': "div.star-name>a"}
       }
Proxy = 'http://127.0.0.1:7890'
Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml'}
info = {}
policy = asyncio.WindowsSelectorEventLoopPolicy()
asyncio.set_event_loop_policy(policy)


async def get_html(url, headers=None, proxy=Proxy):
    if headers is None:
        headers = Headers
    async with aiohttp.ClientSession(headers=headers, trust_env=True) as session:
        async with session.get(url, proxy=proxy) as r:
            print(r.status)
            return await r.text()


def dealbus(site, soup):
    info['director'] = soup.select_one(site['selector']['director'])
    info['studio'] = soup.select_one(site['selector']['studio'])
    info['star'] = soup.select_one(site['selector']['star'])
    info['genre'] = soup.select(site['selector']['genre'])
    for k, v in info.items():
        if v is None:
            info[k] = None
        elif k == 'genre':
            g = {'from': site['name'], 'tags': []}
            for label in v:
                g['tags'].append(label.text.strip())  # 适配
            info[k] = g
        else:
            for r in v:
                info[k] = r.string.strip()  # 适配
    return info


async def get_info(ID, site):
    html = await get_html(site['url'] + ID)
    soup = BeautifulSoup(html, 'html.parser')
    if site['name'] == 'javbus':
        return dealbus(site, soup)


# if __name__ == '__main__':
    # asyncio.run(get_info('XMOM-034', bus))
