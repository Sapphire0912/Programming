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

  int a, b = num1, c=num2;  // c ���ȴN�O�� 1 ���۰����l��
  do {
    a=b;
    b=c;
    c=a%b;             // ����۰�, ���l��
  } while (c!=0);      // ��l�Ƭ� 0 ��, b �N�O�̤j���]��

  cout << num1 << " �M " << num2 << " ���̤j���]�ƬO�G"
       << b;
}
