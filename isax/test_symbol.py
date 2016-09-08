# In this file, I test if symbol.py code is correct

import Symbol as sy
import unittest
import NormalAlphabet as alpha


class SymbolTestCase(unittest.TestCase):
    TEST_PRESISION = 2
    def test_sax_bit_rep(self):
        """
        This part is to test the symbol isax representation
        :return:
        """
        A = sy.Symbol(2,4)
        bits = A.get_isax_bit_representation(0)
        self.assertEquals('010',bits)

        B = sy.Symbol(2, 8)
        self.assertEquals( "0010", B.get_isax_bit_representation(0))

        C = sy.Symbol(4, 8)
        self.assertEquals("0100", C.get_isax_bit_representation(0))

        D = sy.Symbol(4, 16)
        self.assertEquals("00100", D.get_isax_bit_representation(0))

        E = sy.Symbol(4, 16)
        self.assertEquals("0010*", E.get_isax_bit_representation(1))
        self.assertEquals("001**", E.get_isax_bit_representation(2))
        self.assertEquals("00***", E.get_isax_bit_representation(3))

        F = sy.Symbol(4, 32)
        self.assertEquals("00010*", F.get_isax_bit_representation(1))

    def test_symbol_split(self):
        """
        This part is to test if the function can split the symbol correctly
        :return:
        """
        A = sy.Symbol(2, 4)

        a_0 = sy.Symbol()
        a_1 = sy.Symbol()

        A_low = sy.Symbol(4, 8)

        A_high = sy.Symbol(5, 8)

        A.promote_and_split(a_0, a_1)

        self.assertEquals(a_0.cardinality, 8)
        self.assertEquals(a_1.cardinality, 8)

        self.assertEquals(a_0.sax_character, A_low.sax_character)
        self.assertEquals(a_1.sax_character, A_high.sax_character)

    def test_promote_symbol(self):

        A_in = sy.Symbol(0, 2)
        B_in = sy.Symbol(1, 2)
        A_out = sy.Symbol(0, 0)
        B_out = sy.Symbol(0, 0)

        sy.perform_promotion(A_in, B_in, A_out, B_out)


        self.assertEquals(A_out.cardinality, 2)
        self.assertEquals(B_out.cardinality, 2)
        self.assertEquals(A_out.sax_character,0)
        self.assertEquals(B_out.sax_character,1)

        A_in = sy.Symbol(6, 8)
        B_in = sy.Symbol(0, 2)
        A_out = sy.Symbol(0, 0)
        B_out = sy.Symbol(0, 0)

        sy.perform_promotion(A_in, B_in, A_out, B_out)


        self.assertEquals(B_out.cardinality, 8)
        self.assertEquals(A_out.sax_character, 6)
        self.assertEquals(B_out.sax_character, 3)

        A_in = sy.Symbol(1, 2)
        B_in = sy.Symbol(3, 8)
        A_out = sy.Symbol(0, 0)
        B_out = sy.Symbol(0, 0)
        sy.perform_promotion(A_in, B_in, A_out, B_out)

        self.assertEquals(A_out.cardinality, 8)
        self.assertEquals(B_out.cardinality, 8)
        self.assertEquals(A_out.sax_character, 4)
        self.assertEquals(B_out.sax_character, 3)

        A_in = sy.Symbol(1, 2)
        B_in = sy.Symbol(0, 8)
        A_out = sy.Symbol(0, 0)
        B_out = sy.Symbol(0, 0)
        sy.perform_promotion(A_in, B_in, A_out, B_out)
        self.assertEquals(A_out.cardinality, 8)
        self.assertEquals(B_out.cardinality, 8)
        self.assertEquals(A_out.sax_character, 4)
        self.assertEquals(B_out.sax_character, 0)

    def test_comparison(self):
        A = sy.Symbol(0, 4)
        B = sy.Symbol(0, 4)
        val = A.compare_to(B)
        self.assertEquals(0,val)


        A2 = sy.Symbol(1, 4)
        B2 = sy.Symbol(2, 4)
        val = A2.compare_to(B2)
        val2 = B2.compare_to(A2)
        self.assertEquals(-1,val)
        self.assertEquals(1,val2)

        A3 = sy.Symbol(1, 4)
        B3 = sy.Symbol(2, 8)
        val = A3.compare_to(B3)
        self.assertEquals(0, val)

    def test_sax_distance_table(self):
        alphabet = alpha.NormalAlphabet()
        a = sy.Symbol(0,4)
        b = sy.Symbol(1,4)
        val = 0
        val = a.sax_table_dist(b,alphabet)
        self.assertEquals(val,0.0)

        a2 = sy.Symbol(0,4)
        b2 = sy.Symbol(2,4)
        val2 = 0
        val2 = a2.sax_table_dist(b2,alphabet)
        self.assertAlmostEqual(val2,0.67,places=self.TEST_PRESISION)

        a3 = sy.Symbol(3,4)
        b3 = sy.Symbol(0,4)
        val3 = 0
        val3 = a3.sax_table_dist(b3,alphabet)
        self.assertAlmostEqual(val3,1.35,places=self.TEST_PRESISION)

        a4 = sy.Symbol(3,4)
        b4 = sy.Symbol(1,4)
        val4 = 0
        val4 = a4.sax_table_dist(b4,alphabet)
        self.assertAlmostEqual(val4,0.67,places=self.TEST_PRESISION)

        a5 = sy.Symbol(1,4)
        b5 = sy.Symbol(3,4)
        val5 = 0
        val5 = a5.sax_table_dist(b5,alphabet)
        self.assertAlmostEqual(val5,0.67,places=self.TEST_PRESISION)

        a6 = sy.Symbol(0,4)
        b6 = sy.Symbol(3,4)
        val6 = 0
        val6 = a6.sax_table_dist(b6,alphabet)
        self.assertAlmostEqual(val6,1.35,places=self.TEST_PRESISION)




suite = unittest.TestLoader().loadTestsFromTestCase(SymbolTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)