#include<iostream>
#include<string>
using namespace std;

int main()
{
  string s = string();       // �إߪŪ��r��
  s = "Ilha ";               // ���w�s�r�ꤺ�e
  cout << "s �r��G" << s << endl;
  s += "Formosa";            // ���[�r��
  cout << "s �r��G" << s << endl;

  s.assign("Life Is Beautiful",8,9); // �q�� 8 �Ӧr�}�l,
  cout << "s �r��G" << s << endl;   //   �� 9 �Ӧr�����s�r��
  s.append(" Islander",7);           // ���[�ѼƦr��e 7 �Ӧr
  cout << "s �r��G" << s << endl;
}
