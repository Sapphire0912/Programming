#include <iostream>

int main()
{
  int * iptr;

  iptr = new int[536870911]; // �t�m�W�j���}�C
                             // �N�޵o�ҥ~
  delete[] iptr;
  std::cout << "�o�ͨҥ~�ɬݤ����o��T���I\n";
}
