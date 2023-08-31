#include<iostream>
using namespace std;

class AA {
public:
  int geti() {return i;}
  void seti(int i) { this->i = i; }
protected:
  int i;
};

class BB : virtual public AA {   // AA ��������¦���O
};

class CC : virtual public AA {   // AA ��������¦���O
public:
  void seti(int i) { this->i *= i; }  // �\�� AA ���P�W�禡
};

class DD : public BB, public CC {     // �h���~��
public:
  DD (int i=100) { this-> i = i; }
};

int main()
{
  DD d;
  d.seti(33);        // �N�|�I�s CC::seti(33)
  cout << d.geti() << endl;
  d.BB::seti(33);    // �j��g�� BB �I�s AA::seti(33)
  cout << d.geti() << endl;
}
