#include<iostream>
using namespace std;

main(){
	int a=10,b=20,c=30;
	int temp;
	cout << "�洫�e a = " << a
		 << " b = " << b
		 << " c = " << c
		 << endl ;
	temp=a;
	a=c;
	c=b;
	b=temp;
	cout << "�洫�� a = " << a
		 << " b = " << b
		 << " c = " << c
		 << endl ;	
}
