#include <iostream>
using namespace std;

long double fact(int n)  // ���j���禡
{
   if(n == 1)            // �b n==1 �ɰ���U���j
     return 1;           // �Ǧ^ 1
   else
    return ( n * fact(n-1));   // �N�Ѽƴ� 1 �A�I�s�ۤv
}

int main()
{
   int x;
   while (true) {
     cout << "�п�J�@�p��170�����(��J0�����{��)�G";
     cin >> x;
     if(x == 0) break;    // ��J 0 �ɸ��X�j��B�����{��
     cout << x << "! = " << fact(x) << endl;
   }
}
