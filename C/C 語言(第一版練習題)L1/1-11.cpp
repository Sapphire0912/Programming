#include<stdio.h>
#include<stdlib.h>
main(){
	int c;
	int x,y,z;
	x=y=z=0;
	while((c=getchar())!=EOF){
		if((c>='A' && c<='Z')||(c>='a' && c<='z')){
			x++;}
		else if(c>='0'&&c<='9'){
			y++;}
		else if(c=='\n'){
			break;}
		else z++;
	}
	printf("�^���r:%d�� �Ʀr:%d�� ��L:%d��\n",x,y,z);
}
