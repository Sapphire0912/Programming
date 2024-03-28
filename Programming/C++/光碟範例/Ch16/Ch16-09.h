#include <cstring>

// �˪��禡
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

// �� char* �S�s�� min() �禡�˪�
template<>
int min<char*>(char* data[],int size) 
{
  int index = 0;
  for(int i = 1;i < size;i++) {
    // ��ĥ� strcmp �禡����r�ꤺ�e
    if(strcmp(data[i],data[index]) < 0)
      index = i;
  }
  return index;
}
