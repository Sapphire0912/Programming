#include <iostream>
using namespace std;

inline double FtoC (double f)   // �w�q���椺�禡
{
  return (f - 32) * 5 / 9;
}

int main()
{
  double F;
  cout << "�п�J�ؤ󪺷ūסG";
  cin >> F;

  cout << "���⦨���ū׬� " << FtoC(F) << " ��";
}
