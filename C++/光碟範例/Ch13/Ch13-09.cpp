#include <iostream>
using namespace std;

struct Point {  // �y���I
  double x;
  double y;
};

class Shape {                // ��H��¦���O
public:
  virtual double area() = 0; // �µ����禡
};

class Circle: virtual public Shape {
public:
  Circle(double x=0, double y=0, double radius=0)
  { p.x =x; p.y = y; r = radius; }
  double area() { return r*r*3.14159; }  // �w�q�����禡
private:
  Point p;
  double r;     // �b�|
};

class Rectangle: virtual public Shape {
public:
  Rectangle(double x=0, double y=0, double x1=1, double y1=1)
  { p1.x =x; p1.y = y; p2.x =x1; p2.y = y1; }
  double area() { return (p2.x-p1.x)*(p2.y-p1.y); }  // �w�q�����禡
private:
  Point p1,p2;
};

void main()
{
   Shape* sp[4] = {new Circle(5,2,8),  // sp[] ���V�U�ؤ��P������
                   new Circle(1,1,3),
                   new Rectangle(1,2,3,4),
                   new Rectangle(0,3,7,21)};

   for(int i=0; i<4; i++)
      cout << sp[i]->area() << endl;   // ��X�U���󪺭��n
}
