#include<stdio.h>
#include<stdlib.h>
main()//���|���ۦP������H��  ���|���̫ᵲ�G���Ҳ��Ƭ۵� 
{
	int c,a,b;
	int i,j=0,k=0;
	int x=0,y=0;
	printf("��J�X�Ӧ{:");
	scanf("%d",&i);
	for(c=1;c<=i;c++)
	{
		printf("��J�U�Ӧ{��A B�Ҥ���H��:"); 
		scanf("%d %d",&a,&b);
		if(a>b)
		{
			j=a+b;
			x+=j;		
		}
		if(a<b)
		{
			k=a+b;
			y+=k;
		}
	 } 
	if(x>y)
	{
		printf("A %d\n",x-y);
	}
	else if(x<y)
	{
		printf("B %d\n",y-x);
	}
	return main();
}
