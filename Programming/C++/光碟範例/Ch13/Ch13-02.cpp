#include<iostream>
using namespace std;

class Vehicle {
public:
  void setPrice(double p) { price = p;} // �]�w���檺�����禡
  Vehicle(double p = 0, double s = 0)
  {
    price = p;  speed = s;
  }
protected:
  double price; // ����
  double speed; // �t��
};

class ExerciseTool {
public:
  void setPrice(int p) { price = p;}    // �]�w���檺�����禡
  ExerciseTool(int p = 0, double w = 100)
  {
    price = p;  weight = w;
  }
protected:
  int price;    // ����
  double weight;// ���q
};

class Bicycle: public Vehicle, public ExerciseTool { // �h���~��
public:
  Bicycle(double i,double j,double k, bool b): Vehicle(i,j)
  {                             // �I�s Vehicle ���غc�禡
     weight = k;
     discBreak = b;
  }
  double howMuch() { return Vehicle::price; } // �Ǧ^ Vehicle
private:                                      // ������
  bool discBreak;      // �O�_�ϥκз�
};

int main()
{
  Bicycle bike(8000,15,12,true);
  cout << bike.howMuch() << endl;       // ��ܻ���

  bike.Vehicle::setPrice(2999);         // �I�s���P��
  bike.ExerciseTool::setPrice(3999);    // setPrice()
  cout << bike.howMuch() << endl;       // �d�ݭקﵲ�G
}
