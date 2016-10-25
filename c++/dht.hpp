#pragma once

#include <cmath>
#include <string>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <vector>
#include <map>
#include <openssl/sha.h>
using namespace std;

struct subkey {
  // length in bits
  int l;
  vector<char> data;

  subkey(const string & d, int l_): l(l_) {
    // length in bytes
    int bl = ceil((double) l / 8);
    data.insert(data.begin(), d.begin(), d.begin()+bl);

    int r = l % 8;
    unsigned char f = 0xff << (8 - r);

    char b = data.back();

    data.pop_back();
    data.push_back(b & f);
  }

  friend bool operator<(const subkey &a, const subkey& b) {
    if (a.l < b.l)
      return true;
    if (b.l > a.l)
      return false;
    return a.data < b.data;
  }

  friend ostream& operator<<(ostream & o, subkey sk) {

    stringstream ss;

    for ( char d : sk.data ) {
      ss << hex << std::setfill ('0') << std::setw(2);
      ss << (int)d;
    }
    return o << "(" << sk.l << ", " << ss.str() << ")";
  }

};


string sha256(const string str)
{
  unsigned char hash[SHA256_DIGEST_LENGTH];
  SHA256_CTX sha256;
  SHA256_Init(&sha256);
  SHA256_Update(&sha256, str.c_str(), str.size());
  SHA256_Final(hash, &sha256);
  stringstream ss;
  for(int i = 0; i < SHA256_DIGEST_LENGTH; i++)
  {
    ss << hex << setw(2) << setfill('0') << (int)hash[i];
  }
  return ss.str();
}

string sha256int(const int i) {
  stringstream ss;
  ss << i;
  return sha256(ss.str());
}

void subkeys(const string & str, std::vector<subkey> & subkeys) {
  subkeys.clear();
  for (int i = str.size() * 8; i >0; --i) {
    subkeys.emplace_back(str, i);
  }
}

template <typename value_t>
struct ht {
  vector<subkey> sks;

  // This map checks if there is a solt in a subkey
  map<subkey, int> p;
  
  // This map checks if there is the key in the dataset
  typedef map<string, value_t> map_t;
  map_t ks;
  
  int max;

  string k;
  ht(string k_, int max_): 
    k(k_), 
    max(max_) 
  {
    subkeys(k, sks);
    for(auto s : sks) {
      p[s] = max;
    }
  }

  typename map_t::iterator getItem(string k) {
    return ks.find(k);
  }
  typename map_t::iterator end() {
    return ks.end();
  }

  void setItem(string new_k, value_t new_v) {
    if (ks.find(new_k) == ks.end()) {
      vector<subkey> sks_i;
      subkeys(new_k, sks_i);
      for(auto sk : sks_i) {
        auto f = p.find(sk);
        if(f != p.end() && f->second >0) {
          p[sk] -= 1;
          ks[new_k] = new_v;
          break;
        }
      }
    }
  }

};

template <typename value_t>
struct dht {
  string h;
  ht<value_t> t;

  typedef typename ht<value_t>::map_t map_t;

  dht(int k_, int max_): 
    h(sha256int(k_)), 
    t(h,max_) 
  {}

  typename map_t::iterator getItem(int k) {
    return t.getItem(sha256int(k));
  }

  typename map_t::iterator end() {
    return t.end();
  }


  void setItem(int new_k, value_t new_v) {
    t.setItem(sha256int(new_k), new_v);
  }

};

struct N {
  int key;
  vector<int> ns;
  dht<int> d;
  N(int n_, int max) : key(n_), d(n_, max) {}

  void connect(const N & o) {
    d.setItem(o.key, o.key);
    //o.d.setItem(this->key, this->key);
  }

  pair<vector<int>::iterator, vector<int>::iterator>
    neighs() {
    return make_pair(ns.begin(), ns.end());
  }
};

struct Network {
  vector<N> nodes;
  int max;
  int seed;
  Network(int max_): max(max_), seed(0) {
  }

  void addNode() {
    nodes.push_back(N(seed++, max));
  }

  void connect(int a, int b) {
    nodes[a].connect(nodes[b]);
    // cout << "connecting " << a << " and " << b << endl;
  }

  pair<vector<int>::iterator
    , vector<int>::iterator> neighs(int n) 
  {
    return nodes[n].neighs();
  }

};

