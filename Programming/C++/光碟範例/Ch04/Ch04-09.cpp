#include<iostream>
using namespace std;

int main()
{
  int i = 3, j = 0;

  cout << boolalpha; // ��Τ�r���覡��X���L��

  cout << "i = " << i << "\tj =" << j << endl;
  cout << "i || (j++)�G" << (i || (j++)) << endl;
  cout << "i = " << i << "\tj =" << j << endl;

  cout << "j && (++i)�G" << (j && (++i)) << endl;
  cout << "i = " << i << "\tj =" << j << endl;
}
