#include<iostream>
using namespace std;

class Complex {
public:
  Complex(double r=0,double i=0) {real = r; image = i;}
  Complex add(Complex a)       // �[�k
    {return Complex(real + a.real, image + a.image);}
  Complex minus(Complex a)     // ��k
    {return Complex(real - a.real, image - a.image);}
  void show()
    {cout << '(' << real << ',' << image << "i)"; }
private:
  double real;        // �곡
  double image;       // �곡
};

int main()
{
  Complex c1,c2(3),c3(2,1);  // �غc 3 �ӽƼƪ���

  c1.show();  cout << " �[ "; c3.show();
  cout << " ���� ";   c1.add(c3).show();

  cout << endl;

  c2.show();  cout << " �� "; c3.show();
  cout << " ���� ";   c2.minus(c3).show();
}
