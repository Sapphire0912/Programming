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