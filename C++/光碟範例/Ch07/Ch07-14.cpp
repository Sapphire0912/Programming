#include <iostream>
using namespace std;

int main()
{
  char a[3][4] = { "abc", "def", "ghi" };
  char (*str)[4] = a;       // �N�G���}�C�૬���}�C����

  for(int i=0;i<3;i++)
    cout << "���� str+" << i << " ����}�G" << (str+i)
         << "\ta[" << i << "]����}�G" << &a[i] << endl;
  cout << endl;

  for(int i=0;i<3;i++)      // �N�T�Ӧr�걵���X
    cout << str[i];
}
