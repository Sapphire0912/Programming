#include<iostream>
using namespace std;

int main()
{
  for (int x=1; x < 10; x++) {  // �~�j��, x ���ȥ� 1 �� 9
    for (int y=1; y < 10; y++)  // ���j��, y ���ȥ� 1 �� 9
      cout << x << '*' << y << '=' << x*y << '\t';
    cout << endl;               // �~�j��C����@���N����
  }
}
