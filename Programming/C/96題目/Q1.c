#include<stdio.h>
#include<stdlib.h>
main()
{
	int a;
	int x,y,z; //88 188 288
	int i,j ;// �g �� 
	int ans5,ans4,ans3,ans2,ans;
	int W;
	printf("��J�q�ܤ�����:");
	scanf("%d",&a);
	x=a*10;
	y=a*9;
	z=a*8;
	i=a*7+200;
	j=a*5+600;
	if(x<=88)
		x=88;
	if(y<=188)
	 	y=188;
	if(z<=288)
		z=288;
		
		
	if(a<1 || a>1000)
	{
		printf("�ƭȿ��~\n");
		return main();
	}
	if(i>x && j>x && y>x && z>x)
	{
		printf("88�� %d��\n",x);
	}
	if(i>y && j>y && x>y && z>y)
	{
		printf("188�� %d��\n",y);
	}
	if(x>z && y>z && i>z && j>z)
	{
		printf("288�� %d��\n",z);
	}
	if(x>i && y>i && z>i && j>i)
	{
		printf("�g�٫� %d��\n",i);
	}	
	if(x>j && y>j && z>j && i>j)
	{
		printf("�򥻫� %d��\n",j);
	}	
	return main();	
 } 
