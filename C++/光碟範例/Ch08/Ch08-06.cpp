#include<iostream>
#include<cstring>
using namespace std;

class Str {           // ���K���r�����O
public:
  void show() { cout << data;}
  void set(char * ptr) { data = ptr; }
  void set()               // �h���禡
  {
    data = new char[40];   // �t�m�s���O����Ŷ�
    strcpy(data,"Empty!"); // �N "Empty!" �ƻs��s���Ŷ�
  }
private:
  char * data;             // ���V�r�ꪺ����
};

int main()
{
  Str hello, world;
  hello.set("Hello World!");  // �I�s���Ѽƪ�����
  world.set();                // �I�s�L�Ѽƪ�����
  hello.show(); world.show();
}
