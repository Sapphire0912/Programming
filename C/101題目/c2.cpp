#include<stdio.h>
#include<stdlib.h>
int time(int,int,int,int);
main(){//���Ҽ{�����D 
	int h1,h2,m1,m2;
	printf("�п�J���l�i��&�������ɶ�(ex.5�I10�� ��J:5 10)(24�ɨ�)\n");
	scanf("%d %d %d %d",&h1,&m1,&h2,&m2);
	if(h1+h2>46 || m1>60 || m2>60 || h2<h1){
		printf("�榡���~!\n");
		return main();}
		else{
			printf("%d��\n",time(h1,m1,h2,m2));}
			return main();
}
int time(int h1,int m1,int h2,int m2){
	int cost;
	h2-=h1;h2*=60;h2+=m2;h2-=m1;
	if(h2<=30){cost=0;}
	if(h2>30 && h2<=60){cost=30;}
	if(h2>60 && h2<=120){cost=60;}
		if(h2>120){cost=1;
		do{
			h2-=60;cost++;
		}while(h2>=60 && cost<=7);cost*=30;}
	if(cost>=210){cost=210;};
		return cost;
}

