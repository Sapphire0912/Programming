#include<stdio.h>
#include<stdlib.h>
#include<conio.h>
main()
{
	int a,b,d;
	char c;
	printf ("�п�J�n�R�X�i��\n");
	scanf ("%d",&a);
	while(1)
	{
			if (a==0)
		{
			printf ("�ʶR�����T�T");
			return 0;
		}
		printf ("�A�٭n�R%2d�i��\n",a);
		printf ("�п�ܥ�q�u��:\n");
		printf ("1.�x�K\n");
		printf ("2.���K\n");
		printf ("3.����\n");
		c=getche();
		switch (c)
		{
			case	'1':
			case	'2':
			case	'3':
			printf ("\n�п�J�n�R�X�i��");
			scanf ("%d",&b);
			if (b<=a)
			{
				a-=b;
				break;
			}
			else 
			{
				printf ("���~\n");
				break;
			}
			default:
			break;
			
		}
	}
 } 
