#include <iostream>
using namespace std;

class Destruct {
public:
  Destruct(char ch = ' ')
  {
    c = ch;
    cout << "...�I�s�F " << c << " ���غc�禡" << endl;
  }
  ~Destruct()           // �Ѻc�禡
  {
    cout << "...�I�s�F " << c << " ���Ѻc�禡" << endl;
  }
private:
  char c;
};

Destruct a = 'a';  // ���쪫��

void funct()
{
   static Destruct b = 'b'; // �R�A����
   Destruct c = 'c';        // ��������
}

int main()
{
   cout << "�{���}�l, ���I�s funct()" << endl;
   funct();
   cout << "�{�������F�I" << endl;
}
