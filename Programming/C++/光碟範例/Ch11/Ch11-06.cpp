#include<iostream>
#include<string>
using namespace std;

int main()
{
  string s = "longer";

  cout << s.erase(4) << endl;   // �R���� 5�B�� 6 �Ӧr
  cout << s.erase(2,1) << endl; // �R���� 3 �Ӧr
  cout << "�I�s erase() �� s ���e�q���G" << s.capacity() << endl;

  s.clear();                    // �M���r��
  cout << "�I�s clear() �� s �����e���G" << s << endl;
}
