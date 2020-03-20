package main

import "fmt"

type Hex int

func (h Hex) String() string {
	return fmt.Sprintf("%x", int(h))
}

func (h Hex) Twice1() int {
	h *= 2
	return int(h)
}

func (h *Hex) Twice2() int {
	v := Hex(2 * int(*h))
	*h = v
	return int(*h)
}

func main() {
	var hex Hex = 100
	fmt.Println(hex.String())

	var hex1, hex2 Hex = 100, 100
	hex1.Twice1()
	fmt.Println(hex1.String())
	hex2.Twice2()
	fmt.Println(hex2.String())
}
