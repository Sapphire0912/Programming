#include <iostream>
#include <cstring>   // �]���Ψ� strlen(), �G�t�A���ɮ�
using namespace std;

int main()
{
  char name[80];

  cout << "�п�J�@�r��G";
  cin.getline(name,80);      // �� cin �i���o�@��檺��J���e

  cout << "sizeof(name) = " << sizeof(name) << endl;
  cout << "strlen(name) = " << strlen(name) << endl;
}
