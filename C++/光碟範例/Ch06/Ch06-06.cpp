#include <iostream>
using namespace std;
void adding(void);     //�S���Ǧ^�ȤΰѼ�

int main()
{
  for (int i=0;i<3;i++)     // �I�s adding() �T��
    adding();
}

void adding(void)
{
  static int number=100;  // �R�A�����ܼ�
  cout << "number = " << number++ << endl;
}
