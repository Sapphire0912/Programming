#include <iostream>
using namespace std;
double f;       // �Ψ��x�s�ؤ�ūת������ܼ�

double FtoC (void)          // ���ݶǻ��Ѽ�
{
  return (f - 32) * 5 / 9;  // �s�������ܼ�
}

int main()
{
  cout << "�п�J�ؤ󪺷ūסG";
  cin >> f;                 // �N��J���Ȧs�J�����ܼ�

  cout << "���⦨���ū׬� " << FtoC() << " ��";
}
