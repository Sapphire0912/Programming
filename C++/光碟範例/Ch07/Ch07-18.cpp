#include <iostream>
using namespace std;
void swap(int&,int&);

int main()
{
  int a=5,b=10;
  cout << "�b main()��..." << endl;
  cout << "�洫�e a = " << a << "  b = " << b << endl;
  cout << "�ܼ� a ����}�� " << &a << endl;
  cout << "�ܼ� b ����}�� " << &b << endl;

  swap(a,b); // �I�s�禡, �ñN�ܼ� a,b ���Ѽ�
  cout << "\n�b main()��..." << endl;
  cout << "�洫�� a = " << a << "  b = " << b << endl;
}

void swap(int &i,int &j)    // �N��Ѽƭȹ�ժ��禡
{
  int temp;         // �Ȧs�ܼ�
  temp = i;
  i = j;
  j = temp;
  cout << "\n�b swap() �禡��..." << endl;
  cout << "�洫�� i = " << i << "  j = " << j << endl;
  cout << "�ܼ� i ����}�� " << &i << endl;
  cout << "�ܼ� j ����}�� " << &j << endl;
}
