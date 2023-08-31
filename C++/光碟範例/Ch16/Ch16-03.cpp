#include <iostream>
using namespace std;

// �禡�˪�
// ��X�}�C�����̤p�ȩҦb����m
template<class T>
int min(T data[],int size)
{
  int index = 0; // �����̤p�Ȫ���m

  for(int i = 1;i < size;i++) {
    if(data[i] < data[index])
      index = i;
  }
      
  return index;
}

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
