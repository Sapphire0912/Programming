#include <iostream>
using namespace std;
int x=10;   // �����ܼ�

int main()
{
  int x=100;
  cout << "�����ܼ� x = " << x << '\t'
       << "�����ܼ� x = " << ::x << endl;  // �� :: �s�������ܼ�

  x += ::x++;

  cout << "�����ܼ� x = " << x << '\t'
       << "�����ܼ� x = " << ::x << endl;
}
