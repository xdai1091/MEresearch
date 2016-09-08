import numpy as np
from NodeType import NodeType
from IndexHashParams import IndexHashParams
from Sequence import Sequence
from InternalNode import InternalNode
from TimeSeriesInstance import TimeSeriesInstance

##
# Implements iSAX indexing
#
#
# Search
#
# The method of approximation is derived from the intuition that two similar time series are often
# represented by the same iSAX word. Given this assumption, the approximate result is obtained by
# attempting to find a terminal node in the index with the same iSAX representation as the query.
# This is done by traversing the index in accordance with split policies and matching iSAX
# representations at each internal node.
#
# Because the index is hierarchical and without overlap, if such a terminal node exists, it is
# promptly identified. Upon reaching this terminal node, the index file pointed to by the node is
# fetched and returned. This file will contain at least 1 and at most th time series in it. A main
# memory sequential scan over these time series gives the approximate search result.
#
# In the (very) rare case that a matching terminal node does not exist, such a traversal will fail
# at an internal node. We mitigate the effects of non-matches by proceeding down the tree,
# selecting nodes whose last split dimension has a matching iSAX value with the query time series.
# If no such node exists at a given junction, we simply select the first, and continue the descent.
#
# Q. Why not hash directly to the iSAX pattern?
#
# A. what if the bucket has exceeded its th threshold? at that point the iSAX space has been
# promoted and split, we'll have to check the next level
#
#
# Q. Why do we need internal nodes at all?
#
# A. Otherwise we would not know to stop; these provide a type of "breadcrumbs" in search space to
# let us know something is "down the rabbit hole".
#
#
# Q. Why have such wide fan out from the root node?
#
# A. to reduce to number of hops to the terminal nodes at the base cardinality level
#
#
# Q. Are the { .., .., .. } nodes that are exist before the base-card-level actually terminal
# nodes?
#
# A. No. (the theory for now)
#
#
# Q. Is there any need for intermediate nodes at the "pre-base-card-level" ?
#
# A. No. (for now)
#
#
# Java author Josh Patterson
# Python author Xingchi Dai
##

class iSAXIndex:
    def __init__(self,base_card,sax_word_len,orig_ts_len):
        self.p = IndexHashParams()
        self.p.base_card = base_card
        self.p.d = 1
        self.p.isax_word_length = sax_word_len
        self.p.orig_ts_len = orig_ts_len
        self.p.threshold = 100
        self.s = Sequence(orig_ts_len)
        self.root_node = InternalNode(self.s,self.p,NodeType.ROOT)



    def insert_sequence(self,ts,filename,offset,ts_inst = None):
        """
        Takes a Timeseries ts and inserts it into the isax index along with its source file and
        location.
        :param ts:
        :param filename:
        :param offset:
        :return:
        """
        if(ts_inst is None):
            ts_inst = TimeSeriesInstance(ts)
            ts_inst.add_occurance(filename,offset)
        self.root_node.insert(ts_inst)


    def approx_search(self, ts):
        """
        This is a function for looking for similar time-series
        :param ts:
        :return:
        """
        return self.root_node.approx_search(ts)