#include <iostream>
using namespace std;

void volume (double r) // �p��y����n
{
  cout << "�b�| " << r << " ���y����n�� "
       << 4 / 3 * 3.14159 * r * r * r << endl;
}
                         // �p���������n
void volume (double l, double w, double h)
{
  cout << "�� " << l << " �e " << w << " �� " << h
       << " ����������n�� "<< l * w * h << endl;
}

int main()
{
  volume(15);
  volume(5,15,25);
}
