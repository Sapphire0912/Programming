#include <iostream>

int main()
{
   void func();   // �ŧi�禡
   func();        // �I�s�禡
}

void  func()      // ���j�禡
{
   std::cout << "This is a endless program\n";
   func();    // �I�s�ۤv
}
