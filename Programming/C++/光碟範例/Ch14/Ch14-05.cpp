#include<iostream>
#include<iomanip>
using namespace std;
#define pi 3.1415926535897  // �w�q�`��

int main()
{
  cout << "�w�]�����Ħ�Ƭ��G" << cout.precision() << endl;
  cout << showpoint;      // ���]�w����Ƥ]�n��ܤp���I
  cout << fixed;          // �p���I��ܪk
  cout << setprecision(8) << 1234.0 << '\t';
  cout << pi << endl;

  cout << scientific;     // ��ǲŸ���ܪk
  cout << setprecision(4) << 1234.0 << '\t';
  cout << pi << endl;

  cout.precision(8);      // ��Φ����禡�]�w
  cout << scientific << 1234.0 << '\t' << pi << endl;
}
