#include <iostream>
#define SIZE 5               // �}�C�j�p�`��
using namespace std;

int main()
{
  int numbers[SIZE];         // �x�s�ƭȪ��}�C

  cout << "�п�J 5 �ӼƦr, �{���N��X�̤j��" << endl;

  for (int i=0;i<SIZE;i++) { // �ΰj����o�C�Ӥ�����
    cout << "�п�J�� " << (i+1) << " �ӼƦr�G";
    cin >> numbers[i];
  }

  int MAX = numbers[0];      // �Ψ��x�s�̤j�Ȫ��ܼ�
                             // ���]���� 1 �Ӥ�������

  for (int i=1;i<SIZE;i++)   // ���}�C���Ҧ��������j��
    if (numbers[i]>MAX)      // �Y numbers[i] �j�� MAX
      MAX = numbers[i];      // �h�N�̤j�ȳ]�� numbers[i]

  cout << "�b��J���Ʀr��, �ƭȳ̤j���O " << MAX;
}
