#include<stdio.h>
main()
{
	int name[10];
	int no,ch,en,c,sum,aver,x,y;
	
	printf("�H��");
	scanf("%d",&x);

    printf("���X");
	scanf("%d",&y);
	for(y=1;y<=x;y++)
	{	
		printf("�W�r");
		scanf("%s",&name);
	
		printf("���");
		scanf("%d",&ch);
	
		printf("�^��");
		scanf("%d",&en);
	
		printf("�{��");
		scanf("%d",&c);
	
	  sum=ch+en+c;
	  aver=sum/3;
	
	 printf("\t\t\tNAME:%s ",name);
	 printf("\tNO:%d \n",y);
	 printf("\t\t\t*************************\n");
	 printf("\t\t\t*\t���%-10d  * \n",ch);
     printf("\t\t\t*\t�^��%-10d  * \n",en);
	 printf("\t\t\t*\t�{��%-10d  * \n",c);
	 printf("\t\t\t*************************\n");
	 printf("\t\t\t*\t�`��%-10d  * \n",sum);
	 printf("\t\t\t*\t����%-10d  * \n",aver);
	 printf("\t\t\t*************************\n");
	
	 if (aver>79)
	 printf("\t\t\t*--���� A-- �D�`�n      * \n");
	 else
	 if (aver>60)
     printf("\t\t\t*--���� B--  ����       * \n");
	 else
	 printf("\t\t\t*--���� C-- �h�ɭ�      * \n");
	
	 printf("\t\t\t*************************\n");
    }
	return 0;
}
