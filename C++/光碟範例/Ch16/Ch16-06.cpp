#include <iostream>
#include "Ch16-06.h"
using namespace std;

int main()
{
  int all[] = {20,17,39,18,22,46}; // ���ո��
  
  // �ϥΫD���O���˪��Ѽ�
  int minOfAll = min<int,6>(all);
    
  // �sĶ���|�ˬd�}�C�j�p���~
  // minOfAll = min<int,8>(all);
  
  cout << "all[] ���̤p�������O all[" << minOfAll 
       << "]" << endl;
}
