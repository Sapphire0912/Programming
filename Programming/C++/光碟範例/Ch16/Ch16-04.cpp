#include <iostream>
#include "Ch16-04.h"
using namespace std;

int main()
{
  int all[] = {20,17,39,18,22,46}; // ���ո��
  double another[] = {7.65,3.4,2.11,1.5,4.33}; // ���ո��

  int minOfAll = min<int>(all,sizeof(all) / sizeof(int));
  cout << "all[] ���̤p�������O all[" << minOfAll 
       << "]" << endl;
  
  minOfAll = min<double>(another,
    sizeof(another) / sizeof(double));
  cout << "another[] ���̤p�������O another[" << minOfAll 
       << "]" << endl;
}
