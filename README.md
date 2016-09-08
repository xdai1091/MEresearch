# AC297R - iSAX Implementation Practice

Final project for Harvard's AC297R: Spring 2016.

iSAX Implementation in Python

By: Xingchi Dai

---
Check out my [report](https://github.com/xdai1091/MEresearch/blob/master/Thesis_Proposal_final.pdf)!


## General Overview
The iSAX implementation in this repo follows Jin and Eammonn's paper(iSAX: Indexing and Mining Terabyte Sized Time Series). Prof.Shieh's original java implementation was referred for this practice. 

## How to test it?
The most important part to test in this implementation is "test_iSAXIndex.py"(under **index** folder). This file will generate a number of time series and index them(the default number is 50000). We pick one of time series as a query and run the approximate search method to find this time-series. The script will return the result. The maximum sereis I tried so far is 50000. As currently I used look-up table (stated in the paper) to represent time-series, there is a maximum number of time-series we could index. 

## Description of Files

### Data

The raw data, in the form of CSV files, are all stored in the in the
`raw-data` folder.  See the README in there for more information. After
the data gets cleaned, the cleaned data are stored in the `clean-data`
folder.

### Data Cleaning

+ `data-cleaning.ipynb`: This file contains code to convert the raw data
  into a form more amenable for analysis. Here, we merge information
  about players' salary and their game statistics, remove NaN values,
  and create matrices that we will need for indexing purposes.

### Lineup Selection

+ `Simulated Annealing .ipynb`: This file contains code for the
  simulated annealing and the greedy algorithm, which were used to pick
  the best lineup.

### Player Contribution Estimation

The notebooks that address this are the following (you should read them
in this order):

+ `lbfgs-sgd.ipynb`: Contains code for L-BFGS and SGD.
+ `Pymc and Pooling.ipynb`: Contains code for our first implementation
  of PyMC
+ `Cluster and optimize.ipynb`: Contains implementation of clustering
  with PyMC.
+ `ESS_a single game.ipynb`: Contains code for running elliptical slice
  sampling (ESS) on a single game.
+ `ESS_entire games.ipynb`: Contains code for running ESS on the whole
  season.
+ `Simulated Annealing.ipynb`: Contains code for running simulated annealing to find the best line-up basketball team
+ `pystan.ipynb`: Contains code for a model in PyStan.

### Player Condition

This is implemented in the notebook `Condition Estimation.ipynb`.

### Other Folders

+ `attic`: Contains old stuff we didn't actually use
+ `figure`: Just an empty folder---running the code will put figures
  here
