#include<iostream>
using namespace std;

int main()
{
  int range;
  cout << "�п�J�n�M�䪺�d��G";
  cin >> range;

  int count = 0;             // �Ψӭp��@���X�ӽ��

  for (int i=2;i<=range;i++) {
    bool isPrime = true;     // ��ܥثe�� i �O�_����ƪ����L��

    for (int j=2;j<i;j++)    // �����k�B�⪺���j��
      if ((i%j) == 0) {      // �l�Ƭ� 0 ��ܥi�H�㰣,
        isPrime = false;     // �ҥH���O���,
        break;               // �]�����~�򰣤F
      }

    if (isPrime) {           // �Y�O���, �Y��X�Ӽƭ�
      cout << i << '\t';
      count++;
      if ((count%5) == 0)   // �]�w�C��X���ӽ�ƴN����
        cout << endl;
    }
  }

  cout << "\n�p�󵥩� "  << range << " ����Ʀ@�� "
       << count << " ��";
}
