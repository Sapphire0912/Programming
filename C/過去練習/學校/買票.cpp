#include<stdio.h>
#include<stdlib.h>
main()
{
	int a,z; //�� 
	int t;	 //��q�u�� 
	int b;  // �j��
	int S;  //�Ƶ{�� 
	printf("�п�J�`�@�n�ʶR�X�i��:");
	scanf("%d",&a);
	
	for(b=1;b>0;b++)
	{
		S:
		printf("�п�J�n�ʶR�X�i:\n");
		scanf("%d",&z);
		if(z>a)
		{
			printf("sorry�A�W�L��J�i��!\n\n");
			goto S;
		}
		else
		printf("�п�ܥ�q�u��:\n");
		printf("1.�x�K\n2.���K\n3.����\n");
		scanf("%d",&t);
		switch(t)
		{
			case 1: printf("�A��ܪ���q�u�㬰�x�K\n");
					a-=z;
					break;
			case 2: printf("�A��ܪ���q�u�㬰���K\n");
					a-=z;
					break;
			case 3: printf("�A��ܪ���q�u�㬰����\n");
					a-=z;
					break;
			default: goto S;
		}
		if(a==0)
		{
			printf("��������F!\n");
			system("pause");
			return 0;
		}
		if(a<0)
		{
			printf("sorry�A�W�L��J�i��!\n\n");
			goto S;
		}	
			printf("�٥i�H�ʶR%d�i��\n\n",a);
	}
}
