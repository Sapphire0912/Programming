#include<iostream>
using namespace std;

int main()
{
   float height;
   cout << "�п�J���� (���G����)�G";
   cin >> height;

   if (height < 110)
     cout << "�����C��зǡA�i�K�ʲ��I\n";
   else if (height < 140) // �����b 110 �� 140 �������p
     cout << "�����W�L 110�A�жR�b���I\n";
   else                   // �����W�L 140 �����p
     cout << "�����W�L 140�A�жR�����I\n";

   cout << "���ȳ~�r�֡C";
}
