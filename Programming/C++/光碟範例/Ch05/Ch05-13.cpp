#include<iostream>
using namespace std;

int main()
{
  char go_again = 'Y';
  float height, weight;

  while (go_again == 'Y' || go_again == 'y') { // �j�p�g Y ���|
    cout << "�п�J���� (����)�G";             // �~��j��
    cin >> height;
    cout << "�п�J�魫 (����)�G";
    cin >> weight;
    cout << "�z����ײv���G" << weight / (height * height) * 10000
         << '%' << endl;       // ��ײv���魫���H���� (����) ����
    cout << "�n�~��p��t�@��ܡH(�n�п�J Y �� y )�G";
    cin >> go_again;
  }
}
