#include<iostream>
using namespace std;

int main()
{
  int i = 3;
  bool b = false;

  cout << boolalpha;  // ��Τ�r���覡��X���L��
  cout << "i = " << i << "\tb =" << b << endl;
  cout << "i && b�G" << (i && b) << endl;
  cout << "i || b�G" << (i || b) << endl;
  cout << "i &&!b�G" << (i &&!b) << endl;
  cout << "i ||!b�G" << (i ||!b) << endl;
}
