#include<iostream>
using namespace std;

class Car {
public:
  static void setEff(double e) { eff = e;} // �]�w�R�A��Ʀ���
  double getEff() { return eff; }
  static double GtoL(double G) { return G*3.78533; }
                // �N�[�ڴ��⬰����, 1�[�ڬ� 3.78533 ����
  static double LtoG(double L) { return L*0.26418; }
                // �N���ɴ��⬰�[��, 1���ɬ� 0.26418 �[��
private:
  static double eff;    // �R�A��Ʀ���
};

double Car::eff = 0;    // �w�q�R�A��Ʀ���

int main()
{
  // ���إߪ���]�i�I�s�R�A�����禡
  cout << "10�[�ڵ��� " << Car::GtoL(10) << " ����" << endl;
                           // �Ϊ���I�s�����禡
  cout << "10���ɵ��� " << Car::LtoG(10) << " �[��" << endl;
                           // �����O�I�s�����禡

  Car super;           // �ŧi����
  super.setEff(30);    // �Ϊ���]�i�I�s�R�A�����禡

  cout << "�W�Ŭ٪o��1���ɶ] " << super.getEff()
       << " ����" << endl;
}
