#include<iostream>
#include<string>
#include<cstring>
using namespace std;

int main()
{
  string s;
  cout << "�п�J�@�Ӧr��G";
  cin >> s;

  int len = s.size();
  char* cstr = new char(len+1);
  strcpy(cstr,s.c_str());  // �ƻs�r��

  for (int i=0; i<len-2; i++) // �ƧǦr���}�C���e
    for (int j=i+1; j<len-1; j++)
      if (cstr[i]>cstr[j]) {
        char tmp = cstr[i];
        cstr[i] = cstr[j];
        cstr[j] = tmp;
      }

  cout << "�N�r�ꤺ�e�Ƨǫ�G" << cstr;
  delete [] cstr;
}
