#include <iostream>
using namespace std;

void beep()       // �w�q�@�� beep() �禡
{
  cout << "�u�@����\a\n";   // ���q���o�X���n
}

int main()
{
  cout << "�{�b�}�l�B�z�u�@" << endl;

  for (int i=0; i < 50000000; i++)
    ; // �ΰ��椭�d�U���[�k�Τ�����j������q���b���@���
  beep();        // �B�z����, �I�s beep() �禡

  for (int i=0; i < 80000000; i++)
    ; // �ΰ���K�d�U���[�k�Τ�����j������q���b���t�@���
  beep();        // �B�z����, �I�s beep() �禡
}
