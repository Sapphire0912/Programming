#include<iostream>
using namespace std;

int main()
{
  int num1,num2;
  cout << "�p����ƪ��̤j���]��\n";
  cout << "�п�J��1�ӼƦr�G";
  cin >> num1;
  cout << "�п�J��2�ӼƦr�G";
  cin >> num2;

  int a, b = num2, c=num1%num2;  // c ���ȴN�O�� 1 ���۰����l��

  while (c!=0) {                 // ��l�Ƭ� 0 ��,
    a=b;                         // b �N�O�̤j���]��
    b=c;
    c=a%b;                       // ����ۡy���z, ���l��
  }

  cout << num1 << " �M " << num2 << " ���̤j���]�ƬO�G" << b;
}
