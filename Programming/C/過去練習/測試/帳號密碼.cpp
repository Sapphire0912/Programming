#include<stdio.h>
#include<stdlib.h>
#include<windows.h>
#include<time.h>
#include<conio.h>
#include<string.h>
#define acc 20 //�۩w�q�ܼ� 
#define pw 9
main()
{
	char account[acc],password[pw]; //�b���K�X�Ŷ� 
	char ACC[acc]="kotori";
	char PW[pw];
	int l;
	int o,p,q,r;
	unsigned int atm=2000;  //��@�Ȧ�e�A��^^ 
	int a,b,c; //�j��,���פW�� 
	int X,ATM,B,D; //�Ƶ{�� 
	int time=0; //��w�ɶ�
	printf("�е��U�s���K�X:(����8�Ӧr)");
	for(p=0;p<8;p++)
	{
		PW[p]=getch();
		putchar('*');
	}
	X:
		printf("\n�Y�n�i�����п�J9�A�_�h��J0���}\n");
		scanf("%d",&l);
		switch(l)
		{
			case 0:printf("���¥��{�A�w��U���A��!\n");
			   return 0;
			case 9:
			time+=10000;
			int chance=3;
	B: 
	do
	{
		printf("\n\n�п�J�b��:");
		scanf("%s",account);
		printf("�п�J�K�X:");
	for(a=0;a<8;a++)
	{
		password[a]=getch();
		putchar('#');
	}
	b=strncmp(account,ACC,acc-1);
	c=strncmp(password,PW,pw-1);
	if(b==0 && c==0)
	{
		printf("\n�b���K�X���T\n");
		chance=0;  //�s �� �d �w�s�Q�� �K�X�ܧ�
		unsigned int i,j,k;
		ATM:
		printf("�п�ܭn���檺�ʧ@:\n1.�s��\t\t2.����\n3.�d�ߪ��B\t4.�K�X�ܧ�\n");
		scanf("%d",&i);
		switch(i)
		{
			case 1:printf("�{�b�����B��:%d\n\n",atm);
				   printf("�п�J�s�ڪ����B:");
				   scanf("%d",&j);
				   atm+=j;
				   printf("�{�b�����B��:%d\n",atm);
				   printf("�������!!�Y�n�A���ϥνЭ��s��J�b��!�_�h��0���}\n\n");
				   goto X;
			case 2:printf("�{�b�����B��:%d\n\n",atm);
				   D:
				   printf("�п�J���ڪ����B:");
				   scanf("%d",&k);
				   if(k>atm)
				   {
				   		printf("��J���~�A�Э��s��J���B:\n");
				   		goto D;
				   }
				   atm-=k;
				   printf("�{�b�����B��:%d\n\n",atm);
				   printf("�������!!�Y�n�A���ϥνЭ��s��J�b��!�_�h��0���}\n\n");
				   goto X;
			case 3:printf("�{�b�����B��:%d\n\n",atm);
				   printf("�������!!�Y�n�A���ϥνЭ��s��J�b��!�_�h��0���}\n\n");
				   goto X;
			case 4:printf("�п�J�±K�X:");
				   	for(a=0;a<8;a++)
					{
						password[a]=getch();
						putchar('#');
					}
				   printf("\n�п�J�s�K�X:(����8�Ӧr)");
				   for(p=0;p<8;p++)
			    	{
						PW[p]=getch();
						putchar('*');
					}
					printf("\n\n�ק�K�X��Э��s�n�J!\n");
					goto B;
			default:printf("��J���~�A�Э��s��J!\n\n");
					goto ATM;
		}
	}
	else
	{
		chance--;
		printf("\n�b���K�X�����T\n");
		if(chance>0)
		{
			printf("�Э��s��J\n�٦�%d�����|��J\n\n",chance);
		}
		if(chance==0)
		{
		if(time>20000)
		{
			printf("�w��w�A�нT�{�b���K�X��A��J!!!");
			return 0; 
		}
			printf("��w�ɶ�%d��\n\n",time/1000);
			Sleep(time);
			goto X;	
		}
	}
  }while(chance>0);
	}
}

