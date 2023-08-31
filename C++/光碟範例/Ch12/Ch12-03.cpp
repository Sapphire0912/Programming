#include<iostream>
using namespace std;

class Shape {
public:
  Shape (int i=0, int j=0) { x = i;     y = j; }
  double getX() { return x;}
  double getY() { return y;}
private:
  double x, y;         // �N��ϧΪ��_�I
};

class Circle : public Shape   { // �~�� Shape ���S��
  friend ostream& operator<<(ostream& o, Circle& c);
public:
  Circle(int i, int j, int radius): Shape(i,j), r(radius)
  {  }                 // �b������l�Ʀ�C�I�s�����O���غc�禡
private:
  double r;            // �N���b�|
};

ostream& operator<<(ostream& o, Circle& c) // ��X���I�y�ФΥb�|
{
  return o << '(' << c.getX() << ',' << c.getY() << ')' << endl
           << "r = " << c.r;
}

int main()
{
  Circle c(1,1,2);  // �إ� Circle ����
  cout << c;
}
