#include <iostream>
#include <cstring>
using namespace std;
#define LEN 80      // �w�q�r���}�C����
void sort(char [][LEN], int);

int main()
{
  char str[][LEN] = {"Taipei", "Taoyuan", "Hsinchu",
                     "Miaoli", "Ilan", "Chiayi"};

  sort(str,6);      // �N str �Ƨ�, �@�� 6 �Ӧr��

  for (int i=0;i<6;i++)   // ��X�Ƨǫ᪺���G
    cout << str[i] <<endl;
}

void sort (char str[][LEN], int count)
{
  char temp[LEN];               // ��զr��ɪ��Ȧs�}�C
  for(int i=0;i<count-1;i++)    // �ΰj��Ӥ���r�ꪺ�j�p
     for(int j=i+1;j<count;j++)
       if(strcmp(str[i],str[j])>0) { // ����r��
         strcpy(temp,str[j]);        //
         strcpy(str[j],str[i]);      // ��զr��
         strcpy(str[i],temp);        //
       }
}
