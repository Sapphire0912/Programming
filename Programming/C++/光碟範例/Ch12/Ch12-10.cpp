#include<iostream>
using namespace std;

class Shape {
friend ostream& operator<<(ostream&, Shape&);
public:
  Shape (int i=0, int j=0) { x = i;     y = j; }
private:
  int x, y;         // �N��ϧΪ��_�I
};

ostream& operator<<(ostream& o, Shape& s)
{
   return o << '(' << s.x << ',' << s.y << ')';
}

class Circle : public Shape   { // �~�� Shape ���S��
public:
  Circle(int i, int j, int radius): Shape(i,j)
  {                             // �I�s�����O���غc�禡
     r = radius;
  }
private:
  int r;  // ��b�|
};

class Sphere : private Circle  { // �H private �覡�~��
public:
  Sphere(int i, int j, int k, int radius): Circle(i,j,radius)
  { z = k; }
private:
  int z;     // Z �b�y��
};

int main()
{
  Circle disc(1,1,5);
  cout << disc;      // �N����q��X��y��X
  Sphere baseball(0,0,0,10);
  cout << baseball;  // �N����q��X��y��X
}
