#include<iostream>
#include<string>
using namespace std;

int main()
{
  string s = "O Romeo, Romeo! wherefore art thou Romeo?", target;
  cout << "�n�b[" << s << "]��" << "�䤰��r�H";
  cin >> target;

  unsigned int i, count = 0, pos = string::npos;
  cout << endl << "�b[" << s << "]��" << endl;
  while ((i = s.rfind(target,pos))!=string::npos) {
    count++;       // �p�ƾ��[ 1
    cout << "�� " << count << " ���X�{[" << target
         << "]����m�O�b�� " << i+1 << " �Ӧr" << endl;
    pos = i - 1;   // �q�e����쪺��m���e�~��j�M
  }

  if (count == 0)   // �Y�Ǧ^ npos
    cout << "�S���ŦX[" << target << "]���r��I";
  else
    cout << "�`�@��� " << count << " ��";
}
