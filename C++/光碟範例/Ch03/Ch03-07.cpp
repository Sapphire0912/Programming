#include<iostream>
using namespace std;

int main()
{
  float f_pi;
  double d_pi;
  // �N��P�v�ȫ��w���ܼ�
  f_pi  = 3.1415926535897932f;
  d_pi  = 3.1415926535897932;

  cout.precision(17);
  cout << "f_pi = "  << f_pi  << endl
       << "d_pi = "  << d_pi  << endl;
}
