#include<iostream>
using namespace std;

class Time {
  friend Time& operator++(Time&);
  friend Time& operator--(Time&);
public:
  Time(int,int,int);    // �u���@�ӫغc�禡
  void show()
  {
    cout << hour << "�I" << min << "��" << sec << "��" << endl;
  }
private:
  int hour, min, sec;   // �N��ɤ�������
};

Time::Time(int h =12 ,int m=0 , int s=0)
{
  hour = (h>=0 && h<=23) ? h:12;     // �ˬd h �O�_�b 0 �� 23 ��
  min  = (m>=0 && m<=59) ? m:0;      // �ˬd m �O�_�b 0 �� 59 ��
  sec  = (s>=0 && s<=59) ? s:0;      // �ˬd s �O�_�b 0 �� 59 ��
}

Time& operator++(Time& t)            // �٦�禡
{
  if (++t.sec == 60) {
    t.sec = 0;
    if (++t.min == 60) {
       t.min = 0;
       if (++t.hour == 24)
         t.hour = 0;
    }
  }
  return t;                          // �Ǧ^����
}

Time& operator--(Time& t)            // �٦�禡
{
  if (--t.sec == -1) {
    t.sec = 59;
    if (--t.min == -1) {
       t.min = 59;
       if (--t.hour == -1)
         t.hour = 23;
    }
  }
  return t;                          // �Ǧ^����
}

int main()
{
  Time t1(9,59,59);
  Time t2(10);

  (++t1).show();
  (--t2).show();
}
