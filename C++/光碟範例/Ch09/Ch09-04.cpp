#include<iostream>
using namespace std;

class Car {
public:
  Car() { gas = 10; counter++; } // �N�o�q�]�� 10, �p�ƾ��[ 1
  static const int howmany() { return counter; } // �Ǧ^�p�ƾ���
private:
  double gas;            // �o�q
  static double eff;     // �R�A����
  static int counter;    // ����p�ƾ�
};

double Car::eff = 30.0;  // �U�o�Ĳv�@�߬��C���� 30 ����
int Car::counter = 0;    // �@�}�l������ƶq�O 0 ��

int main()
{
  Car goodcar[10];
  cout << "���� Car goodcar[10]; ��, "
       << "�{�b�� " << Car::howmany() << " ����" << endl;

  Car *badcar = new Car;
  cout << "���� Car *badcar = new Car; ��, "
       << "�{�b�� " << Car::howmany() << " ����" << endl;
}
