package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

func input(r io.Reader) <-chan string {
	c := make(chan string)
	go func() {
		s := bufio.NewScanner(r)
		for s.Scan() {
			c <- s.Text()
		}
		close(c)
	}()
	return c
}

func main() {
	ch := input(os.Stdin)
	for {
		fmt.Print("> ")
		fmt.Println(<-ch)
	}
}
