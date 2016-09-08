# AC297R - iSAX Implementation Practice

Final project for Harvard's AC297R: Spring 2016.

iSAX Implementation in Python

By: Xingchi Dai

---
Check out my [report](https://github.com/xdai1091/MEresearch/blob/master/Thesis_Proposal_final.pdf)!


## General Overview
The iSAX implementation in this repo follows Jin and Eammonn's paper(iSAX: Indexing and Mining Terabyte Sized Time Series). Prof.Shieh's original java implementation was referred for this practice. 

## How to test it?
The most important part to test in this implementation is "test_iSAXIndex.py"(under **index** folder). This file will generate a number of time series and index them(the default number is 50000). We pick one of time series as a query and run the approximate search method to find this time-series. The script will return the result. The maximum sereis I tried so far is 50000. As currently I used alook-up table (stated in the paper) to represent time-series, there is a maximum number of time-series we could index. 

## Description of Files

There are two big parts of implementation: iSAX representation and indexing. All indexing related files are stored in the **index** folder. All files which start with *test* are unit test files. They can be run to test specific implementation for iSAX. You can read all of those test cases in files. 

## iSAX Objects

### iSAX Utilities Tools (iSAXUtils.py)

This iSAX Utilities tool contains two major functionalities:

+ generate a random time-series given the specific length. 

+ create isax sequence based on given cardinalities

### iSAX distance look-up table (NormalAlphabet.py)

This file is for looking up iSAX distances, which is described in details in the paper mentioned above.

### Symbol (Symbol.py)

+ Each iSAX data point can be treated as one symbol. Each symbol has its own cardinality and integer representation. Each symbol can be promoted to a higher cardinality by calling **promote** method. 

### Sequence (Sequence.py)

A number of consecutive symbols make a sequence of iSAX. One sequence can be used to represent a time series. Each sequence can have mixed-cardinalities symbols. Two sequence's distance can be calculated using the MINDIST formula given in the paper. 
$MINDIST = \sqrt{\frac{n}{w}}\sqrt{\sum_{i=1}^{w}{{dist(t,s)}^2$


### Player Condition

This is implemented in the notebook `Condition Estimation.ipynb`.

### Other Folders

+ `attic`: Contains old stuff we didn't actually use
+ `figure`: Just an empty folder---running the code will put figures
  here
