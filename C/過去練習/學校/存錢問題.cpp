#include<stdio.h>
#include<stdlib.h>
main()
{
	int a,b,c,d;
	printf("�п�J�s��:\n");
	scanf("%d",&d);
	while(d>=0)
	{
		printf("�п�J(1)�[(2)��:");
		scanf("%d",&c);
		switch(c)
		{
			case 1:
				printf("�п�J�[�h��:\n");
				scanf("%d",&b);
				d+=b;
				printf("�{�b�����B��:%d\n",d);
				break;
			case 2:
				printf("�п�J��h��:\n");
				scanf("%d",&a);
				d-=a;
				printf("�{�b�����B��:%d\n",d);
				break;
			default:
				printf("��J���~ ���s��J\n");
				return main();
		}
	}
	printf("���B�����Х��[��!\n");
	system("pause\n");
	return 0;
 } 
