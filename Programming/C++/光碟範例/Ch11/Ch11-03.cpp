#include<iostream>
#include<string>
using namespace std;

int main()
{
  string s = string();
  cout << "s �����e�G" << s << endl;
  cout << "s �ثe�e�q�G" << s.capacity() << endl;

  s.reserve(30);        // �O�d�Ŷ��� s
  cout << "s �s�e�q�G" << s.capacity() << endl;
  s.reserve(40);        // �O�d�Ŷ��� s
  cout << "s �s�e�q�G" << s.capacity() << endl;
  cout << "s �����׬� " << s.size() << '\n' << endl;

  s = "The Hunchback of Notre Dame";
  s.reserve(13);        // �O�d�p��r����ת��Ŷ�
  cout << "reserve(13) �� s �����e�G" << s << endl;
  s.resize(13);         // �ܧ�j�p
  cout << "resize(13)  �� s �����e�G" << s << endl;
  s.resize(150);        // �A��r���ܤj
  cout << "resize(150) �� s �����e�G" << s << endl;
  cout<< "s �������ܦ� " << s.size();
}
