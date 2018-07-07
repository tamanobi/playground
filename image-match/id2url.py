# coding: utf-8
import redis
import glob
from pixiv.collector import urlToIllustId

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

urls = []
with open('../keras/rankedin_uniq.txt') as f:
    urls = f.readlines()

for i, url in enumerate(urls):
    url_stripped = url.strip()
    illust_id = urlToIllustId(url_stripped)
    print(f'{illust_id} -> {url_stripped}')
    redis_client.set(f'id2url_{illust_id}', url_stripped)
