#include<iostream>
using namespace std; 

/* 
   1. �]�q�O���q���q�O�p��覡�����T��: 
  (1) �a�x�ιq: 100�ץH�U,2.5��/�� 101~300��,3.3��/�� 301�ץH�W,4.2��/��
  (2) �u�~�ιq: �򥻶O��100��,150�� �W�L�����C��1.9��
  (3) ��~�ιq: 0~300��,6��/�� 301�ץH�W,6.8��/��
  
  Q. ��J�ιq���O�ΨϥΫ׼ƫ�,�p�����ú�ǶO�Φp��?
  PS. �H�W�T�إιq���O�����H�禡�覡���g
*/

double family();
double industry();
double open();

main(){
	int type;
	double spend;
	while(1){
		cout << "��J�ιq���O: ((1)�a�x�ιq,(2)�u�~�ιq,(3)��~�ιq)) ";	
		cin >> type;
		if(type==1)
			spend=family();
		if(type==2)
			spend=industry();
		if(type==3)
			spend=open();
		if(type>3 || type<1){
			cout << "Error." << endl;
			break;
		}
		cout << "Cost: NT$ " << spend << endl << endl;
	}
}

double family(){
	double e,cost=0;
	cout << "��J�ϥιq�q(���: ��) : " ;
	cin >> e;
	if(e<=100)
		cost=e*2.5;
	if(e>100 && e<301)
		cost=e*3.3;
	if(e>300)
		cost=e*4.2;
	return cost;
}

double industry(){
	double e,cost=0;
	cout << "��J�ϥιq�q(���: ��) : " ;
	cin >> e;
	if(e<=100)
		cost=150;
	else
		cost=(e-100)*1.9+150;
	return cost;
}

double open(){
	double e,cost=0;
	cout << "��J�ϥιq�q(���: ��) : " ;
	cin >> e;
	if(e<=300)
		cost=e*6;
	else
		cost=e*6.8;
	return cost;
}
