#include <iostream>
using namespace std;

int main()
{
  int   *iptr,age=18;         // �ŧi��ƫ��O���лP�ܼ�
  float *fptr,weight=65.05f;  // �ŧi�B�I�ƫ��O���лP�ܼ�
  char  *cptr,bloodtype='O';  // �ŧi�r�����O���лP�ܼ�
  iptr=&age;                  // iptr ���V age ����}
  fptr=&weight;               // fptr ���V weight ����}
  cptr=&bloodtype;            // cptr ���V bloodtype ����}

  cout << "�~�֡G" << *iptr <<  "��" << endl;
  cout << "�魫�G" << *fptr <<  "����" << endl;
  cout << "�嫬�G" << *cptr <<  "��" << endl;
}
