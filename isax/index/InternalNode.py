from ISAXUtils import ISAXUtils
import Sequence as sq
from NodeType import NodeType
from IndexHashParams import IndexHashParams
import SortedCollection as treemap
from operator import itemgetter
from TerminalNode import TerminalNode

##
# 
# An internal node designates a split in SAX space and is created when the number of time series
# contained by a terminal node exceeds th. The internal node splits the SAX space by promotion of
# cardinal values along one or more dimensions as per the iterative doubling policy.
# 
# A hash from iSAX words (representing subdivisions of the SAX space) to nodes is maintained to
# distinguish differentiation between entries.
# 
# Time series from the terminal node which triggered the split are inserted into the newly created
# internal node and hashed to their respective locations.
# 
# If the hash does not contain a matching iSAX entry, a new terminal node is created prior to
# insertion, and the hash is updated accordingly. For simplicity, we employ binary splits along a
# single dimension, using round robin to determine the split dimension.
# 
# 
# 
# Root Node
# 
# The root node is representative of the complete SAX space and is similar in functionality to an
# internal node. The root node evaluates time series at base cardinality, that is, the granularity
# of each dimension in the reduced representation is b. Encountered iSAX words correspond to some
# terminal or internal node and are used to direct index functions accordingly.
# 
# Java author jpatterson
# Python author Xingchi Dai
#

class InternalNode:
    def __init__(self,isax_base_rep, params, nt):
        self.params = params
        self.type = nt
        self.key = isax_base_rep
        self.descendants = treemap.SortedCollection(key=itemgetter(0))


    def get_masked_representation(self):
        return self.params.create_masked_bits_sequence(self.key)


    def get_child_node_iterator(self):
        # This impl should not return anything since the internal nodes never actual hold instances
        return None

    def insert(self,ts_inst):
        """
         /**
           *
           * When a split occurs in SAX space, we turn a terminal node into an internal node, which then
           * changes how it handles inserts: example: internal node A now points to B and C
           *
           * node A's SAX key stays the same, yet B and C have a split in SAX space based on increasing the
           * dim on the lowest cardinality in the array of symbols: 0^2 becomes 00^4 and 01^4, where 1^2
           * becomes 10^4 and 11^4
           *
           * when we insert a new ts in this internal node, we hash at the card of its key (params)
           *
           * if this new hash rep of the ts is in the hash-table, we pass it on to that node for insertion
           *
           *
           */

        :param ts_inst:
        :return:
        """
        ts_isax = None
        assert ts_inst is not None, "null ts"
        if(self.type == NodeType.ROOT):
            ts_isax = ISAXUtils().create_isax_sequence(ts_inst.ts,self.params.base_card,
                                                    self.params.isax_word_length)
        else:
            # if the node type is not root
            ar_cards = IndexHashParams().generate_child_cardinality(self.key.get_cardinalities())
            assert ts_inst.ts is not None, "ts value is none"
            assert ar_cards is not None, "no cardinality pattern was found"
            ts_isax = ISAXUtils().create_isax_sequence_based_on_seq_array(ts_inst.ts,ar_cards)
        assert ts_isax is not None,"failed to insert"
        isax_hash = ts_isax.get_index_hash()
        # we want to fan out at a rate of 2d
            # check if the current children nodes have such time - series
        node = self.descendants.find(isax_hash)

        # print "I found tihe node", node
        if node is not None:

            node = node[1] # get he node value

            if(node.type == NodeType.TERMINAL):
                # Does it need to split
                if(node.is_over_threshold() == False):
                    node.insert(ts_inst)
                else:
                    # need to split the node
                    new_node = InternalNode(node.key,node.params,NodeType.INTERNAL)
                    new_node.insert(ts_inst)
                    itr = node.get_node_instances_iterator()
                    assert itr is not None,"itr is none, double check"
                    for ele in itr:
                        str_key = str(ele)
                        new_node.insert(node.get_node_instance_by_key(str_key))
                    self.descendants.remove_key(isax_hash)
                    self.descendants.insert([isax_hash,new_node])
            elif(node.type == NodeType.INTERNAL):
                node.insert(ts_inst)

        elif(node is None):
            # If it doesn'e contain this code, create a new one
            node = TerminalNode(ts_isax,self.params)
            node.insert(ts_inst)
            self.descendants.insert([isax_hash,node])

            # self.descendants.insert([isax_hash, node])
            # print node.get_node_instances_iterator()


    def debug_child_nodes(self):
        # get the key set
        i = self.descendants._getkey()
        if(self.type == NodeType.ROOT):
            print "debugging root node"
        for ele in i:
            print "found the key:", ele




    def approx_search(self,ts):
        ts_isax = None
        node = None

        if(self.type == NodeType.ROOT):
            # lets get out SAX word based on the params of this node and key
            ts_isax = ISAXUtils().create_isax_sequence(ts,self.params.base_card,
                                                     self.params.isax_word_length)
        else:
            ar_cards = IndexHashParams().generate_child_cardinality(self.key.get_cardinalities())

            # get the isax again
            ts_isax = ISAXUtils().create_isax_sequence_based_on_seq_array(ts,ar_cards)

        isax_hash = ts_isax.get_index_hash()

        node  = self.descendants.find(isax_hash)


        if(node is None):
            return None
        else:
            node = node[1] # get the real node
            return node.approx_search(ts)



