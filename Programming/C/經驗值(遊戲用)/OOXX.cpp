#include<stdio.h>
#include<stdlib.h>
#include<windows.h>
#include<conio.h> 
#define max 3 
int rale(void);
main(){
	int i=1,j,k,time,a,b;
	k=max*max;
	char ooxx[k],y;
	int x,re;
if(rale()==0)
	do{
re:		printf("��%d�^�X �����%d�� player\n",i,i);Sleep(800);
		printf("�п�J�n�U����m(�u�������Үɶ�):");
		for(time=2000;time<=0;time-=2000){
			Sleep(time);
			if(time==0){
				printf("�w�W�ɡA�����!\n");a++;i++;Sleep(800);goto re;}
			else{
				scanf("%d %c",&x,&y);}
		}	
	}while(1);
}
int rale(void){
	int x;
	printf("���a&���a OOXX�C��!\n");
	printf("1st:�п�J�N�n�񪺦�m�M�Ÿ�(ex.�Ĥ���n�����/�e�e�h�п�J:5 O/5 X)\n");
	printf("2nd:�s���@���u�Y�i���!\n");
	printf("3rd:�C�@��u���Ҩ����!\n");
	printf("4th:�T�Ԩ�Ө�!\n");
	printf("�A�ѤW�z�W�h���J0�}�l�C��!\n");
	scanf("%d",&x);
	return x;
}
