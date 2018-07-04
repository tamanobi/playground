# coding: utf-8
from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES
from PIL import Image
import requests
import io

es = Elasticsearch(hosts="127.0.0.1", ports=9200)
ses = SignatureES(es)

r = ses.search_image("./demo_69460932.jpg")
res = requests.get(r[0]['path'], headers={'referer': 'https://www.pixiv.net/'})
im2 = Image.open(io.BytesIO(res.content))
im2.show()
