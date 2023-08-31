#include<iostream>
using namespace std;

class Time {
public:                 // �w�]�غc�禡�N�ɶ��]�� 12 �I��
  Time() { hour = 12; min = 0; sec = 0; };
  Time(int);            // �@�ӰѼƪ��غc�禡
  Time(int,int,int);    // �T�ӰѼƪ��غc�禡
  void show()
  {
    cout << hour << "�I" << min << "��" << sec << "��" << endl;
  }
private:
  int hour, min, sec;   // �N��ɤ�������
};

Time::Time(int h)
{
  hour = (h>=0 && h<=23) ? h:12;     // �ˬd h �O�_�b 0 �� 23 ��
  min = 0; sec = 0;
}

Time::Time(int h,int m, int s)
{
  hour = (h>=0 && h<=23) ? h:12;     // �ˬd h �O�_�b 0 �� 23 ��
  min  = (m>=0 && m<=59) ? m:0;      // �ˬd m �O�_�b 0 �� 59 ��
  sec  = (s>=0 && s<=59) ? s:0;      // �ˬd s �O�_�b 0 �� 59 ��
}

int main()
{
  Time t1;           // �I�s�w�]�غc�禡
  Time t2(9);        // �I�s�u���@�ӰѼƪ��غc�禡
  Time t3(15,45,75); // �I�s���T�ӰѼƪ��غc�禡

  t1.show();
  t2.show();
  t3.show();
}
