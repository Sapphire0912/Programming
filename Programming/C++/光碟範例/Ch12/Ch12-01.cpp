#include<iostream>
using namespace std;

class Shape {
public:
  double x, y;         // �N��ϧΪ��_�I
};

class Rectangle : public Shape   { // �~�Ӧ� Shape ���O
  double x2,y2;        // �N��x�Υk�U������
};

class Circle : public Shape   {    // �~�Ӧ� Shape ���O
  double r;            // �N���b�|
};

int main()
{
  Shape s;
  Rectangle r;
  Circle c;
  cout << "s ���j�p�G" << sizeof(s) << endl;
  cout << "r ���j�p�G" << sizeof(r) << endl;
  cout << "c ���j�p�G" << sizeof(c) << endl;
}
