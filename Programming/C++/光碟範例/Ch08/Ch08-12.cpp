#include <iostream>
#include "Ch08-12.h"

int main()
{
   Stack st1, st2;    // �w�q�G�Ӱ��|����
   st1.init();
   st2.init();

   // �N��Ʀs�J�Ĥ@�Ӱ��|��
   st1.push(1); st1.push(2); st1.push(3);

   // �N��Ʀs�J�ĤG�Ӱ��|��
   st2.push(7); st2.push(8); st2.push(9);

   cout << st1.pop();
   cout << st2.pop();
   cout << st1.pop();
   cout << st2.pop();
   cout << st1.pop();
   cout << st2.pop();    st2.pop(); // �G�N�h pop �@��
}
