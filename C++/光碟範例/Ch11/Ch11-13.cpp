#include<iostream>
#include<string>
using namespace std;

int main()
{
  string s, target = " \n\t";
  cout << "�п�J�@�Ӧr��G";
  getline(cin, s);

  unsigned int i, count = 0, pos = 0;
  while ((i = s.find_first_not_of(target,pos))!=string::npos) {
    count++;       // �p�ƾ��[ 1
    pos = i + 1;   // �q�e����쪺��m���e�~��j�M
  }

  cout << endl << "�b[" << s << "]��";
  if (count == 0)   // �Y�Ǧ^ npos
    cout << "�u���ťզr���I";
  else
    cout << "�@�� " << count << " �ӫD�ťզr��";
}
