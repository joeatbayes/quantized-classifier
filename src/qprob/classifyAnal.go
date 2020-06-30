package qprob

// classifyAnal.go

import (
	"encoding/json"
	"fmt"
	iou "io/ioutil"
	"qutil"
	"sort"
)

const AnalNoClassSpecified = TClassId(-9999)

// Structures to report on results
// and make them easy to analyze
// Some of these are also used
// by the optimizer.   Not to be confused
// with ResultForRow which contains
// more detail such as probability for
// membership in each class.
type testRowRes struct {
	rowNum    int32
	actClass  TClassId
	predClass TClassId
}

type testRes struct {
	rows        []testRowRes
	cntRow      int32
	cntCorrect  int32
	percCorrect float32
}

func TestClassifyAnal() {
	fmt.Println("Hello World!")
}

/*
// Function Create Summary Results
func (fier *Classifier) createSummaryResults(astr string) *summaryResult {
	// NOTE: Some of this code already exists in ClassifyFiles
	return nil
}

func (sumRes *summaryResult) ToSimpleRowCSV(fier *Classifier) string {
	return ""

}


// function to build statistics by class
// from a given result set.


*/

type AnalResByFeat struct {
	FeatNdx    int
	FeatWeight float32 // assigned by
	ColName    string
	MinNumBuck int16
	MaxNumBuck int16
	EffMinVal  float32
	EffMaxVal  float32
	TotCnt     int32
	SucCnt     int32
	Prec       float32
	TargClass  TClassId
	TargPrec   float32
	ByClasses  map[TClassId]ResByClass
}

type AnalResults struct {
	Cols   []AnalResByFeat
	TotCnt int32
	SucCnt int32
	Prec   float32
}

func makeAnalResults(numCol int) *AnalResults {
	tout := new(AnalResults)
	tout.Cols = make([]AnalResByFeat, numCol)
	for tndx := 0; tndx < numCol; tndx++ {
		tout.Cols[tndx].ByClasses = make(map[TClassId]ResByClass)
		tout.Cols[tndx].FeatWeight = 1
		tout.Cols[tndx].FeatNdx = -1
	}
	return tout
}

// Sort Feature Set By precision of Chosen class
type srtAnalResByFeatSpecClass []AnalResByFeat

func (v srtAnalResByFeatSpecClass) Len() int {
	return len(v)
}

func (v srtAnalResByFeatSpecClass) Swap(i, j int) {
	v[i], v[j] = v[j], v[i]
}

func (v srtAnalResByFeatSpecClass) Less(i, j int) bool {
	if v[i].FeatNdx == -1 {
		return false
	}
	// Priority 1 = precision
	//   tie-break = SucCnt
	//     ti-break = total feature precision
	//        ti-break = featNdx
	if v[i].TargPrec == v[j].TargPrec {
		if v[i].SucCnt == v[j].SucCnt {
			if v[i].Prec == v[j].Prec {
				return v[i].FeatNdx > v[j].FeatNdx
			}
			return v[i].Prec > v[j].Prec
		}
		return v[i].SucCnt > v[j].SucCnt
	}
	return v[i].TargPrec > v[j].TargPrec
}

// Sort Feature Set By precision of Total Set
type srtAnalResByFeat []AnalResByFeat

func (v srtAnalResByFeat) Len() int {
	return len(v)
}

func (v srtAnalResByFeat) Swap(i, j int) {
	v[i], v[j] = v[j], v[i]
}

func (v srtAnalResByFeat) Less(i, j int) bool {
	if v[i].FeatNdx == -1 {
		return false
	}
	if v[i].Prec == v[j].Prec {
		return v[i].FeatNdx > v[j].FeatNdx
	}
	return v[i].Prec > v[j].Prec
}

