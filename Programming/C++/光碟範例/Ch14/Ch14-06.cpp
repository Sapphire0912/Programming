#include<iostream>
#include<iomanip>
using namespace std;

int main()
{
  cout << "�п�J�@�ӼƦr�G";
  int i;
  cin >> hex >> i;
  cout << showbase;
  cout << i << " ���⦨8�i�쬰 "  << oct << i << endl;
  cout << i << " ���⦨16�i�쬰 " << hex << i << endl;;

  cout << "�ЦA��J�@�ӼƦr�G";
  cin >> i;
  cout << uppercase;
  cout << i << " ���⦨10�i�쬰 " << setbase(10)<< i << endl;
  cout << i << " ���⦨8�i�쬰 "  << setbase(8) << i;
}
