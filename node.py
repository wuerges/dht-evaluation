
import dht
import networkx as nx
import scipy
from random import shuffle
from copy import copy

number_of_nodes = 1000

class N:
    def __init__(self, name):
        self.name = name
        self.dht = dht.DHT(str(name).encode(), 1)

    def connect(self, o):
        self.dht.ht[o.dht.key] = o.name

    def __repr__(self):
        return "%s" % self.dht.key[:10]


def compare(al, bl):
    p = 0
    for (a, b) in zip(al, bl):
        if a == b:
            p = 2 * p + 1
        else:
            break
    return p

def lookup(n0, r, network, y):
    worklist = list(nx.all_neighbors(network, n0))
    best = worklist.pop()
    results = set([best])
    while worklist:
        #print("Worklist", worklist)
        n = worklist.pop()
        ns = list(nx.all_neighbors(network, n))
        results.update(ns)
        results.add(n)
        for ni in [n] + ns:
            if compare(ni.dht.key, r.dht.key) > compare(best.dht.key, r.dht.key):
                best = ni
                worklist.append(ni)

    results = list(results)
    results.sort(key=lambda x : compare(x.dht.key, r.dht.key), reverse=True)

    for res in results[:y]:
        print("Result", res, r, compare(res.dht.key, r.dht.key))
    return results[:y]




#g = networkx.erdos_renyi_graph(number_of_nodes, edge_probability)

nodes = [N(n) for n in range(number_of_nodes)]
g = nx.Graph()
for n in nodes:
    g.add_node(n)

shuffled_nodes = copy(nodes)
shuffle(shuffled_nodes)


for ni in nodes:
    for nj in shuffled_nodes:
        ni.connect(nj)


for ni in nodes:
    for nj in nodes:
        if ni.dht.key in nj.dht: # and nj.dht.key in ni.dht:
            g.add_edge(ni, nj)




