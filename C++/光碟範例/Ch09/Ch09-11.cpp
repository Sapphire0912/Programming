#include<iostream>
#include "Ch09-09.h"    // �����Ϋe���d�Ҫ��t�A��
using namespace std;

class Account {         // �s�ڱb�����O
public:
  Account(char *, double); // �ŧi�ɤ��Υ[�W������l�Ʀ�C
  void show();
private:
  Str name;             // �b��W�٬O Str ���O������
  double balance;       // �b��l�B
};

Account::Account(char *s, double d) : name(s)
{               // name �����O�b������l�Ʀ�C���]�w��
  balance = d;  // �b�غc�禡���u�����w�b��l�B
}

void Account::show()
{
  name.show();
  cout << "���b���٦� " << balance << " ��";
}

int main()
{
  Account mary("���O",5000); // �غc�b�᪫��
  mary.show();               // ��ܱb���T
}
