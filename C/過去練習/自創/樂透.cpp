#include<stdio.h>
#include<stdlib.h>
#include<time.h>
main()
{
	int b;
	int i[7],c,j,B;
	int x,y,z;
	printf("��J1����Ʀr�A��J0�����{��");
	scanf("%d",&b);
	srand(time(NULL));
	switch(b)
	{
		case 1: 
				 for(c=1;c<=6;c++) 
				 {
					B:
					i[c]=(rand()%49)+1;
					for(j=1;j<c;j++)
					{
						if(i[c]==i[j])
						{
							goto B;
						}
					}
					printf("%3d",i[c]);
				 }
				 printf("\n");
				return main();
		case 0: system("pause");
				break;
				return 0;
		default: printf("�ƭȿ��~ ���s��J�I\n");
				 return main();
	}
}
