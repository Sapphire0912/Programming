#include<iostream>
#include<stdexcept>            // ���t bad_alloc ���O���ŧi
#include<string>
using namespace std;

int main()
{
  string s = "Exception";      // ���եΪ��r�ꪫ��

  try {
    cout << s.at(100);         // �s���W�X���޽d�򪺦r��
  }                            // �N�޵o�ҥ~
  catch (bad_alloc e) {
    cerr << "�ɮ��� std::bad_alloc �ҥ~...\n";
    cerr << e.what();          // ��ܨҥ~�������T��
  }

  cout << "\n�o�ͨҥ~�ɬݤ����o��T���I\n";
}
