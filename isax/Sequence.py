import NormalAlphabet as alpha
import Symbol as sy
import numpy as np
import math

class Sequence:

    def __init__(self,length = 0):
        self.orig_length = length
        self.symbols = []

    def clone(self,source = None):
        """
        Clone an exact same sequence
        :return:
        """
        if source is None:
            source  = self
        new_sequence = Sequence(source.orig_length)
        new_sequence.symbols = source.symbols

        return new_sequence


    def sax_distance(self,other):
        """
        Calculates SAX euclidean distance between two iSAX sequences.
        :param other:
        :return:
        """
        alphabet = alpha.NormalAlphabet()
        sqd_dist = 0

        # Compare symbol by symbol
        for x in xrange(len(self.symbols)):
            a = sy.Symbol()
            b = sy.Symbol()
            sy.perform_promotion(self.symbols[x],other.symbols[x],a,b)
            distance_matrix = np.array([[0],[0]])
            distance_matrix = alphabet.get_distance_matrix(a.cardinality)
            local_dist = distance_matrix[a.sax_character][b.sax_character]
            sqd_dist += local_dist
        return sqd_dist

    def mind_dist(self,other):
        alphabet = alpha.NormalAlphabet()
        sqd_dist = 0
        for x in xrange(len(self.symbols)):
            a = sy.Symbol()
            b = sy.Symbol()
            sy.perform_promotion(self.symbols[x],other.symbols[x],a,b)
            distance_matrix = alphabet.get_distance_matrix(a.cardinality)
            local_dist = distance_matrix[a.sax_character][b.sax_character]
            sqd_dist += local_dist * local_dist

        # get the sq root of the sum of the squares
        dist_sqrt = math.sqrt(sqd_dist)

        # Calculate the coefficient
        original_ts_length = self.orig_length * 1.0
        derived_sax_length = len(self.symbols)

        coef = math.sqrt(original_ts_length/derived_sax_length)

        return dist_sqrt * coef

    def get_cardinalities(self):
        """
        extracts the cardinalities of each symbol
        """
        ar_cards = []
        for x in xrange(len(self.symbols)):
            ar_cards.append(self.symbols[x].cardinality)
        return ar_cards

    def get_index_hash(self):
        """
        generate a label for the isax sequence, to be used in the isax
        indexing mechanics
        """
        str_name = ""
        for x in xrange(len(self.symbols)):
            str_name += "" + str(self.symbols[x].sax_character) + '.' + str(self.symbols[x].cardinality) + '_'
        return str_name

    def parse_from_index_hash(self,hash):
        parts = hash.split('_')
        self.symbols = []
        for x in xrange(len(parts)):
            nums = parts[x].split(".")
            if(len(nums) == 2):
                sax = int(nums[0])
                card = int(nums[1])
                self.symbols.append(sy.Symbol(sax,card))

    def get_bit_string_representation(self):
        rep = ""
        for x in xrange(len(self.symbols)):
            node_symbol_rep = self.symbols[x].get_isax_bit_representation(0)
            rep += node_symbol_rep + ","
        return rep


    def equals(self,other):
        if (other.get_bit_string_representation() == self.get_bit_string_representation()):
            return True
        return False




def perform_promotion(w1_in,w2_in,w1_out,w2_out):
    """
    Takes 2 isax sequences and promotes each symbol to the higher cardinality
    :return:
    """
    for x in xrange(len(w1_in.symbols)):
        a = sy.Symbol()
        b = sy.Symbol()

        sy.perform_promotion(w1_in.symbols[x],w2_in.symbols[x],a,b)
        w1_out.symbols.append(a)
        w2_out.symbols.append(b)