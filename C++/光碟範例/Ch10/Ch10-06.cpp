#include "Ch10-06.h"    // �t�A�r�����O�w�q

int main()
{
  Str s1("moon "), s2("cake");
  s1[0] = 'n';   // �ק�r�ꤤ�� 1 �Ӧr��
  s2[2] = 'f';   // �ק�r�ꤤ�� 3 �Ӧr��
  (s1+s2).show();
}
