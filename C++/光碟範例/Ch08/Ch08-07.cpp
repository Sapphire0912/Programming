#include<iostream>
using namespace std;

class Str {           // ���K���r�����O
public:
  void show() { cout << str; }
  void set(char * ptr) { str = ptr; }
  void showthis() { cout << this; }  // ��X this ����
private:
  char * str;       // ���V�r�ꪺ����
};

int main()
{
  Str hello, world;
  hello.set("Hello");  world.set("World!");
  cout << "hello ���󪺦�}�G" << &hello << endl;
  cout << "world ���󪺦�}�G";
  world.showthis();
}
