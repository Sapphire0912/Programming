#include<iostream>
using namespace std;

int main()
{
  while(true) {
    cout << "�п�J 1-170 �������(��J 0 �Y�����{��)�G";
    int num = 0;
    cin >> num;

    if (num == 0)
      break;          // �Y�ϥΪ̿�J 0, �N���X�j��

    cout << num << "! ���� ";

    double fact;            // �Ψ��x�s�B�p�ⶥ���Ȫ��ܼ�
    for(fact=1;num>0;num--) // �p�ⶥ�����j��
      fact = fact * num;    // �C���ұN fact ���W�ثe�� num

    cout << fact << "\n\n"; // ��X�p��ұo��������
  }
  cout << "���±z�ϥζ����p��{���C";
}
