import copy


class TimeSeriesInstance:
    def __init__(self, ts):
        self.ts = ts
        self.hm_occurences = {}
        self.ts_compare_to_base_ref = []


    def add_occurences(self,instances):
        hm = instances.hm_occurences
        itr = set(instances.hm_occurences.keys())
        # iterate through hashMap values iterator
        for e in itr:
            str_key = str(e)
            self.add_occurence_by_key(str_key,hm[str_key])

    def add_occurance(self,str_file_name, offset):
        str_key = str_file_name + "+" + str(offset)
        self.add_occurence_by_key(str_key,offset)


    def add_occurence_by_key(self, str_key, offset):
        if(self.hm_occurences.has_key(str_key)):
            print str_key,"has been added"
        else:
            self.hm_occurences[str_key] = offset

    def clone(self):
        tsi = TimeSeriesInstance(copy.deepcopy(self.ts))
        hm = self.hm_occurences
        itr = set(self.hm_occurences)
        for e in itr:
            str_key = str(e)
            tsi.add_occurence_by_key(str_key,hm[str_key])

        return tsi

    def set_comparable_reference_point(self,ts_base):
        self.ts_compare_to_base_ref = ts_base