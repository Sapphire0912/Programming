#include<iostream>
using namespace std;

class Complex {
  friend ostream& operator<<(ostream&, const Complex&);
  friend istream& operator>>(istream&, Complex&);
public:
  Complex(double r=0,double i=0) {real = r; image = i;}
  Complex operator+(Complex a)    // �[�k
    {return Complex(real+a.real, image+a.image);}
  Complex operator-(Complex a)    // ��k
    {return Complex(real-a.real, image-a.image);}
  bool operator==(const Complex a) // ���
  {
    if (real == a.real && image == a.image)
      return true;
    else
      return false;
  }
private:
  double real;        // �곡
  double image;       // �곡
};

ostream& operator<<(ostream& o, const Complex& c)
{
   return o << '(' << c.real << ',' << c.image << "i)";
}

istream& operator>>(istream& i, Complex& c)
{
  cout << "�п�J�Ƽƪ��곡�P�곡(�����Ϊťչj�}�B���ο�Ji)�G";
  return i >> c.real >> c.image;
}

int main()
{
  Complex c1,c2;

  cin >> c1 >> c2; // ����L��J��Ƽƪ���ss
  cout << c1 << " �[ " << c2 << " ���� " << (c1+c2) << endl;

  if (c1 == c2)    // �ˬd��ƼƬO�_�۵�
    cout << "�z��J����ƼƬ۵�";
  else
    cout << "�z��J����ƼƤ��۵�";
}
