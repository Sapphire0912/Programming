#include <iostream>
#include <cstring>
using namespace std;

int main()
{
  char str1[]="Lazy Boy";
  char str2[]="Cute Girl";
  char str3[]="Pink Panther";
  cout << "�� 1 �Ӧr��G" << str1 << '\n'
       << "�� 2 �Ӧr��G" << str2 << '\n'
       << "�� 3 �Ӧr��G" << str3 << endl;

  strcpy(str2,str1);    // �N�r��1 �ƻs��r�� 2
  cout << "�N�� 1 �Ӧr������ƻs��� 2 �Ӧr��G" << '\n'
       << "�� 2 �Ӧr��G" << str2 << endl;

  int n;
  cout << "�n�ƻs�� 1 �Ӧr�ꪺ�e�X�Ӧr����� 3 �Ӧr��G";
  cin >> n;
  strncpy(str3,str1,n); // �N�r�� 1 ���e n �Ӧr���ƻs��r�� 3
  cout << "�N�� 1 �Ӧr��e " << n << " �Ӧr�ƻs��� 3 �Ӧr��G"
       << "\n�� 3 �Ӧr��G" << str3;
}
