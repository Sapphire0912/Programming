#include<iostream>
#include<cstring>     // �]���Ψ� strcpy() �禡�G�t�A���ɮ�
using namespace std;

class Person {  // �H�����O
public:
  Person(const char*, int);
  Person& operator=(Person &p);
  Person() {}
  ~Person() { delete [] name; }
  void setName(const char* ptr) { strcpy(name,ptr); }
  const char* getName() { return name;}
private:
  char* name;   // �m�W
  int age;      // �~��
};

Person::Person(const char* s, int a)
{
  name = new char[strlen(s)];
  strcpy(name, s);
  age = a;
}

Person& Person::operator=(Person& p) // �h�����w�B��l
{
  name = new char[strlen(p.name)];
  strcpy(name, p.name);
  age = p.age;
  return *this;
}

class Student : public Person {      // �ǥ����O�~�ӤH�����O
public:
  void reading()
  {
    cout << id << " - " << getName() << "�b�ݮ�" << endl;
  }
  Student() {}
  Student(const char* s, int a, int i) : Person(s, a)
  {                                  // �I�s�����O���غc�禡
    id = i;
  }
  Student& operator= (Student&);
private:
  int id;                            // �Ǹ�
};

Student& Student::operator= (Student& s)    // �h�����w�B��l
{
  //Person::operator=(s);        // �I�s�����O�����w�B��l
  id = s.id+100;
  return *this;
}

int main()
{
  Student st1("�����", 10, 4), st2;
  st2 = st1;                    // �N st1 ���w�� st2
  st1.setName("���a��");        // ��� st1 ���󪺩m�W
  st1.reading();
  st2.reading();
}
