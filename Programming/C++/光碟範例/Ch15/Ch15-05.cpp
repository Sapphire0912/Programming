#include<iostream>
#include<string>
using namespace std;

int main()
{
  int* ptr;
  string s = "Exception";      // ���եΪ��r�ꪫ��
  long num;

  try {
    cout << "�п�J�n�t�m�� int �}�C�����ƶq�G";
    cin >> num;
    ptr = new int[num];

    cout << "�аݭn�˵��r�ꤤ���ĴX�Ӧr���G";
    cin >> num;
    cout << s.at(num);
  }
  catch (...) {                // �i�ɮ��Ҧ��ҥ~�� catch �϶�
    cerr << "\n...�ܩ�p�A�o�͵{���L�k�B�z�����D�A�{��������������...";

  }

  delete [] ptr;
  cout << "\n�{�������I\n";
}
