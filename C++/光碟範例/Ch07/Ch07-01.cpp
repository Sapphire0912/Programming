#include <iostream>
using namespace std;

int main()
{
  int iArray[5];          // �ŧi�}�C

  for(int i=0;i<5;i++)    // �ΰj��]�w�U������
    iArray[i] = i * 5;

  cout << "iArray �}�C���j�p�� " << sizeof(iArray)
       << " �Ӧ줸��" << endl;
  for(int i=0;i<5;i++)    // �ΰj���X�U������
    cout << "iArray[" << i << "] =" << iArray[i] << endl;
}
