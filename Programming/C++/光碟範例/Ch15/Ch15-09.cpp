#include <iostream>
using namespace std;

double fact(int n)    // ���j���禡
{
  if(n>170 || n<0)   // �p�⪺�ȤӤj�Τp�� 0
    throw n;         // �N�ѼƷ��ҥ~�ߥX
  else if (n==0)
    return 1;        // 0! ���Ȭ� 1

  double total = 1;
  for (int i=1; i<=n; i++)
    total *= i;
  return total;
}

int main()
{
  int x,y;
  cout << "���{���i�p�� C(x,y) ���զX�`��\n";

  while (true) {
    cout << "�п�J x�By ���� (��J��� 0 ����)�G";
    cin >> x >> y;
    if(x == 0)
      break;     // ��J 0 �ɸ��X�j��B�����{��

    try {
      cout << "C(" << x << ',' << y << ") = "
           << fact(x) / (fact(x-y)*fact(y)) << endl;
    }                // �yX �� Y ���զX�z���p�⤽��
    catch (int) {
      cerr << "��J���ƭȤӤj�μƭȦ��~�A�L�k�p��\n";
    }
  }
}
