#include <iostream>
#include <fstream>       // �ϥ��ɮצ�y
using namespace std;

int main()
{
  ifstream file1("Ch14-01.cpp");
  fstream file2;             // ���غc����
  file2.open("Ch14-02.cpp"); // �A�}���ɮ�

  if (!file1 || !file2)       // �Y�L�k�}���ɮ�
    cerr << "�ɮ׶}�ҥ���" << endl;
  else {
    char str[80];
    file1.getline(str,80); // �q file1 Ū�@�椺�e
    cout << str << endl;   // ��XŪ�쪺���e

    file2.getline(str,80); // �q file2 Ū�@�椺�e
    file2.getline(str,80); // �A�q file2 Ū�@�椺�e
    cout << str;           // ��X�� 2 ��Ū�쪺���e
  }
} // �Ѻc�禡�|�۰������ɮ�
