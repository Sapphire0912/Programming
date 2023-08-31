#include<iostream>
#include<cstring>
using namespace std;

class Str {          // ���K���r�����O
public:
  void show() { cout << data; }
  Str(const Str&);
  Str(const char * ptr);
  Str(int);
  ~Str() { delete [] data; }  // �Ѻc�禡
  bool operator!() { return len==0; }  // �Y�r����׬� 0 �Y�Ǧ^�u
private:
  char * data;     // ���V�r�ꪺ����
  int len;         // �r�����
};

Str::Str(const char *s)
{
   len = strlen(s);
   data = new char[len+1];   // �t�m�s���O����Ŷ�
   strcpy(data, s);          // �N�r�ꤺ�e�ƻs��s���Ŷ�
}

Str::Str(int n=0)           // �u�����w�r����ת��غc�禡
{
  if ( n < 0)               // �Y�ѼƬ��t��
    n = 0;                  // �N�N���׳]�� 0
  len = n;
  data = new char[len+1];
  for(int i=0; i<n; i++)     // �N�s�t�m���Ŷ���W�ť�
    data[i] = ' ';
  data[n] = 0;               // �b�r��̫᭱�[�W�����r��
}

Str::Str(const Str& s)
{
  len = s.len;               // �ƻs�r�����
  data = new char[len+1];    // ���t�m�s�Ŷ�
  strcpy(data, s.data);      // �A�ƻs�r��
}
