#include "Ch10-08.h"    // �t�A�r�����O�w�q

int main()
{
  char s1[] = "Mickey ";
  Str s2 ="Mighty", s3 ="Magic ";
  s2 = s1;            // �N�r���}�C���w������
  s2.show();
  s3 = s2 = "Mouse";  // �N�`�Ʀr����w������
  s3.show();
}
