#include<stdio.h>
#include<stdlib.h>
main()
{
	int a,b;
	printf("���~2007�~,�п�J��.��");  //2007.8.1 �T 
	scanf("%d %d",&a,&b);
	if(a<1 || a>12 || b<1 || b>31)
	{
		printf("�Э��s��J\n");
		return main();
	}
	if(a==2 && b>28 || a==4 && b>30 || a==6 && b>30 || a==9 && b>30 || a==11 && b>30 )
	{
		printf("�Э��s��J\n");
		return main();
	 } 
	switch(a)
	{
		case 1:
				if((b-1)%7==0)
					printf("��\n");
				if((b-1)%7==1)
					printf("��\n");	
				if((b-1)%7==2)
					printf("��\n");
				if((b-1)%7==3)
					printf("��\n");	
				if((b-1)%7==4)
					printf("��\n");	
				if((b-1)%7==5)
					printf("�g\n");
				if((b-1)%7==6)
					printf("��\n");						
				break;
		case 2:
		case 3:
				if((b-1)%7==0)
					printf("��\n");
				if((b-1)%7==1)
					printf("��\n");	
				if((b-1)%7==2)
					printf("�g\n");
				if((b-1)%7==3)
					printf("��\n");	
				if((b-1)%7==4)
					printf("��\n");	
				if((b-1)%7==5)
					printf("��\n");
				if((b-1)%7==6)
					printf("��\n");						
				break;	
		case 4:
				if((b-1)%7==0)
					printf("��\n");
				if((b-1)%7==1)
					printf("��\n");	
				if((b-1)%7==2)
					printf("��\n");
				if((b-1)%7==3)
					printf("��\n");	
				if((b-1)%7==4)
					printf("��\n");	
				if((b-1)%7==5)
					printf("��\n");
				if((b-1)%7==6)
					printf("�g\n");						
				break;
		case 5:
				if((b-1)%7==0)
					printf("��\n");
				if((b-1)%7==1)
					printf("��\n");	
				if((b-1)%7==2)
					printf("��\n");
				if((b-1)%7==3)
					printf("��\n");	
				if((b-1)%7==4)
					printf("�g\n");	
				if((b-1)%7==5)
					printf("��\n");
				if((b-1)%7==6)
					printf("��\n");						
				break;	
		case 6:
				if((b-1)%7==0)
					printf("��\n");
				if((b-1)%7==1)
					printf("�g\n");	
				if((b-1)%7==2)
					printf("��\n");
				if((b-1)%7==3)
					printf("��\n");	
				if((b-1)%7==4)
					printf("��\n");	
				if((b-1)%7==5)
					printf("��\n");
				if((b-1)%7==6)
					printf("��\n");						
				break;
		case 7:
				if((b-1)%7==0)
					printf("��\n");
				if((b-1)%7==1)
					printf("��\n");	
				if((b-1)%7==2)
					printf("��\n");
				if((b-1)%7==3)
					printf("��\n");	
				if((b-1)%7==4)
					printf("��\n");	
				if((b-1)%7==5)
					printf("��\n");
				if((b-1)%7==6)
					printf("�g\n");						
				break;
		case 8:
				if((b-1)%7==0)
					printf("��\n");
				if((b-1)%7==1)
					printf("��\n");	
				if((b-1)%7==2)
					printf("��\n");
				if((b-1)%7==3)
					printf("�g\n");	
				if((b-1)%7==4)
					printf("��\n");	
				if((b-1)%7==5)
					printf("��\n");
				if((b-1)%7==6)
					printf("��\n");						
				break;	
		case 9:
				if((b-1)%7==0)
					printf("�g\n");
				if((b-1)%7==1)
					printf("��\n");	
				if((b-1)%7==2)
					printf("��\n");
				if((b-1)%7==3)
					printf("��\n");	
				if((b-1)%7==4)
					printf("��\n");	
				if((b-1)%7==5)
					printf("��\n");
				if((b-1)%7==6)
					printf("��\n");						
				break;	
		case 10:
				if((b-1)%7==0)
					printf("��\n");
				if((b-1)%7==1)
					printf("��\n");	
				if((b-1)%7==2)
					printf("��\n");
				if((b-1)%7==3)
					printf("��\n");	
				if((b-1)%7==4)
					printf("��\n");	
				if((b-1)%7==5)
					printf("�g\n");
				if((b-1)%7==6)
					printf("��\n");						
				break;
		case 11:
				if((b-1)%7==0)
					printf("��\n");
				if((b-1)%7==1)
					printf("��\n");	
				if((b-1)%7==2)
					printf("�g\n");
				if((b-1)%7==3)
					printf("��\n");	
				if((b-1)%7==4)
					printf("��\n");	
				if((b-1)%7==5)
					printf("��\n");
				if((b-1)%7==6)
					printf("��\n");						
				break;
		case 12:
				if((b-1)%7==0)
					printf("�g\n");
				if((b-1)%7==1)
					printf("��\n");	
				if((b-1)%7==2)
					printf("��\n");
				if((b-1)%7==3)
					printf("��\n");	
				if((b-1)%7==4)
					printf("��\n");	
				if((b-1)%7==5)
					printf("��\n");
				if((b-1)%7==6)
					printf("��\n");						
				break;																				
	 } 
	 return main();
}
