#include <iostream>
#include <exception>
#define MaxSize 20
using namespace std;

class StackFull : public exception {};  // �ۭq���ҥ~���O
class StackEmpty: public exception {};

class Stack {
public:
  Stack() { sp = 0; }   // �غc�禡, �N sp �]�� 0 ��ܰ��|�O�Ū�
  void push(int data);  // �ŧi�s�J�@�Ӿ�ƪ��禡
  int pop();            // �ŧi���X�@�Ӿ�ƪ��禡
private:
  int sp;               // �ΨӰO���ثe���|���w�s�X�����
  int buffer[MaxSize];  // �N����|���}�C
};

void Stack::push(int data)   // �N�@�Ӿ�ơy��z�J���|
{
   if(sp == MaxSize)         // �Y�w�F�̤j��, �h����A���ƶi��
     throw StackFull();      // �ߥX�ۭq�� StackFull �ҥ~
   else
     buffer[sp++] = data;    // �N��Ʀs�J sp �ҫ�����, �ñN sp �[ 1
}                            // ��ܩҦs����Ʀh�F�@��

int Stack::pop()             // �q���|�����X�@�Ӿ��
{
   if(sp == 0)               // �Y�w�g�쩳�F, ��ܰ��|�����L���
     throw StackEmpty();     // �ߥX�ۭq�� StackEmpty �ҥ~
   return buffer[--sp];      // �Ǧ^ sp �ҫ�������, �ñN sp �� 1
}                            // ��ܩҦs����Ƥ֤F�@��
