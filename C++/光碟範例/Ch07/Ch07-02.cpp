#include <iostream>
using namespace std;

int main()
{
  int iArray[] = {1,2,3,4,5};  // �����w�}�C�j�p
  int nArray[5] = {6,7,8};     // ���]�w������������l��

  cout << "iArray �}�C���j�p�� " << sizeof(iArray)
       << " �Ӧ줸��" << endl;
  cout << "nArray �}�C���j�p�� " << sizeof(nArray)
       << " �Ӧ줸��" << endl;

  for(int i=0;i<5;i++) {  // �ΰj���X�U������
    cout << "iArray[" << i << "] =" << iArray[i] << '\t'   
         << "nArray[" << i << "] =" << nArray[i] << endl;
  }
}
