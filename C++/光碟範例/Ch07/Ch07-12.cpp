#include <iostream>
#include <cstring>
using namespace std;

int main()
{
  char str[]="How are you?";
  char *ptr = str;

  for (unsigned i=0;i<strlen(str);i++)
    cout << *(str+i); // �N�}�C�W�� str ������
  cout << endl;

  for (unsigned i=0;i<strlen(ptr);i++)
    cout << ptr[i];   // �N���� ptr ���}�C�W�٨ϥ�
}
