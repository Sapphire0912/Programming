#include<iostream>
using namespace std;

class AA {
public:
  int geti() {return i;}
  void seti(int i) { this->i = i; }
protected:
  int i;
};

class BB : virtual public AA {}; // AA ��������¦���O
class CC : virtual public AA {}; // AA ��������¦���O

class DD : public BB, public CC {}; // �h���~�� BB�BCC

int main()
{
  cout << "AA �� " << sizeof(AA) << " �Ӧ줸��" << endl;
  cout << "BB �� " << sizeof(BB) << " �Ӧ줸��" << endl;
  cout << "CC �� " << sizeof(CC) << " �Ӧ줸��" << endl;
  cout << "DD �� " << sizeof(DD) << " �Ӧ줸��" << endl;

  DD d;
  d.BB::seti(99);               // �z�L BB �I�s
  cout << d.geti() << endl;
  d.CC::seti(100);              // �z�L CC �I�s
  cout << d.geti() << endl;
}
