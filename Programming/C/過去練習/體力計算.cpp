#include<stdio.h>
#include<stdlib.h>
main()
{
	int a,b,c,d,e;
	int t,u,v,w,x,y,z=0;
	printf("�п�J�{�b���ɶ�:(24�ɨ�)(��J�覡:�� ��)");
	scanf("%d %d",&a,&b);
	printf("�п�J��O(MAX):");
	scanf("%d",&c);
	printf("�п�J�{�b��O�Ȭ�:");
	scanf("%d",&d);
	printf("�п�J�X�����^�_:");
	scanf("%d",&e);
	t=c-d; //�tt��O 
	u=t*e; //u�����^�� 
	v=u%60;//v���� 
	w=u/60;//w�p�� 
	x=a+w;
	y=b+v;
	if(y>=60)
	{
		y-=60;
		x++;
	}
	if(x>=24)
	{
		x-=24;
	}
	printf("��O�^��̤j�Ȫ��ɶ���: %d�I%d��(24�ɨ�)\n\n",x,y);
	return main();
 } 
