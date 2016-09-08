import Symbol as sy
import unittest
import NormalAlphabet as alpha
import Sequence as sq
import ISAXUtils as ut

class UtilTestCase(unittest.TestCase):
    def test_ts_to_isax_decomp(self):
        ts = [-1.0, -0.5, -0.25, 0.0, 0.25, 0.50, 0.75, 1.0]
        isax_utils = ut.ISAXUtils()
        isax = None
        isax = isax_utils.create_isax_sequence(ts,4,4)
        self.assertEquals(isax.orig_length,8)
        self.assertEqual(len(isax.symbols),4)
        self.assertEqual('0.4_1.4_2.4_3.4_',isax.get_index_hash())

    def test_isax_sequence_split(self):
        ts = [-1.0, -0.5, -0.25, 0.0, 0.25, 0.50, 0.75, 1.0]
        A = sq.Sequence(16)
        isax_util = ut.ISAXUtils()
        A.symbols.append(sy.Symbol(3,4))
        A.symbols.append(sy.Symbol(3,4))
        A.symbols.append(sy.Symbol(1,4))
        A.symbols.append(sy.Symbol(0,8))
        seq_out = isax_util.create_isax_sequence_based_on_cardinality(ts,A)
        isax = isax_util.create_isax_sequence(ts,4,4)
        print "normally", isax.get_bit_string_representation()
        print "out", seq_out.get_bit_string_representation()
        print "based on:", A.get_bit_string_representation()

    def test_isax_sequence_split_test_1(self):
        ts = [1,-0.5,0.25,0.0,0.25,0.5,0.75,0]
        A = sq.Sequence(16)
        isax_util = ut.ISAXUtils()
        A.symbols.append(sy.Symbol(3,4))
        A.symbols.append(sy.Symbol(3,4))
        A.symbols.append(sy.Symbol(1,4))
        A.symbols.append(sy.Symbol(0,4))

        A2 = sq.Sequence(16)
        A2.symbols.append(sy.Symbol(3,4))
        A2.symbols.append(sy.Symbol(3,4))
        A2.symbols.append(sy.Symbol(1,4))
        A2.symbols.append(sy.Symbol(0,8))

        seq_out_0 = isax_util.create_isax_sequence_based_on_cardinality(ts,A)
        seq_out_1 = isax_util.create_isax_sequence_based_on_cardinality(ts,A2)

        print seq_out_0.get_bit_string_representation(), "based on:",A.get_bit_string_representation()
        print seq_out_1.get_bit_string_representation(), "based on:",A2.get_bit_string_representation()



suite = unittest.TestLoader().loadTestsFromTestCase(UtilTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)