# coding: utf-8
from annoy import AnnoyIndex
import json
import random
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

illust_vector_list = []
dim = 512
t = AnnoyIndex(dim)  # Length of item vector that will be indexed
path = '../keras/pixiv-ranking-features.txt'
with open(path, 'r') as f:
    i = 0
    line = f.readline()
    while line:
        js = json.loads(line)
        illust_vector_list.append(js)
        print(i)
        if i > 1e6:
            break
        i = i + 1

for i, illust_vector in enumerate(illust_vector_list):
    print(i)
    if not redis_client.exists(str(i)):
        redis_client.set(str(i), illust_vector['illust_id'])
    try:
        t.get_item_vector(i)
    except IndexError as err:
        t.add_item(i, illust_vector['features'])

t.build(100) # 100 trees
if t.get_n_items() > 0:
    t.save('pixiv-ranking.ann')

#u = AnnoyIndex(dim)
#u.load('test.ann') # super fast, will just mmap the file
#print(u.get_nns_by_item(i=0, n=10, search_k=-1, include_distances=False)) # will find the 1000 nearest neighbors
