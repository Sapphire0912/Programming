#include<iostream>
#include<fstream>
#include<string>
using namespace std;

int main()
{
  string filename;
  cout << "�п�J�nŪ�����ɮצW�١G";
  cin >> filename;

  ifstream file(filename.c_str());  // �}�Ұ�Ū�ɮ�
  if (!file)                        // �Y�L�k�}���ɮ�
    cerr << "�ɮ׶}�ҥ���" << endl;
  else {
    char ch;
    while(!file.get(ch).eof())      // �Y�٨S���ɮ׵���
      cout << ch;                   // �����ɮ�
  }
}
