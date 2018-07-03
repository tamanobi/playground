# coding: utf-8
import requests
import json
import re
import datetime

def getUrlsFromPixivRanking(dstring):
    l = [];

    base = 'https://www.pixiv.net/ranking.php'
    if dstring is None:
        datestring = "20180702"
    else:
        datestring = dstring

    for page in range(1, 100):
        params = f'?mode=daily&content=illust&p={page}&format=json&date={datestring}'
        res = requests.get(f"{base}{params}")
        if res.status_code != 200:
            return l
        js = json.loads(res.text)
        for contents in js['contents']:
            l.append(contents['url'])
    return l

def urlToIllustId(url):
    m = re.search(r"/([0-9]+)_p", url)
    if m:
        return m.group(1)
    else:
        return False

def getYmdStringListUntilLastYear():
    """現在日からYmd形式で1年分の文字列配列を生成"""
    today = datetime.date.today()
    datestrings = []
    for d in range(1, 365):
        dt = today + datetime.timedelta(days=-1 * d)
        datestrings.append(f"{dt:%Y%m%d}")
    return datestrings

def generatePixivRankingUrlsFile():
    filenames = []
    datestrings = getYmdStringListUntilLastYear()
    for i, ymdstring in enumerate(datestrings):
        print(i)
        urls = getUrlsFromPixivRanking(ymdstring)
        fname = f'pixiv-ranking-urls-{ymdstring}.txt'
        with open(fname, "w") as f:
            f.write("\n".join(urls))
        filenames.append(fname)
    return filenames

if __name__ == "__main__":
    print(generatePixivRankingUrlsFile())

