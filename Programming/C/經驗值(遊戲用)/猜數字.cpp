#include<stdio.h>
#include<stdlib.h>
#include<windows.h>
#include<conio.h>
#include<time.h>
#define max 4
int rale(void);
int game(int [],int [],int);
int com(int [],int);
int deofdi(int),choose;
int deofdi(int choose){
start:	printf("�п��������:\n");
		printf("(1)²���Ҧ�\n");
		printf("(2)���q�Ҧ�\n");
		printf("(3)�x���Ҧ�\n");
		printf("(4)��ù�Ҧ�\n");
		printf("(5)��H�Ҧ�(������)\n");
		scanf("%d",&choose);
		if(choose>5 || choose<1){
			printf("��J���~�A�Э��s��J�I\n");
			goto start;}
		else{return choose;}
}
main(){
	int a[max],i,j,m,math[max],guess,com,loop;
if(rale()==0)
	deofdi(choose);
	srand(time(NULL));
com:	
	guess=rand()%9000+1000;
	if(guess>9876 || guess<1023){printf("��J�ƭȿ��~�I�Э��s��J�I\n");goto com;}
		for(i=0;i<max;i++){
			math[i]=guess%10;guess/=10;
		for(j=0;j<i;j++){
			if(math[i]==math[j]){goto com;}}}
	printf("�q�����Ʀr��:");
		for(i=max-1;i>=0;i--){
			printf("*",i);}
loop:	
	printf("\n�п�J4�ӼƦr:\n");
	scanf("%d",&m);
	if(m>9876 || m<1023){printf("��J�ƭȿ��~�I�Э��s��J�I\n");goto loop;}
		for(i=0;i<max;i++){
			a[i]=m%10;m/=10;
			for(j=0;j<i;j++){
				if(a[i]==a[j]){printf("��J�ƭȿ��~�I�Э��s��J�I\n");goto loop;}}}
		printf("���a���Ʀr��:");
		for(i=max-1;i>=0;i--){
			printf("%d",a[i]);}
			game(math,a,choose);
// �x�s�Ʀr 
}
int rale(void){
	int x;
	printf("�q��&���a���۲q�Ʀr!!\n");
	printf("�W�h:\n");
	printf("1st�G�п�J4��0~9���Ʀr(���୫��)�I\n");
	printf("2nd�G�Ĥ@�ӼƦr���i�H��0�I\n");
	printf("3rd�G�p�G�q�@�ӼƦr���T��m�]���T�A�h�|���A�F�_�h�Ʀr���T��m���~�A�h�|���B�I\n");
	printf("4th�G�p�G4�ӼƦr�����q���h�|���C�I\n");
	printf("5th�G���J��4�ӼƦr��A�q���h�|�}�l�q���a���Ĥ@�ռƦr�A���۴����a�q�q���@�ռƦr�I\n");
	printf("6th�G����Ʀr���賣�q������A�q���ռƶV�֫h��ӡI\n");
	printf("�F�ѤW�z�W�h��J0�Y�i�}�l�C���I\n");
	scanf("%d",&x);
	return x;
}
//math[i] is com num; a[i] is player num
int game(int math[],int a[],int choose){
	int i=1,x,y;
	int per,p[max],c[max];
	int o=0,q=0; //o A q B
	int debug;
	Sleep(2000);
	do{
debug:	printf("\n��%d�^�X:\n",i);
		printf("�вq�q������%d�ռƦr:",i);
		scanf("%d",&per);
		for(x=0;x<max;x++){
			p[x]=per%10;per/=10;
		for(y=0;y<x;y++){
			if(p[x]==p[y]){printf("��J�ƭȿ��~�I�Э��s��J�I\n"); goto debug;}}}
				for(x=0;x<max;x++){
					for(y=0;y<max;y++){
						if(p[x]==math[y]){
							if(x==y){o++;}
							else if(x!=y){q++;}}}}
			printf("%dA%dB\n",o,q);i++;
			if(o==4){printf("���ߵ���F�I�`�@��F%d�ղq���I",i-1);break;}
			else{o=0;q=0;}
		}while(1);
}// ���a�q�q��  

