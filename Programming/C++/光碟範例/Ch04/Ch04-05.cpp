#include<iostream>

int main()
{
  int i = 100, j;
  j = (i++) + 5;   // ��m���W
  std::cout << "i = " << i << "\t\tj = " << j;

  i = 100;
  j = (++i) + 5;   // �e�m���W
  std::cout << "\ni = " << i << "\t\tj = " << j;
}
