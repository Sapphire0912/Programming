#include<iostream>
using namespace std;

int main()
{
  wcout.imbue(locale("cht"));   // �]�w�ϥΤ���
  wcout << L"�п�J�@�ӼƦr�G";

  int i;
  wcin >> i;
  wcerr.imbue(locale("cht"));   // �]�w�ϥΤ���
  wcerr << L"���� wcerr�G" << ++i << endl;
  wclog.imbue(locale("cht"));   // �]�w�ϥΤ���
  wclog << L"���� wclog�G" << ++i << endl;
}
