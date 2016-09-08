from NodeType import NodeType
from ISAXUtils import ISAXUtils

class TerminalNode:


    def __init__(self,seq_key,params):
        self.type = NodeType.TERMINAL
        self.key = seq_key
        self.params = params
        self.ar_instances = {}


    def is_over_threshold(self):
        """
        Determines if a TerminalNode needs to split based on how many TimeseriesInstances it contains
        and the threshold.
        :return:
        """
        assert self.params.threshold >= 1,"bad threshold"
        if(len(self.ar_instances) > self.params.threshold):
            return True
        return False


    def get_node_instances_iterator(self):
        # python should be able to iterate set.
        return set(self.ar_instances)


    def get_node_instance_by_key(self, str_key):
        return self.ar_instances[str_key]



    def insert(self,ts_inst):
        """
        The insert call used from a parent internal/root node
        :return:
        """
        ts_isax = None
        ts_isax = ISAXUtils().create_isax_sequence_based_on_cardinality(ts_inst.ts,self.key)
        isax_hash = ts_isax.get_index_hash()
        # termination check
        if(self.key.get_index_hash() == isax_hash):
            if(self.ar_instances.has_key(str(ts_inst.ts))):
                # merge
                ts_int_existing = self.ar_instances[str(ts_inst.ts)]
                ts_int_existing.add_occurences(ts_inst)
            else:
                # add

                self.ar_instances[str(ts_inst.ts)] = ts_inst.clone()

        else:
            print "i try to insert", ts_inst.ts
            print self.key.get_index_hash()
            print "ts shouldn't point to this terminal node"
            print isax_hash


    # Approximate Search

    def approx_search(self,ts):
        ts_isax = None
        ar_cards = self.key.get_cardinalities()
        ts_isax = ISAXUtils().create_isax_sequence_based_on_seq_array(ts,ar_cards)
        # Here we could have a debug instances
        # self.debug_instances
        isax_hash = ts_isax.get_index_hash()
        # termination check
        if(self.key.get_index_hash() == isax_hash):
            if(self.ar_instances.has_key(str(ts))):
                return self.ar_instances[str(ts)]

        # There is no such similar result
        return None