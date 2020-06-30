// csvInfoTest.go
package main

import (
	"fmt"
	"qprob"
)

func main() {
	fmt.Println("csvInfoTest.go")
	md := qprob.LoadCSVMetaDataFile("../data/breast-cancer-wisconsin.adj.data.csv")
	fmt.Println("constructor complete")
	fmt.Println(md.String())
	md.BuildDistMatrixFile()
	fmt.Println("\nfinished build distrib matrix")

}
