#include<iostream>
using namespace std;

class Shape {
public:
  Shape (int i=0, int j=0) { x = i;     y = j; }
  double getX() { return x;}
  double getY() { return y;}
protected:
  double x, y;         // �N��ϧΪ��_�I
};

class Rectangle : public Shape   { // �~�� Shape
public:
  Rectangle(int i, int j, int k, int l):Shape(i,j)
  { x = k; y = l; }
  double getX() { return x;}  // �P�����O��
  double getY() { return y;}  // �����禡�P�W
private:
  double x,y;          // �P�����O����Ʀ����P�W
};

int main()
{
  Rectangle r(0,0,3,5);
  cout << '(' << r.getX() << ',' << r.getY() << ')';
}
