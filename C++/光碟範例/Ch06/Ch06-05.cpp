#include <iostream>
using namespace std;
void adding();          //�S���Ǧ^�ȤΰѼ�, �ݵ����� void

int main()
{
  for (int i=0;i<3;i++) // �I�s adding() �T��
    adding();
}

void adding(void)
{
  int number=100;       // �����ܼ�, ����l��
  cout << "number = " << number++ << endl;
}
