#include<iostream>
using namespace std;

int main()
{
  for (int i=1;i<=10;i++) { // �� 1 �� 10 �] 10 �����j��
    if (i == 5)   // �j������� 5 ����, if ����B�⦡����
      continue;   // ���X�� 5 �����j��, �~��� 6 �����j��
    cout << i << '_';
  }
}
