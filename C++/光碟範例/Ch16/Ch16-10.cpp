#include <iostream>
#include <algorithm>
using namespace std;

int main()
{
  int all[] = {20,17,39,18,22,46}; // ���ո��
  double another[] = {7.65,3.4,2.11,1.5,4.33}; // ���ո��
  
  // �ϥ�min_element()�禡�˪��B�z��ư}�C
  int* minInt = min_element<int*>(&all[0],&all[6]);
  cout << "all[] ���̤p�������O " << *minInt << endl;

  // �ϥ�min_element()�禡�˪��B�z����װ}�C
  double* minDouble = 
    min_element<double*>(&another[0],&another[5]);
  cout << "another[] ���̤p�������O " << *minDouble << endl;
}
