#include<stdio.h>
#include<stdlib.h>
#include<windows.h>
#include<time.h>
int main()
{
	char x;
	int a;
	printf("��JY�i�J�C���A�_�h��N���}�C��\n");
	scanf("%s",&x);
	switch(x)
	{
		case 'n':
		case 'N':printf("���}�C��BYE BYE!!\n");
				 system("pause");
				 return 0;
		case 'y':
		case 'Y':printf("�}�l�C��\n");
			   	 printf("�X���R\n");
				 scanf("%d",&a);
				 printf("%d���R �}�l�i�J�C��\n",a);
				 Sleep(2000);
				 printf("�Ĥ@��");
				 break;
		default:printf("�ƭȿ��~\n");
				return main();
	}
}
