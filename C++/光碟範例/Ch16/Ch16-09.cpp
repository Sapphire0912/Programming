#include <iostream>
using namespace std;
#include "Ch16-09.h"

int main()
{
  char* all[] = { // ���ո��
    "zebra",
    "dog",
    "cat",
    "frog",
  };
  
  // �ϥΫD���O���˪��Ѽ�
  int minOfAll = min<char*>(all,4); 
    
  cout << "all[] ���̤p�������O all[" << minOfAll << 
    "]" << endl;
}