import sys
sys.path.append('..')
import unittest
from TimeSeriesInstance import TimeSeriesInstance
from ISAXUtils import ISAXUtils
from IndexHashParams import IndexHashParams
from TerminalNode import TerminalNode

class testTerminalNode(unittest.TestCase):

    def test_split_threshold(self):

        # This test is to check the same instance key insert
        ts_2 = [-1.0,-0.5,-0.25,0.0,0.25,0.5,0.75,2.0]
        seq = None
        seq = ISAXUtils().create_isax_sequence(ts_2,4,4)
        p = IndexHashParams()
        p.base_card = 4
        p.d = 1
        p.isax_word_length = 4
        p.orig_ts_len = 8

        node = TerminalNode(seq, p)
        tsi_A = TimeSeriesInstance(ts_2)
        tsi_A.add_occurance('foo.txt',10)
        tsi_B = TimeSeriesInstance(ts_2)
        tsi_B.add_occurance('foo.txt',1)

        node.insert(tsi_B)
        self.assertEqual(1,len(node.ar_instances))

        node.insert(tsi_A)
        self.assertEqual(1,len(node.ar_instances))

    def test_split_threshold_2(self):
        ts_1 = [1.0,-0.5,-0.25,0.0,0.25,0.5,0.75,-2.0]
        ts_2 = [-1.0,-0.5,-0.25,0.0,0.25,0.5,0.75,2.0]

        seq = None
        seq = ISAXUtils().create_isax_sequence(ts_2,4,4)

        p = IndexHashParams()
        p.base_card = 4
        p.d = 1
        p.isax_word_length = 4
        p.orig_ts_len = 8
        p.threshold = 2

        node  = TerminalNode(seq,p)

        tsi_A = TimeSeriesInstance(ts_1)
        tsi_A.add_occurance('foo.txt',10)

        tsi_B = TimeSeriesInstance(ts_2)
        tsi_B.add_occurance('foo.txt',1)


        node.insert(tsi_B)
        self.assertEqual(1,len(node.ar_instances))

        node.insert(tsi_A)
        # Should not get this ts, becasue one terminal node
        # cannot hold two different isax sequence
        self.assertEqual(1,len(node.ar_instances))

    def test_split_threshold_3(self):
        ts_1 = [1.0,-0.5,-0.25,0.0,0.25,0.5,0.75,-2.0]
        ts_2 = [1.0,-0.5,-0.25,0.0,0.25,0.5,0.75,-2.1]
        ts_3 = [1.0,-0.5,-0.25,0,0.25,0.50,0.75,-2.1]
        ts_4 = [1.0,-0.5,-0.25,0.0,0.25,0.50,0.75,-1.92]
        ts_5 = [1.0,-0.5,-0.25,0.0,0.25,0.50,0.75,-1.92]

        seq = None
        seq = ISAXUtils().create_isax_sequence(ts_2,4,4)
        p = IndexHashParams()
        p.base_card = 4
        p.d = 1
        p.isax_word_length = 4
        p.orig_ts_len = 8
        p.threshold = 2

        node = TerminalNode(seq,p)

        tsi_A = TimeSeriesInstance(ts_1)
        tsi_A.add_occurance('foo.txt',10)

        tsi_B = TimeSeriesInstance(ts_2)
        tsi_B.add_occurance('foo.txt',1)

        tsi_C = TimeSeriesInstance(ts_3)
        tsi_C.add_occurance('foo.txt',12)

        node.insert(tsi_B)
        self.assertEqual(1,len(node.ar_instances))
        node.insert(tsi_A)
        self.assertEqual(2,len(node.ar_instances))
        node.insert(tsi_C)
        self.assertEqual(3,len(node.ar_instances))

        # Check if it should split the work
        self.assertEqual(True,node.is_over_threshold())


    def test_gen(self):
        gen1 = ISAXUtils().generate_random_ts(8)
        print "gen1:", gen1
        print "isax:", ISAXUtils().create_isax_sequence(gen1,4,4).get_index_hash()








suite = unittest.TestLoader().loadTestsFromTestCase(testTerminalNode)
unittest.TextTestRunner(verbosity=2).run(suite)