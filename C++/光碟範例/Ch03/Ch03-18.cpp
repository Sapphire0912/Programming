#include <iostream>
using namespace std;

int main()
{
  int a=10, b=20;  // �ŧi��� int �ܼ� a, b
  int temp;        // �ŧi�Ȧs����ܼ� temp

  cout << "�洫�e a = " << a << "\tb = " << b << endl;

  temp = a;  // �N�ܼ� a ���ȫ��w���Ȧs�ܼ�
  a = b;     // ���ܼ� b ���ȫ��w�� a
  b = temp;  // �N�Ȧs�ܼƩҦs�� a �ȫ��w�� b

  cout << "�洫�� a = " << a << "\tb = " << b << endl;
}
