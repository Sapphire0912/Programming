#include<iostream>
using namespace std;

class Time {
public:                 // �w�]�غc�禡�N�ɶ��]�� 12 �I��
  Time() { hour = 12; min = 0; sec = 0; };
  void show()
  {
    cout << hour << "�I" << min << "��" << sec << "��" << endl;
  }
private:
  int hour, min, sec;   // �N��ɤ�������
};

void main()
{
  Time t[3];             // �إߧt 3 �� Time ���󪺰}�C
  for (int i =0;i<3;i++) // �ΰj����ܨC�Ӫ��󪺮ɶ�
    t[i].show();
}
