#include <iostream>
using namespace std;

int main()
{
  int a[5] = { 1,22,333,4444,55555};
  int *ptr = a;

  for(int i=0;i<5;i++)
    cout << "���� ptr+" << i << " ����}�G" << (ptr+i)
         << "\t�ҫ����O����s�񪺸�Ƭ��G" << *(ptr+i) << endl;
}
