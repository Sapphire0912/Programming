#include <iostream>
#include <cstring>
#include <cctype>       // �ϥ� toupper() �ݧt�A����
using namespace std;

char *toUpper(const char *);   // �ŧi�禡�Ǧ^�Ȭ��r������

int main(void)
{
  cout << toUpper("happy Birthday");
}

char *toUpper(const char* ptr)        // �N�r��Ҧ��p�g�r��
{                                     // �ন�j�g���禡
  unsigned len = strlen(ptr);
  char *newStr = new char[len];       // �إߤ@�s�r��
  for(unsigned i=0;i<len;i++)
    *(newStr+i) = toupper(*(ptr+i));  // �N�r���ন�j�g

  return newStr;        // �Ǧ^�ഫ�᪺�r��
}
