#include <iostream>
#define SIZE 5              // �}�C�j�p�`��
using namespace std;

int main()
{
  char array[SIZE]={'s','c','i','o','n'};

  cout << "�Ƨǫe�G";
  for (int i=0;i<SIZE;i++)    // ��X�Ƨǫe���}�C���e
    cout << array[i];

  for (int i=0;i<SIZE;i++)
    for (int j=i+1;j<SIZE;j++)
      if (array[i]<array[j])  // �Y array[i] ���Ȥp�� array[j]
      {                       // �N�N 2 �Ӥ������ȹ��
        char temp = array[i]; // temp �O��ծɥΨ쪺�Ȧs�ܼ�
        array[i] = array[j];
        array[j] = temp;
      }

  cout << endl << "�Ƨǫ�G";
  for (int i=0;i<SIZE;i++)    // ��X�Ƨǫ᪺�}�C���e
    cout << array[i];
}
