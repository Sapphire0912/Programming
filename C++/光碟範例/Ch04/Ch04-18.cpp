#include <iostream>
using namespace std;

int main()
{
  int money;
  int ten,five,one;

  cout << "�п�J�z���������B�G";
  cin >> money;
  ten = money / 10;     // �p��B��w�����Ӽ�
  five = (money%10)/5;  // �p����w�����Ӽ�
  one = (money%10)%5;   // �p�����w�����Ӽ�
  cout << money << " ���@�i�I���s���G\n"
       << " �B�� " << ten << " ��\n"
       << " ��� " << five << " ��\n"
       << " ���� " << one << " ��\n";
}
