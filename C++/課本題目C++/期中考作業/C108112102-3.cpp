#include<iostream>
#include<cstdlib>
#include<ctime>
using namespace std;

/* 
	�ϥζüƨ禡���;�� 1~20 ������ 6 �Ӥ��P�ü�, 
    ��J�@���}�C��, �N��C�L�X��, 
    �ÿ�J�@�Ӿ�ƦA�Q�Ϋ��Ъ��覡 �`�Ƿj�M �ҿ�J����ƬO�_�b�}�C�� 
*/ 

bool search(int *num,int input){
	for(int i=0;i<6;i++){
		if (*(num+i) == input)
			return true;
	}
	return false;
}

main(){
	srand(time(NULL));
	int c;
	int num[6];
	int *p = num;
	
	for(int i=0;i<6;i++){
		c = rand() % (20) + 1;
		num[i] = c;
		for(int j=0;j<i;j++){
			if(num[j] == num[i]){
				i--;
				break;
			}
		}
	}
	
	cout << "�}�C�̭����Ʀr: ";
	for(int i=0;i<6;i++)
		cout << *(p+i) << " " ;
	cout << endl;
	
	int n;
	cout << "�п�J�@�ӼƦr(1~20): ";
	cin >> n;
	if(search(p,n))
		cout << "�Ʀr " << n << " �s�b�󦹰}�C��" << endl; 
	else
		cout << "�Ʀr " << n << " ���s�b���}�C��" << endl; 
}
