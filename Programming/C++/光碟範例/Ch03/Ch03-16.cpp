#include<iostream>
using namespace std;

int main()
{
  enum fruit_tea { apple, banana, orange };
  fruit_tea taste;   // taste �O fruit_tea ���O������

  taste = apple;     // �ݥΦC�|�����ӳ]�w���
  cout << "taste = " << taste << endl;

  taste = orange;
  cout << "taste = " << taste << endl;
}
