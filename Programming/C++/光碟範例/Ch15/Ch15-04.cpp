#include<iostream>
#include<stdexcept>            // ���t�зǨҥ~���O���ŧi
#include<string>
using namespace std;

int main()
{
  int* ptr;
  string s = "Exception";      // ���եΪ��r�ꪫ��
  long num;

  try {
    cout << "�п�J�n�t�m�� int �}�C�����ƶq�G";
    cin >> num;
    ptr = new int[num];

    cout << "�аݭn�˵��r�ꤤ���ĴX�Ӧr���G";
    cin >> num;
    cout << s.at(num);
  }
  catch (bad_alloc e) {        // �����t�m�O���饢�Ѫ��ҥ~
    cerr << e.what();          // ��ܨҥ~�������T��
    cerr << "...�z�n�D�t�m���}�C�Ӥj�F...\n";
  }
  catch (out_of_range e) {     // �����W�X���޽d�򪺨ҥ~
    cerr << e.what();          // ��ܨҥ~�������T��
    cerr << "...�z�n�˵����r���W�X�d��...\n";
  }

  delete [] ptr;
  cout << "\n�{�������I\n";
}
