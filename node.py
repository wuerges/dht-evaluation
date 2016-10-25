
import dht
import networkx
import scipy
import sys
from random import shuffle
from copy import copy

number_of_nodes = int(sys.argv[1])


class N:
    def __init__(self, name):
        self.name = name
        self.dht = dht.DHT(str(name).encode())

    def connect(self, o):
        o_key = str(o.name).encode()
        self.dht[o_key] = o.name

    def lookup():
        pass


#g = networkx.erdos_renyi_graph(number_of_nodes, edge_probability)

nodes = [N(n) for n in range(number_of_nodes)]

shuffled_nodes = copy(nodes)
shuffle(shuffled_nodes)


for ni in nodes:
    for nj in shuffled_nodes:
        ni.connect(nj)
