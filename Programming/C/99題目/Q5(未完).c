#include<stdio.h>
#include<stdlib.h>
main()
{
	int m,n;
	int a,b,l;
	int i,j;  
	int A[11],B[11],L[101];
	int x=0,y=0,z=0;//x=1~�̻� y=1~�F�� z=+1~�F��  (city) 
	printf("�п�J�����ӼƩM�X�����|(n m):");
	scanf("%d %d",&n,&m);
	printf("�п�J�U���������Z��(a b l):\n");
	for(i=0;i<m;i++)
	{
		scanf("%d %d %d",&a,&b,&l);
		A[i]=a;
		B[i]=b;
		L[i]=l;
	}
	for(j=0;j<m;j++)
	{
		if(A[j+1]-A[j]==1){
			y+=L[j]; //m=2; y=1~2city(distance)
			if(B[j+1]-B[j]==1){
				z+=L[j+1];}//m=2 z=2~3city(distance)
			if(A[j+1]-A[j]==1 || B[j+1]-B[j]==1)
				x+=L[j]+L[j+1];//m=2 x=1~3city(distance)
		}
	}

		printf("��X:%d %d %d \n",x,y,z);
}

