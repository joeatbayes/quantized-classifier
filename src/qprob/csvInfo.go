package qprob

/*  Reads CSV Files line by line attempting
to find min,max values for every column and
to determine how each column can be parsed.
it also builds a distribution rank showing
how records are distributed across 1,000
evenly sized buckes for each colums so we can
use those to detect and filter outliers in
subsequent statistical functions.

we process line by line even though we will be
required to eread the file multile times
because some of the CSV files are larger than
available memory.  Pass-1 computes absolute
min,max values and detects columns that are
parsable as float or int.  Pass-2 builds the
distribution rank.    Pass-3 is when actual
data values will be used.
*/

import (
	"bufio"
	"bytes"
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	s "strings"
)

// CSVColInf information describing A CSV Column
type CSVCol struct {
	ColNum        int
	ColName       string
	IsInt         bool
	CanParseFloat bool
	MaxStr        string
	MinStr        string
	MaxFlt        float32
	MinFlt        float32
	AbsRange      float32
	distStepSize  float32
	distCounts    [1000]int
}

//CSVInfo information describing a CSV table
// This data is needed by other modules that
// may modify values based on contents discovered
// in the CSV data.
type CSVInfo struct {
	FiName string // name of file read
	NumCol int    // number of columns processed
	NumRow int    // number of rows
	//Col    map[int]*CSVCol  // Index of colums by column Num
	Col    []*CSVCol          // Index of colums by column Num
	ByName map[string]*CSVCol // Index of columns by Name
}

func LoadCSVMetaDataFile(fiName string) *CSVInfo {
	fmt.Printf("fiName=%s", fiName)
	file, err := os.Open(fiName)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	// Return the Header and use it's
	// contents to create the columns
	scanner := bufio.NewScanner(file)
	cc := LoadCSVMetaData(scanner)
	cc.FiName = fiName
	return cc
}

// A set of classifiers indexed by
// name to allow a single process
// to serve data from multiple training
// data sets
func LoadCSVMetaData(scanner *bufio.Scanner) *CSVInfo {

	// Return the Header and use it's
	// contents to create the columns
	scanner.Scan()
	headStr := scanner.Text()
	//fmt.Printf("headStr=%s", headStr)
	heada := s.Split(headStr, ",")
	numCol := len(heada)
	tout := &CSVInfo{
		FiName: "",
		NumRow: 0,
		NumCol: len(heada),
		Col:    make([]*CSVCol, numCol),
		ByName: make(map[string]*CSVCol)}

	for i := 0; i < numCol; i++ {
		colName := s.TrimSpace(heada[i])
		tout.Col[i] = &CSVCol{
			ColNum:        i,
			ColName:       colName,
			IsInt:         true,
			CanParseFloat: true,
			MaxStr:        "",
			MinStr:        "ZZ",
			MaxFlt:        0.0 - math.MaxFloat32,
			MinFlt:        math.MaxFloat32}
	} // for

	// parse the CSV Rows to get min, max values
	for scanner.Scan() {
		txt := s.TrimSpace(scanner.Text())
		if err := scanner.Err(); err != nil {
			log.Fatal(err)
		}
		a := s.Split(txt, ",")
		if len(a) < tout.NumCol {
			continue
		}
		tout.NumRow++
		for i := 0; i < numCol; i++ {
			col := tout.Col[i]
			ctxt := a[i]
			// Record Min, Max string
			if ctxt > col.MaxStr {
				col.MaxStr = ctxt
			} else if ctxt < col.MinStr {
				col.MinStr = ctxt
			}

			// Record Min, Max Float
			f64, err := strconv.ParseFloat(ctxt, 32)
			f32 := float32(f64)
			if err != nil {
				col.CanParseFloat = false
			} else {
				col.MinFlt = MinF32(f32, col.MinFlt)
				col.MaxFlt = MaxF32(f32, col.MaxFlt)
				// Record Min, Max Int Encountered
				x64, x64err := strconv.ParseInt(ctxt, 10, 32)
				if x64err != nil || (float64(x64) != f64) {
					col.IsInt = false
				}
			}
			//fmt.Printf("i=%v ctxt=%s f32=%v maxStr=%s minStr=%s\n", i, ctxt, f32, col.MaxStr, col.MinStr)
		} // for columns
	} // for row

	// Finish up basic numeric range
	// and step size for basic values
	for x := 0; x < tout.NumCol; x++ {
		col := tout.Col[x]
		col.AbsRange = col.MaxFlt - col.MinFlt
		col.distStepSize = col.AbsRange / 1001
	}
	return tout
}

