#include <iostream>
using namespace std;

// �禡�ŧi
int min(int data[],int size);
int min(double data[],int size);

int main()
{
  int all[] = {20,17,39,18,22,46}; // ���ո��
  double another[] = {7.65,3.4,2.11,1.5,4.33}; // ���ո��

  int minOfAll = min(all,sizeof(all) / sizeof(int));
  cout << "all[] ���̤p�������O all[" << minOfAll 
       << "]" << endl;
  minOfAll = min(another,sizeof(another) / sizeof(double));
  cout << "another[] ���̤p�������O another[" << minOfAll 
       << "]" << endl;
}

// ��X int ���O�}�C�����̤p�ȩҦb����m
int min(int data[],int size)
{
  int index = 0; // �����̤p�Ȫ���m
  
  for(int i = 1;i < size;i++) {
    if(data[i] < data[index])
      index = i;
  }
      
  return index;
}

// ��X double ���O�}�C�����̤p�ȩҦb����m
int min(double data[],int size)
{
  int index = 0; // �����̤p�Ȫ���m
 
  for(int i = 1;i < size;i++) {
    if(data[i] < data[index])
      index = i;
  }
      
  return index;
}