#include <iostream>
using namespace std;

double stdWeight(int sex, double height)  // �魫�p��禡
{
  if (sex == 1)     // �k
    return (height - 80) * 0.7;
  else              // �k
    return (height - 70) * 0.6;
}

int main()
{
  int sex;               // �N��ʧO�ﶵ
  double height, weight; // �������魫

  do {  // �@�w�n��� 1 �� 2
    cout << "�ʧO(1)�k(2)�k�G";
    cin >> sex;
  } while (sex!=1 && sex!=2);

  cout << "�п�J����(����)�G";
  cin >> height;

  weight = stdWeight(sex, height);
  cout << "�z���з��魫�d��O " << endl << weight * 0.9
       << " ����� " << weight * 1.1 << " ���礧��";
}
