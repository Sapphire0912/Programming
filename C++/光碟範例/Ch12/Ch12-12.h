#include<iostream>
#include<string>
using namespace std;

enum Gender {male,female};      // �N��ʧO���C�|���O

class Person {  // �H�����O
public:
  string& getName() { return name; }
  bool operator>(Person& p) { return (age > p.age); }
  Person(string, Gender, int);
  Person() {}
protected:
  string name;  // �m�W
  Gender sex;   // �ʧO
  int age;      // �~��
};

Person::Person(string n, Gender s, int a) : name(n)
{
  sex = s;  age = a;
}
