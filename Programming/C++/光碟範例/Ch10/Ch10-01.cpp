#include "Ch10-01.h"    // �t�A���O�w�q

int main()
{
  Str array[2] = {0, Str("Apple Pie")}; // �t 2 �Ӧr�ꪫ�󪺰}�C

  for(int i=0;i<2;i++)  // �ΰj���X�U�������󪺦r��
    cout << "array[" << i << "] ������"
         << (!array[i] ? "�� 0" : "���� 0") << endl;
}
