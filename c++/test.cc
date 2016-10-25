#include <string>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <vector>
#include <map>
#include <cmath>
#include <openssl/sha.h>

#include "dht.hpp"


using namespace std;


int main() {
  string s = "abcdefghijklmnopqrstuv121";

  for (int i = 1; i <= s.size(); ++i) {
    subkey sk(s, i);
    cout << "subkey: " << sk << endl;
  }
}
