#include<iostream>
using namespace std;

int main()
{
  double fee = 100;      // ���� 100 ��
  int ticket;
  cout << "�n�R�X�i���H";
  cin >> ticket;

  fee *= (ticket <10) ? (ticket) : (ticket*0.8);
  cout << "�z�n�ʶR " << ticket << " �i��" << endl
       << "�@�p " << fee << " ��";
}