// Compute Bucket Id for a given value
// based on the absRange and number of
// values.  All values must be coerced
// into 1 of 1000 discrete buckets of
// even size.
func (cc *CSVCol) buckId(vin float32) int16 {
	tout := int16((vin - cc.MinFlt) / cc.distStepSize)
	if tout > 999 {
		//fmt.Printf("buckId overeflow vin=%v tout=%v minFlt=%v maxFlt=%v stepSize=%v\n",
		//	vin, tout, cc.MinFlt, cc.MaxFlt, cc.distStepSize)
		tout = 999
	} else if tout < 0 {
		//fmt.Printf("buckId underflow vin=%v tout=%v minFlt=%v maxFlt=%v stepSize=%v\n",
		//	vin, tout, cc.MinFlt, cc.MaxFlt, cc.distStepSize)
		tout = 0
	}
	return tout
}

// Helper method to create the stream used to build
// the matrix.
func (cv *CSVInfo) BuildDistMatrixFile() {
	fmt.Printf("BuildDistMatrix() fiName=%s", cv.FiName)

	file, err := os.Open(cv.FiName)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Scan() // skip header
	// parse the CSV Rows to get min, max values
	cv.BuildDistMatrix(scanner)
}

/* Build a 1,000 bucket distribution marix
with counts of inidents with the values
spread across a matrix of 1,000 buckets
or if integer range less than 1,000 will
have that many buckets.  This is used
to allow us to identify outlier values
as a portion of the set so we can remove
them from the typical distribution range
when quantizign latter. */
func (cv *CSVInfo) BuildDistMatrix(scanner *bufio.Scanner) {
	fmt.Printf("BuildDistMatrix() fiName=%s", cv.FiName)
	for scanner.Scan() {
		txt := s.TrimSpace(scanner.Text())
		if err := scanner.Err(); err != nil {
			log.Fatal(err)
		}
		a := s.Split(txt, ",")
		if len(a) < cv.NumCol {
			continue
		}
		for i := 0; i < cv.NumCol; i++ {
			col := cv.Col[i]
			ctxt := a[i]
			f64, err := strconv.ParseFloat(ctxt, 32)
			if err == nil {
				f32 := float32(f64)
				buckId := col.buckId(f32)
				//fmt.Printf("buckid=%v\n", buckId)
				col.distCounts[buckId] += 1
				//fmt.Printf("i=%v f32=%v buckId=%v cnt=%v \n",
				//	i, f32, buckId, col.distCounts[buckId])
			}
		}
	} // for row
} // func

func (cc *CSVCol) String() string {
	var b bytes.Buffer
	fmt.Fprintf(&b, "ColNum=%v ColName=%s IsInt=%v CanParseFloat=%v ",
		cc.ColNum, cc.ColName, cc.IsInt, cc.CanParseFloat)
	fmt.Fprintf(&b, " MinStr=%v minStr=%s MaxFlt=%v MinFlt=%v",
		cc.MaxStr, cc.MinStr, cc.MaxFlt, cc.MinFlt)

	fmt.Fprintf(&b, " AbsRange=%v distStepSize=%v",
		cc.AbsRange, cc.distStepSize)

	return b.String()
}

func (cc *CSVInfo) String() string {
	var b bytes.Buffer

	fmt.Fprintf(&b, "CSVInfo FiName=%s NumCol=%v NumRow=%v\n",
		cc.FiName, cc.NumCol, cc.NumRow)
	for _, col := range cc.Col {
		fmt.Fprintf(&b, "  %s\n", col.String())
	}
	return b.String()
}
