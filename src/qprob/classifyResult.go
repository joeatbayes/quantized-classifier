// Methods to apply the QProb Classifier for 1..N
// records and return results in a form that can
// easily be consumed by downstream consumers
// such as the optimizer and classifyFiles

// classifyResult.go
package qprob

import (
	"bytes"
	"encoding/json"
	"fmt"
	//"math"
)

// For results look up each feature for the
// row then compute a bucket Id for that  value
// and want to know the count and count and
// probability each class relative to the
// total probability of an item being in that
// bucket.
type ResultItem struct {
	Prob float32
}

// ResultRow is the total set of probabilities
// along with feeding counts for each Row
// Not keeping Result items as pointer because
// we want to be able to feed this direclty
// into JSON formatter.
type ResultForFeat struct {
	Cls    map[TClassId]ResultItem
	TotCnt int32
}

// we want to know the best chosent
// result along with the computed results
// for each feature.   In
// some applications with many classes we
// may need to reduce this.
type ResultForRow struct {
	BestClass TClassId
	BestProb  float32
	ActClass  TClassId // actual class when known -9999 when not known
	Classes   map[TClassId]ResultItem
	Features  []ResultForFeat
}

// Structures to support most basic
// classify save of chosen class and
// basic probability for that choice
type SimpResRow struct {
	BestClass TClassId
	BestProb  float32
	ActClass  TClassId
}

type SimpResults struct {
	TotCnt int32
	SucCnt int32
	Precis float32
	Rows   []SimpResRow
}

type ResByClass struct {
	ClassId   TClassId
	ClassCnt  int32
	ClassProb float32
	FoundCnt  int32
	SucCnt    int32
	Recall    float32
	Prec      float32
	Lift      float32
}

type ResByClasses struct {
	ByClass map[TClassId]*ResByClass
	TotCnt  int32
	SucCnt  int32
	Prec    float32
}

// Save simple results as if running validation test
func (sr *SimpResults) AsStrToBuffTest(sb *bytes.Buffer) {
	fmt.Fprintln(sb, "ndx,bestClass,bestProb,actClass,status")
	for ndx, row := range sr.Rows {
		stat := "ok"
		if row.BestClass != row.ActClass {
			stat = "fail"
		}
		fmt.Fprintf(sb, "%v,%v,%v,%v,%s\n",
			ndx, row.BestClass, row.BestProb, row.ActClass, stat)
	}

}

// Save simple results as if classifying request
func (sr *SimpResults) AsStrToBuffClass(sb *bytes.Buffer) {
	fmt.Fprintln(sb, "ndx,bestClass,bestProb")
	for ndx, row := range sr.Rows {

		fmt.Fprintf(sb, "%v,%v,%v\n",
			ndx, row.BestClass, row.BestProb)
	}
}

func (sr *SimpResults) ToDispStr() string {
	var sbb bytes.Buffer
	sb := &sbb
	sr.AsStrToBuffTest(sb)
	failCnt := sr.TotCnt - sr.SucCnt
	failP := 1.0 - sr.Precis
	fmt.Fprintf(sb, "numRow=%v  sucCnt=%v precis=%v failCnt=%v failPort=%v\n",
		sr.TotCnt, sr.SucCnt, sr.Precis, failCnt, failP)
	return sb.String()
}

func (sr *SimpResults) ToJSON() []byte {
	ba, _ := json.Marshal(sr)
	return ba
}

func (fier *Classifier) ClassRowStr(astr string) *ResultForRow {
	a := ParseStrAsArrStr(astr)
	if len(a) < fier.NumCol {
		fmt.Println("classRowStr inputStr has wrong num fields numFld=%v numExpect=%v astr=%v",
			len(a), fier.NumCol, astr)
		return nil
	}
	return fier.ClassRow(a, fier.ColDef)
}

