#include<stdio.h>
#include<stdlib.h>
#include<conio.h>
#include<math.h>
#include<windows.h>
#include<time.h>
main()
{
	printf("�q�Ʀr!!\n");
	printf("�W�h:\n");
	printf("1st�G�п�J4��0~9���Ʀr(���୫��)�I\n");
	printf("2nd�G�Ĥ@�ӼƦr���i�H��0�I\n");
	printf("3rd�G�p�G�q�@�ӼƦr���T��m�]���T�A�h�|���A�F�_�h�Ʀr���T��m���~�A�h�|���B�I\n");
	printf("4th�G�p�G4�ӼƦr�����q���h�|���C�I\n");
	printf("�\Ū���W�z�W�h�Y�i�}�l�C���I\n");
	
	char x;
	int a,b,c,d;
	int i,j,k,l;
	int m;
	int q,w,e,r;
	q=a;
	w=b;
	e=c;
	r=d;
	q=getchar();
	printf("\n�п�J�|�ӼƦr�G(x.x.x.x)");
	scanf("%d.%d.%d.%d",&q,&w,&e,&r);

		printf("\n�O�_�n���Ʀr�H(y/n)\n");
		scanf("%s",&x);
	
		if(x=='y')
		{
			printf("\n");
			return main();
		}
		else if(x=='n')
		{
			printf("%d%d%d%d",a,b,c,d);
			Sleep(500);
			printf("\t\t\b\b\b\b");
			printf("\n�}�l�C���a�I\n");
			for(m=1;m>0;m++)
			{
				printf("�вq��%d�ռƦr�G(x.x.x.x)",m);
				scanf("%d.%d.%d.%d",&i,&j,&k,&l);
				if(a==i && b==j && c==k && d==l)
				{
					printf("\t\t\t      4A  ");
					printf("���߲q��F�I�I�I\n");
					return 0;
				}
				else if(a==i && b==j && c==k && d!=l)
				{
					 printf("\t\t\t      3A  ");
					 printf("\n");
				}
				else if(a==i && b==j && c!=k && d==l)
				{
					printf("\t\t\t      3A  ");
					printf("\n");
				}
				else if(a==i && b!=j && c==k && d==l)
				{
					printf("\t\t\t      3A  ");
					printf("\n");
				}
				else if(a!=i && b==j && c==k && d==l)
				{
					printf("\t\t\t      3A  ");
					printf("\n");
				}
				else if(a==i && b==j && c!=k && d!=l)
				{
					printf("\t\t\t      2A  ");
					printf("\n");
				}
				else if(a==i && b!=j && c==k && d!=l)
				{
					printf("\t\t\t      2A  ");
					printf("\n");
				}
				else if(a!=i && b==j && c==k && d!=l)
				{
					printf("\t\t\t      2A  ");
					printf("\n");
				}
				else if(a==i && b!=j && c!=k && d==l)
				{
					printf("\t\t\t      2A  ");
					printf("\n");
				}
				else if(a!=i && b==j && c!=k && d==l)
				{
					printf("\t\t\t      2A  ");
					printf("\n");
				}
				else if(a!=i && b!=j && c==k && d==l)
				{
					printf("\t\t\t      2A  ");
					printf("\n");
				}
				else if(a!=i && b!=j && c!=k && d==l)
				{
					printf("\t\t\t      1A  ");
					printf("\n");
				}
				else if(a!=i && b!=j && c==k && d!=l)
				{
					printf("\t\t\t      1A  ");
					printf("\n");
				}
				else if(a!=i && b==j && c!=k && d!=l)
				{
					printf("\t\t\t      1A  ");
					printf("\n");
				}
				else if(a==i && b!=j && c!=k && d!=l)
				{
					printf("\t\t\t      1A  ");
					printf("\n");
				}
			}
		}
		return 0;
}
