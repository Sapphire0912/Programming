#include<stdio.h>
#include<stdlib.h>
main()
{
	int a,b,c;
	int i,j;
	int Z;
	printf("���X�Ӿǥ�:");
	scanf("%d",&c);
	if(c<1 || c>10)
	{
		printf("�ƭȿ��~\n");
		return main();
	}
	Z:	
	for(i=1;i<=c;i++)
	{
		printf("���ɶ�A,�I��ɶ�B.");
		scanf("%d %d",&a,&b);
		if(a<1 || b>100)
		{
			printf("�Э��s��J\n");
			goto Z;
		}
	}
	
}
