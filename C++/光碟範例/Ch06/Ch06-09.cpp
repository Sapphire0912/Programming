#include <iostream>
using namespace std;
void showresult(double); // �S���Ǧ^�Ȫ��禡
                             // �n�ŧi�� void
int main()
{
  int sex;                   // �N��ʧO�ﶵ
  double height, weight;     // �����P�魫

  do {  // �Q�ΰj��n�D�ϥΪ̤@�w�n��� 1 �� 2
    cout << "�ʧO:(1)�k(2)�k�G";
    cin >> sex;
  } while (sex!=1 && sex!=2);

  cout << "�п�J����(����)�G";
  cin >> height;

  if (sex == 1)
    weight = (height - 80)*0.7; // �k�ʪ��з��魫����
  else
    weight = (height - 70)*0.6; // �k�ʪ��з��魫����

  showresult(weight);           // �I�s��ܵ��G���禡
}

void showresult(double result)  // �w�q��X���G���禡
{
  cout << "�z���з��魫�d��O " << endl << result * 0.9
       << " ����� " << result * 1.1 << " ���礧��";
}
