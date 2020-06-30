package main

import (
	"fmt"
	"os"
	"qprob"
)

func main() {
	fmt.Println("classifyFiles.go ")
	req := qprob.ParseClassifyFileCommandParms(os.Args)
	fmt.Printf("parsed commands %s\n", req.ToJSON())

	if req.OkToRun {
		fmt.Println("start ClassifyTestFiles()")
		qprob.ClassifyTestFiles(req)
		fmt.Println("Finished ClassifyTestFiles()")
	} else {
		fmt.Println("Can not run problem with input parms")
	}
}
