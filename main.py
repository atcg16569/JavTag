import pandas as pd
import jsonReq
import sys


def extract(path, key):
    movies = jsonReq.json2dict(path)
    keys = []
    for movie in movies:
        keys.append(movie[key])
    print(f'keys list\n  {keys}\n')
    same = {}
    unique = {}
    for i, v in enumerate(keys):
        cop = keys.copy()
        cop[i] = None
        if v in cop:
            if v in same:
                same[v].add(i)
            else:
                same[v] = {i}
        else:
            unique[v] = i
    print(f"same index\n  {same}\n")
    print(f"unique index\n  {unique}\n")
    for k, v in same.items():
        tlist = []
        for ind in v:
            tlist += movies[ind]['genre']['tags']
        same[k] = tlist
    # print(f"same tag list\n  {same}\n")
    for k, v in same.items():
        count_dict = {}
        for stag in set(v):
            count_dict[stag] = v.count(stag)
        same[k] = count_dict
    print(f"same dict\n  {same}\n")
    for k, i in unique.items():
        count_dict = {}
        tags = movies[i]['genre']['tags']
        for t in tags:
            count_dict[t] = tags.count(t)
        unique[k] = count_dict
    print(f"unique dict\n  {unique}\n")
    result = same | unique
    return result


if __name__ == '__main__':
    if len(sys.argv)==1:
        jpath = sys.argv[1]
        mpath = jsonReq.search(jpath)
        print('please input key column')
        key = input()
        if len(key) == 0:
            print('exit without key')
        else:
            x = extract(mpath, key)
            print(pd.DataFrame(x))
    else:
        print('')
    sys.exit()

# jsonReq.dict2json(f"{jsonReq.namematch('xuexiao_javbus.json')}_studio", x)
