import Symbol as sy
import Sequence as sq
import NormalAlphabet as alpha
import numpy as np
import scipy.stats as stats
import TSProcessor as tsp


class SAXBreakPoints:
    def __init__(self):
        B_Li = 0
        U_Ui = 0


class ISAXUtils:

    tp = tsp.TSProcessor()

    def generate_random_ts(self,length):
        """
        Creates a Timeseries of length len; typically used in Unit Tests.
        :param length:
        :return:
        """
        # setting hyper-prameters
        h_alpha=4
        h_beta=1

        sigma_square=stats.invgamma.rvs(size=1,a=h_alpha,scale=h_beta)[0]

        # Generate observations
        sample_size=length
        y=np.array([0.0 for i in range(sample_size)])
        noise=np.array(stats.norm.rvs(size=sample_size,loc=0,scale=np.sqrt(sigma_square)))

        for i in range(1,sample_size):
            alpha= np.random.uniform(0.1,1,size = 1)
            # round the answer into two digits.
            y[i]=round(alpha*y[(i-1)]+noise[i],2)

        return y

    def create_isax_sequence(self,ts,base_cardinality,word_length):
        alphabet = alpha.NormalAlphabet()
        paa_size = word_length
        ts_util = tsp.TSProcessor()
        paa = self.tp.paa(ts_util.z_normalize(ts),paa_size)
        isax = sq.Sequence(len(ts))

        # Transpose into numeric isax representation
        ar_cuts = self.tp.ts_2_index(paa,alphabet,base_cardinality)

        for x in xrange(len(ar_cuts)):
            isax.symbols.append(sy.Symbol(ar_cuts[x],base_cardinality))

        return isax


    def create_isax_sequence_based_on_cardinality(self,ts,seq):
        # Create sax representation
        alphabet = alpha.NormalAlphabet()
        paa_size = len(seq.symbols)
        ts_util = tsp.TSProcessor()
        # perform PAA conversion
        paa = ts_util.paa(ts_util.z_normalize(ts), paa_size)
        isax = sq.Sequence(len(ts))
        for x in xrange(len(seq.symbols)):
            ar_cuts = ts_util.ts_2_index(paa,alphabet,seq.symbols[x].cardinality)
            isax.symbols.append(sy.Symbol(ar_cuts[x],seq.symbols[x].cardinality))
        return isax


    def create_isax_sequence_based_on_seq_array(self, ts, ar_cards):
        alphabet = alpha.NormalAlphabet()
        paa_size = len(ar_cards)
        ts_util = tsp.TSProcessor()
        paa = self.tp.paa(ts_util.z_normalize(ts),paa_size)
        isax = sq.Sequence(len(ts))
        for x in xrange(len(ar_cards)):
            ar_cuts = ts_util.ts_2_index(paa,alphabet,ar_cards[x])
            isax.symbols.append(sy.Symbol(ar_cuts[x],ar_cards[x]))
        return isax
