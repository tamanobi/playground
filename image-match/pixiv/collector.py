# coding: utf-8
import requests
import json

def getUrlsFromPixivRanking():
    l = [];

    base = 'https://www.pixiv.net/ranking.php'
    for page in range(1, 100):
        params = f'?mode=daily&content=illust&p={page}&format=json'
        res = requests.get(f"{base}{params}")
        if res.status_code != 200:
            return l
        js = json.loads(res.text)
        for contents in js['contents']:
            l.append(contents['url'])
    return l

if __name__ == '__main__':
    print(getUrlsFromPixivRanking())
