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
$MINDIST = \sqrt{\frac{n}{w}}\sqrt{\sum_{i=1}^{w}{dist(t,s)}^2}$

## Index Objects

### Indexing Hash Parameters (IndexHashParam.py)
Each node has its own indexing hash parameter. The parameter contains the following fields.
+ base_card: the base cardinality
+ isax_word_length: the length of isax 
+ orig_ts_len: the original time series length 
+ threshold: if the time seires stored in the node exceeds a certain threshold, the node will be splited. 

### Internal Node

An internal node designates a split in SAX space and is created when the number of time series contained by a terminal node exceeds th. The internal node splits the SAX space by promotion of cardinal values along one or more dimensions as per the iterative doubling policy.

The root node is representative of the complete SAX space and is similar in functionality to an internal node. The root node evaluates time series at base cardinality, that is, the granularity of each dimension in the reduced representation is b. Encountered iSAX words correspond to some terminal or internal node and are used to direct index functions accordingly.

Also, we use sorted collection to store each node's children, as such the look up complexity will be log(n),

### Terminal Node

A terminal node is the node pointing to files stored time-series. 
 
From iSAX paper: A terminal node is a leaf node which contains a pointer to an index file on disk with raw time series entries. All time series in the corresponding index file are characterized by the terminal node's representative iSAX word. A terminal node represents the coarsest granularity necessary in SAX space to enclose the set of contained time series entries. In the event that an insertion causes the number of time series to exceed th, the SAX space (and node) is split to provide additional differentiation.
