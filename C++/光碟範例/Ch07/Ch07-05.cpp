#include <iostream>
using namespace std;

int main()
{
  char name1[]="John Smith";  // �H�r�ꬰ��l��
  char name2[]={'M','a','r','y',' ','W','h','i','t','e'};
                              // �]�w�ӧO�r������l��
  cout << "name1[]�j�p���G" << sizeof(name1) << endl;
  cout << "name2[]�j�p���G" << sizeof(name2) << endl;

  cout << "name1[]�G" << name1 << endl;
  cout << "name2[]�G" << name2 << endl;
}
