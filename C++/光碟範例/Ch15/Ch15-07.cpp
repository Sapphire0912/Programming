#include<iostream>
using namespace std;

void divide(int i, int j)  // ���k�B�⪺�禡
{
  if (j == 0)       // �Y���Ƭ��s
    throw j;        // �Y�ߥX�ҥ~
  else
    cout << i << '/' << j << " = " << i/j << "..." << i%j;
}

int main()                 // ���եΪ��D�{��
{
  int i,j;
  cout << "���{���|�p�Ⱓ�k�B�⤤���Ӥξl��, "
       << "�Ш̧ǿ�J�Q���ƻP���ơG";
  cin >> i >> j;

  try {
    divide (i,j);          // �I�s���k�禡
  }
  catch (int) {            // �ɮ���ƫ��O���ҥ~
    cerr << "\n...�o�Ͱ��H�s���ҥ~...";
  }
}
