import copy
import math
import numpy as np

class TSProcessor:
    def __init__(self, length = 0):
        self.length = 0

    def paa(self,ts,paa_size):
        """
        Approximate the timeseries using PAA. If the timeseries has some NaN's they are handled as
        follows: 1) if all values of the piece are NaNs - the piece is approximated as NaN, 2) if there
        are some (more or equal one) values happened to be in the piece - algorithm will handle it as
        usual - getting the mean.
        :param ts:
        :param paa_size:
        :return:
        """

        ts_length = len(ts)
        assert  ts_length > paa_size, "PAA size can't be greater than the ts"

        # Check for the trivial case
        if(ts_length == paa_size):
            return copy.deepcopy(ts)
        else:
            breaks = []
            paa = []
            points_per_seg = (ts_length * 1.0) / paa_size
            for i in xrange(paa_size + 1):
                breaks.append(i * points_per_seg)

            for i in xrange(paa_size):
                seg_start = breaks[i]
                seg_end = breaks[i+1]

                fraction_start = math.ceil(seg_start) - seg_start
                fraction_end = seg_end - math.floor(seg_end)

                full_start = int(math.floor(seg_start))
                full_end = int(math.ceil(seg_end))

                segment = ts[full_start:full_end]

                if(fraction_start > 0):
                    segment[0]  *= fraction_start

                if(fraction_end > 0):
                    segment[-1] *= fraction_end

                element_sum = 0.0

                for e in segment:
                    element_sum += e

                paa.append(element_sum / points_per_seg)

        return paa

    def ts_2_index(self,series,alphabet,alphabet_size):
        cuts = alphabet.get_cuts(alphabet_size)
        res = []
        for i in xrange(len(series)):
            res.append(self.num_2_index(series[i],cuts))
        return res

    def num_2_index(self,value, cuts):
        """
        get mapping of number to cut index
        :param value:
        :param cuts:
        :return:
        """
        count = 0
        while((count < len(cuts)) and (cuts[count] <= value)):
            count += 1
        return count

    def z_normalize(self,series):
        res = []
        series_np = np.array(series)
        mean = np.mean(series_np)
        sd = np.std(series_np)
        for i in xrange(len(series)):
            res.append((series[i] - mean)/sd)
        return res