//  Output is a structure that shows us the count
//  for each class plust the prob for each class
//  plus the chosen out
func (fier *Classifier) ClassRow(drow []string, feats []*Feature) *ResultForRow {
	tout := new(ResultForRow)
	tout.Classes = make(map[TClassId]ResultItem)
	clsm := make(map[TClassId]*ResultItem)
	featOut := make([]ResultForFeat, fier.NumCol)
	for fc := 0; fc < fier.NumCol; fc++ {
		featOut[fc].Cls = make(map[TClassId]ResultItem)
	}
	tout.Features = featOut
	for _, feat := range feats {
		fc := feat.ColNum
		if fc == fier.ClassCol {
			continue // skip the feature
		}
		if feat.Enabled == false {
			continue // skip the feature
		}

		strval := drow[fc]
		dval := ParseStrAsFloat32(strval)

		//cs := feat.Spec
		fwrk := &featOut[fc]
		isFeatCat := feat.IsCategory

		// This is critical feature where we try to find the most
		// precise bucket we can working backwards to less precise
		// buckets until we know we will always find a bucket when
		// it reaches 1 which is essentially the class probability
		// but we will not use that one.
		buckId := TQuantId(-16001)
		buck, bfound := feat.Buckets[0][buckId] // ensure empty / false lookup
		if isFeatCat || dval == MaxFloat32 {
			// We Only lookup Category Features
			// at one level
			buckId = feat.GetCategoryBucketId(strval)
			buck, bfound = feat.Buckets[1][buckId]
			//fmt.Printf("L173 bfound=%v  buck=%v\n", buck, bfound)
		} else {
			// Loop from Most precise down to Most general
			// until we find a match.
			maxBuck := feat.MaxNumBuck
			minBuck := feat.MinNumBuck
			numBuck := maxBuck
			for ; numBuck >= minBuck; numBuck-- {
				//fmt.Printf("L181: numBuck=%v maxBuck=%v minBuck=%v ", numBuck, maxBuck, minBuck)
				buckId = feat.BucketId(fier, dval, numBuck)
				//fmt.Printf(" buckId=%v \n", buckId)
				buck, bfound = feat.Buckets[numBuck][buckId]
				//fmt.Printf("L172: numBuck=%v dval=%v buckId=%v bfound=%v buck=%v\n", numBuck, dval, buckId, bfound, buck)
				//if bfound != true {
				//	spec := feat.Spec
				//	fmt.Printf("L163: No Bucket found dval=%v numBuck=%v buckId=%v fc=%v effMin=%v effMax=%v  effRange=%v ",
				//		dval, numBuck, buckId, fc, feat.EffMinVal, feat.EffMaxVal, feat.EffRange)
				//	fmt.Printf("  minFlt=%v maxFlt=%v  absRange=%v\n",
				//		spec.MinFlt, spec.MaxFlt, spec.AbsRange)
				//}
				if bfound == true && buck.totCnt > 1 {
					break
				}
			}
		}

		if bfound == true {
			// Our training data set includes
			// at least row that had one feature
			// that contained one value the derived
			// to the same bucket Id.

			for classId, classCnt := range buck.Counts {
				//fmt.Printf("204:classId=%v classCnt=%v\n", classId, classCnt)
				// Ieterate over the classes that match
				// and record them for latter use.
				if classCnt < 2 {
					continue
				}
				fBuckWrk := new(ResultItem)
				baseProb := float32(classCnt) / float32(buck.totCnt)
				//classProb := fier.ClassProb[classId]
				workProb := baseProb
				//workProb := baseProb * classProb
				//workProb := baseProb / classProb
				//workProb := baseProb - classProb
				fBuckWrk.Prob = workProb
				fwrk.TotCnt += int32(classCnt)
				fwrk.Cls[classId] = *fBuckWrk
				clswrk, clsFound := clsm[classId]
				if clsFound == false {
					clswrk = new(ResultItem)
					clsm[classId] = clswrk
				}
				// TODO: This should be done using
				//  the WeightByLevel to allow the optimizer
				//  more precise control.
				clswrk.Prob += workProb * feat.FeatWeight
				//clswrk.Prob += baseProb * feat.FeatWeight
				//fmt.Printf("230: col%v val=%v buck=%v class=%v baseProb=%v outProb=%v\n",
				//	fc, dval, buckId, classId, baseProb, fBuckWrk.Prob)
			} // for class
		} // if buck exist
	} // for feat

	// Copy Classes to acutal output
	// and select best item
	bestProb := float32(0.0)
	bestClassCnt := int32(0)
	for classId, classWrk := range clsm {
		if classWrk.Prob <= 0.0 {
			fmt.Printf("L227: ERR: Class Prob should not be 0 classId=%v classWrk=%v\n", classId, classWrk)
		}
		//classWrk.Prob = classWrk.Prob / float32(fier.totFeatWeight())
		classWrk.Prob = classWrk.Prob / float32(len(fier.ColDef))
		//fmt.Printf("L246: classId=%v prob=%v bestProb=%v classWrk=%v\n", classId, classWrk.Prob, bestProb, classWrk)
		tout.Classes[classId] = *classWrk
		//fmt.Printf("L48: classId=%v bestProb=%v classWorkProb=%v classWrk=%v\n", classId, bestProb, classWrk.Prob, classWrk)

		if bestProb < classWrk.Prob || (bestProb == classWrk.Prob && int32(fier.ClassCounts[classId]) > bestClassCnt) {
			// Had to add more sophisticated check her to tie break identical
			// class Probability.   I made an arbitrary choice to choose the
			// class with the greater total number of records assuming the tied
			// record would have a better chance of being in that class.
			// still have a potential of random differences between runs
			// if the total class probabilties are equal because GO
			// re-orders hash tables unpredictably
			bestProb = classWrk.Prob
			bestClassCnt = int32(fier.ClassCounts[classId])
			tout.BestProb = classWrk.Prob
			tout.BestClass = classId
			tout.ActClass = -9999
		}
	}
	//fmt.Printf("L265: bestClass=%v bestProb=%v\n", tout.BestClass, tout.BestProb)

	return tout
} // func

