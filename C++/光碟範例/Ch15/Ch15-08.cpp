#include<iostream>
#include<exception>
using namespace std;

void divide(int i, int j)  // ���k�B�⪺�禡
{
  if (j == 0)       // �Y���Ƭ��s�Y�ߥX�ҥ~
    throw exception("\n...�o�Ͱ��H�s���ҥ~...");
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
    divide (i,j);
  }
  catch (exception e) {
    cerr << e.what();
  }
}
