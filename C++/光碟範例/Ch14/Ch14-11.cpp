#include <iostream>
#include <fstream>
using namespace std;

int main()
{
  fstream file;     // ���غc����

  file.open("c:\\test.txt", ios_base::out); // �}�ҥi�g�J���ɮ�
  if (!file)                    // �Y�L�k�}���ɮ�
    cerr << "�ɮ׶}�ҥ���" << endl;
  else {
    file << "���դ@�U" << endl; // �g�J�@���r
    file.close();               // �����ɮ�
    cout << "�g�J����" << endl;
  }                                                          

  file.open("c:\\test.txt", ios_base::app); // �H���[���覡�}��
  if (!file)                    // �Y�L�k�}���ɮ�
    cerr << "�ɮ׶}�ҥ���" << endl;
  else {
    for (int i = 0; i<10; i++)  // �ΰj��b�ɮ׫᭱
      file << i;                // �[�W�Ʀr 0 �� 9
    cout << "�g�J����" << endl;
  }
}
