#include <iostream>
#include <stdexcept>           // ���t bad_alloc ���O���ŧi
using namespace std;
int main()
{
  int * iptr;

  try {
    iptr = new int[536870911]; // �t�m�W�j���}�C
  }                            // �N�޵o�ҥ~
  catch (bad_alloc e) {
    cerr << "�ɮ��� std::bad_alloc �ҥ~...\n";
    cerr << e.what();          // ��ܨҥ~�������T��
  }

  delete[] iptr;
  cout << "\n�o�ͨҥ~�ɬݤ����o��T���I\n";
}
