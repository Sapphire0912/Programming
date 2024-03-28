#include<iostream>
using namespace std;

class Time {
public:
  Time(int,int,int);    // �u���@�ӫغc�禡
  void show()
  {
    cout << hour << "�I" << min << "��" << sec << "��" << endl;
  }
  Time& operator++();
  Time& operator--();
private:
  int hour, min, sec;   // �N��ɤ�������
};

Time::Time(int h =12 ,int m=0 , int s=0)
{
  hour = (h>=0 && h<=23) ? h:12;     // �ˬd h �O�_�b 0 �� 23 ��
  min  = (m>=0 && m<=59) ? m:0;      // �ˬd m �O�_�b 0 �� 59 ��
  sec  = (s>=0 && s<=59) ? s:0;      // �ˬd s �O�_�b 0 �� 59 ��
}

Time& Time::operator++()
{
  if (++sec == 60) {         // �Y�ܦ� 60 ��
    sec = 0;                 // �h�]�� 0 ��å[ 1 ��
    if (++min == 60) {       // �Y�ܦ� 60 ��
       min = 0;              // �h�]�� 0 ���å[ 1 �p��
       if (++hour == 24)     // �Y�ܦ� 24 ��
         hour = 0;           // �h�]�� 0 ��
    }
  }
  return *this;
}

Time& Time::operator--()
{
  if (--sec == -1) {         // �Y�ܦ� -1 ��
    sec = 59;                // �h�]�� 59 ��ô� 1 ��
    if (--min == -1) {       // �Y�ܦ� -1 ��
       min = 59;             // �h�]�� 59 ���ô� 1 �p��
       if (--hour == -1)     // �Y�ܦ� -1 ��
         hour = 23;          // �h�]�� 23 ��
    }
  }
  return *this;
}

int main()
{
  Time t1(9,59,59);
  Time t2(10);

  (++t1).show();
  (--t2).show();
}
