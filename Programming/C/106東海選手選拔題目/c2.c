#include<stdio.h>
#include<stdlib.h>
main()
{
	int a;
	int i,j;
	printf("�п�J���:");
	scanf("%c",&i);
	switch(i)
	{
		case 'V':
		case 'v':printf("�q��,V,V,��S\n");
				break;
		case 'A':
		case 'a':printf("�q�y,I,A,�w��\n");
				break;
		case 'O':
		case 'o':printf("�q��,R,O,�کi\n");
				break;
		case 'S':
		case 's':printf("�q��,G,S,����l\n");
				break;
		case 'F':
		case 'f':printf("�q�e,C,F,�k��\n");
				break;
		case 'H':
		case 'h':printf("�q�P,L,H,��Q\n");
				break;	
		case 'W':
		case 'w':printf("�\�v,P,W,�˯S\n");
				break;	
		case 'J':
		case 'j':printf("�q��,W,J,�J��\n");
				break;	
		case 'c':
		case 'C':printf("�q�q,Q,C,�w��\n");
				break;
		default:
		return main();													
	}
}
