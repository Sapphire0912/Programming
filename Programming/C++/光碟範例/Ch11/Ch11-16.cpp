#include<iostream>
#include<string>
using namespace std;

int main()
{
  string s, s1, s2;
  cout << "�п�J�@�Ӧr��G";
  getline(cin, s);
  cout << "�п�J�n���������r��G";
  getline(cin, s1);
  cout << "�n�N[" << s1 << "]�����H";
  getline(cin, s2);

  unsigned int i, pos = 0;
  unsigned len1 = s1.size(), len2 = s2.size();
  while ((i = s.find(s1,pos))!=string::npos) {
    s.replace(i,len1, s2); // �N s1 ���� s2
    pos = i + len2 + 1;    // �q���쪺��m�����~���
  }

  cout << "�s�r��G" << s;
}