/* Classify a array of rows returns the analyzed
rows and the Test summary results.   The
list of feats parameter is required to allow the
classify operation to run on a subset of featurs
rather than the entire set.  This is required by
some of the data data discovery capabilities.  */
func (fier *Classifier) ClassifyRows(rows [][]string, feats []*Feature) ([]ResultForRow, *SimpResults) {
	numRow := len(rows)
	tout := make([]ResultForRow, 0, numRow)

	//sucessCnt := 0
	//rowCnt := 0
	resRows := new(SimpResults)
	resRows.TotCnt = int32(numRow)
	resRows.Rows = make([]SimpResRow, numRow)

	for ndx := 0; ndx < numRow; ndx++ {
		rowIn := rows[ndx]
		classId := fier.getClassId(rowIn)
		cres := fier.ClassRow(rowIn, feats)
		cres.ActClass = classId
		tout = append(tout, *cres)
		//fmt.Printf("L239: ndx=%v cres=%v numRow=%v \n", ndx, cres, numRow)
		// Copy into Simplified structure
		// for use generating the output
		// CSV.   We also need this one to
		// generate the simplified version
		// of the JSON
		rrow := &resRows.Rows[ndx]
		rrow.BestClass = cres.BestClass
		rrow.BestProb = cres.BestProb
		rrow.ActClass = cres.ActClass
		if rrow.BestClass == rrow.ActClass {
			resRows.SucCnt += 1
		}
		//fmt.Printf("L281: ndx=%v bestClass=%v bestProb=%v actClass=%v\n", ndx, rrow.BestClass, rrow.BestProb, rrow.ActClass)
		//fmt.Printf("252: ndx=%v rrow=%v\n", ndx, rrow)
		//if cres.actClass == cres.BestClass {
		//	sucessCnt += 1
		//}
		// TODO: We want to track sucess by class
		// TODO: Build the Result Records here
		// TODO: Return them as a separate set of parms
		//rowCnt += 1

	} // for row
	resRows.Precis = float32(resRows.SucCnt) / float32(resRows.TotCnt)
	//percCorr := (float32(sucessCnt) / float32(rowCnt)) * float32(100.0)
	//percFail := 100.0 - percCorr

	return tout, resRows

}

