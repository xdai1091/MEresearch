import Symbol as sy
import unittest
import NormalAlphabet as alpha
import Sequence as sq


class SequenceTestCase(unittest.TestCase):
    TEST_PRESISION = 2
    def test_clone(self):
        A = sq.Sequence(16)
        A.symbols.append(sy.Symbol(1,1))
        A.symbols.append(sy.Symbol(1,1))
        A.symbols.append(sy.Symbol(1,1))
        A.symbols.append(sy.Symbol(1,1))
        B = None

        B = A.clone()

        self.assertEqual(4,len(B.symbols))

    def test_sax_distance_table_dist_00_01(self):
        A_s1 = sy.Symbol()
        A_s1.cardinality = 4
        A_s1.sax_character = 1

        w1 = sq.Sequence(16)
        w1.symbols.append(A_s1)

        B_s1 = sy.Symbol()
        B_s1.cardinality = 4
        B_s1.sax_character = 0

        w2 = sq.Sequence(16)
        w2.symbols.append(B_s1)

        localDist = 0
        localDist = w1.sax_distance(w2)

        self.assertAlmostEqual(0.00, localDist, places=self.TEST_PRESISION);


    def test_sax_distance_table_dist_00_10(self):

        A_s1 = sy.Symbol()
        A_s1.cardinality = 4
        A_s1.sax_character = 2

        w1 = sq.Sequence(16)
        w1.symbols.append(A_s1)

        B_s1 = sy.Symbol()
        B_s1.cardinality = 4
        B_s1.sax_character = 0

        w2 = sq.Sequence(16)
        w2.symbols.append(B_s1)

        localDist = 0
        localDist = w1.sax_distance(w2)
        self.assertAlmostEqual(0.67, localDist, places = self.TEST_PRESISION)

    # def test_single_symbol_compare(self):
    #     A = sq.Sequence(16)
    #     A_s1 = sy.Symbol()
    #     A_s1.cardinality = 4
    #     A_s1.sax_character = 3
    #     A.symbols.append(A_s1)
    #
    #     B = sq.Sequence(16)
    #     B_s1 = sy.Symbol()
    #     B_s1.cardinality = 4
    #     B_s1.sax_character - 0
    #     B.symbols.append(B_s1)

    def test_mindist_calc(self):
        A = sq.Sequence(16)
        A.symbols.append(sy.Symbol(3, 4))
        A.symbols.append(sy.Symbol(3, 4))
        A.symbols.append(sy.Symbol(1, 4))
        A.symbols.append(sy.Symbol(0, 4))

        B =  sq.Sequence(16)
        B.symbols.append(sy.Symbol(0, 4))
        B.symbols.append(sy.Symbol(1, 4))
        B.symbols.append(sy.Symbol(3, 4))
        B.symbols.append(sy.Symbol(3, 4))

        val = A.mind_dist(B)

        actual = 4.266
        self.assertAlmostEqual(actual, val, places = 3)

    def test_sequence_naming_mechanics(self):
        A = sq.Sequence(16)
        A.symbols.append(sy.Symbol(3,4))
        A.symbols.append(sy.Symbol(3,4))
        A.symbols.append(sy.Symbol(1,4))
        A.symbols.append(sy.Symbol(0,4))

        self.assertEqual(A.get_index_hash(),'3.4_3.4_1.4_0.4_')

    def test_comparison(self):
        A = sq.Sequence(16)
        A.symbols.append(sy.Symbol(0,4))
        A.symbols.append(sy.Symbol(0,4))

        B = sq.Sequence(16)
        B.symbols.append(sy.Symbol(0,4))
        B.symbols.append(sy.Symbol(0,4))

        C = sq.Sequence(16)
        C.symbols.append(sy.Symbol(0,4))
        C.symbols.append(sy.Symbol(1,4))

        D = sq.Sequence(16)
        D.symbols.append(sy.Symbol(0,8))
        D.symbols.append(sy.Symbol(0,4))

        E = sq.Sequence(16)
        E.symbols.append(sy.Symbol(0, 4))
        E.symbols.append(sy.Symbol(0, 4))
        E.symbols.append(sy.Symbol(0, 4))

        self.assertEquals(True, A.equals(B))
        self.assertEquals(False, A.equals(C))
        self.assertEquals(False, A.equals(D))
        self.assertEquals(False, A.equals(E))

    # def test_ser_de(self):
    # Test serialize
    #     A = sq.Sequence(16)
    #     A.symbols.append(sy.Symbol(1,4))
    #     A.symbols.append(sy.Symbol(2,8))
    #     A.symbols.append(sy.Symbol(3,16))
    #     A.symbols.append(sy.Symbol(4,32))
    #     ser = A.get

    def test_index_hash_mechanics(self):
        A = sq.Sequence(16)
        A.symbols.append(sy.Symbol(1,4))
        A.symbols.append(sy.Symbol(2,8))
        A.symbols.append(sy.Symbol(3,16))
        A.symbols.append(sy.Symbol(4,32))

        hash = A.get_index_hash()

        B = sq.Sequence(0)
        B.parse_from_index_hash(hash)

        self.assertEqual(A.get_index_hash(),B.get_index_hash())

    def test_sequence_bit_mechanics(self):
        A_s1 = sy.Symbol()
        A_s1.cardinality = 4
        A_s1.sax_character = 1

        w1 = sq.Sequence(16)
        w1.symbols.append(A_s1)

        self.assertEqual(3,A_s1.number_bits_in_cardinality(A_s1.cardinality))

        B_s1 = sy.Symbol()
        B_s1.cardinality = 16
        A_s1.sax_character = 1

        self.assertEqual(5,B_s1.number_bits_in_cardinality(B_s1.cardinality))

        B_wild_0 = sy.Symbol(2,16,1)
        self.assertEqual("0001*",B_wild_0.get_isax_bit_representation(1))

        B_wild_1 = sy.Symbol(2,16,2)
        self.assertEqual("000**",B_wild_1.get_isax_bit_representation(2))

        B_wild_2 = sy.Symbol(2,16,3)
        self.assertEqual("00***", B_wild_2.get_isax_bit_representation(3))


    def contains_sequence(self,ts):
        """
        Confirm whether this sequence with wildcard bits "contains" another sequence
        :param ts:
        :return:
        """
        # scan through the Symbols, looking to make sure each one falls within the symbols+wildcard
        # bits in this node's region

        for x in xrange(len(self.symbols)):
            wild_card_bits = self.symbols[x].wildcardbits
            node_symbol_rep = self.symbols[x].get_isax_bit_representation(wild_card_bits)
            ts_symbol_rep = ts.symbols[x].get_isax_bit_representation(wild_card_bits)
            if(node_symbol_rep.equals(ts_symbol_rep) == False):
                return False
        return True



suite = unittest.TestLoader().loadTestsFromTestCase(SequenceTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)