#include<iostream>
using namespace std;

int main()
{
  int season;
  cout << "�п�ܩu�`�G1.�K 2.�L 3.�� 4.�V�G";
  cin >> season;

  switch (season)
  {
    case 1:  // �� season ���ƭȬ� 1
      cout << "�Ь�۪��S�X��";
      break; // ������ case
    case 2:  // �� season ���ƭȬ� 2
      cout << "�Ь�۵u�S�X��";
      break; // ������ case
    case 3:  // �� season ���ƭȬ� 3
      cout << "�Х[����S�����~�M�X��";
      break; // ������ case
    case 4:  // �� season ���ƭȬ� 4
      cout << "�Ь�ۤ��Τj��X��";
      break; // ������ case
  }
}
