# Convert Day level history for EOD data files
# contained in a specific directory from a list
# of prices for all symbols by day into a set of
# standard bar files one per symbol which contains
# all the available data for each symbol.
#
# Known weakness of this approach is that for each
# symbol for each day it must open and close # symbol
# files for the append operation.   I didn't figure it
# was worth building a buffered write cache because
# this operation is not particularly time senstive.
# and only take a long time the first time when converting
# large amounts of historical data.
#
#  by Joe Ellsworth 2017-08-12
#  See license.txt

import os.path
import time
from datetime import date

def  processFile(fiName):
  print ("fiName=", fiName)
  with open(fiName) as f:
      for line in f:
          line = line.strip()
          #print("line=", line)
          arr = line.split(",")
          #print("arr=", arr)
          symbol = arr[0]
          date = arr[1]
          diso = date[0:4] + "-" + date[4:6] + "-" + date[6:8]
          popen = float(arr[2])
          phigh = float(arr[3])
          plow = float(arr[4])
          pclose = float(arr[5])
          vol  = long(arr[6])
          #pdate = parse(date)
          # TODO:  The output file name should be computed
          #  relative to the input file removing the /src/finame and
          #  replacing it with /gen/symbol.  That way it would work
          #  for other exchanges.
          outFiName = "../../../jtdata/eoddata/nyse/gen" + "/" + symbol + ".csv"
          cm = ","
          if not os.path.isfile(outFiName):
            # Create a new file for this symbol if it does not
            # already exist.   
            with open(outFiName, "w") as outFile:
              outFile.write("symbol,date,open,close,high,low,volume\n")
              
          # Append the reformatted BAR data to the file.
          with open(outFiName, "a") as outFile:
              outFile.write("%s,%s,%s,%s,%s,%s,%d\n"
                            % (symbol, diso, str(popen), str(pclose), str(phigh), str(plow), vol))
          

def processDir(globPath):
  import glob
  flist =  glob.glob(globPath)
  flist.sort(); # process oldest dates first assuming
    # the file names are generated to produce correct
    # ordering using string compare of file name.
  print("numFiles=", len(flist), flist[0])
  for fiName in flist:
    processFile(fiName)


processDir("../../../JTDATA/eoddata/nyse/src/NYSE_*.txt")
