#include<iostream>
using namespace std;

int main()
{
  bool test1,test2;
  test1 = true;
  test2 = 0;    // �۷��]�� false
  cout << "test1 = " << test1 << endl
       << "test2 = " << test2 << endl;

  // ��Τ�r���覡��X���L��
  cout << boolalpha;
  cout << "test1 = " << test1 << endl
       << "test2 = " << test2 << endl;
}
