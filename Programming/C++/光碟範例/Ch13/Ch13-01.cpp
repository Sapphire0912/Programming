#include<iostream>
using namespace std;

class Vehicle {        // ��q�u�����O
public:
  Vehicle(double p = 0)
  {
    cout << "Vehicle ����غc��" << endl;
    speed = p;
  }
protected:
  double speed;        // �t��
};

class ExerciseTool {   // �B�ʾ������O
public:
  ExerciseTool(double w = 100)
  {
    cout << "ExerciseTool ����غc��" << endl;
    weight = w;
  }
protected:
  double weight;       // ���q
};

class Bicycle: public Vehicle, public ExerciseTool { // �h���~��
public:
  Bicycle(bool b = true) { discBreak = b; }
private:
  bool discBreak;      // �O�_�ϥκЫb
};

int main()
{
  Bicycle bike;        // �ŧi�ۦ樮����
}
