#include<stdio.h>
#include<stdlib.h>
main ()
{
	char oao;
	int a,b,x,y,c,d,k;
	float i;
	printf("��J1�ӼƦr:(��J0�Y�i�����{��)\n");
	scanf("%d",&a);
	if(a>=60&&a<=69)
	{
		printf("�п�J1�ӼƦr�A�����\n");
		scanf("%d",&b);
		if(b>0)
		printf("%d\n",b);
		else
		printf("%d\n",0-b);
		return main();
	}
	else
	if(a>=70&&a<=79)
	{
		printf("�п�J1�ӼƦr�A8�i��\n");
		scanf("%d",&c);
		printf("%o\n",c);
		return main();
	}
	else
	if(a>=80&&a<=89)
	{
		printf("��J1����A�P�_�j�p�g\n");
		scanf("%s",&oao);
		if(oao>96)
		printf("%c �p�g\n",oao);
		if(oao<91)
		printf("%c �j�g\n",oao);
		
		return main();
	}
	else
	if(a>=90&&a<=99)
	{
		printf("��J1�ӼƦr\n");
		scanf("%f",&i);
		printf("��J1�AC��F�F��J2�AF��C\n");
		scanf("%d",&x);
		if(x==1)
		printf("%f\n",9*i/5+32);
		else
		if(x==2)
		printf("%f\n",((i-32)*5/9));
		return main();
	}
	else
	if(a==0) 
	{
		printf("���}�{��");
		return 0;
	}
	if(a<59)
	{
		printf("��J��ӼƦr(a,b)\n");
		scanf("%d,%d",&d,&y);
		printf("%d,%d\n",y,d);
		return main();
	}
	if(a>99)
	{
		printf("��J��ӼƦr(a,b)\n");
		scanf("%d,%d",&d,&y);
		printf("%d,%d\n",y,d);
		return main();
	}
}
