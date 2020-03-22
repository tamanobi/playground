package main

import (
	"context"
	"fmt"
	"time"
)

// heavyFunc はキャンセル可能な長時間かかる処理
func heavyFunc(cancel <-chan struct{}) {
	ch := make(chan string)
	go func() {
		defer close(ch)
		time.Sleep(1000 * time.Millisecond)
		ch <- "終わったよ"
	}()

	select {
	case message := <-ch:
		fmt.Println("heavyFunc is done")
		fmt.Println(message)
	case <-cancel:
		fmt.Println("heavyFunc is cancelled")
		return
	}
}

func something(ctx context.Context) error {
	ch := make(chan struct{})
	go heavyFunc(ch)

	select {
	case <-ctx.Done():
		fmt.Println("context is done.")
		close(ch)
		return ctx.Err()
	}
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	something(ctx)
	time.Sleep(5 * time.Second)
}
