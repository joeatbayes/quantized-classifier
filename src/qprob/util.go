package qprob

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	s "strings"
	"time"
)

const OneK = 1024
const OneMeg = OneK * OneK
const OneGig = OneMeg * OneK
const FiveGig = OneGig * 5

func Nowms() float64 {
	nn := time.Now()
	return float64(nn.UnixNano()) / float64(time.Millisecond)
}

func Elap(msg string, beg_time float64, end_time float64) float64 {
	elap := end_time - beg_time
	fmt.Printf("ELAP %s = %12.3f ms\n", msg, elap)
	return elap
}

func check(msg string, e error) {
	if e != nil {
		fmt.Println("ERROR:")
		fmt.Println(e)
		panic(e)
	}
}

func MaxI16(x, y int16) int16 {
	if x > y {
		return x
	} else {
		return y
	}
}

func MinI16(x, y int16) int16 {
	if x < y {
		return x
	} else {
		return y
	}
}

func MaxI32(x, y int32) int32 {
	if x > y {
		return x
	} else {
		return y
	}
}

func MinI32(x, y int32) int32 {
	if x < y {
		return x
	} else {
		return y
	}
}

func MaxF32(x, y float32) float32 {
	if x > y {
		return x
	} else {
		return y
	}
}

func MinF32(x, y float32) float32 {
	if x < y {
		return x
	} else {
		return y
	}
}

func Float32ToString(input_num float32, numDec int) string {
	// to convert a float number to a string
	return strconv.FormatFloat(float64(input_num), 'f', numDec, 64)
}

func Float64ToString(input_num float64, numDec int) string {
	// to convert a float number to a string
	return strconv.FormatFloat(input_num, 'f', 6, 64)
}

func ParseStrAsFloat32(astr string) float32 {
	ctxt := s.TrimSpace(astr)
	x64, err := strconv.ParseFloat(ctxt, 32)
	if err != nil {
		return math.MaxFloat32
	}
	return float32(x64)
}

func ParseStrAsFloat64(astr string) float64 {
	ctxt := s.TrimSpace(astr)
	x64, err := strconv.ParseFloat(ctxt, 64)
	if err != nil {
		return math.MaxFloat64
	}
	return float64(x64)
}

func ParseStrAsInt(astr string) int {
	ctxt := s.TrimSpace(astr)
	x64, err := strconv.ParseInt(ctxt, 10, 64)
	if err != nil {
		return math.MaxInt64
	}
	return int(x64)
}

func ParseStrAsInt16(astr string) int16 {
	ctxt := s.TrimSpace(astr)
	i64, err := strconv.ParseInt(ctxt, 10, 16)
	if err != nil {
		return math.MaxInt16
	}
	return int16(i64)
}

func ParseStrAsInt32(astr string) int32 {
	ctxt := s.TrimSpace(astr)
	i64, err := strconv.ParseInt(ctxt, 10, 32)
	if err != nil {
		return math.MaxInt32
	}
	return int32(i64)
}

func ParseStrAsArrInt32(astr string) []int32 {
	a := s.Split(astr, ",")
	numCol := len(a)
	wrkArr := make([]int32, numCol)
	for fc := 0; fc < numCol; fc++ {
		ctxt := s.TrimSpace(a[fc])
		i64, err := strconv.ParseInt(ctxt, 10, 32)
		i32 := int32(i64)
		if err != nil {
			i32 = math.MaxInt32
		}
		wrkArr[fc] = i32
	}
	return wrkArr
}

/* Any values that failed to parse will contain
math.MaxFloat32 as error indicator */
func ParseStrAsArrFloat(astr string) []float32 {
	a := s.Split(astr, ",")
	numCol := len(a)
	wrkArr := make([]float32, numCol)
	for fc := 0; fc < numCol; fc++ {
		ctxt := s.TrimSpace(a[fc])
		f64, err := strconv.ParseFloat(ctxt, 32)
		f32 := float32(f64)
		if err != nil {
			f32 = math.MaxFloat32
		}
		wrkArr[fc] = f32
	}
	return wrkArr
}

/* Any values that failed to parse will contain
math.MaxFloat32 as error indicator */
func ParseStrAsArrFloat32(astr string) []float32 {
	a := s.Split(astr, ",")
	numCol := len(a)
	wrkArr := make([]float32, numCol)
	for fc := 0; fc < numCol; fc++ {
		//ctxt := s.TrimSpace(a[fc])
		ctxt := a[fc]
		f64, err := strconv.ParseFloat(ctxt, 32)
		f32 := float32(f64)
		if err != nil {
			f32 = math.MaxFloat32
		}
		wrkArr[fc] = f32
	}
	return wrkArr
}

// Return string delimited by comma as array
// of delimited strings with strings trimmed
// from all the tokens.
func ParseStrAsArrStr(astr string) []string {
	a := s.Split(astr, ",")
	numCol := len(a)
	for fc := 0; fc < numCol; fc++ {
		a[fc] = s.TrimSpace(a[fc])
	}
	return a
}

// load CSV rows from file as array of float
// stop when more than maxBytes have been read.
func LoadCSVRows(fiName string, maxBytes int64) (string, [][]float32) {
	rows := make([][]float32, 0, 1)
	fiIn, err := os.Open(fiName)
	check("opening file", err)
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(fiIn)
	defer fiIn.Close()

	// Copy of header to both files
	scanner.Scan() // skip headers
	headTxt := s.TrimSpace(scanner.Text())

	byteCnt := int64(0)
	for scanner.Scan() {
		txt := scanner.Text()
		byteCnt += int64(len(txt))
		if err := scanner.Err(); err != nil {
			log.Fatal(err)
		}

		flds := ParseStrAsArrFloat32(txt)
		rows = append(rows, flds)
		if byteCnt >= maxBytes {
			break
		}
	} // for row
	return headTxt, rows
}

// load CSV rows from file as array of float
// stop when more than maxBytes have been read.
func LoadCSVStrRows(fiName string, maxBytes int64) (string, [][]string) {
	rows := make([][]string, 0, 1)
	fiIn, err := os.Open(fiName)
	check("opening file", err)
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(fiIn)
	defer fiIn.Close()

	// Copy of header to both files
	scanner.Scan() // skip headers
	headTxt := s.TrimSpace(scanner.Text())

	byteCnt := int64(0)
	for scanner.Scan() {
		txt := scanner.Text()
		byteCnt += int64(len(txt))
		if err := scanner.Err(); err != nil {
			log.Fatal(err)
		}

		flds := ParseStrAsArrStr(txt)
		rows = append(rows, flds)
		if byteCnt >= maxBytes {
			break
		}
	} // for row
	return headTxt, rows
}
