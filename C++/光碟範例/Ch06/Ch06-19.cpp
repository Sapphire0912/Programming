#include <iostream>
#include <cmath>
using namespace std;

inline double root(double x, int n) { return pow(x,1.0/n); }

int main()
{
  int n;
  double x;
  while (true)
  {
    cout << "�п�J�n�D n ����ڪ������(��J0�h�����{��)�G";
    cin >> x;
    cout << "�n�D�X�����(����J���)�G";
    cin >> n;

    if(x == 0 || n==0)    // ��J 0 �ɸ��X�j��B�����{��
      break;
    else if (x < 0)       // �Y x ���t��, �N���ܦ�����
      x *= -1;            // �]�i�I�s <cmath> ������Ȩ禡 abs()
    cout << x << " �� " << n << " ����ڬ� " << root(x,n) << endl;
  }
}
