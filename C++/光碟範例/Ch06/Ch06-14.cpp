#include <iostream>
#include <cmath>
using namespace std;
#define PI   3.141592653589793     // �w�q�`�� �k

int main()
{
  cout << "����\tsin()" << endl;

  for(int i=30;i<=180;i+=30) { // �p�� 30�B60�B90...�ת�������ƭ�
    cout << i << '\t';
    cout << sin(i *PI / 180) << endl;
  }
}
