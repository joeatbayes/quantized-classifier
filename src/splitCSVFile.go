package main

/* splitCSVFile.go  - Split a CSV file into two separate files
one which contains training data and another which contains
test data */
import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	s "strings"
)

func check(msg string, e error) {
	if e != nil {
		panic(e)
	}
}

func printLn(f *os.File, txt string) {
	_, err1 := f.WriteString(txt)
	check("err in printLn ", err1)

	_, err2 := f.WriteString("\n")
	check("err in printLn ", err2)
}

/* Reads lines out of a CSV file extracting
one line every trainEvery to save in a test file
both files end up with the CSV header */
func SplitFileOnEvery(testEvery int, inFiName string, outTrainName string, outTestName string) {
	fiIn, err := os.Open(inFiName)
	check("opening file", err)
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(fiIn)
	defer fiIn.Close()

	ftrain, err := os.Create(outTrainName)
	check("open training file", err)
	defer ftrain.Close()

	ftest, err := os.Create(outTestName)
	check("open test file", err)
	defer ftest.Close()

	// Copy of header to both files
	scanner.Scan() // skip headers
	headTxt := s.TrimSpace(scanner.Text())
	printLn(ftrain, headTxt)
	printLn(ftest, headTxt)

	// Copy the rows.
	sinceTest := 0
	rowCnt := 0
	allTest := 0
	for scanner.Scan() {
		txt := s.TrimSpace(scanner.Text())
		if err := scanner.Err(); err != nil {
			log.Fatal(err)
		}
		if sinceTest >= testEvery {
			printLn(ftest, txt)
			sinceTest = 0
			allTest += 1
		} else {
			printLn(ftrain, txt)
		}
		sinceTest += 1
		rowCnt += 1
	} // for row
	fmt.Printf("input=%v numRow=%v allTest=%v\n", inFiName, rowCnt, allTest)
}

func printHelp() {
	fmt.Println("eg: splitCSVFile ../data/titanic.csv 50")
	fmt.Println("will read the file ../data/titanic.csv creating ")
	fmt.Println("data/titanic.train.csv and data/titanic.test.csv")
	fmt.Println("copying one out of ever 50 lines to the test file")
	fmt.Println("instead of the training file")
	fmt.Printf("args = %v\n", os.Args)
}

func main() {
	fmt.Println("splitCSVFile.go inFiName TrestEvery")
	if len(os.Args) != 3 {
		fmt.Println("ERROR: Incorrect number of command args")
		printHelp()
		return
	}

	fInName := s.TrimSpace(os.Args[1])
	if _, err := os.Stat(fInName); os.IsNotExist(err) {
		fmt.Printf("ERROR: file does not exist %s\n", fInName)
		printHelp()
		return
	}

	tmpEvery, err := strconv.ParseInt(os.Args[2], 10, 32)
	if err != nil {
		fmt.Printf("ERROR: parsing tmpEvery valIn=%v\n", os.Args[2])
		printHelp()
		return
	}
	testEvery := int(tmpEvery)

	fTrainName := s.Replace(fInName, ".csv", ".train.csv", 1)
	fTestName := s.Replace(fInName, ".csv", ".test.csv", 1)
	fmt.Printf("fin=%s trainEvery=%d  train=%s test=%s\n",
		fInName, testEvery, fTrainName, fTestName)

	SplitFileOnEvery(testEvery, fInName, fTrainName, fTestName)
}
