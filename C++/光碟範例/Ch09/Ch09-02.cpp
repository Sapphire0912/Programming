#include<iostream>
using namespace std;

class Time {
public:                 // �غc�禡�u��X�@�q�T��
  Time() { cout << "...���b���� Time ���غc�禡" << endl; };
private:
  int hour, min, sec;   // �N��ɤ�������
};

class Clock {
public:
  Clock() { cout << "...���b���� Clock ���غc�禡" << endl; };
private:
  Time clock_time;     // �����ɶ�
  Time alarm_time;     // �x���ɶ�
};

int main()
{
  Clock old_clock;   // �إ� Clock ����
}
