#include<iostream>
#include<string>
using namespace std;

int main()
{
  string s, target = "book", ins = "the ";
  cout << "�п�J�@�Ӧr��G";
  getline(cin, s);

  unsigned int i, pos = 0;
  while ((i = s.find(target,pos))!=string::npos) {
    s.insert(i,ins);  // �b�j�M�� target ����m���J ins �r��
    pos = i + ins.size() + 1;    // �q���쪺��m�����~���
  }

  cout << "�s�r��G" << s;
}
