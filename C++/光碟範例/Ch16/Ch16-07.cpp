#include <iostream>
#include "Ch16-07.h"

void main()
{
   Stack<int> st1;  // �w�q�@�Ӿ�ư��|
   Stack<char,10> st2; // �w�q�@�Ӧr�����|
   st1.init();
   st2.init();

   // �N��Ʀs�J�Ĥ@�Ӱ��|��
   st1.push(1); st1.push(2); st1.push(3);

   // �N��Ʀs�J�ĤG�Ӱ��|��
   st2.push('a'); st2.push('b'); st2.push('c');

   cout << st1.pop();
   cout << st2.pop();
   cout << st1.pop();
   cout << st2.pop();
   cout << st1.pop();
   cout << st2.pop();    st2.pop(); // �G�N�h pop �@��
}