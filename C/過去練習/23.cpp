#include<stdio.h>
#include<stdlib.h>
#include<conio.h>
main()
{
	int a[6],b[20],c,f,g;   //a�b�� b�K�X c�Ҧ����� 
	char d,e;
	printf("\n");
	printf("\n��J�ϥΪ̱b��:");
	scanf("%s",&a[d]);
	printf("\n��J�ϥΪ̱K�X:");
    scanf("%s",&b[d]);

    printf("-----------------------");
{	
    printf("\n\n���U����!!");
    printf("\n\n�z���ϥΪ̱b����:%s",a);
	printf("\n\n�z���ϥΪ̱K�X��:%s",b);
 } 
 {

 S:
 printf("\n\n�п�ܱz�n���C���Ҧ�~~");
 printf("\n(1)�@��Ҧ� \n(2)�G�ƼҦ� \n(3)���L�Ҧ� \n(4)�L�ļҦ�");
 printf("\n�ڭn��  ",g);
 scanf("%d",&g);}
if(g<1||g>4) 
{
 printf("\n�ЧO�}����");
 goto S;
}
 switch(g)

 { 	
{
case 1:printf("�A��ܤF �@��Ҧ�\n");
break;
case 2:printf("�A��ܤF �G�ƼҦ�\n");
break;
case 3:printf("�A��ܤF ���L�Ҧ�\n");
break;
case 4:printf("�A��ܤF �L�ļҦ�\n");
break;  	

 	
 }

 
 }

	
	
	
	return main();
	}
