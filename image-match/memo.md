# TODO
- [x] pixivの1年分ランキングサムネイルのURLをリストに書き出す
- [ ] URLをすべてElasticsearchに登録する(403や404はskip)

# image-matchの注意
pHashをアルゴリズムとして利用しているため、まったく違う系統の画像は検出できない。
意味レベルの類似の検出は見込めない。テキストを重疊したり、画像を変形させたりした場合は検出可能。

## elasticsearchpyのバージョンとの相性
elasticsearchpyのバージョンによっては動作しない。image-matchのrequirement.txtには、2.3以上、2.4未満の指定があるが、動作させるには、5あるいは6系が必要。

https://github.com/ascribe/image-match/issues/88

解決策: image-matchのgithubリポジトリのソースからインストールする(`pip install .`)。PyPIに登録されているものは古い