func (fier *Classifier) MakeByClassStats(sr *SimpResults, tstdta [][]string) *ResByClasses {
	tout := new(ResByClasses)
	tout.Prec = sr.Precis
	tout.TotCnt = sr.TotCnt
	tout.SucCnt = sr.SucCnt
	tout.ByClass = make(map[TClassId]*ResByClass)
	byClass := tout.ByClass
	numRow := len(sr.Rows)

	// We must update actual Counts by Class from the
	// source test data rather than classified results
	// because otherwise if the classifer didn't classify
	// anything belonging to a given class it would
	// be supressed from the results.
	//
	// TODO: Sort the ClassID before running
	//  so we get them out of the dictionary
	//  in sorted order latter.
	//
	// TODO: This will not change between runs
	//   of the optimizer and it is called for
	//   every one of the low level optimizer
	//   runs so it should be computed once rather
	//   than for every time we compute a result.
	//fmt.Printf("L335: tout=%v\n  byClass=%v\n sr=%v\n  sr.Rows=%v\n", tout, byClass, sr, sr.Rows)
	for _, row := range tstdta {
		actClassId := fier.getClassId(row)
		actClass, ccfnd := byClass[actClassId]
		if ccfnd == false {
			actClass = new(ResByClass)
			actClass.ClassId = actClassId
			actClass.ClassCnt = 1
			byClass[actClassId] = actClass
		} else {
			actClass.ClassCnt += 1
		}
	}

	// for accurate recall we need the count of rows
	// by actual class for the test rows.
	//fmt.Printf("L351: tout=%v\n  byClass=%v\n sr=%v\n  sr.Rows=%v\n", tout, byClass, sr, sr.Rows)
	for _, row := range sr.Rows {
		classId := row.BestClass

		// Update Counts by Predicted Class
		bclass, found := byClass[classId]
		if found == false {
			bclass = new(ResByClass)
			bclass.ClassId = row.BestClass
			byClass[classId] = bclass
		}
		bclass.FoundCnt += 1
		if row.BestClass == row.ActClass {
			bclass.SucCnt += 1
		}
	}
	// Update final stats for each class
	for _, bclass := range byClass {
		if bclass.FoundCnt > 0 {
			bclass.Prec = float32(bclass.SucCnt) / float32(bclass.FoundCnt)
		} else {
			bclass.Prec = 0.0
		}
		if bclass.ClassCnt > 0 {
			bclass.Recall = float32(bclass.SucCnt) / float32(bclass.ClassCnt)
		} else {
			bclass.Prec = 1.0
		}
		bclass.ClassProb = float32(bclass.ClassCnt) / float32(numRow)
		bclass.Lift = bclass.Prec - bclass.ClassProb
	}
	return tout
}

func (fier *Classifier) PrintResultsByClass(rbc *ResByClasses) {
	// Update final stats for each class
	for classId, bclass := range rbc.ByClass {
		fmt.Printf("class=%v ClassCnt=%v classProb=%v\n   Predicted=%v Correct=%v\n   recall=%v  Prec=%v\n   Lift=%v\n",
			classId, bclass.ClassCnt, bclass.ClassProb, bclass.FoundCnt, bclass.SucCnt, bclass.Recall, bclass.Prec, bclass.Lift)
	}
}

// NOTE: Consider just writing the formatting from JSON results
//   save the JSON results and make it easily read by ajax
//   That would save writting custom formatting in go and push
//   over to javascript where it is easier.

// function save testResult by row as csv

// function save classifyResult by row as csv

// function save results by class as json

// function save summary results by class as csv

// function printout nice summary of results by class
