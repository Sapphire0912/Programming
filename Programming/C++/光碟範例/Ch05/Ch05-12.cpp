#include<iostream>
using namespace std;

int main()
{
  int sum = 0;       // �x�s�`�M���ܼ�

  for (int i=1; i<=100; i++) {
    sum += i;        // �N sum �[�W�ثe�� i ��
    cout << "1 �[�� " << i << " ���`�M�� " << sum << endl;
  }
}
