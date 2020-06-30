// csvInfoTest.go
package main

import (
	js "encoding/json"
	"fmt"
	"qprob"
)

func main() {
	fmt.Println("classifyTest.go")

	fmt.Println("Test for Breast Cancer")
	breastCancerFiName := "../data/breast-cancer-wisconsin.adj.data.csv"
	numBuck := int16(8)

	fier := qprob.LoadClassifierTrainFile(breastCancerFiName, "bcancer", numBuck)
	fmt.Println("constructor complete")
	//fmt.Println(fier.String())

	fmt.Println("\nfinished build Now Try to classify")

	testStr := "4, 5, 4, 4, 9, 2, 10, 5, 6, 10"
	fmt.Printf("testStr=%v\n", testStr)
	cres := fier.ClassRowStr(testStr)
	//fmt.Printf("classRow=%v\n", cres)
	//fmt.Printf("Classes = %v", cres)
	tjson, _ := js.Marshal(&cres)
	fmt.Printf("\nASJSON=%s\n", string(tjson))
}
