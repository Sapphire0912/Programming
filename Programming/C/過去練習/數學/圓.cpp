#include<iostream>
#include<cmath>
using namespace std;

const float a = 3.14159f;
int main ()
{
	float x, y;
	float z = 5;
	x = a* float (pow(z, 2)) ;
	y =2*a*z;
	cout <<"�ꭱ�n1 =" << x
	     <<"\t��P��1 ="<< y;
    z = 10;
	x = a*float (pow(z,2));
	y =2*a*z;
	cout <<"\n�ꭱ�n2 =" << x
	     <<"\t��P��2 =" << y << endl;
	system("pause");
	return 0;
}
