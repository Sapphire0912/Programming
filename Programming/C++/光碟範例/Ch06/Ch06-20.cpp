#include <iostream>
using namespace std;
#define XX (c*e- f*b)/(a*e- d*b)  // �w�q�� x ������
#define YY (a*f- d*c)/(a*e- d*b)  // �w�q�� y ������

int main()
{
  float a,b,c,d,e,f;              // �G���@����{�����Y��
  char go = 'y';

  cout << "���p�ߤ�{��" << endl
       << "ax + by = c" << endl
       << "dx + ey = f" << endl;

  while (go == 'y' || go =='Y') {
    cout << "�п�Ja���ȡG";  cin >> a;
    cout << "�п�Jb���ȡG";  cin >> b;
    cout << "�п�Jc���ȡG";  cin >> c;
    cout << "�п�Jd���ȡG";  cin >> d;
    cout << "�п�Je���ȡG";  cin >> e;
    cout << "�п�Jf���ȡG";  cin >> f;

    if ((a*e- d*b)== 0)      // �קK������ 0
      continue;

    cout << a << "x + " << b << "y = " << c << endl;
    cout << d << "x + " << e << "y = " << f << endl;
    cout << "���Ѭ� x = " << XX << endl
         << "       y = " << YY << endl;

    cout << "�٭n�A��ܡH(y/n)�G";
    cin >> go;
  }
}
