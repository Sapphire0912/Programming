#include <iostream>
using namespace std;

int main()
{
  int    i;          // �ŧi��Ƥ��ܼ�
  double d;          // �ŧi����ׯB�I���ܼ�
  int    *iptr = &i; // �w�q�����ܼ�, �ñN��l�ȳ]�� i ����}
  double *dptr = &d; // �w�q�����ܼ�, �ñN��l�ȳ]�� d ����}

  cout << "iptr ���j�p���G" << sizeof(iptr) << endl;
  cout << "iptr �s���Ȭ��G" << iptr << endl;

  cout << "dptr ���j�p���G" << sizeof(dptr) << endl;
  cout << "dptr �s���Ȭ��G" << dptr << endl;
}
