#include "dht.hpp"


#include <vector>
#include <iostream>
using namespace std;

int main() {
  cout << sha256("1234567890_1") << endl;
  cout << sha256("1234567890_2") << endl;
  cout << sha256("1234567890_3") << endl;
  cout << sha256("1234567890_4") << endl;

  dht<int> d("abcde", 256);
  d.setItem("asdf", 7);
  d.setItem("asf", 8);
  auto it = d.getItem("asdf");

  if(it != d.end()) {
    cout << it->second << endl;
  }
  else {
    cout << "not found" << endl;
  }
}
