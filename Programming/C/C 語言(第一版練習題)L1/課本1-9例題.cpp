#include<stdio.h>
#include<stdlib.h>
#define MAXLINE 1000  //maximum input line size �̤j��J�r��j�p 
int getline(char line[],int maxline);
void copy(char to[],char from[]);
//print longest input line
main(){
	int len;  //current line length ��e�r�ꪺ���� 
	int max;  // maximum length seen so far �ثe����ݨ쪺�̤j���� 
	char line[MAXLINE];  //current input line ��e��J�r��  
	char longest[MAXLINE]; // longest line saved here �̪����r��O�s�b�o��
	max=0;
	while((len=getline(line,MAXLINE))>0){
		if(len>max){
			max=len;
			copy(longest,line);
		}
		if(max>0){
			printf("Longest line is %3d character...%s\n",len,longest);			
		}
		return 0;
	} 
}
// getline:read a line into s,return length �NŪ�쪺�r��s��s[] �Ǧ^���� 
int getline(char s[],int lim){
	int c,i;
	for(i=0;i<lim-1 && (c=getchar())!=EOF && c!='\n';++i)
		s[i]=c;
	if(c=='\n'){
		s[i]=c;
		++i;
	}
	s[i]='\0';
	return i;
} 
//copy:copy 'from' into 'to';assume 'to' is big enough �ƻsfrom[]��to[];�ð��]to[]�����j
void copy(char to[],char from[]){
	int i;
	i=0;
	while((to[i]=from[i])!='\0')
		++i;
} 
