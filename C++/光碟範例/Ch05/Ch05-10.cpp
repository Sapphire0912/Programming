#include<iostream>
using namespace std;

int main()
{
  int choice;
  cout << "�ڭ̦��|���\, �п�ܡG\n";
  cout << "1.�����\ 2.�~���\ 3.�_�q���\ 4.�����\�G";
  cin >> choice;

  switch (choice) {
    case 1: // �����\���� 109 ��
      cout << "�z�I���\�I������ 109 ��";
      break;
    case 2: // �~���\�M�_�q���\�P��
    case 3: // �_�q���\������ 99 ��
      cout << "�z�I���\�I������ 99 ��";
      break;
    case 4: // �����\������ 69 ��
      cout << "�z�I���\�I������ 69 ��";
      break;
  }
}
