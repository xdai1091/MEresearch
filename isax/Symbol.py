import math
import numpy as np

class Symbol:

    
    # The default init function 
    def __init__(self, sax_character = 0, cardinality = 0, wildcardbits = 0):
        self.cardinality = cardinality
        self.sax_character = sax_character
        self.wildcardbits = wildcardbits

    # A method to promote the cardinality of a symbol based on another symbol
    def promote(self, target):
        return self.promote_private(target.sax_character,target.cardinality)


    # A method to promote the cardinality of a symbol based on another symbol
    def promote_private(self, sax_number, i_cardinality):

       # check the validity of the params
    	assert i_cardinality > 1, "not a possible cardinality"
        assert self.power_of_two(i_cardinality) is True, "cardinality is not the power of two"
        assert i_cardinality > self.cardinality, "can't promote to a lesser cardinality"
        assert sax_number < i_cardinality, "sax_number is out range of the cardinality"

        s = Symbol() 

        # figure out how many bits to shift
        i_new_bits = self.cardinality_bit_delta(self.cardinality, i_cardinality)

        s.cardinality = i_cardinality

        # see if the local one form prefix
        i_target_sax_number_prefix = (sax_number >> i_new_bits) << i_new_bits
        i_local_sax_number_prefix = (self.sax_character << i_new_bits)

        # check if they are equal
        if(i_target_sax_number_prefix == i_local_sax_number_prefix):
            # If they are equal, then copy over the bits from the target symbol
            s.sax_character = sax_number
        elif(i_target_sax_number_prefix > i_local_sax_number_prefix):
            # if this symbol's compared bits are lexographically SMALLER than the bits in the target
            # symbol, then we use all 1's to fill out the promoted symbol we'll return from the function

            s.sax_character = i_local_sax_number_prefix
            i_mask = 1
            for x in xrange(i_new_bits):
                s.sax_character = s.sax_character ^ i_mask
                i_mask = i_mask << 1
        elif(i_target_sax_number_prefix < i_local_sax_number_prefix):
            # we use all 0 to fill out the promoted symbol
            s.sax_character = i_local_sax_number_prefix
        else:
            raise ValueError('promote error, check your value. the case not meant to be happen')

        # return the new promoted symbol
        return s

    def promote_and_split(self, new_low_symbol, new_high_symbol):
        """
        promote the cardinality by adding a bit to the right hand side,
        this splits the cardinality space into two halves
        the low side gets a 0 bit, the high side gets a 1 bit
        """
        i_new_cardinality = self.cardinality << 1
        new_low_symbol.cardinality = i_new_cardinality
        new_high_symbol.cardinality = i_new_cardinality

        new_low_symbol.sax_character = self.sax_character << 1
        new_high_symbol.sax_character = (self.sax_character << 1) + 1


    def power_of_two(self,num):
        return ((num & (num - 1)) == 0) and num != 0

    def count_lead_zs(self,x):
        """
        counts how many zeros we have in the bit representation
        of an integer before we hit a 1, later on, we will shift
        this value
        """
        display_mask = 1 << 31
        cnt = 0
        for c in xrange(1,33):
            if((x & display_mask) == 0):
                cnt += 1
            else:
                return cnt
            x <<= 1
        return cnt



    def number_bits_in_cardinality(self,card):
        """
        calculates the minimum number of bits a cardinality fits in
        assume the max bits are 32
        """
        return 32 - self.count_lead_zs(card)


    def cardinality_bit_delta(self,c0, c1):
        """
        Used to figure out how many bits we need to shift a SAX value for promotion to 
        a higher cardinality
        
        """
        c0_bits = self.number_bits_in_cardinality(c0)
        c1_bits = self.number_bits_in_cardinality(c1)

        return int(math.fabs(c1_bits - c0_bits))




    def clone(self):
        return Symbol(self.sax_character,self.cardinality,self.wildcardbits)

    def clone(self,source):
        """
        clone a source symbol to the current instance
        :param: the source symbol we wish to copy from
        """
        self.cardinality = source.cardinality
        self.sax_character = source.sax_character
        self.wildcardbits = source.wildcardbits

    def reset(self):
        """
        reset this symbol to all 0
        :return: Void
        """
        self.cardinality = 0
        self.sax_character = 0
        self.wildcardbits = 0


    def compare_to(self,other):
        """
        Compares the TPoint object with other TPoint using timestamps first: i.e. by the timestamp
        values, if they are equal, the TPoint values used.
        :return: the standard compreTo result
        """
        if(self.cardinality == other.cardinality and self.sax_character == other.sax_character):
            return 0
        else:
            # do a card promotion
            a_out = Symbol()
            b_out = Symbol()
            perform_promotion(self,other,a_out,b_out)
            if(a_out.sax_character == b_out.sax_character):
                return 0
            elif(a_out.sax_character > b_out.sax_character):
                return 1
            elif(a_out.sax_character < b_out.sax_character):
                return -1
        return -1

    ##############################
    # The following methods are only for debug purpose
    ##############################
    def get_isax_bit_representation(self,wildcard_bits):

        """
        Debug method to look at the bits of a SAX value.
        param - value SAX value, or any integer, that we want to convert into a string of bits.
        """
        display_mask = 1 << 31
        bits_for_card = self.number_bits_in_cardinality(self.cardinality)
        val = self.sax_character
        buf = ""
        for c in xrange(1,33):
            if (32 - c < bits_for_card):
                if(wildcard_bits >= 33 - c):
                    buf += '*'
                else:
                    buf += '0' if ((val & display_mask) == 0) else '1'

            val <<= 1


        return buf

    def sax_table_dist(self,other, alphabet):
        """
        A debug method to pull the SAX distance value out of the SAX distance lookup table.
        :param alphabet:
        :return:
        """
        distance_matrix = np.array([[0],[0]])
        distance_matrix = alphabet.get_distance_matrix(other.cardinality)
        return distance_matrix[self.sax_character][other.sax_character]



def perform_promotion(a_in,b_in,a_out,b_out):
    if(a_in.cardinality > b_in.cardinality):
        a_out.clone(a_in)
        b_out.clone(b_in.promote(a_in))
    elif(a_in.cardinality < b_in.cardinality):
        a_out.clone(a_in.promote(b_in))
        b_out.clone(b_in)
    else:
        a_out.clone(a_in)
        b_out.clone(b_in)