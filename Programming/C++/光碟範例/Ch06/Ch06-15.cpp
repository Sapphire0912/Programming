#include <iostream>
#include <ctime>
using namespace std;

int main()
{
  cout << "����[�k�Τ���B��@�����ݭn ";
  clock_t starttime = clock();
  for(int i=0;i<100000000;i++) ;   // �S�����ƪ��j��
  clock_t endtime = clock();

  cout << (double)(endtime - starttime) / CLK_TCK << " ��" ;
}
