#include<iostream>
#include<string>
#include "Ch12-11.h"
using namespace std;

class Student : public Person { // �ǥ����O
friend ostream& operator<<(ostream&, Student &);
public:
  static int count() { return counter;}
  Student(string n, Gender s, int a):Person(n,s,a)
  {
    id = ++counter;     // �N�p�ƾ��ȥ[ 1 ���Ǹ�
  }
private:
  int id;               // �Ǹ�
  static int counter;   // ����p�ƾ�
};
int Student::counter = 0;

ostream& operator<<(ostream& o, Student & s)
{
  return o << s.id << "���G" << s.name << '/'
           << s.age << " ��" << endl;
}

int main()
{
  Student ss[3]={Student("�����", male, 17),
                 Student("���a��", female, 18),
                 Student("���Q�s", male, 19)};

  cout << "�ǥͦ@�� " << Student::count() << " �H" << endl;
  for(int i=0;i<Student::count();i++)  // �̧ǿ�X�U����
    cout << ss[i];
}
