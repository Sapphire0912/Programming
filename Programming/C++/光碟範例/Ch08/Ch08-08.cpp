#include<iostream>
using namespace std;

class Time {
public:
  void set(int, int, int);
  void copy(Time source) { *this = source; } // �ƻs��Ʀ���
  void show() { cout << hour << ':' << min << ':' << sec; }
private:
  int hour, min, sec;   // �N��ɤ�������
};

void Time::set(int hour, int min, int sec)   // �ѼƦW�ٻP
{                                            // ��Ʀ����ۦP
  this->hour = hour;    // �N�Ѽ� hour ���ȫ��w����Ʀ��� hour
  this->min  = min;     // �N�Ѽ� min  ���ȫ��w����Ʀ��� min
  this->sec  = sec;     // �N�Ѽ� sec  ���ȫ��w����Ʀ��� sec
}

void main()
{
   Time t1, t2;
   t1.set(12,15,30);
   t2.copy(t1);  // �N t1 �����e�ƻs�� t2
   t2.show();
}
