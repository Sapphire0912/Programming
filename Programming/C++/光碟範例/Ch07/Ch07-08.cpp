#include <iostream>
#include <cstring>
using namespace std;

int main()
{
  char str1[60];   // ���ŧi��ӥΥH�s��
  char str2[60];   // �ϥΪ̿�J�r�ꪺ�}�C

  cout << "�п�J�� 1 �Ӧr��G";
  cin.getline(str1,80);      // �� cin �i���o�@��檺��J���e
  cout << "�п�J�� 2 �Ӧr��G";
  cin.getline(str2,80);      // �� cin �i���o�@��檺��J���e

  if(strcmp(str1,str2) == 0) // ��� str1�Bstr2 �����e�O�_�ۦP
    cout << "�⦸��J���r�ꪺ���e�ۦP";
  else
    cout << "�⦸��J���r�ꤺ�e���P";
}
