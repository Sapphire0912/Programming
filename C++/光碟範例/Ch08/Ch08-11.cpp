#include<iostream>
using namespace std;

class Complex {
public:
  void set(double r,double i) {real = r; image = i;}
  void show()
      { cout << '(' << real << ',' << image << "i)"; }
  Complex& add(Complex a)       
      {real += a.real; image += a.image; return *this;}
  Complex& minus(Complex a)    
      {real -= a.real; image -= a.image; return *this;}
private:
  double real;        
  double image;       
};

int main()
{
  Complex c1,c2;
  c1.set(3, 9);
  c2.set(-1, 2.5);

  c1.show();  cout << " �[ "; c2.show();
  cout << " ���� ";   c1.add(c2).show();
  cout << endl;
  c2.show();  cout << " �� "; c1.show();
  cout << " ���� ";   c2.minus(c1).show();
}
