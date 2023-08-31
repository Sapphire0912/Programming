#include<iostream>
using namespace std;

class AA {
public:
  int geti() {return i;}
  void seti(int i) { this->i = i; }
protected:
  int i;
};

class BB : public AA {}; // �~�� AA
class CC : public AA {}; // �~�� AA

class DD : public BB, public CC {}; // �h���~�� BB�BCC

int main()
{
  DD d;
  d.BB::seti(10);               // �I�s BB ���������禡
  d.CC::seti(8);                // �I�s CC ���������禡
  cout << d.BB::geti() << endl; // �I�s BB ���������禡
  cout << d.CC::geti() << endl; // �I�s CC ���������禡
}
