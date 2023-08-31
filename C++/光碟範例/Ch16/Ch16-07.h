using namespace std;

template<class T,int MaxSize = 20>
class Stack {
public:
  void init() { sp = 0; }  // ��l�ƪ������禡
  void push(T data);       // �ŧi�s�J�@�Ӿ�ƪ��禡
  T pop();               // �ŧi���X�@�Ӿ�ƪ��禡
private:
  int sp;             // �ΨӰO���ثe���|���w�s�X�����
  T buffer[MaxSize];  // �N����|���}�C
  static void Error() { cout << "\nStack Error\n"; }
};

template<class T,int MaxSize>
void Stack<T,MaxSize>::push(T data)  // �N�@�Ӿ�ơy��z�J���|
{
   if(sp == MaxSize)      // �Y�w�F�̤j��, �h����A���ƶi��
     Error();
   else
     buffer[sp++] = data; // �N��Ʀs�J sp �ҫ�����, �ñN sp �[ 1
}                         // ��ܩҦs����Ʀh�F�@��

template<class T,int MaxSize>
T Stack<T,MaxSize>::pop()            // �q���|�����X�@�Ӿ��
{
   if(sp == 0) {          // �Y�w�g�쩳�F��ܰ��|�����L���
     Error();
     return 0;
   }
   return buffer[--sp];   // �Ǧ^ sp �ҫ�������, �ñN sp �� 1
}                         // ��ܩҦs����Ƥ֤F�@��