#include<iostream>
using namespace std;

int main()
{
  unsigned int i;  // �ܼ� i �u��O������Ʃ� 0
  short j;  // �ٲ� "int" ����r
  long  k;  // �ٲ� "int" ����r
  unsigned long  l;  // �ٲ� "int" ����r
  i = 1999;
  j = 32767;
  k = 2147483648;  // �G�N�]�� long �̤j�ȥ[ 1
  l = 4294967295;
  cout << i << ' ' << j << ' ' << k << ' ' << l << endl;
}
