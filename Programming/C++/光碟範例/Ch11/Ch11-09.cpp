#include<iostream>
#include<string>
using namespace std;

int main()
{
  string s = "To be or not to be", target;
  cout << "�п�J�@�r��G";
  cin >> target;

  unsigned int i = s.find(target); // �b s ���j�M target
  if (i == string::npos)   // �Y�Ǧ^ npos
    cout << "�䤣��I";
  else                     // �Y�����
    cout << "�b[" << s << "]���Ĥ@���X�{[" << target
         << "]����m�O�b�� " << i+1 << " �Ӧr";
}
