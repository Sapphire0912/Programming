#include<iostream>
#include<string>
using namespace std;

int main()
{
  char array[] ="Happy new year!";
  string str[] = { string(),            // �Ū��r�ꪫ��
                   string(array),       // �q�r���}�C�إߦr��
                   string(array,5),
                   string(array,6,3),
                   string(10, 'x')};    // �q�r���إߦr��

  for(int i=0;i<5;i++) {
    cout << "str[" << i << ']' << "�����e���G" << str[i] << endl
         << "\tsizeof()�G" << sizeof(str[i])     // ��ܪ���j�p
         << "\tsize()�G" << str[i].size()        // ��ܦr��j�p
         << "\tlength()�G" << str[i].length() << endl;//�r�����
  }
}
