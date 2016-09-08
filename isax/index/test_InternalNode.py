import sys
sys.path.append("..")
import unittest
from IndexHashParams import IndexHashParams
from Sequence import Sequence
from InternalNode import InternalNode
from NodeType import NodeType
from TimeSeriesInstance import TimeSeriesInstance

class testInternalNode(unittest.TestCase):

    def test_knn_search_for_node(self):
        p = IndexHashParams()
        p.base_card = 4
        p.d = 1
        p.isax_word_length = 4
        p.orig_ts_len = 8
        p.threshold = 100

        s = Sequence(8)
        node = InternalNode(s,p,NodeType.ROOT)
        ts = [-1.0,-0.5,-0.25,0.0,0.25,0.5,0.75,1.0]
        # we will change the last element
        for x in xrange(5):
            ts[-1] = x
            ts_inst = TimeSeriesInstance(ts)
            ts_inst.add_occurance("foo.txt",x)
            # insert the node
            node.insert(ts_inst)
        print "insertion should be finished!"





suite = unittest.TestLoader().loadTestsFromTestCase(testInternalNode)
unittest.TextTestRunner(verbosity=2).run(suite)