#include<iostream>
#include<fstream>
#include<string>
using namespace std;

int main()
{
  string filename;
  cout << "�п�J�n�g�J���ɮצW�١G";
  cin >> filename;
                                               // �}�ҤG����
  fstream file(filename.c_str(), ios_base::out|ios_base::binary);
  if (!file)                        // �Y�L�k�}���ɮ�
    cerr << "�ɮ׶}�ҥ���" << endl;
  else {
    for (int i = 1; i<=10; i++) {
      double d = i * i * i;     // �p�� 1��10 ���ߤ�
      file.write((char*) &d, sizeof(double));
    }
    file.close();
    cout << "�g�J����" <<endl;
  }
                                               // ���s�}���ɮ�
  file.open(filename.c_str(), ios_base::in|ios_base::binary);
  if (!file)                        // �Y�L�k�}���ɮ�
    cerr << "�ɮ׶}�ҥ���" << endl;
  else {
    for (int i = 1; i<=10; i++) {   // �ΰj��Ū�Q�ӼƦr
      double d;
      file.read((char*) &d, sizeof(double));
      cout << d << endl;
    }
    file.close();
    cout << "Ū������";
  }
}
