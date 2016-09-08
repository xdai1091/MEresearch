class IndexHashParams:
    def __init__(self,base_card = 4,isax_word_length = 4,d = 1,
                 orig_ts_len = 0,dim_index = 0,threshold = 4,
                 ar_cards = []):
        self.base_card = base_card
        self.isax_word_length = isax_word_length
        self.d = d #iterative double rate per level, has to be less than w
        self.orig_ts_len = orig_ts_len
        self.dim_index = dim_index # the index of the dimension that we are expanding
        self.threshold = threshold
        self.ar_wild_bits = []


    def create_masked_bits_sequence(self,isax):
        rep = ""
        for x in xrange(len(isax.symbols)):
            ts_symbol_rep = isax.symbols[x].get_isax_bit_representation(0)
            rep += ts_symbol_rep + ','
        return rep


    # We here promote the lowest cardinality symbol
    def generate_child_cardinality(self,ar_sequence_cards):
        ar_cards = []
        if(len(ar_sequence_cards) < 1):
            return ar_cards
        i_lsf = ar_sequence_cards[0]
        index = 0
        for x in xrange(len(ar_sequence_cards)):
            if(i_lsf > ar_sequence_cards[x]):
                i_lsf = ar_sequence_cards[x]
                index = x
            ar_cards.append(ar_sequence_cards[x])
        ar_cards[index] = ar_cards[index] << 1
        return ar_cards