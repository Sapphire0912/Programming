#include<iostream>
using namespace std;

int main()
{
  float i,j,k;       // �Ψ��x�s 3 �䪺���

  cout << "�Ш̧ǿ�J�T���Ϊ��T����G\n";
  cout << "��� 1 ��";
  cin >> i;          // ��J�� 1 �����
  cout << "��� 2 ��";
  cin >> j;          // ��J�� 2 �����
  cout << "��� 3 ��";
  cin >> k;          // ��J�� 3 �����

  if ((i+j) > k)     // �P�_�� 1, 2 �䪺�M�O�_�j��� 3 ��
    if ((i+k) > j)   // �P�_�� 1, 3 �䪺�M�O�_�j��� 2 ��
      if ((j+k) > i) // �P�_�� 2, 3 �䪺�M�O�_�j��� 1 ��
        cout << "�i�H���T���Ϊ��T����C";
      else
        cout << "�� 2�B3 �䪺�M�p��ε���� 1 ��";
    else
      cout << "�� 1�B3 �䪺�M�p��ε���� 2 ��";
  else
    cout << "�� 1�B2 �䪺�M�p��ε���� 3 ��";
}
