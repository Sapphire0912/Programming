#include<iostream>
using namespace std;

int main()
{
  cout << true << endl;                 // �ϥιw�]���覡
  cout << boolalpha << false << endl;   // �]����X�y��r�z
  cerr << "cerr�G" << true << endl;     // cerr �|���|�ܡH
  cout << true << endl;                 // �ող{�b��X���O�H
  cout << noboolalpha << false << endl; // �]����X�y�Ʀr�z
}
