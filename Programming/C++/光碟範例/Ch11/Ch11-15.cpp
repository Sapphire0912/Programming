#include<iostream>
#include<string>
using namespace std;

int main()
{
  string s, target = "top";
  cout << "�п�J�@�Ӧr��G";
  getline(cin, s);

  unsigned int i, pos = 0;
  while ((i = s.find(target,pos))!=string::npos) {
    s.insert(i,1,'s');   // �b�j�M�� target ����m���J 's'
    pos = i + 2;         // �q���쪺��m�����~���
  }

  cout << "�s�r��G" << s;
}
