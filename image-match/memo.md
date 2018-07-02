pHashをアルゴリズムとして利用しているため、まったく違う系統の画像は検出できない。
意味レベルの類似の検出は見込めない。テキストを重疊したり、画像を変形させたりした場合は検出可能。

# image-matchの注意
elasticsearchpyのバージョンによっては動作しない。image-matchのrequirement.txtには、2.3以上、2.4未満の指定があるが、動作させるには、6系が必要。

https://github.com/ascribe/image-match/issues/88
