#include<iostream>
#include<string>
using namespace std;

int main()
{
  string s, target = "0123456789";
  cout << "�п�J�@�Ӧr��G";
  getline(cin, s);

  unsigned int i, count = 0, pos = 0;
  while ((i = s.find_first_of(target,pos))!=string::npos) {
    count++;       // �p�ƾ��[ 1
    pos = i + 1;   // �q�e����쪺��m�����~��j�M
  }

  cout << endl << "�b[" << s << "]��";
  if (count == 0)   // �Y�Ǧ^ npos
    cout << "�S���Ʀr�r���I";
  else
    cout << "�@�� " << count << " �ӼƦr�r��";
}
