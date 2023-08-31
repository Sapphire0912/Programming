#include<iostream>
#include<cstring>
#include<cctype>
using namespace std;

class Str {          // ���K���r�����O
  friend ostream& operator<<(ostream&, const Str&);  // ��X�� cout
  friend istream& operator>>(istream&, const Str&);  // �� cin ��J
public:
  Str(const Str&);
  Str(const char * ptr);
  Str(int);
  ~Str() { delete [] data; }  // �Ѻc�禡
  bool operator!() { return len==0; }  // �Y�r����׬� 0 �Y�Ǧ^�u
  Str operator+();    // �N�r���ܦ��j�g
  Str operator-();    // �Y�r���ܦ��p�g
  Str operator+(Str); // �u�w�q�@�ت���
private:
  char *data;         // ���V�r�ꪺ����
  int len;            // �r�����
};

ostream& operator<<(ostream& o, const Str& s)
{                                               
   return o << s.data; // �Ǧ^�N�r�����п�X�� cout �����G
}                                               
                                                
istream& operator>>(istream& i, const Str& s)
{                                               
   return i.getline(s.data,80); // �Ǧ^�� cin ��J�r�����Ъ����G
}                                               

Str::Str(const char *s)
{
   len = strlen(s);
   data = new char[len+1];   // �t�m�s���O����Ŷ�
   strcpy(data, s);          // �N�r�ꤺ�e�ƻs��s���Ŷ�
}

Str::Str(int n=0)           // �u�����w�r����ת��غc�禡
{
  if ( n < 0)               // �Y�ѼƭȬ��t
    n = 0;                  // �N���׳]�� 0
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

Str Str::operator+()
{
  char* temp = new char[len];
  strcpy(temp,data);
  for(int i=0; i<len; i++)   // �N�r���ܦ��j�g���j��
    temp[i]=toupper(temp[i]);// �I�s�禡�N�r���ܦ��j�g
  return Str(temp);
}

Str Str::operator-()
{
  char* temp = new char[len];
  strcpy(temp,data);
  for(int i=0; i<len; i++)   // �N�r���ܦ��j�g���j��
    temp[i]=tolower(temp[i]);// �I�s�禡�N�r���ܦ��j�g
  return Str(temp);
}

Str Str::operator+(Str s)
{
  Str tmp(len + s.len);      // ���إ߼Ȧs����
                             // �]�w���׬���r�ꪺ���שM
  strcpy(tmp.data, data);    // �ƻs�e�b�r��
  strcat(tmp.data, s.data);  // �ƻs��b�r��
  return tmp;  // �N�걵�����G�Ǧ^, �H�ѻP���򪺹B��
}
