#include<iostream>
#include<iomanip>
using namespace std;

int main()
{
  cout.fill('*');   // ��R�r���]�� '*'
  cout << setw(8) << -1000    << endl;
  cout << setw(8) << internal << -1000 << endl;
  cout << setw(8) << left     << -1000 << endl;

  cout.width(9);    // �]�w�e�׬� 9 �Ӧr��
  cout << setfill('_') << "Good" << endl; // ���O�V�����
  cout.width(9);    // �]�w�e�׬� 9 �Ӧr��
  cout << internal << "Good" << endl
       << right    << "Good" << endl;  // �걵��X
}
