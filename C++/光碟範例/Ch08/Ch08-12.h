#include <iostream>
#define MaxSize 20
using namespace std;

class Stack {
public:
  void init() { sp = 0; }  // ��l�ƪ������禡
  void push(int data);     // �ŧi�s�J�@�Ӿ�ƪ��禡
  int pop();               // �ŧi���X�@�Ӿ�ƪ��禡
private:
  int sp;               // �ΨӰO���ثe���|���w�s�X�����
  int buffer[MaxSize];  // �N����|���}�C
  static void Error() { cout << "\nStack Error\n"; }
};

void Stack::push(int data)   // �N�@�Ӿ�ơy��z�J���|
{
   if(sp == MaxSize)         // �Y�w�F�̤j��, �h����A���ƶi��
     Error();
   else
     buffer[sp++] = data;    // �N��Ʀs�J sp �ҫ�����, �ñN sp �[ 1
}                            // ��ܩҦs����Ʀh�F�@��

int Stack::pop()             // �q���|�����X�@�Ӿ��
{
   if(sp == 0) {             // �Y�w�g�쩳�F��ܰ��|�����L���
     Error();
     return 0;
   }
   return buffer[--sp];      // �Ǧ^ sp �ҫ�������, �ñN sp �� 1
}                            // ��ܩҦs����Ƥ֤F�@��
