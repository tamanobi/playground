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
