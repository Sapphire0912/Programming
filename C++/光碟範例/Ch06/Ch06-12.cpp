#include <iostream>
using namespace std;
#define  cube(x)   x * x * x   // �p��ߤ誺����

int main()
{
  for(int i=1;i<10;i+=2)
    cout << i << " ���T���赥�� "
         << cube(i) << endl;
}
