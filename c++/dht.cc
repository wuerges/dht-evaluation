#include "dht.hpp"


#include <vector>
#include <iostream>
using namespace std;

int main() {
  cout << sha256("1234567890_1") << endl;
  cout << sha256("1234567890_2") << endl;
  cout << sha256("1234567890_3") << endl;
  cout << sha256("1234567890_4") << endl;

  dht<int> d(1, 256);
  d.setItem(2, 7);
  d.setItem(3, 8);
  auto it = d.getItem(3);

  if(it != d.end()) {
    cout << it->second << endl;
  }
  else {
    cout << "not found" << endl;
  }

  Network network(256);
  for(int i = 0; i < 1000; ++i) {
    network.addNode();
  }
  for(int i = 0; i < 1000; ++i) {
    for(int j = 0; j < 1000; ++j) {
      network.connect(i,j);
    }
  }

  return 0;
}
