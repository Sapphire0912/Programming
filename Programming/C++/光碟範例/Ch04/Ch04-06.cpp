#include<iostream>

int main()
{
  int i = 10, j;
  j = (i++) + i + (i++);  // ��ӫ�m���W
  std::cout << "i = " << i << "\t\tj = " << j << '\n';

  i = 10;                // �N i �A�]�� 10
  j = (--i) + i + (--i);  // ��ӫe�m����
  std::cout << "i = " << i << "\t\tj = " << j;
}
