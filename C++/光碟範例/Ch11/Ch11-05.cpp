#include<iostream>
#include<string>
using namespace std;

int main()
{
  string s = string(3,'+');  // �إ߷s�r�� "+++"
  s[0] = 'C';                // �ק�� 1 �Ӧr��

  for (int i=0;i<(int) s.size();i++) // �̧ǿ�X�r�ꤤ�U�r��
    cout << s.at(i);
}
