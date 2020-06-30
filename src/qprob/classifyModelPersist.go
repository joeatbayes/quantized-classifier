// classifyModelPersist.go
package qprob

import (
	"bufio"
	"fmt"
	//iou "io/ioutil"
	"os"
)

//
// Saves a file in JSON format that contains sufficient data to
// reload the model without having to re-process the training
// data.    Most of the critical data comes from LoadModel but
// a few things like maxNumBuck for all of the Fier do not exist
// in that data so must be loaded from the rest of the system.
//func (fier *Classifier) SaveRestorableModel(fiName string) bool {
//}

// Trim model Memory
//  Used to remove bucket computations for a given feature
//  where numBuck is above or below maxNum Buck for that
/// tree.

// Retore in memory model by reading state from file without
// needing to re-read the training data.
//func (fier *Classifier) LoadModel(fiName string) {
//	}

// Saves the statisitics model in a CSV to allow secondary
// analysis.
// Format is:
//   featureNdx, NumOfQuant, QuantNum, ClassNum, Count, CntForQuant...etc
func (fier *Classifier) SaveModel(fiName string) bool {
	fi, err := os.Create(fiName)
	check("opening file", err)
	if err != nil {
		fmt.Printf("L24: Error opening %s for write err=%v\n", fiName, err)
		return false
	}
	defer fi.Close()
	wtr := bufio.NewWriter(fi)
	fmt.Fprintf(wtr, "featNdx,colName,numBuck,buckId,classId,classCnt,buckCnt,qlProb,qlLift,valLow,valHigh,classProb\n")
	for numBuck := int16(1); numBuck < fier.MaxNumBuck; numBuck += 1 {
		for featNdx, feat := range fier.ColDef {
			buckMap := feat.Buckets[numBuck]
			MinNumBuck := feat.MinNumBuck
			MaxNumBuck := feat.MaxNumBuck
			if feat.IsCategory {
				MinNumBuck = 1
				MaxNumBuck = 1
			}
			if numBuck >= MinNumBuck && numBuck <= MaxNumBuck {
				for buckId, qlist := range buckMap {
					valLow, valHigh := feat.BuckValRange(fier, buckId, numBuck)
					valLowStr := ""
					valHighStr := ""
					if feat.IsCategory {
						tmpval, fnd := feat.CatNdxById[buckId]
						if fnd == false {
							valLowStr = "err"
							valHighStr = "err"
						} else {
							valLowStr = tmpval
							valHighStr = valLowStr
						}
					} else {
						valLowStr = Float32ToString(valLow, 5)
						valHighStr = Float32ToString(valHigh, 5)
					}
					for classId, classCnt := range qlist.Counts {
						classProb := float32(classCnt) / float32(qlist.totCnt)
						lift := classProb - fier.ClassProb[classId]

						fmt.Fprintf(wtr, "%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v\n",
							featNdx, feat.Spec.ColName, numBuck, buckId, classId,
							classCnt, qlist.totCnt, classProb, lift, valLowStr, valHighStr, fier.ClassProb[classId])
					} // end for class
				} // end for buck
			} // if feature in range
		} // for feat
	} // end for num Buck
	wtr.Flush()
	return true

} // end func

func testModelLoad() {

}

func testModelSave() {
	fmt.Println("Hello World!")
}
