#include<iostream>
#include<fstream>
#include<string>
#include<iomanip>    // �ϥΨ� setw() ���
#include<cctype>     // �ϥΨ� isupper()�Bislower() �禡
using namespace std;

int main()
{
  string filename;
  cout << "�п�J�nŪ�����ɮצW�١G";
  cin >> filename;

  int count[26] = {0};             // �ΨӲέp�U�r���r�ƪ��}�C
  fstream file(filename.c_str(), ios_base::in);
  if (!file)                       // �Y�L�k�}���ɮ�
    cerr << "�ɮ׶}�ҥ���" << endl;
  else {
    char ch;
    while (!file.get(ch).eof())    // �����ɮ׵����e����Ū��
      if (isupper(ch))             // �Y���j�g�r��
        count[ch-65]++;            // �N������m�������ȥ[ 1
      else if (islower(ch))        // �Y���p�g�r��
        count[ch-97]++;            // �N������m�������ȥ[ 1
  }
  file.close();

  for(int i=0;i<26;i++) {  // �b�ù��W��ܲέp���G
    cout << "�r��" << char(65+i) << '/' << char(97+i) << "�� "
         << setw(3) << count[i] << " ��";
    cout << ((i%2)? '\n' : '\t');  // �C��X�ⵧ�N����
  }
}