#include<iostream>
using namespace std;

class Car {
public:
  double getEff()       { return eff;} // �Ǧ^�U�o�Ĳv
  void setEff(double d) { eff = d;}    // �]�w�U�o�Ĳv
private:
  static double eff;       // �R�A����
};

double Car::eff = 30.0;  // �w�q�Ϊ�l���R�A��Ʀ�������

int main()
{
  Car *One = new Car;
  One->setEff(8);    // �]�w�@����1���ɪo�i�]8����
  cout << "�@����1���ɪo�i�] " << One->getEff()
       << " ����" << endl;
}
