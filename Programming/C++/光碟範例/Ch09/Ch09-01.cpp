#include<iostream>
using namespace std;

class Time {
public:                 // �غc�禡�u��X�@�q�T��
  Time() { cout << "...���b���� Time ���غc�禡" << endl; };
private:
  int hour, min, sec;   // �N��ɤ�������
};

void main()
{
  cout << "�ŧi t1�Bt2 ����" << endl;
  Time t1, t2;
  cout << "�ŧi������� t3" << endl;
  Time* t3;  // �sĶ���|��o��ԭz�o�Xĵ�i, �������z�|
  cout << "�w�q������� t4" << endl;
  Time* t4 = new Time;
}
