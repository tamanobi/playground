# coding: utf-8
from pixiv.collector import getUrlsFromPixivRanking
import os

fname = 'pixiv-ranking-urls.txt'
if not os.path.exists(fname):
    urls = getUrlsFromPixivRanking()
    with open(fname, 'w') as f:
        f.write("\n".join(urls))
else:
    with open(fname, 'r') as f:
        urls = f.readlines()

from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES

es = Elasticsearch(hosts="127.0.0.1", ports=9200)
ses = SignatureES(es)
reg_flg = True
if reg_flg is False:
    #print(es.indices.delete(index='images'))
    pass
for i, url in enumerate(urls):
    if reg_flg:
        print(i, url, es.indices.stats())
        ses.add_image(url)
    if i >= 400:
        break
# ses.add_image('https://pixabay.com/static/uploads/photo/2012/11/28/08/56/mona-lisa-67506_960_720.jpg')
# ses.add_image('https://upload.wikimedia.org/wikipedia/commons/e/e0/Caravaggio_-_Cena_in_Emmaus.jpg')
# ses.add_image('https://c2.staticflickr.com/8/7158/6814444991_08d82de57e_z.jpg')
#r = ses.search_image('https://pixabay.com/static/uploads/photo/2012/11/28/08/56/mona-lisa-67506_960_720.jpg')
#r = ses.search_image(urls[401])
r = ses.search_image("./69471592_p0_master1200.jpg")

print(r)
