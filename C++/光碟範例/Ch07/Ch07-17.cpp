#include <iostream>
using namespace std;
void swap(int*,int*);

int main()
{
  int a=5,b=10;
  cout << "�b main()��..." << endl;
  cout << "�洫�e a = " << a << "  b = " << b << endl;
  cout << "�ܼ� a ����}�� " << &a << endl;
  cout << "�ܼ� b ����}�� " << &b << endl;

  swap(&a,&b); // �I�s�禡, �ñN�ܼ� a,b ����}���Ѽ�
  cout << "�b main()��..." << endl;
  cout << "�洫�� a = " << a << "  b = " << b << endl;
}

void swap(int *a,int *b)    // �N��Ѽƭȹ�ժ��禡
{
  int temp;         // �Ȧs�ܼ�
  temp = *a;
  *a = *b;
  *b = temp;
  cout << "�b swap() �禡��..." << endl;
  cout << "�洫�� a = " << *a << "  b = " << *b << endl;
  cout << "�ܼ� a ����}�� " << a << endl;
  cout << "�ܼ� b ����}�� " << b << endl;
}
