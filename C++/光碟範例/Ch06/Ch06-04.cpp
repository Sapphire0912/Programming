#include <iostream>
using namespace std;

double newV(double t, double a=9.8, double v0 = 0)
{                     // ��ӰѼƦ��w�]��
  return v0 + a*t;
}

int main()
{
  cout << "�t�׻P�[�t�ת��p��ܽd�GV=V0+at" << endl;

  cout << "�Y V0 = 100, a = 2.8, t =15, �h "
       << "V = " << newV(15,2.8,100) << endl;

  cout << "�Y V0 = 0  , a = 9.8, t =15, �h "
       << "V = " << newV(15);  // �u�Ǥ@�ӰѼ�
}
