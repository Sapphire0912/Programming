#include <iostream>
using namespace std;

int main()
{
  int iArray[3][4] = {1,2,3,4,5,6};

  cout << "iArray �}�C���j�p�� " << sizeof(iArray)
       << " �Ӧ줸��" << endl;

  for(int i=0;i<3;i++) {  // �α_���j��C���Ҧ�������
    for(int j=0;j<4;j++)
      cout << "iArray[" << i << "][" << j << "]= "
           << iArray[i][j] << '\t';

    cout << endl;        // �C��X���@�C�����N����
  }
}
