package main

import (
	"fmt"
)

func main() {
	ch1, ch2 := make(chan int), make(chan int)
	go func() { ch1 <- 1; close(ch1) }()
	go func() { ch2 <- 2; close(ch2) }()

	for {
		select {
		case v1, ok := <-ch1:
			if !ok {
				return
			}
			fmt.Println(v1)
		case v2, ok := <-ch2:
			if !ok {
				return
			}
			fmt.Println(v2)
		}
	}
}
