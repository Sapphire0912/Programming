#include <iostream>
#include "Ch16-08.h"
using namespace std;

int main()
{
  char* all[] = { // ���ո��
    "zebra",
    "dog",
    "cat",
    "frog",
  };
  
  // �M�Ψ�r��}�C�W
  int minOfAll = min<char*>(all,4); 
    
  cout << "all[] ���̤p�������O all[" << minOfAll 
       << "]" << endl;
}