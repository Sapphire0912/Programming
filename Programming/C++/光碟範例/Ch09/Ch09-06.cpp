#include<iostream>
using namespace std;

class Time {
public:
  Time(int,int,int);    // �u���@�ӫغc�禡
  void show()
  {
    cout << hour << "�I" << min << "��" << sec << "��" << endl;
  }
private:
  int hour, min, sec;   // �N��ɤ�������
};

Time::Time(int h =12, int m=1, int s=1)
{
  hour = (h>=0 && h<=23) ? h:12;     // �ˬd h �O�_�b 0 �� 23 ��
  min  = (m>=0 && m<=59) ? m:0;      // �ˬd m �O�_�b 0 �� 59 ��
  sec  = (s>=0 && s<=59) ? s:0;      // �ˬd s �O�_�b 0 �� 59 ��
}

int main()
{
  Time t1;           // ���[�Ѽ�
  Time t2(10);       // �@�ӰѼ�
  Time t3(8,24);     // �G�ӰѼ�
  Time t4(10,20,30); // �T�ӰѼ�

  t1.show();   t2.show();
  t3.show();   t4.show();
}
