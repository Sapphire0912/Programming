#include<iostream>
using namespace std;

int main()
{
  char   c = 10;
  int    i = 100;
  long   l = 1000;
  float  f = 0.5f;
  double d = 0.5e-10;

  i = (i + f) - (c * i) / d + (l - i) / (f + c) ;
  cout << "i = " << i << endl;
  // �P�˪��⦡�A��@��, �����w�� double �ܼ�
  d = (i + f) - (c * i) / d + (l - i) / (f + c) ;
  cout << "d = " << d << endl;
}
