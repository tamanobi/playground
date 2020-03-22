package main

import (
	"context"
	"fmt"
	"time"
)

// heavyFunc はキャンセル可能な長時間かかる処理
func heavyFunc(ch <-chan struct{}) {
	select {
	case <-time.After(3 * time.Second):
		fmt.Println("heavyFunc is done")
	case <-ch:
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
		ch <- struct{}{}
		return ctx.Err()
	}
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	something(ctx)
	time.Sleep(5 * time.Second)
}
