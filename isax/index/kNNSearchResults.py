from SortedCollection import SortedCollection

class kNNSearchResults:

    def __init__(self, k = 0, ts_search= None):
        self.kNN = k
        self.results = SortedCollection()
        self.search_ts = ts_search

    def add_result(self,tsi):
        insert = tsi.clone()
        insert.set_comparable_reference_point(self.search_ts)
        self.results.insert(insert)

    def count(self):
        return len(self.results)


    def complete(self):
        if(self.kNN < len(self.results)):
            return True
        return False


    def remove_extra_results(self):
        if(self.complete()):
            # get rid of the last one
            self.results.remove_last()

