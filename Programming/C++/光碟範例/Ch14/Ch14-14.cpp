#include<iostream>
#include<fstream>
#include<string>
using namespace std;

int main()
{
  string filename;
  cout << "�п�J�n�g�J���ɮצW�١G";
  cin >> filename;

  ifstream file(filename.c_str(),ios_base::binary);   // �}�ҤG����
  if (!file)                        // �Y�L�k�}���ɮ�
    cerr << "�ɮ׶}�ҥ���" << endl;
  else {
    cout << "�ثeŪ����m�b�G" << file.tellg() << endl;

    double d;
    file.seekg(5 * sizeof(double));      // ����� 6 ��
    cout << "�ثeŪ����m�b�G" << file.tellg() << endl;
    file.read((char*) &d, sizeof(double));
    cout << d << endl;
    cout << "�ثeŪ����m�b�G" << file.tellg() << endl;

                                    // ����˼Ʋ� 2 ��
    file.seekg(-2*sizeof(double),ios_base::end);
    cout << "�ثeŪ����m�b�G" << file.tellg() << endl;
    file.read((char*) &d, sizeof(double));
    cout << d << endl;
    cout << "�ثeŪ����m�b�G" << file.tellg() << endl;
  }
}
