#include<iostream>
using namespace std;

class Time {
public:
  Time& set(int, int, int);   // �ŧi���Ǧ^ Time �Ѧҫ��O
  void copy(Time source) { *this = source; }   // �ƻs��Ʀ���
  void show() { cout << hour << ':' << min << ':' << sec; }
private:
  int hour, min, sec;   // �N��ɤ�������
};

Time& Time::set(int h, int m, int s)
{
   hour = h; min  = m; sec  = s;
   return *this;     // �Ǧ^��I�s�̪���
}

void main()
{
   Time t;
   t.set(13,42,56).show();
}
