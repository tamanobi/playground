# ループ中のgoroutineでは束縛に気をつける

https://qiita.com/tamanobi/items/ced276961789d4943948

ほかのプログラミング言語の非同期処理でもよく起こしてしまう問題が、キャプチャのミスだ。今回は、 `go vet` で機械的に見つけ方法を紹介する

## 例題
goroutine を使って1,2,3とプリントする関数を3並列で処理したいとする[^1]。以下のコードを書いてみた。どういう動作をするだろうか？

[^1] 今回はプリントする関数としたが、実用であれば重い処理を実行する関数になるはず。

```go

package main

import (
	"fmt"
	"sync"
)

func main() {
	integers := make([]int, 3)
	for i := range integers {
		integers[i] = i
	}

	wg := &sync.WaitGroup{}
	for _, v := range integers {
		wg.Add(1)
		go func() {
			defer wg.Done()
			fmt.Println(v)
		}()
	}
	wg.Wait()
}
```

これを実行すると、2が3回プリントされる。

```console
$ go run main.go
2
2
2
```

## 回避

`fmt.Println` の引数として与えられている `v` がループ変数の `v` にキャプチャされているから起こる。これを回避するには以下のように書き換える。無名関数の部分に引数を渡す形にすればいい。

```diff
 	wg := &sync.WaitGroup{}
 	for _, v := range integers {
 		wg.Add(1)
-		go func() {
+		go func(v int) {
 			defer wg.Done()
 			fmt.Println(v)
-		}()
+		}(v)
 	}
 	wg.Wait()
 }
```

こうすることで期待した動作になる。

```console
$ go run  ./main.go
2
1
0
```

## 機械的に見つけ出す

`go vet` を使う。

```console
$ go vet
# _/your/path/
./main.go:19:16: loop variable v captured by func literal
```

「ループ変数にキャプチャされているよ」と `go vet` が教えてくれた。ループ変数にキャプチャされていると、無名関数が実行されたとき(goroutineがスケジュールされたとき)にループ変数の値を読みに行ってしまう。goroutineがいつスケジュールされるか未定であるから、出力される数字も未定になってしまう。

ということで、ループ変数をキャプチャしないように引数を渡してやれば解消する。

> Note that the tool does not check every possible problem and depends on unreliable heuristics, so it should be used as guidance only, not as a firm indicator of program correctness.

https://golang.org/cmd/vet/

公式ドキュメントから和訳すると、「vet コマンドは問題になりえそうなものを発見してくれるが、それが必ず問題であるわけではない。ガイダンスとして利用すること」ということ。

今回のケースでは機械的に問題を発見できた。
