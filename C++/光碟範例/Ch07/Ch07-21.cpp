#include <iostream>
using namespace std;
int findmax(int[],int);
int findmin(int[],int);

int main()
{
   // �x�s�U�����~�B���}�C
  int income[]={156548, 152074, 176325, 120159, 94876, 163584,
                179541, 146587, 156472, 135587, 95443, 169994};

  int i = findmax(income,12);
  cout << "��~�B�̰����O " << (i+1) << " ��G"
       << income[i] << " ��" << endl;
  i = findmin(income,12);
  cout << "��~�B�̧C���O " << (i+1) << " ��G"
       << income[i] << " ��" << endl;
}

int findmax(int in[], int size)
{
  int max = 0;
  for (int i=1;i<size;i++)     // ��̤j�Ȫ��j��
    if(in[max] < in[i])
      max = i;

  return max;
}

int findmin(int in[], int size)
{
  int min = 0;
  for (int i=1;i<size;i++)     // ��̤p�Ȫ��j��
    if(in[min] > in[i])
      min = i;

  return min;
}
