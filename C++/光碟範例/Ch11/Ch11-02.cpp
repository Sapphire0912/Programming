#include<iostream>
#include<string>
using namespace std;

int main()
{
  string s1 = "Object-oriented programming";
  cout << "s1 ���e�q�G" << s1.capacity() << endl
       << "s1 �̤j�i��e�q�G" << s1.max_size() << endl;

  string s2 = string();
  if (s2.empty())                    // �Y s2 �O�Ŧr��
    cout << "s2 �O�Ŧr��" << endl;   // �h��X�T��
  cout << "s2 ���e�q�G" << s2.capacity() << endl;
}
