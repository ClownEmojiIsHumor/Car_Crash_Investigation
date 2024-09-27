from pathlib import Path
import math
import os

import pandas as pd
import numpy as np

import seaborn as sns 

inputDir = Path("./data")

dataframes = []

# Iterate through all the files in the directory and grab the ones that match up with our yearscovered.
# Adding them to our dataframes array
# Where we can further process them as required
def readDfFromDir(_dataframes:list =[], _inputDir:Path =Path("./data")) -> None:
    for filename in os.listdir(_inputDir):
        filePath = inputDir/Path(filename)
        # print(f'The full relative path of the file is: {filePath}')
        df = pd.read_excel(filePath)
        _dataframes.append(df)
    return _dataframes

def readDfFromYearRange(yearStart:int, yearEnd:int, _dataframes:list =[], _inputDir:Path =Path("./data")) -> None:
    yearList = range(yearStart, yearEnd + 1)
    for year in yearList:
        filePath = inputDir/Path(f'{year}ncdb.xls')
        df = pd.read_excel(filePath)
        _dataframes.append(df)
    return _dataframes


def helperDisplay(_dataframes:list, displayHead:bool=False, displayShape:bool=True, displayColName:bool=False) -> None:
    if displayHead:
        print(f"{'-'*8}HEAD{'-'*8}")
        for df in _dataframes:
            print(f"Year: {df['C_YEAR'].unique()}")
            print(df.head)
    if displayShape:        
        print(f"\n{'-'*8}Shapes{'-'*8}")
        for df in _dataframes:
            print(f"Year: {df['C_YEAR'].unique()}")
            print(f"Shape: {df.shape}")
            if displayColName:
                print(df.columns)

# maybe update this to return some sort of useful object?
def checkColDiscrepency(_dataframes:list, display:bool=True) -> None:
    prevColSet = None
    prev = None
    prevYear = None
    for df in _dataframes:
        year = df['C_YEAR'].unique()[1]
        numCols = df.shape[1]
        colSet = set(df.columns)

        prev = numCols if prev == None else prev
        prevYear = year if prevYear == None else prevYear
        prevColSet = colSet if prevColSet == None else prevColSet

        colSetDiff1 = colSet.difference(prevColSet)
        colSetDiff2 = prevColSet.difference(colSet)

        if colSetDiff1 or colSetDiff2:
            colDiff = numCols - prev
            print(f'Discrepency identified between {prevYear} and {year} of {colDiff} cols')
            print(f'{prevYear} has {prev} and {year} has {numCols}')
            print(f'{colSetDiff1} or {colSetDiff2}')

        prev = numCols
        prevYear = year
        prevColSet = colSet
        



# readDfFromDir(_dataframes=dataframes, _inputDir=inputDir)
readDfFromYearRange(yearStart=2000, yearEnd=2022,_dataframes=dataframes, _inputDir=inputDir)
helperDisplay(dataframes, displayColName=True)
checkColDiscrepency(_dataframes=dataframes)


allYearsDf = pd.concat(dataframes, axis=0, ignore_index=True)

print(allYearsDf.shape)
print(allYearsDf.head())


os.makedirs('proccessed_data', exist_ok=True)
allYearsDf.to_excel('proccessed_data/combined.xlsx', index=False)


