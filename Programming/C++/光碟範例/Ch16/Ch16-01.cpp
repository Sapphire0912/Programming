#include <iostream>
using namespace std;

// �禡�ŧi
int min(int data[],int size);

int main()
{
  int all[] = {20,17,39,18,22,46}; // ���ո��
  int minOfAll = min(all,sizeof(all) / sizeof(int));

  cout << "all[] ���̤p�������O all[" << minOfAll 
       << "]" << endl;
}

// ��X�}�C�����̤p�ȩҦb����m
int min(int data[],int size)
{
  int index = 0; // �����̤p�Ȫ���m
  
  for(int i = 1;i < size;i++) {
    if(data[i] < data[index])
      index = i;
  }
      
  return index;
}