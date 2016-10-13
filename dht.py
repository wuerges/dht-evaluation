
import bitarray
import hashlib 
from itertools import repeat


class hbitarray(bitarray.bitarray):
    def __hash__(self):
        return int("2" + self.to01())



def digest(s):
    h = hashlib.sha256()
    h.update(s)
    return h.digest()

def bitdigest(s):
    h = hbitarray()
    h.frombytes(digest(s))
    return h


def subkeys(k):
    for i in range(len(k), -1, -1):
        yield k[:i]


class HT:
    def __init__(self, k):
        self.key = k

        self.dict = dict(zip(subkeys(self.key), repeat(True)))
        self.set = {}

    def __getitem__(self, k):
        return self.set.__getitem__(k)

    def __setitem__(self, k, value):
        if not k in self.set:
            for sk in subkeys(k):
                if self.dict.get(sk):
                    self.dict[sk] = False
                    self.set[k] = value
                    break

class DHT:
    def __init__(self, d):
        self.key = bitdigest(d)
        self.ht = HT(self.key)

    def __getitem__(self, k, value):
        return self.ht.__getitem__(bitdigest(k),value)

    def __setitem__(self, k, value):
        return self.ht.__setitem__(bitdigest(k),value)

