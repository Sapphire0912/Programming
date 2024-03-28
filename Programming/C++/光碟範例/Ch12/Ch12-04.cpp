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

class Circle : public Shape   { // �~�� Shape ���S��
  friend ostream& operator<<(ostream& o, Circle& c);
public:
  Circle(int i, int j, int radius)
  { x = i; y = j;  r = radius; } // �����s�� protected ��Ʀ���
private:
  double r;            // �N���b�|
};

ostream& operator<<(ostream& o, Circle& c) // ��X���I�y�ФΥb�|
{                    // �i�����s�� protected ��Ʀ���
  return o << '(' << c.x << ',' << c.y << ')' << endl
           << "r = " << c.r;
}

int main()
{
  Circle c(1,3,5);  // �إ� Circle ����
  cout << c;
}
