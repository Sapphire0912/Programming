#include<iostream>
using namespace std;

class Car {   // �w�q���O
public:       // �H�U�������O��~���}��
  double gas; // ���o�q
  double eff; // �C���ɥi��p������
};

int main()
{
  Car superone;
  superone.eff = 30;
  superone.gas = 20;
  cout << "�W�Ŭ٪o��1���ɥi�] " << superone.eff
       << " ����" << endl;
  cout << "�{�b�o�c�� " << superone.gas << " ���ɪo" << endl;

  float kilo;
  while(superone.gas > 0) {   // �Y�٦��o
    cout << "�{�b�n�}�X�����G";
    cin >> kilo;
    if (superone.gas >= (kilo/superone.eff)) { // �Y�o�q��
      superone.gas -= kilo/superone.eff;       // ��α����o�q
      if (superone.gas == 0)                   // �Y�o�Χ��F
        cout << "�S�o�F�I";
      else
        cout << "�o�c�٦� " << superone.gas << " ���ɪo" << endl;
    } else {                                   // �Y�o�q����
      cout << "�o�q�����A�ثe���o�u���] "
           << (superone.gas * superone.eff) << " ����";
      break;
    }
  }
}
