#include <iostream>
#include <stack>
using namespace std;

int main()
{
   stack<int> st1;  // �w�q�@�Ӿ�ư��|
   stack<char> st2; // �w�q�@�Ӧr�����|

   // �N��Ʀs�J�Ĥ@�Ӱ��|��
   st1.push(1); st1.push(2); st1.push(3);

   // �N��Ʀs�J�ĤG�Ӱ��|��
   st2.push('a'); st2.push('b'); st2.push('c');

   cout << st1.top();st1.pop();
   cout << st2.top();st2.pop();
   cout << st1.top();st1.pop();
   cout << st2.top();st2.pop();
   cout << st1.top();st1.pop();
   cout << st2.top();st2.pop();
}
