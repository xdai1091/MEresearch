import sys
sys.path.append("..")
import unittest
from ISAXUtils import ISAXUtils
from Sequence import Sequence
from Symbol import Symbol
from IndexHashParams import IndexHashParams
from InternalNode import InternalNode
from NodeType import NodeType
from iSAXIndex import iSAXIndex
import time


class test_iSAX_Index(unittest.TestCase):

    def test_basic_index_insert(self):
        ts = [-1.0,-0.5,-0.25,0,0.25,0.50,0.75,1.0]
        isax = None
        isax = ISAXUtils().create_isax_sequence(ts,4,4)
        print "isax", isax.get_index_hash()
        print 'bits repre.', isax.get_bit_string_representation()



    def test_isax_root_node_construct(self):
        A = Sequence(16)
        A.symbols.append(Symbol(1,4))
        A.symbols.append(Symbol(1,4))
        A.symbols.append(Symbol(1,4))
        A.symbols.append(Symbol(1,4))

        p = IndexHashParams()
        p.base_card = 4
        p.d = 1
        p.isax_word_length = 3

        p.ar_wild_bits.append(1)
        p.ar_wild_bits.append(1)
        p.ar_wild_bits.append(1)
        p.ar_wild_bits.append(1)

        root_node = InternalNode(A,p,NodeType.ROOT)
        print "masked rep:", root_node.get_masked_representation()


    def test_isax_index_0(self):
        ts = [-1.0,-0.5,-0.25,0.0,0.25,0.50,0.75,1.0]
        index = iSAXIndex(4,4,8)
        index.insert_sequence(ts, "genome.txt", 104526)
        index.insert_sequence(ts, "genome.txt", 2304526)
        index.insert_sequence(ts, "genome.txt", 2304526)
        index.insert_sequence(ts, "genome.txt", 3304526)
        index.insert_sequence(ts, "genome.txt", 4304526)
        index.insert_sequence(ts, "genome.txt", 5304526)
        index.insert_sequence(ts, "genome.txt", 6304526)
        index.insert_sequence(ts, "genome.txt", 7304526)
        index.insert_sequence(ts, "genome.txt", 8304526)

        ts2 = [-1.0,-0.5,-0.25,0.0,0.25,0.50,0.75,0.0]

        index.insert_sequence(ts2,"genome.txt", 8304526)


    def test_random_insert(self):
        num_entries = 50000
        index = iSAXIndex(4,4,8)
        search_ts = None
        for x in xrange(num_entries):
            ts_insert = ISAXUtils().generate_random_ts(8)
            if (x==1000):
                search_ts = ts_insert
                print "The search ts should be", search_ts
            index.insert_sequence(ts_insert,'ts.txt',1000 + x * 20)
        print ("\n**** Done with inserting ****")

        start = time.time()
        result = index.approx_search(search_ts)
        diff = time.time() - start
        if(result is None):
            print "Approx Search No Result Found!"
        else:
            print result.ts

        print "The total time we used is", diff




suite = unittest.TestLoader().loadTestsFromTestCase(test_iSAX_Index)
unittest.TextTestRunner(verbosity=2).run(suite)