#include<stdio.h>
#include<stdlib.h>
#include<windows.h> 
#include<time.h>
int main()
{
	char c;
	int a=0; 
	int b=0; 
	int low=99,high=100;  
	int count=0;  

	srand(time(NULL)); 
	b=rand()%(high-low+1)+low;

	do 
	{	  
		printf("�q�� %d ���A�п�J %d �� %d ���� ==> ",++count, low, high); 
		scanf("%d",&a);
		if(a>high)
		{
			printf("���U�O�x!!\n");
			break;
		}
		else
		if(a<low)
		{
			printf("�A���D�O�³J��?!\n");
			break;
		}
		else
		if (a==b) 
			{
				printf("\t\t\t\t\tBINGO!!\n");
				break;
			}
		else
			{
				printf("\t\t\t\t\tagain!!\n"); 
				if (a>b) 
				high=a-1;  
					else 
					low=a+1;  
			}
		 
	}
	while(a!=b); 
	printf("input y or n\n");
	scanf("%c",&c);
	if(c=='y')
	{
		printf("new game start\n");
		return main();
	}
	else if (c=='n')
	{
		printf("BYE BYE !! \n");
		return 0;
	}
} 
