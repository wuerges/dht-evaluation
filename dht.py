
import bitarray
import hashlib 
from itertools import repeat


class hbitarray(bitarray.bitarray):
    def __hash__(self):
        return int("2" + self.to01())

def compare(al, bl):
    p = 0
    for (a, b) in zip(al, bl):
        if a == b:
            p = 2 * p + 1
        else:
            break
    return p


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
    def __init__(self, k, s):
        self.key = k

        self.dict = dict(zip(subkeys(self.key), repeat(s)))
        self.set = {}

    def __getitem__(self, k):
        return self.set.__getitem__(k)

    def __setitem__(self, k, value):
        if not k in self.set:
            for sk in subkeys(k):
                if sk in self.dict and self.dict[sk] > 0:
                    self.dict[sk] -= 1
                    self.set[k] = value
                    break

    def __contains__(self, k):
        return k in self.set


class DHT:
    def __init__(self, d, s=1):
        self.key = bitdigest(d)
        self.ht = HT(self.key, s)

    def __getitem__(self, k, value):
        return self.ht.__getitem__(bitdigest(k),value)

    def __setitem__(self, k, value):
        return self.ht.__setitem__(bitdigest(k),value)

    def __contains__(self, k):
        return self.ht.__contains__(k)

if __name__ == "__main__":
    d = DHT("abc".encode(), 1)
    d["123123".encode()] = "123123"
    d["123124".encode()] = "123124"
    d["123125".encode()] = "123125"
    print(d.ht.set)
