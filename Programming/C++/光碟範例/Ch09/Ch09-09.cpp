#include "Ch09-09.h"         // �t�A�ۭq���t�A��

int main()
{
  Str a=5;  // �۷�� a="     ";
  a.show(); cout << endl;
  Str b("abcde");
  b.show(); cout << endl;
  Str c = Str("C++");
  c.show(); cout << endl;
  Str *d = new Str("�����v");
  d->show();
  delete d;
}
