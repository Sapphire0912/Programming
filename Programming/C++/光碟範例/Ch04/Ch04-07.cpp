#include<iostream>
using namespace std;

int main()
{
  int i = 3, j = 3;

  cout << boolalpha;  // ��Τ�r���覡��X���L��

  cout << "(i == j) �G" << (i == j) << endl;
  cout << "(i > j)  �G"  << (i > j) << endl;
  cout << "(++i > j)�G"<< (++i > j) << endl;
  cout << "(j-- < 3)�G"<< (j-- < 3) << endl;
  cout << "(i != j) �G" << (i != j) << endl;
}
