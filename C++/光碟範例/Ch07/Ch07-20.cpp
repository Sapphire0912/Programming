#include <iostream>
#include <cstdlib>
using namespace std;

long double fact(int n) // ���j���禡
{
   if(n == 1)           // �b n==1 �ɰ���U���j
     return 1;          // �Ǧ^ 1
   else
    return ( n * fact(n-1));   // �N�Ѽƴ� 1 �A�I�s�ۤv
}

int main(int argc, char *argv[])
{
   if (argc > 1)        // �Y���R�O�C�Ѽ�
     for(int i=1;i<argc;i++) {
       int f = atoi(argv[i]);
       cout << f << "! = " << fact(f) << endl;
     }
   else                 // �Y�S���[�ѼƴN��X�ϥλ���
     cout << "�Ϊk�G\"�{���W�� �Ʀr\"" << endl;
}
