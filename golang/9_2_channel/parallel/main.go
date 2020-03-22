package main

import (
	"fmt"
	"sync"
	"time"
)

// Job は自らの識別子をもったRunメソッドを持った存在
type Job struct {
	n int
}

// Run は1秒程度時間を要する処理を実行するメソッド
func (j Job) Run() {
	fmt.Printf("start %d job\n", j.n)
	time.Sleep(1 * time.Second)
	fmt.Printf(" - end %d job\n", j.n)
}

// parallel は並列数を指定してJobを並列処理する
func parallel(n int, jobs []Job) {
	wg := &sync.WaitGroup{}
	sem := make(chan struct{}, n)
	for _, j := range jobs {
		sem <- struct{}{}
		wg.Add(1)
		go func(job Job) {
			job.Run()
			<-sem
			wg.Done()
		}(j)
	}
	wg.Wait()
}

func main() {
	jobs := make([]Job, 10)
	for i := range jobs {
		jobs[i] = Job{n: i}
	}

	parallel(2, jobs)
}
