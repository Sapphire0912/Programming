#include<iostream>
using namespace std;

int main()
{
  int i;

  i = 1 + 3 * 5 >> 1; // �۷�� 16 >> 1 -> 8
  cout << "i = " << i << endl;

  i = 8 / 2 << 1;     // �۷�� 4 << 1 -> 8
  cout << "i = " << i << endl;
}
