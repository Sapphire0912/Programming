#include<iostream>
using namespace std;

class Car {   // �w�q���O
public:       // �����禡�]�����}
  void init(double,double);        // ��l�ƨ禡
  double getEff()   { return eff;} // �Ǧ^�U�o�Ĳv
  double checkGas() { return gas;} // �ˬd�o�q, �Ǧ^�Ѿl�o�q
  double go(double);  // �樫�Ѽƫ��w���{, �Ǧ^��ڦ樫���{
private:      // ����Ʀ������p��
  double gas; // ���o�q
  double eff; // �C���ɥi��p������
};

double Car::go(double kilo)
{
  if (gas >= (kilo/eff)) { // �Y�o�q��
    gas -= kilo/eff;       // ��үӱ����o�q
    cout << "�o�c�٦� " << checkGas() << " ���ɪo" << endl;
    if (gas == 0)             // �o�Χ��F
      cout << "�S�o�F�I";
  } else {
    cout << "�o�q�����A�ثe���o�u���] "
         << (kilo = gas * eff) << " ����";
    gas = 0;
  }
  return kilo;
}

void Car::init(double G,double E)
{
  gas = G;  // ��l�ƪo�q
  eff= E;   // ��l�ƿU�o�Ĳv
}

int main()
{
  Car super;            // �ŧi����
  super.init(20,30);    // ��l�ƪ���
  cout << "�W�Ŭ٪o��1���ɶ] " << super.getEff()
       << " ����" << endl;
  cout << "�{�b�o�c�� " << super.checkGas() << " ���ɪo" << endl;

  while (super.checkGas() > 0) {
    double kilo;
    cout << "�{�b�n�}�X�����G";
    cin >> kilo;
    super.go(kilo);     // �樫���w���{
  }
}
