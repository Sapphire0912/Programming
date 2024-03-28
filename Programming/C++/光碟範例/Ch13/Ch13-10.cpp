#include<iostream>
#include<string>
#include "Ch13-10.h"    // �t�A�H�����O�w�q
using namespace std;

class Student : virtual public Person { // �ǥ����O
public:
  void goClass() { cout << name << "�b�W��" << endl; }
  Student(string n, Gender s, int a):Person(n,s,a)
  {
    id = ++counter;     // �N�p�ƾ��ȥ[ 1 ���Ǹ�
  }
  Student() {id = ++counter;}
protected:
  int id;               // �Ǹ�
  static int counter;   // ����p�ƾ�
};
int Student::counter = 0;

class Teacher : virtual public Person { // �Юv���O
public:
  void goClass() { cout << name << "�Ѯv�b�W��" << endl;}
  Teacher(string n, Gender s, int a):Person(n,s,a)
  {
    id = ++counter;     // �N�p�ƾ��ȥ[ 1 ���Юv�s��
  }
  Teacher() {id = ++counter;}
protected:
  int id;               // �Юv�s��
  static int counter;   // ����p�ƾ�
};
int Teacher::counter = 0;

class Graduated : public Teacher, public Student { // ��s�����O
friend ostream& operator<<(ostream&, Graduated& );
public:
  Graduated(string n, Gender s, int a):Person(n,s,a) { }
                                   // �u�I�s�@�� Person ���غc�禡
  void goClass(bool b)
  {   // ���w�H true ��ܥξǥͨ����W�� (ť��)
    b ? Student::goClass() : Teacher::goClass();
  }
};

ostream& operator<<(ostream& o, Graduated & g)
{
  return o << g.name << "���Ǹ��G" << g.Student::id
           << ", �Юv�s���G" << g.Teacher::id << endl;
}

int main()
{
  Student ss[9];        // �H�N�شX�Ӿǥͪ���
  Teacher tt[3];        // �H�N�شX�ӱЮv����
  Graduated g("�v�a��", male, 25);

  cout << g;
  g.goClass(true);
  g.goClass(false);
}
