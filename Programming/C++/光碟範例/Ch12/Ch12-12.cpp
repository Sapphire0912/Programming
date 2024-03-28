#include<iostream>
#include<string>
#include "Ch12-12.h"
using namespace std;

class Employee: public Person { // ���u���O
friend ostream& operator<<(ostream&, Employee &);
public:
  static int count() { return counter;}
  Employee(string n, Gender s, int a, int y):Person(n,s,a)
  {
    id = ++counter;
    seniority = y;
  }
private:
  int seniority;        // �~��
  int id;               // ���u�s��
  static int counter;   // ����p�ƾ�
};
int Employee::counter = 0;

ostream& operator<<(ostream& o, Employee & e)
{
  return o << e.id << " - " << e.name << '(' << e.age << ')'
           << " �w�A�� " << e.seniority << " �~" << endl;
}

void swap(void* a, void* b)     // �洫���ХΪ��禡
{
  void* temp = a;
  a = b;
  b = temp;
}

int main()
{                  // �إ� 5 �Ӫ���
  Employee* em[5]={new Employee("���a��", female, 28,5),
                   new Employee("�����", male, 37,9),
                   new Employee("���u��", female, 30,3),
                   new Employee("���Q�s", male, 55,20),
                   new Employee("�i���", male, 47,15)};

  cout << "�Ƨǫe..." << endl;
  for(int i=0;i<Employee::count();i++)   // �̧ǿ�X�U����
    cout << *em[i];

  for(int i=0;i<Employee::count()-1;i++) // �̦~�ֱƧǪ���
    for(int j=i;j<Employee::count();j++)
      if (*em[i] > *em[j])
         swap(em[i],em[j]);     // �洫����

  cout << "�Ƨǫ�..." << endl;
  for(int i=0;i<Employee::count();i++)   // ��X�U����
    cout << *em[i];
}
