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
        print(js['illust_id'])
        illust_vector_list.append(js)
        if i > 1e3:
            break
        i = i + 1
        line = f.readline()

for i, illust_vector in enumerate(illust_vector_list):
    illust_id = illust_vector['illust_id']

    line2illustId = f"line2illustId_{i}"
    illustId2line = f"illustId2line_{illust_id}"
    print(f"{line2illustId} -> {illustId2line}")
    redis_client.delete(line2illustId)
    redis_client.delete(illustId2line)
    if not redis_client.exists(line2illustId):
        # 本当はトランザクションを貼りたい
        redis_client.set(line2illustId, illust_vector['illust_id'])
        redis_client.set(illustId2line, str(i))
        try:
            t.get_item_vector(i)
        except IndexError as err:
            t.add_item(i, illust_vector['features'])

t.build(100) # 100 trees
if t.get_n_items() > 0:
    t.save('pixiv-ranking.ann')