//If targClass is != AnalNoClassSpecified then the results
// for that class will be used as the driving input where
// as long as precision is >= targPrecision then increasing
// recall is chosen otherwise increasing precision is chosen.
// when targClass == AnalNoClassSpecified then increasing precision for entire
// data set is chosen.   This is used to pre-set the maxNumBuck
// for each column. In some instances it could be used to set
// MinNumBuck as well becaause if we know that a low number such
// as 2 yeidls poor results for a given class we do not want to
// allow the results module to fall back to those lower numbers
func (fier *Classifier) TestColumnNumBuck(targClass int16, targPrecis float32, trainRow [][]float32, testRow [][]float32) []*AnalResults {
	return nil
}

// Loads the saved analysis input and uses those values
// to override the default minNumBuck,  MaxNumBuck, featWeight
// for each column.
func (fier *Classifier) LoadSavedAnal(fiName string) {
	fmt.Printf("L108: Attempt Load Saved Analysis settings from %s\n", fiName)
	ba, err := iou.ReadFile(fiName)
	if err != nil {
		fmt.Printf("L105: LoadSavedAnal() Error Reading %s  err=%v \n", fiName, err)
	} else {
		tobj := AnalResults{}
		if err := json.Unmarshal(ba, &tobj); err != nil {
			fmt.Printf("L111: LoadSavedAnal() Error JSON Parsing from %s err=%v\n", fiName, err)
		} else {
			// Copy our important values from the saved set back into the
			// classifier so it can use them to adjust it's classificaiton
			// results.

			// WARN:   The MaxBuck used when the saved values are generated
			//   must be the same or smaller as the MaxBuck used in this run
			//   or a index error will occur.  The number of features in the
			//   training file must be identical to those used when the
			//   saved settings were generated.
			// fmt.Printf("L112 tobj=%v\n", tobj)

			for _, acol := range tobj.Cols {
				featndx := acol.FeatNdx
				if featndx != fier.ClassCol && featndx != -1 {
					feat := fier.ColDef[featndx]
					if acol.MaxNumBuck > feat.MaxNumBuck {
						feat.MaxNumBuck = acol.MaxNumBuck
						feat.initializeBuckets()
					}
					feat.MinNumBuck = acol.MinNumBuck
					feat.FeatWeight = acol.FeatWeight
					fmt.Printf("L182 Load ndx=%v, name=%v  MinNB=%v MaxNB=%v weight=%v\n",
						featndx, feat.Spec.ColName, feat.MinNumBuck, feat.MaxNumBuck, feat.FeatWeight)
				}
			}
		}
	}
}

func sortColumnsByPrecision(col []AnalResByFeat) {

}

func setFeatWeightByOrderedPrecision(col []AnalResByFeat) {

}

func (fier *Classifier) DoPreAnalyze(analFiName string) {
	req := fier.Req

	// Pre-analyze each column to try and find the sweet spot
	// for precision and recall as number of buckets.
	origTrainRows := fier.GetTrainRowsAsArr(OneGig)
	testRows := origTrainRows
	trainRows := origTrainRows
	if req.AnalTestPort == 100 {
		fmt.Printf("L139: DoPreAnalyze() Use entire training set as test numRow=%v", len(origTrainRows))
	} else if req.AnalSplitType == 1 {
		// pull test records from the body of test data using 1 row every
		// so often.   Nice to get a good sampling of data that is not
		// time series.
		oneEvery := int(float32(len(origTrainRows)) / (float32(len(origTrainRows)) * req.AnalTestPort))
		fmt.Printf("Analyze SplitOneEvery=%v  portSet=%v\n", oneEvery, req.AnalTestPort)
		trainRows, testRows = qutil.SplitFloatArrOneEvery(origTrainRows, 1, oneEvery)
	} else {
		// pull records from end of test data.  Best for
		// time series when predicting on records near the end
		fmt.Printf("Analyze splitEnd PortSet=%v", req.AnalTestPort)
		trainRows, testRows = qutil.SplitFloatArrTail(origTrainRows, req.AnalTestPort)
	}
	_, sumRows := fier.ClassifyRows(testRows, fier.ColDef)

	// Have to retrain based on the newly split data
	fmt.Printf("L215: Analyze #TrainRow=%v #TestRow=%v analFiName=%v\n", len(trainRows), len(testRows), analFiName)
	fier.Retrain(trainRows)
	anaRes := fier.TestIndividualColumnsNB(AnalNoClassSpecified, -1.0, trainRows, testRows)
	jsonRes, err := json.Marshal(anaRes)
	if err != nil {
		fmt.Printf("L220: Error converting analyze res to JSON err=%v  analRes=%v\n", err, anaRes)
	} else {
		//fmt.Printf("L222: Analysis Results=\n%s\n", jsonRes)
		barr := []byte(jsonRes)
		fmt.Printf("L256: write %v bytes to %v\n", len(barr), analFiName)
		err := iou.WriteFile(analFiName, barr, 0666)
		if err != nil {
			fmt.Printf("L92: Error writting analyzis output file %s err=%v\n", analFiName, err)
		}
	}

	if req.AnalTestPort != 100 {
		// Rerun the classificaiton using all our columns but with the new
		// bucket and weights for each column
		fier.Retrain(origTrainRows)
		_, sumRows = fier.ClassifyRows(testRows, fier.ColDef)
		fmt.Printf("L178: DoPreAnalyze() Precision with all columns = %v\n  Based on training data\n", sumRows.Precis)

	}
}

