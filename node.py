
from itertools import permutations
import dht
import networkx as nx
import scipy
import sys
from random import shuffle
from copy import copy

number_of_nodes = int(sys.argv[1])
number_of_rs = int(sys.argv[2])
#value_of_y = int(sys.argv[3])
#value_of_k = int(sys.argv[4])

class N:
    def __init__(self, name):
        self.name = name
        self.dht = dht.DHT(str(name).encode(), 1)

    def __hash__(self):
        return self.name

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
    visited = set()
    while worklist:
        #print("Worklist", worklist)
        n = worklist.pop()
        visited.add(n)
        ns = list(nx.all_neighbors(network, n))
        results.update(ns)
        results.add(n)
        for ni in [n] + ns:
            if ni not in visited:
                if compare(ni.dht.key, r) > compare(best.dht.key, r):
                    best = ni
                    worklist.append(ni)

    results = list(results)
    results.sort(key=lambda x : compare(x.dht.key, r), reverse=True)

    #for res in results[:y]:
    #    print("Result", res.dht.key, r, compare(res.dht.key, r))
    return results[:y]

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


class S:
    def __init__(self):
        self.vs = []

    def add(self, v):
        self.vs.append(v)

    def avg(self):
        return float(sum(self.vs)) / len(self.vs)

    def min(self):
        return min(self.vs)

    def max(self):
        return max(self.vs)

def do_the_maths(value_of_y):
    i_size = value_of_y

    s1 = S()
    s2 = S()

    qs = []

    for ri in range(number_of_rs):
        q = set(lookup(nodes[0], dht.bitdigest(str(ri).encode()), g, value_of_y))
        qs.append(q)
        for ni in nodes[1:]:
            qi = lookup(ni, dht.bitdigest(str(ri).encode()), g, value_of_y)
            q &= set(qi)

        s1.add(len(q))

        count = 0
    for [q1, q2] in permutations(qs, 2):
        count += 1
        if count > 100:
            break
        s2.add(len(set(q1) & set(q2)))

        #print("Result set: ", len(q), q)
        #print("    intersection betwen results", len(it1 & it0), it1 & it0)
        #print()
    print(value_of_y, "\t", s1.avg(), "\t", s1.max(), "\t", s1.min(), "\t", s2.avg(), "\t", s2.max(), "\t", s2.min())

print("y\t avg s1\t max s1\t min s1\t avg s2\t max s2\t min s2")
for y in range(4,20):
    do_the_maths(y)

