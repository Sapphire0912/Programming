#include <iostream>
using namespace std;

void FtoC (double f)      // �N�ؤ�ū��ন��󪺨禡
{
  cout << "���⦨���ū׬� "
       <<  ((f - 32) * 5 / 9) << " ��";  // �ū��ഫ�������⦡
}

int main()
{
  double x;
  cout << "�п�J�ؤ󪺷ūסG";
  cin >> x;
  FtoC(x);               // �� x ���ѼƩI�s FtoC()
}
