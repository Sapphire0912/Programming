#include<iostream>
using namespace std;

class Car {
public:
  Car (double s = 10) { speed = s;}
  double go(double time) { return time * speed;}
private:
  double speed;        // �ɳt
};

class Ship: private Car {  // �H private �覡�~�� Car ������
public:
  Ship(double s, double c):Car(s) { coff = c; }
  double go(double time, double waterspeed)
  {
    return Car::go(time) + time * waterspeed * coff;
  }
private:
  double coff;   // ���y�t�׳y����y�ʳt�ת��Y��
};

int main()
{
  Ship s(15,0.4);
  int waterspeed;
  cout << "�п�J�ثe���y�t�סH";
  cin >> waterspeed;
  cout << "�p�� s �@�p�ɥi�� " << s.go(1,waterspeed) << " ����";
}
