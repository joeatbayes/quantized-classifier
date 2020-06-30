package main
//package backtest
/* Implement Backtest logic in GO to support backtesting and rolling forward test using ML predictions.
 *  Start with a given balance
 *  Receive a Bar of data with Buy, Sell signal
 *  Compute equity amount held based on balance purchases
 *  compute average price based on total price paide for shared held.
 *  assumed can hold at most one position.
 * 
 *  Need ability to drive classifier to train on upto X bars then
 *   generate a prediction for next bar and then train on the subsequent
 *   bar to get a better test.  Need to allow this to run through
 *   historical bars to current this way then continue to predict
 *   moving into the future.
 * 
 *  Need ISO date parser to obtain hold time.
 *  Need driver to run from classification input
 *  Need sample test driver to run from CSV sample
 * 
 */

import (
//  "qprob"   
"fmt"
)


type BKPosition struct {
    Symbol string
    Qty int
    BuyPrice float64
    BuyFees float64
    SellPrice float64
    
    PurchaseTime string
    SoldTime string
    
    
    // Simple Exit Critera
    maxHoldBars  int
    percStopLossRatio  float64
    profitTakerRatio  float64
    
    // Extended Entry & Exit Criteria 
    minProbProfit  float64 
    
    
}

// Position netprofit
// grossProfit
// isOpen
// PurchasedAsTime()
// SoldAsTime()
// BarsOpened()

// sell()
// amountAtRisk()


type BTestSpec struct {
  StartCapital float64
  MaxAtRiskRatio float64
  MinCashValue float64
  MinCashReserveRatio float64
  buyComissionFee float64
  sellComissionFee float64
  maxHoldBars int
  MaxPositionSizeRatio float64
  
    
}

type BKTest struct {
   OriginalBalance float64
   CashBalance float64
   EquityValue float64
   Fees float64
   NumTrade int
   // Postions array of BKPosition
   //cashAtRisk
   
   //maxCashAtRisk
    
   
}

  //AvailableCash
  //canOpenAnotherPosition(value)
  //atRiskForSymbol
  //CanBuyMoreSymbol()
  //canBuy(symbol, amount)
  //
  // BackTestPrint()
  

//func (BKTest *s) MakeBackTest(StartCapital float,  MaxPositionRation float) {

    
//}

func MakeBKTest(cashBalance float64,  defaultTranValue float64) *BKTest{
    r := BKTest{ CashBalance : cashBalance}
    return &r
}

func (s *BKTest) Buy(symbol string, price float64, qty int, fees float64) float64 {
  grossVal := (price * float64(qty))
  buyCost :=  grossVal + fees
  s.EquityValue += grossVal
  s.CashBalance -= buyCost
  s.Fees += fees
  s.NumTrade += 1
  return buyCost
}

func (s *BKTest) Sell(symbol string, price float64, cost float64, qty int, fees float64) float64 {
  grossValue := (price * float64(qty))
  netProc := grossValue - fees
  s.EquityValue -= cost * float64(qty) 
  s.CashBalance += netProc
  s.Fees += fees
  s.NumTrade += 1
  return netProc
}

func (s *BKTest) Print() {
 fmt.Println("cash=", s.CashBalance, "EquityValue=", s.EquityValue, "Fees=", s.Fees, "#Tran=", s.NumTrade, "Value=", s.CashBalance + s.EquityValue)  
}

func main() {
    fmt.Println( "backtest.go")
    
    tester := MakeBKTest(50000.0, 1000.0)
    tester.Buy("CAT", 87.50, 50, 6.00)
    tester.Sell("CAT", 93.00, 87.50, 50, 6.00)
    
    tester.Print()
}




