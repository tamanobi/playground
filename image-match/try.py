# coding: utf-8
from pixiv.collector import getUrlsFromPixivRanking
from pixiv.collector import urlToIllustId
from pixiv.collector import getYmdStringListUntilLastYear
import os
import glob
import urllib
from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES

es = Elasticsearch(hosts="127.0.0.1", ports=9200)
ses = SignatureES(es)

# reset
reset = True
if reset:
    es.indices.delete(index='images', ignore=[400, 404])
    es.indices.create(index='images', ignore=[400])

urls = []
for path in glob.glob('*.txt'):
    with open(path, "r") as f:
        urls.extend(f.readlines())

for i, url in enumerate(urls):
    print(f"{i}/{len(urls)}", url)
    illust_id = urlToIllustId(url)

    meta = {}
    if illust_id is not False:
        meta = {'illust_id': illust_id}
    else:
        meta = None
    r = ses.es.search(index="images", body={
        'query': {
            'match': {
                'metadata.illust_id': illust_id
            }
        }
    })
    if (r['hits']['total'] == 0):
        try:
            ses.add_image(url, metadata=meta)
        except urllib.error.HTTPError as err:
            if err.code == 403 or err.code == 404:
                print('skip because 403 or 404')
            else:
                raise err

#r = ses.search_image("./69471592_p0_master1200.jpg")
#print(r)
