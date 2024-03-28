#include<iostream>
using namespace std;

class Circle {
public:
  Circle(double,double,double);
  Circle(double,double,double,double);
  double area() { return 3.1415926 * r * r; }  // �p��ꭱ�n
  double circum() { return 3.1415926 * 2 * r; }// �p���g��
private:
  double x,y;         // ��߮y��
  double r;           // �b�|
};

Circle::Circle(double x0,double y0,double r0 = 1)
{
  x = x0; y = y0; r = r0;
}

Circle::Circle(double x0,double y0,double x1, double y1)
{
  double w = min( (x1>x0)? (x1-x0):(x0-x1),    // �p�⥿������
                  (y1>y0)? (y1-y0):(y0-y1) );
  r = w/2;     // �b�|���e�ΰ����@�b
  x = x0 + r;  // ��X��ߪ� x �y��
  y = y0 + r;  // ��X��ߪ� y �y��
}

int main()
{
  Circle c1(3,5),c2(10,10,30,30);
  cout << "c1 �����n�� " << c1.area() << endl;
  cout << "c2 ����P���� " << c2.circum() << endl;
}
