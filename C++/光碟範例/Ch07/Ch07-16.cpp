#include <iostream>
using namespace std;

int main()
{
  int age=18;
  int &old=age;  // �w�q�Ѧҫ��O�ܼ�

  cout << "age���ȡG" << age << "\told���ȡG" << old << endl;
  cout << endl << "�п�J age ���s�ƭȡG";
  cin >> age;;
  cout << "age���ȡG" << age << "\told���ȡG" << old << endl;
  cout << endl << "�п�J old ���s�ƭȡG";
  cin >> old;;
  cout << "age���ȡG" << age << "\told���ȡG" << old << endl;
}
