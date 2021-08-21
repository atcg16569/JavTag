import json
import asyncio
import random
import javReq
import re


def json2dict(file):
    with open(file, encoding='utf-8') as jsonfile:
        mlist = json.load(jsonfile)
    return mlist


def dict2json(name, data):
    with open(f'{name}.json', 'w', encoding='utf-8') as out:
        json.dump(data, out, ensure_ascii=False)


def namematch(fpath):
    match = re.findall(r'[/\\]?(\w+)\.json', fpath)
    if match:
        return match[0]
    else:
        print(r'path not \w')
        return False


async def search(fpath):
    name = namematch(fpath)
    if name:
        jlist = json2dict(fpath)
        newlist = []
        suffix = '_'
        for p in jlist:
            for m in p['movies']:
                time = random.randint(2, 20)
                print(f'{time} seconds')
                await asyncio.sleep(time)
                m |= await javReq.get_info(m['id'], javReq.bus)
                if suffix == '_':
                    suffix = suffix + m['genre']['from']
                newlist.append(m)
                print(f'add {m}\n')
        dict2json(f"{name}{suffix}", newlist)
        moviespath = f"{name}{suffix}.json"
        print(f"{moviespath} wrote\n")


# if __name__ == '__main__':
#     asyncio.run(search('F:\\xuexiao.json'))
