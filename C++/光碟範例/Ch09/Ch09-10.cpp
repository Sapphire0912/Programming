#include "Ch09-09.h"    // �����Ϋe�@�d�Ҫ��t�A��

int main()
{
  Str array[4] = {10, Str("Apple "), "Pie"};

  cout << "Str  ������Ϊ��줸�աG" << sizeof(Str)   << endl
       << "array�}�C���Ϊ��줸�աG" << sizeof(array) << endl;
  for(int i=0;i<4;i++)  // �ΰj���X�U�������󪺦r��
    array[i].show();
}
