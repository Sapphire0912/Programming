#include<iostream>
using namespace std;

class AA {
protected:
  int i;
};

class BB : virtual public AA {}; // AA ��������¦���O
class CC : virtual public AA {}; // AA ��������¦���O

class DD : public BB, CC {       // �H�p���覡�~�� CC
public:
  DD (int i=100) { this-> i = i; }
  int geti() {return i;}
  void change()
  {
    i = -1000;  // �i�s���������¦���O�� protected ����
  }
};

int main()
{
  DD d;
  d.change();
  cout << d.geti() << endl;
}
