#include<iostream>
using namespace std;

class Shape {
public:
  Shape (int i=0, int j=0)
  {
     x = i;     y = j;
     cout << "���b���� Shape ���غc�禡" << endl;
  }
private:
  double x, y;         // �N��ϧΪ��_�I
};

class Circle : public Shape   { // �~�� Shape ���S��
public:
  Circle() { cout << "���b���� Circle ���غc�禡" <<endl; }
private:
  double r;            // �N���b�|
};

int main()
{
  Circle c;  // �إ� Circle ����
}