// TODO: Add the Save Feature
// TODO: Add a human legible save feature
// TODO: Add ability to sort the list of featurs by precision
// TODO: Convert the analysis result structure to direct storage to allow JSON conversion.
// TODO: Need a smaller JSON structure that is just enough to reload latter classification runs.
// TODO: We should take the highest precision feature and give it a weight
//    value of that is high then assign each lower precision value
//    a lower weight.
// TODO: Need human editable stucture to turn feature columns off.

// Analyze inidividual columns predictive power.  This can help identify
// columns that have better predictive input.  It can also help
// identify columns with low predictive input so they can be
// removed from the dataset.
//
// Runs each feature independantly by the number of buckets
// seeking the number of columns for this feature that return
// the best results.
func (fier *Classifier) TestIndividualColumnsNB(targClass TClassId, targPrecis float32, trainRows [][]string, testRows [][]string) *AnalResults {
	// Question how do you quantify better.  If Precision is high
	// but recall is very low then which is better.  Seems like you
	// must set one as a minimum value and alllow the others to
	// vary.
	req := fier.Req
	featSet := make([]*Feature, 1)
	specClass := req.AnalClassId
	if specClass != AnalNoClassSpecified {
		fmt.Printf("Analyze for ClassId=%v\n", specClass)
	} else {
		fmt.Printf("Analyze for Total Set\n")
	}

	numCol := len(fier.ColDef)
	tout := makeAnalResults(numCol)

	//fmt.Printf("L108:trainRows=%v\n", trainRows)
	//fmt.Printf("L100: testRows=%v\n", testRows)

	for _, feat := range fier.ColDef {
		featNum := feat.ColNum
		if featNum == fier.ClassCol || feat.Enabled == false {
			continue
		}
		startMaxNumBuck := feat.MaxNumBuck
		startMinNumBuck := feat.MinNumBuck
		featSet[0] = feat
		//featSet = fier.ColDef // see if changing individual feature changes entire set score

		_, sumRows := fier.ClassifyRows(testRows, featSet)
		//detRow, sumRows := fier.ClassifyRows(testRows, featSet)
		//fmt.Printf("L122: detRow=%v\n", detRow)
		//fmt.Printf("L123: sumRows=%s\n", sumRows.ToDispStr())
		startMaxPrec := sumRows.Precis
		startMaxRecall := float32(0.0)
		bestMaxPrecis := sumRows.Precis
		bestMaxBuck := startMaxNumBuck
		bestMaxRecall := startMaxRecall
		if specClass != AnalNoClassSpecified {
			clasSum := fier.MakeByClassStats(sumRows, testRows)
			tclass := clasSum.ByClass[specClass]
			//fmt.Printf("L113: Init by class tclass=%v\n", tclass)
			startMaxRecall = tclass.Recall
			startMaxPrec = tclass.Prec
			bestMaxRecall = tclass.Recall
			bestMaxPrecis = tclass.Prec
		}

		//fmt.Printf("L102: featNum=%v StartPrecis=%v startMaxNB=%v startMinNB=%v\n", featNum, startMaxPrec, startMaxNumBuck, startMinNumBuck)
		//fmt.Printf("specClass=%v AnalNoClassSpecified=%v\n", specClass, AnalNoClassSpecified)

		for maxNumBuck := feat.MaxNumBuck; maxNumBuck >= fier.Req.MinNumBuck; maxNumBuck-- {
			feat.MaxNumBuck = maxNumBuck
			_, sumRows := fier.ClassifyRows(testRows, featSet)
			//fmt.Printf("L120: sumRows=%s\n", sumRows.ToDispStr())
			//fmt.Printf("L115: fe#=%v maxNB=%v setPrec=%v bMaxPrec=%v bMaxRec=%v bestNb=%v\n", featNum, maxNumBuck, sumRows.Precis, bestMaxPrecis, bestMaxRecall, bestMaxBuck)
			if req.AnalClassId == AnalNoClassSpecified {
				if sumRows.Precis >= bestMaxPrecis {
					// measure by accuracy when all rows are forced
					// to be classified eg: recall is forced to 100%
					// for the set by forcing the classifier to take
					// it's best guess for every row.
					bestMaxBuck = maxNumBuck
					bestMaxPrecis = sumRows.Precis
				}
			} else {
				// measure by target class or by set

				clasSum := fier.MakeByClassStats(sumRows, testRows)
				tclass := clasSum.ByClass[specClass]
				//fmt.Printf("L137: test by class tclass=%v\n", tclass)
				if (tclass.Prec >= bestMaxPrecis && tclass.Recall >= bestMaxRecall) || (tclass.Prec >= bestMaxPrecis && tclass.Recall > bestMaxRecall) {
					bestMaxRecall = tclass.Recall
					bestMaxPrecis = tclass.Prec
					bestMaxBuck = maxNumBuck
				}
			}

		} // for maxNumBuck
		feat.MaxNumBuck = bestMaxBuck

		//fmt.Printf("L133: BEST MAX featNdx=%v  numBuck=%v Precis=%v\n", featNum, bestMaxBuck, bestMaxPrecis)
		//_, sumRows = fier.ClassifyRows(testRows, featSet)
		//fmt.Printf("L135: Retest with max  prec=%v\n", sumRows.Precis)

		// Now tighen  the minimum number of buckets to find our best setting
		bestMinBuck := startMinNumBuck
		bestMinPrecis := startMaxPrec
		bestMinRecall := startMaxRecall

		for minNumBuck := startMinNumBuck; minNumBuck <= feat.MaxNumBuck; minNumBuck++ {
			feat.MinNumBuck = minNumBuck
			_, sumRows := fier.ClassifyRows(testRows, featSet)

			//fmt.Printf("L145: fe#=%v minNB=%v SPrec=%v Bprec=%v BRecal=%v bNB=%v\n", featNum, minNumBuck, sumRows.Precis, bestMinPrecis, bestMinRecall, bestMinBuck)
			if req.AnalClassId == AnalNoClassSpecified {
				if sumRows.Precis >= bestMinPrecis {
					// measure by accuracy when all rows are forced
					// to be classified eg: recall is forced to 100%
					// for the set by forcing the classifier to take
					// it's best guess for every row.
					bestMinBuck = minNumBuck
					bestMinPrecis = sumRows.Precis
				}
			} else {
				// measure by target class or by set
				clasSum := fier.MakeByClassStats(sumRows, testRows)
				tclass := clasSum.ByClass[specClass]
				//fmt.Printf("L137: test by class tclass=%v\n", tclass)
				if (tclass.Prec > bestMinPrecis && tclass.Recall >= bestMinRecall) || (tclass.Prec >= bestMinPrecis && tclass.Recall > bestMinRecall) {
					bestMinRecall = tclass.Recall
					bestMinPrecis = tclass.Prec
					bestMinBuck = minNumBuck
				}
			}

		} // for minNumBuck
		feat.MinNumBuck = bestMinBuck
		_, sumRows = fier.ClassifyRows(testRows, featSet)
		//fmt.Printf("L163:MIN fe#=%v BMinNB=%v BPrec=%v retestPre%v\n", featNum, bestMinBuck, bestMinPrecis, sumRows.Precis)

		// TODO: Add complete printout of what we discovered by Feature
		fmt.Printf("L158: After Analyze ColNum=%v colName=%v\n   startPrecis=%v endPrecis=%v\n",
			feat.ColNum, feat.Spec.ColName, startMaxPrec, bestMinPrecis)

		if req.AnalClassId != AnalNoClassSpecified {
			fmt.Printf("   startRecall=%v endRecall=%v\n", startMaxRecall, bestMinRecall)
		}

		fmt.Printf("   startMaxNumBuck=%v endMaxNumBuck=%v\n   startMinNumBuck=%v  endMinNumBuck=%v\n",
			startMaxNumBuck, bestMaxBuck, startMinNumBuck, bestMinBuck)

		// Update output structure
		clasSum := fier.MakeByClassStats(sumRows, testRows)

		targPrec := float32(0.0)
		for classId, aclass := range clasSum.ByClass {
			tout.Cols[featNum].ByClasses[classId] = *aclass
			if aclass.ClassId == req.AnalClassId {
				targPrec = aclass.Prec
			}
		}
		col := &tout.Cols[featNum]
		col.FeatNdx = feat.ColNum
		col.ColName = feat.Spec.ColName
		col.EffMinVal = feat.EffMinVal
		col.EffMaxVal = feat.EffMaxVal
		col.MinNumBuck = bestMinBuck
		col.MaxNumBuck = bestMaxBuck
		col.TotCnt = sumRows.TotCnt
		col.SucCnt = sumRows.SucCnt
		col.Prec = sumRows.Precis
		col.TargPrec = targPrec
		col.TargClass = req.AnalClassId

	} // for features

	// Update out output structure for enire set.
	_, sumRows := fier.ClassifyRows(testRows, fier.ColDef)
	tout.Prec = sumRows.Precis
	tout.SucCnt = sumRows.SucCnt
	tout.TotCnt = sumRows.TotCnt
	if req.AnalClassId != AnalNoClassSpecified {
		// Sort features by total precision
		sort.Sort(srtAnalResByFeatSpecClass(tout.Cols))
	} else {
		// Sort Features based on Specified Class
		// performance.
		sort.Sort(srtAnalResByFeat(tout.Cols))
	}

	// Adjust the feature weights to the most
	// beneficial feature to reflect the feature
	// that provides highest predictive value.
	if req.AnalAdjFeatWeight == true {
		currWeight := float32(10.0)
		for tndx, acol := range tout.Cols {
			if acol.FeatNdx != -1 {
				feat := fier.ColDef[acol.FeatNdx]
				if feat.Enabled == true {
					tout.Cols[tndx].FeatWeight = currWeight // have to assign it directly because we are working with a copy
					feat.FeatWeight = currWeight
					currWeight = currWeight * 0.8
					fmt.Printf("L450: featNdx=%v name=%v MinNumBuck=%v maxNumBuck=%v featWeight=%v\n",
						feat.ColNum, feat.Spec.ColName, feat.MinNumBuck, feat.MaxNumBuck, feat.FeatWeight)
				}
			}
		}
	}

	fmt.Printf("L274: After analyze setPrec all Feat enabled = %v\n", sumRows.Precis)

	return tout
}
